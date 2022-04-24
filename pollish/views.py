from django.db import transaction
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.filters import SearchFilter
from rest_framework.mixins import ListModelMixin, CreateModelMixin, UpdateModelMixin, RetrieveModelMixin
from rest_framework.pagination import PageNumberPagination
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet, GenericViewSet


from .models import Poll, Choice, Comment, PollImage, Profile, Community
from core.models import User
from .serializers import ChoiceSerializer, CommentSerializer, PollImageSerializer, PollSerializer, ProfileSerializer, CommunitySerializer



class PollImageUpload(GenericViewSet, CreateModelMixin, ListModelMixin):
    '''
    MultiPartParser+FormParser => use if sending data in HTML form format
    FileUploadParser => use if just sending a raw file in the request
    '''
    # handling the multi-format of images...

    parser_classes = [MultiPartParser, FormParser]
    permission_classes = [IsAuthenticated]
    serializer_class = PollImageSerializer

    def get_queryset(self):
        return PollImage.objects.filter(poll_id=self.kwargs['poll_pk'])
    
    def get_serializer_context(self):
        return {'poll_id': self.kwargs['poll_pk']}
    

    def post(self, request, format=None):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PollViewSet(GenericViewSet, UpdateModelMixin, ListModelMixin, RetrieveModelMixin):
    

    serializer_class = PollSerializer
    pagination_class = PageNumberPagination

    def get_queryset(self):
        user_id = self.kwargs.get('user_pk', None)
        community_id = self.kwargs.get('community_pk', None)

        if user_id:
            return Poll.objects.select_related('user').prefetch_related('choices__users', 'comments', 'images').filter(user_id=user_id)
        elif community_id:
            return Poll.objects.select_related('user').prefetch_related('choices__users', 'comments', 'images').filter(community_id=community_id)
        else:
            return Poll.objects.select_related('user').prefetch_related('comments', 'choices__users', 'images').all()

    
    def get_serializer_context(self):
        return {'user_id': self.request.user.id}


    # Function for returning authenticated users polls
    @action(detail=False, methods=['GET', 'POST'])
    def me(self, request):
        polls = Poll.objects.select_related('user').filter(user_id=request.user.id)
        if request.method == "GET" and polls.exists():
            serializer = self.serializer_class(polls, many=True)
            return Response(serializer.data)
        elif request.method == "POST":
            serializer = self.serializer_class(data=request.data, context={'user_id': request.user.id})
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data)
        return Response([])



class CommentViewSet(ModelViewSet):

    serializer_class = CommentSerializer

    def get_queryset(self):
        return Comment.objects.select_related('user').filter(poll_id=self.kwargs['poll_pk'])
    
    def get_serializer_context(self):
        return {'poll_id': self.kwargs['poll_pk']}
    

class RegisterVote(GenericViewSet, ListModelMixin, UpdateModelMixin, RetrieveModelMixin):

    serializer_class = ChoiceSerializer

    def get_queryset(self):
        return Choice.objects.prefetch_related('users').filter(poll_id=self.kwargs['poll_pk'])
    
    def get_serializer_context(self):
        return {'poll_id': self.kwargs['poll_pk']}


    @action(detail=True, methods=['PATCH'])
    def me(self, request, format=None, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid():
            valid_choice_qset = Choice.objects.filter(id=self.kwargs['pk'])
            if not valid_choice_qset.exists():
                return Response({'msg': 'choice not found'}, status.HTTP_404_NOT_FOUND)
            user_voted_qset = valid_choice_qset.filter(users__id=request.user.id)
            if len(user_voted_qset):
                # user is de-registering vote
                with transaction.atomic():
                    choice = user_voted_qset[0]
                    choice.users.remove(request.user.id)
            else:
                # makes sure that fields only update if all other updates are successful
                with transaction.atomic():
                    choice = valid_choice_qset[0]
                    choice.users.add(request.user.id)

            return Response(ChoiceSerializer(choice).data, status=status.HTTP_202_ACCEPTED)
        

        return Response({'msg': 'bad serializer'}, status.HTTP_400_BAD_REQUEST)


class ProfileViewSet(ModelViewSet):

    parser_classes = [MultiPartParser, FormParser]
    permission_classes = [IsAuthenticated]
    serializer_class = ProfileSerializer

    def get_queryset(self):
        return Profile.objects.select_related('user').all()
    

    @action(detail=False, methods=['GET', 'PATCH'])
    def me(self, request):
        (profile, created) = Profile.objects.get_or_create(user_id=request.user.id)
        if request.method == "GET":
            serializer = ProfileSerializer(profile)
            return Response(serializer.data)
        elif request.method == "PATCH":
            serializer = ProfileSerializer(profile, data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_202_ACCEPTED)


class CommunityViewSet(ModelViewSet):

    filter_backends = [SearchFilter]
    parser_classes = [MultiPartParser, FormParser, JSONParser]
    permission_classes = [IsAuthenticated]
    queryset = Community.objects.select_related('created_by').prefetch_related('polls', 'users').all()
    search_fields = ['name']
    serializer_class = CommunitySerializer

    def get_serializer_context(self):
        return {'user_id': self.request.user.id}

    def create(self, request):
        serializer = self.serializer_class(data=request.data, context={'user_id': self.request.user.id})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def update(self, request, *args, **kwargs):
        poll_id = request.query_params.get('poll_id')
        update_user = request.query_params.get('update_user', 'False')
        user_id = request.user.id

        queryset = Community.objects.filter(id=self.kwargs['pk'])

        if not queryset.exists():
                return Response({'msg': 'choice not found'}, status.HTTP_404_NOT_FOUND)

        community = queryset[0]

        name = request.data.get('name', community.name)
        image = request.data.get('image', community.image)
        
        if poll_id is not None:
            poll_queryset = Poll.objects.filter(id=poll_id)
            community_queryset = community.polls.filter(id=poll_id)
            if len(community_queryset):
                poll = poll_queryset[0]
                community.polls.remove(poll)
            elif len(poll_queryset):
                poll = poll_queryset[0]
                community.polls.add(poll)
            else:
                return Response('Poll not found with that id', status=status.HTTP_400_BAD_REQUEST)
        elif user_id is not None and update_user == 'True':
            user_queryset = User.objects.filter(id=user_id)
            community_queryset = community.users.filter(id=user_id)
            if len(community_queryset):
                user = user_queryset[0]
                community.users.remove(user)
            elif len(user_queryset):
                user = user_queryset[0]
                community.users.add(user)
            else:
                return Response('User not found with that id', status=status.HTTP_400_BAD_REQUEST)
        elif name or image:
            community.name = name
            community.image = image
            community.save(update_fields=['name', 'image'])

        else:
            return Response('Error in body', status=status.HTTP_400_BAD_REQUEST)


        return Response(CommunitySerializer(community, context={'user_id': user_id}).data, status=status.HTTP_202_ACCEPTED)
