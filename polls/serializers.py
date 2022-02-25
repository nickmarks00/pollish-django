from rest_framework import serializers
from .models import Poll, Choice, Comment

from users.serializers import UserSerializer


class ChoiceSerializer(serializers.ModelSerializer):

    # ensures that the id is included
    # there may be issues here in the sense that the id is NOT read-only though it should be
    id = serializers.IntegerField(required=True)
    users = UserSerializer(many=True)
    class Meta:
        model = Choice
        fields = ('choice_text', 'id', 'choice_image', 'users', 'votes')


class CommentSerializer(serializers.ModelSerializer):

    user = UserSerializer(read_only=True)

    class Meta:
        model = Comment
        fields = ('comment_text', 'user', 'created_at')


class PollSerializer(serializers.ModelSerializer):

    # Meta class
    class Meta:
        model = Poll
        fields = ('id', 'user', 'created_at', 'question_text', 'choices', 'num_comments')
    
    # Defined fields
    choices = ChoiceSerializer(many=True)
    user = UserSerializer(read_only=True)
    num_comments = serializers.SerializerMethodField(method_name='count_comments')

    # Serializer class methods
    def count_comments(self, poll:Poll):
        return poll.comments.count()


    # the following method handles creation of new choices
    def create(self, validated_data):
        choices_data = validated_data.pop('choices')
        poll = Poll.objects.create(**validated_data) # I think this should update an existing poll if found, not sure tho...
        for choice_data in choices_data:
            Choice.objects.create(poll=poll, **choice_data)
        return poll

    # handles updating of existing choice (e.g. vote registered)
    def update(self, instance, validated_data):
        instance.choice_text = validated_data.get('choice_text', instance.choice_text)
        instance.votes = validated_data.get('votes', instance.votes)
        instance.save()

        return instance

class SimplePollSerializer(serializers.ModelSerializer):
    class Meta:
        model = Poll
        fields = ('id', 'updated_at', 'question_text', 'total_votes')

    total_votes = serializers.SerializerMethodField(method_name='get_total_votes')

    def get_total_votes(self, poll: Poll):
        return sum([choice.votes for choice in poll.choices.all() ])
