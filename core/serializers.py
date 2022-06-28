from djoser.serializers import UserSerializer as BaseUserSerializer, UserCreateSerializer as BaseUserCreateSerializer
from rest_framework import serializers

from .models import User
from pollish.base_serializers import SimpleProfileSerializer


class UserCreateSerializer(BaseUserCreateSerializer):

    class Meta(BaseUserCreateSerializer.Meta):
        fields = ['id', 'username', 'password', 'email', 'first_name', 'last_name']


class SimpleUserSerializer(serializers.ModelSerializer):

    profile = SimpleProfileSerializer(read_only=True)
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'profile']

class UserSerializer(BaseUserSerializer):

    following = SimpleUserSerializer(many=True, read_only=True)
    profile = SimpleProfileSerializer(read_only=True)

    class Meta(BaseUserSerializer.Meta):
        fields = ['id', 'username',  'email', 'first_name', 'last_name', 'following', 'profile']

