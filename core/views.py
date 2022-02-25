from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter
from rest_framework.viewsets import ModelViewSet


from core.serializers import UserSerializer


from core.models import User

class UserViewSet(ModelViewSet):
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_fields = ['username']
    queryset = User.objects.all()
    search_fields = ['username', 'email']
    serializer_class = UserSerializer



    
