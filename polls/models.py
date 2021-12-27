from django.db import models
from users.models import User

# Create your models here.
class Poll(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    question_text = models.CharField(max_length=120, blank=False, default="Add your question here")

    def __str__(self):
        return f"{self.question_text} by {self.user.username}"
    

class Choice(models.Model):
    choice_text = models.CharField(max_length=60, blank=False, default="Add your option here")
    votes = models.PositiveIntegerField(default=0, blank=False)
    poll = models.ForeignKey(Poll, on_delete=models.CASCADE, default=1, related_name='choices')

    def __str__(self):
        return self.choice_text