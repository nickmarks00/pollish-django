from rest_framework import serializers

from core.serializers import SimpleUserSerializer
from .models import Poll, Choice, Comment, PollImage, Profile


from .base_serializers import BaseCommunitySerializer
from .list_serializers import ListChoiceSerializer


class ChoiceSerializer(serializers.ModelSerializer):

    users = SimpleUserSerializer(many=True, required=False)
    num_votes = serializers.SerializerMethodField(method_name='get_num_votes')
    class Meta:
        model = Choice
        fields = ('choice_text', 'id', 'users', 'num_votes')
    
    def get_num_votes(self, choice:Choice):
        return choice.users.all().count()
    

    def create(self, validated_data):
        users = validated_data.pop('users')
        choice = Choice.objects.create(**validated_data)
        
        return choice


class CommentSerializer(serializers.ModelSerializer):

    choice_id = serializers.IntegerField(required=False)
    user_id = serializers.IntegerField(required=True)

    class Meta:
        model = Comment
        fields = ('choice_id', 'comment_text', 'user_id', 'created_at')
    
    def create(self, validated_data):
        poll_id = self.context['poll_id']
        return Comment.objects.create(poll_id=poll_id, **validated_data)


class PollImageSerializer(serializers.ModelSerializer):

    choice_id = serializers.IntegerField(required=False)
    poll_id = serializers.IntegerField(read_only=True)

    class Meta:
        model = PollImage
        fields = ['image', 'choice_id', 'poll_id']
    
    def create(self, validated_data):
        poll_id = self.context['poll_id']
        return PollImage.objects.create(poll_id=poll_id, **validated_data)


class PollSerializer(serializers.ModelSerializer):

    # Meta class
    class Meta:
        model = Poll
        fields = ('community', 'id', 'user_id', 'created_at', 'question_text', 'choices', 'images',  'num_comments', 'user_vote')
    
    # Defined fields
    choices = ListChoiceSerializer(many=True)
    community = BaseCommunitySerializer(required=False)
    images = PollImageSerializer(many=True, required=False)
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


class ProfileSerializer(serializers.ModelSerializer):

    user_id = serializers.IntegerField(read_only=True)
    class Meta:
        model = Profile
        fields = ['id', 'user_id', 'avatar', 'bio', 'votes_registered']






