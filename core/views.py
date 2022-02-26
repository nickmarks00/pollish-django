from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter
from rest_framework.viewsets import ModelViewSet


from core.serializers import UserSerializer
from core.models import User

class UserSearchFilter(SearchFilter):
    def get_search_fields(self, view, request):
        if request.query_params.get('username'):
            return ['^=username']
        elif request.query_params.get('email'):
            return ['^email']
        
        return super().get_search_fields(view, request)
class UserViewSet(ModelViewSet):
    filter_backends = [DjangoFilterBackend, UserSearchFilter]
    filterset_fields = ['username']
    queryset = User.objects.all()
    search_fields = ['^=username', '^email']
    serializer_class = UserSerializer



    
