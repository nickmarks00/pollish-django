from rest_framework import serializers
from .models import Poll

class PollSerializer(serializers.ModelSerializer):

    choices = serializers.StringRelatedField(many=True)
    
    class Meta:
        model = Poll
        fields = ('id', 'user', 'created', 'updated', 'question_text', 'choices')