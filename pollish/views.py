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


from .serializers.detail_serializers import DetailCommunitySerializer, DetailCommentSerializer, DetailPollImageSerializer, DetailPollSerializer, DetailProfileSerializer
from .serializers.list_serializers import ListCommunitySerializer, ListChoiceSerializer

from core.models import User

class PollImageUpload(GenericViewSet, CreateModelMixin, ListModelMixin):
    '''
    MultiPartParser+FormParser => use if sending data in HTML form format
    FileUploadParser => use if just sending a raw file in the request
    '''
    # handling the multi-format of images...

    parser_classes = [MultiPartParser, FormParser]
    # permission_classes = [IsAuthenticated]
    serializer_class = DetailPollImageSerializer

    def get_queryset(self):
        return PollImage.objects.filter(poll_id=self.kwargs['poll_pk'])
    
    def get_serializer_context(self):
        return {'poll_id': self.kwargs['poll_pk']}
    

    def create(self, request, *args, **kwargs):
        poll_id = self.kwargs['poll_pk']

        # check that choice ID matches option on Poll
        choice_id = request.data.get('choice_id', None)
        if choice_id:
            choice_queryset = Poll.objects.filter(id=poll_id, choices__in=[choice_id])
            print(choice_queryset)
            if not choice_queryset.exists():
                return Response({"message": "No such choice on poll"}, status=status.HTTP_400_BAD_REQUEST)

        return super().create(request)


class PollViewSet(GenericViewSet, UpdateModelMixin, ListModelMixin, RetrieveModelMixin):
    
    filter_backends = [SearchFilter]
    pagination_class = PageNumberPagination
    permission_classes = [IsAuthenticated]
    search_fields = ['question_text']
    serializer_class = DetailPollSerializer


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

            # check that at least two choices provided
            if len(request.data.get("choices", [])) < 2:
                return Response({"message": "At least two choices are required"}, status=status.HTTP_400_BAD_REQUEST)

            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response([])


    @action(detail=True, methods=['PATCH'])
    def vote(self, request, *args, **kwargs):
        
        response = []

        vote_id = request.data.get('vote_id', None)
        unvote_id = request.data.get('unvote_id', None)
        user_id = request.query_params.get('user_id')
        poll_id = self.kwargs.get('pk')


        if not user_id:
            return Response({"user_id": ["This parameter is required"]}, status=status.HTTP_400_BAD_REQUEST)

        if not (vote_id or unvote_id):
            return Response({"body": ["Both choice to vote and choice to unvote missing"]}, status=status.HTTP_400_BAD_REQUEST)

        
        # handle vote
        if vote_id:
            choice_to_vote = Choice.objects.filter(id=vote_id, poll__id=poll_id)
            if not choice_to_vote.exists():
                return Response({"vote_id": ["This choice doesn't exist on this poll"]}, status=status.HTTP_400_BAD_REQUEST)

            with transaction.atomic():
                choice_vote = choice_to_vote[0]
                choice_vote.users.add(user_id)

                profile_qs = Profile.objects.filter(user_id=user_id)
                profile = profile_qs[0]

                profile.votes_registered += 1
                profile.save()

            response.append(ListChoiceSerializer(choice_vote).data)
        

        # handle unvote
        if unvote_id:
            choice_to_unvote = Choice.objects.filter(id=unvote_id, poll__id=poll_id)
            if not choice_to_unvote.exists():
                return Response({"unvote_id": ["This choice doesn't exist on this poll"]}, status=status.HTTP_400_BAD_REQUEST)

            with transaction.atomic():
                choice_unvote = choice_to_unvote[0]
                choice_unvote.users.remove(user_id)

                profile_qs = Profile.objects.filter(user_id=user_id)
                profile = profile_qs[0]

                profile.votes_registered -= 1
                profile.save()

            response.append(ListChoiceSerializer(choice_unvote).data)
            

        return Response(response, status=status.HTTP_202_ACCEPTED)

    

class CommentViewSet(ModelViewSet):

    serializer_class = DetailCommentSerializer
    permission_classes = [IsAuthenticated]


    def get_queryset(self):
        return Comment.objects.select_related('user').filter(poll_id=self.kwargs['poll_pk'])
    
    def get_serializer_context(self):
        return {'poll_id': self.kwargs['poll_pk']}


    def create(self, request, *args, **kwargs):
        poll_id = self.kwargs['poll_pk']
        choice_id = request.data.get('choice_id', None)
        user_id = request.data.get('user_id', None)
        
        queryset = Poll.objects.filter(id=poll_id, choices__in=[choice_id])

        if not queryset.exists():
            return Response({"message": "No such choice on poll"}, status=status.HTTP_400_BAD_REQUEST)

        if user_id != request.user.id:
            return Response({"message": "Mismatching user in body to authorization header"}, status=status.HTTP_401_UNAUTHORIZED)

        return super().create(request)
    


class ProfileViewSet(ModelViewSet):

    parser_classes = [MultiPartParser, FormParser]
    permission_classes = [IsAuthenticated]
    serializer_class = DetailProfileSerializer

    def get_queryset(self):
        return Profile.objects.select_related('user').all()
    

    @action(detail=False, methods=['GET', 'PATCH'])
    def me(self, request):
        (profile, created) = Profile.objects.get_or_create(user_id=request.user.id)
        if request.method == "GET":
            serializer = DetailProfileSerializer(profile)
            return Response(serializer.data)
        elif request.method == "PATCH":
            serializer = DetailProfileSerializer(profile, data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_202_ACCEPTED)


class CommunityViewSet(ModelViewSet):

    filter_backends = [SearchFilter]
    parser_classes = [MultiPartParser, FormParser, JSONParser]
    pagination_class = PageNumberPagination
    permission_classes = [IsAuthenticated]
    queryset = Community.objects.select_related('all').all()
    search_fields = ['name']
    
    serializer_classes = {
        'list': ListCommunitySerializer,
        'retrieve': DetailCommunitySerializer
    }

    default_serializer_class = ListCommunitySerializer

    def get_serializer_class(self):
        user_id = self.kwargs.get('user_pk', None)
        if user_id is not None:
            return ListCommunitySerializer
        return self.serializer_classes.get(self.action, self.default_serializer_class)

    def get_serializer_context(self):
        return {'user_id': self.request.user.id,
                'is_community': True}

    def get_queryset(self):
        user_id = self.kwargs.get('user_pk', None)
        if user_id is not None:
            return Community.objects.filter(users__in=[user_id])
        return Community.objects.all()

    def create(self, request):
        serializer_class = self.get_serializer_class()
        serializer = serializer_class(data=request.data, context={'user_id': self.request.user.id})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def update(self, request, *args, **kwargs):
        poll_id = request.query_params.get('poll_id')
        user_id = request.query_params.get('user_id')

        queryset = Community.objects.filter(id=self.kwargs['pk'])

        if not queryset.exists():
                return Response({'message': 'community not found'}, status.HTTP_404_NOT_FOUND)

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
        elif user_id is not None:
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


        return Response(ListCommunitySerializer(community, context={'user_id': user_id}).data, status=status.HTTP_202_ACCEPTED)
