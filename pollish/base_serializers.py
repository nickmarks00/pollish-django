from rest_framework import serializers
from .models import Profile, Community, Poll


from core.serializers import SimpleUserSerializer


class BaseCommunitySerializer(serializers.ModelSerializer):

    id = serializers.IntegerField(read_only=True)

    class Meta:
        model = Community
        fields = ['name', 'id']


class BasePollSerializer(serializers.ModelSerializer):

    class Meta:
        model = Poll
        fields = ['id', 'user', 'created_at', 'question_text', 'num_comments', 'num_votes']

    num_comments = serializers.SerializerMethodField(method_name='count_comments')
    num_votes = serializers.SerializerMethodField(method_name='count_votes')
    user = SimpleUserSerializer(read_only=True)
    
    # Serializer class methods
    def count_comments(self, poll:Poll):
        try:
            return poll.comments.count()
        except AttributeError:
            return 0

    def count_votes(self, poll:Poll):
        return sum([choice.users.count() for choice in poll.choices.all()])

class BaseProfileSerializer(serializers.ModelSerializer):

    class Meta:
        model = Profile
        fields = ['id', 'avatar']