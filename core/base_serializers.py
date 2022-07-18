from rest_framework import serializers

from .models import User

from pollish.serializers.base_serializers import BaseProfileSerializer

class BaseUserSerializer(serializers.ModelSerializer):

    profile = BaseProfileSerializer(read_only=True)
    class Meta:
        model = User
        fields = ['id', 'username', 'profile']