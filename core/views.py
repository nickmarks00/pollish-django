from django_filters.rest_framework import DjangoFilterBackend
from django.urls import resolve
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.filters import SearchFilter
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet


from core.serializers import SimpleUserSerializer, UserSerializer
from core.models import User

from pollish.models import Poll, Community
from pollish.serializers import PollSerializer



class UserSearchFilter(SearchFilter):
    def get_search_fields(self, view, request):
        if request.query_params.get('username'):
            return ['^username']
        elif request.query_params.get('email'):
            return ['^email']
        
        return super().get_search_fields(view, request)
class UserViewSet(ModelViewSet):
    filter_backends = [DjangoFilterBackend, UserSearchFilter]
    filterset_fields = ['username', 'email']
    pagination_class = PageNumberPagination
    permission_classes = [IsAuthenticated]
    queryset = User.objects.select_related('profile').prefetch_related('following').all()
    search_fields = ['^username', '^email']


    def get_serializer_class(self):
        if resolve(self.request.path_info).url_name == 'users-followers' or 'users-following':
            return SimpleUserSerializer
        return UserSerializer


    @action(detail=True, methods=['GET'])
    def followers(self, request, *args, **kwargs):

        user_id = self.kwargs.get('pk', None)
        users = User.objects.filter(following__in=[user_id])
        serializer_class = self.get_serializer_class()
        serializer = serializer_class(users, many=True)
        return Response(serializer.data)


    @action(detail=True, methods=['GET'])
    def following(self, request, *args, **kwargs):
        '''
        Endpoint at /core/users/<id1>/following/?id=<id2>
        returns True if id1 following id2, else False
        '''

        user_id = self.kwargs.get('pk', None)
        id2 = request.query_params.get('id', None)
        
        queryset = User.objects.filter(id=user_id)

        if id2 is not None:
            if queryset.exists():
                queryset = queryset.filter(following__in=[id2])

                if len(queryset) == 1:
                    return Response(True)
                elif not len(queryset):
                    return Response(False)
                else:
                    return Response('More than one user found', status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response('Bad queryset', status=status.HTTP_400_BAD_REQUEST)
        else:
            serializer_class = self.get_serializer_class()
            serializer = serializer_class(queryset[0].following.all(), many=True)
            return Response(serializer.data)



    @action(detail=True, methods=['GET'])
    def feed(self, request, *args, **kwargs):
        # fetch polls belonging to users I follow
        response = []

        user_id = self.kwargs.get('pk', None)
        
        queryset = User.objects.filter(id=user_id)
        if queryset.exists():
            user = queryset[0]
            following_users = user.following.values_list('id', flat=True)
            
            polls = Poll.objects.select_related('user').filter(user_id__in=following_users)
            
            if polls.exists():
                serializer_following = PollSerializer(polls, many=True)
                response.append(serializer_following.data)


        # fetch polls belonging to communities I follow
        communities = Community.objects.filter(users__in=[user_id]).values_list('id', flat=True)
        if queryset.exists():
            polls = Poll.objects.select_related('user').filter(community_id__in=communities)
            if polls.exists():
                serializer_communities = PollSerializer(polls, many=True)
                response.append(serializer_communities.data)

        return Response(response)



    def update(self, request, *args, **kwargs):
        user_to_follow_id = request.query_params.get('user_id')
        unfollow = request.query_params.get('unfollow', 'False')

        if user_to_follow_id is not None:
            current_user_id = request.user.id
            user_to_follow_queryset = User.objects.filter(id=user_to_follow_id)
            current_user_queryset = User.objects.filter(id=current_user_id)

            if not user_to_follow_queryset.exists() or not current_user_queryset.exists() :
                return Response('User not found', status=status.HTTP_400_BAD_REQUEST)

            user_to_follow = user_to_follow_queryset[0]
            current_user = current_user_queryset[0]

            if unfollow == 'True':
                current_user.following.remove(user_to_follow)
            else:
                current_user.following.add(user_to_follow)

            return Response(UserSerializer(current_user).data, status=status.HTTP_202_ACCEPTED)

        else:
            super().update(request)



    
