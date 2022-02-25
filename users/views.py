from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter
from rest_framework.viewsets import ModelViewSet


from users.serializers import ProfileSerializer, UserSerializer


from users.models import User, Profile

class UserViewSet(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_fields = ['username']
    search_fields = ['username', 'email']


class ProfileViewSet(ModelViewSet):
    serializer_class = ProfileSerializer

    def get_queryset(self):
        return Profile.objects.select_related('user').all()
    
