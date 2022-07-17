from rest_framework import serializers

from .models import Community, Poll, Choice, Comment, PollImage, Profile



class DetailProfileSerializer(serializers.ModelSerializer):

    class Meta:
        model = Profile
        fields = ['id', 'avatar']