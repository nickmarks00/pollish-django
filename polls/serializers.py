from rest_framework import serializers
from .models import Poll, Choice

from users.serializers import UserSerializer


class ChoiceSerializer(serializers.ModelSerializer):

    class Meta:
        model = Choice
        fields = ['choice_text', 'votes']

class PollSerializer(serializers.ModelSerializer):

    choices = ChoiceSerializer(many=True)
    user = UserSerializer(read_only=True)
    
    class Meta:
        model = Poll
        fields = ('id', 'user', 'created', 'updated', 'question_text', 'choices')


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