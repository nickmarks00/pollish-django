from rest_framework import serializers
from .models import Profile

class SimpleProfileSerializer(serializers.ModelSerializer):

    class Meta:
        model = Profile
        fields = ['id', 'avatar', 'bio']