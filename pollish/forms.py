from django import forms
from .models import Poll

class PollForm(forms.ModelForm):


    class Meta:
        model = Poll
        fields = ['question_text', 'user']
        readonly_fields = ['created_at', 'updated_at']