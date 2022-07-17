from rest_framework import serializers

from core.serializers import SimpleUserSerializer
from .models import Community, Poll, Choice, Comment, PollImage, Profile


class ListCommunitySerializer(serializers.ModelSerializer):

    id = serializers.IntegerField(read_only=True)
    created_by = SimpleUserSerializer(read_only=True)
    num_polls = serializers.SerializerMethodField(method_name='count_polls')
    num_users = serializers.SerializerMethodField(method_name='count_users')
    class Meta:
        model = Community
        fields = ['id', 'created_by', 'created_at', 'image','name', 'num_polls', 'num_users']

    def count_users(self, community:Community):
        return community.users.count()

    def count_polls(self, community:Community):
        return community.polls.count()

    def create(self, validated_data):
        community = Community.objects.create(created_by_id=self.context['user_id'], **validated_data)

        return community


class ListChoiceSerializer(serializers.ModelSerializer):

    num_votes = serializers.SerializerMethodField(method_name='get_num_votes')
    
    class Meta:
        model = Choice
        fields = ('choice_text', 'id', 'num_votes')
    
    def get_num_votes(self, choice:Choice):
        return choice.users.all().count()

    def create(self, validated_data):
        users = validated_data.pop('users')
        choice = Choice.objects.create(**validated_data)
        
        return choice