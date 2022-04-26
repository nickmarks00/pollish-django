from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status
from rest_framework.filters import SearchFilter
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet


from core.serializers import UserSerializer
from core.models import User

class UserSearchFilter(SearchFilter):
    def get_search_fields(self, view, request):
        if request.query_params.get('username'):
            return ['^username']
        elif request.query_params.get('email'):
            return ['^email']
        
        return super().get_search_fields(view, request)
class UserViewSet(ModelViewSet):
    filter_backends = [DjangoFilterBackend, UserSearchFilter]
    filterset_fields = ['username']
    pagination_class = PageNumberPagination
    permission_classes = [IsAuthenticated]
    queryset = User.objects.prefetch_related('following').all()
    search_fields = ['^username', '^email']
    serializer_class = UserSerializer


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



    
