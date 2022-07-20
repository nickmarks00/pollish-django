from rest_framework import serializers

from core.base_serializers import BaseUserSerializer
from pollish.serializers.base_serializers import BaseCommunitySerializer
from ..models import Community, Poll, Choice, Comment, PollImage, Profile


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

class ListCommunitySerializer(serializers.ModelSerializer):

    id = serializers.IntegerField(read_only=True)
    num_polls = serializers.SerializerMethodField(method_name='count_polls')
    num_users = serializers.SerializerMethodField(method_name='count_users')
    class Meta:
        model = Community
        fields = ['id', 'created_by_id', 'created_at', 'image','name', 'num_polls', 'num_users']

    def count_users(self, community:Community):
        return community.users.count()

    def count_polls(self, community:Community):
        return community.polls.count()

    def create(self, validated_data):
        community = Community.objects.create(created_by_id=self.context['user_id'], **validated_data)

        return community


class ListPollImageSerializer(serializers.ModelSerializer):

    choice_id = serializers.IntegerField(required=False)
    poll_id = serializers.IntegerField(read_only=True)

    class Meta:
        model = PollImage
        fields = ['image', 'choice_id', 'poll_id']
    
    def create(self, validated_data):
        poll_id = self.context['poll_id']
        return PollImage.objects.create(poll_id=poll_id, **validated_data)


class ListPollSerializer(serializers.ModelSerializer):

    # Meta class
    class Meta:
        model = Poll
        fields = ('id', 'user_id', 'created_at', 'question_text', 'choices', 'images',  'num_comments', 'user_vote')
    
    # Defined fields
    choices = ListChoiceSerializer(many=True)
    images = ListPollImageSerializer(many=True, required=False)
    num_comments = serializers.SerializerMethodField(method_name='count_comments')
    user_id = serializers.IntegerField(read_only=True)
    user_vote = serializers.SerializerMethodField(method_name='get_user_vote')

    # Serializer class methods
    def count_comments(self, poll:Poll):
        try:
            return poll.comments.count()
        except AttributeError:
            return 0

    def get_user_vote(self, poll:Poll):
        user_id = self.context.get('user_id')
        if user_id:
            choice = poll.choices.filter(users__id=user_id)
            if choice:
                return choice[0].id
        return None

    #the following method handles creation of new choices
    def create(self, validated_data):
        choices = validated_data.pop('choices')
        poll = Poll.objects.create(user_id=self.context['user_id'], **validated_data)
        for choice in choices:
            choice_text = choice.pop('choice_text')
            c = Choice.objects.create(poll=poll, choice_text=choice_text)
        
        return poll

class ListProfileSerializer(serializers.ModelSerializer):

    class Meta:
        model = Profile
        fields = ['id', 'avatar']