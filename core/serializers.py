from djoser.serializers import UserSerializer as BaseUserSerializer, UserCreateSerializer as BaseUserCreateSerializer

from .models import User
from .serializers import BaseUserSerializer

from pollish.serializers.detail_serializers import DetailProfileSerializer


class UserCreateSerializer(BaseUserCreateSerializer):

    class Meta(BaseUserCreateSerializer.Meta):
        fields = ['id', 'username', 'password', 'email', 'first_name', 'last_name']


class UserSerializer(BaseUserSerializer):

    following = BaseUserSerializer(many=True, read_only=True)
    profile = DetailProfileSerializer(read_only=True)

    class Meta(BaseUserSerializer.Meta):
        fields = ['id', 'username',  'email', 'first_name', 'last_name', 'following', 'profile']

