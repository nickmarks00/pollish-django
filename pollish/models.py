from django.conf import settings
from django.db import models
from uuid import uuid4


class Profile(models.Model):

    def __str__(self):
        return f'{self.user.username}'
    
    def profile_path(self, filename):
        return f'users/user_{self.user.id}/profile_{self.id}/{filename}'
        

    avatar = models.ImageField(upload_to=profile_path, default='no_picture.png')
    bio = models.TextField(max_length=250, default="", null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    # removes dependency of Profile on specific User model
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='profile')
    uuid = models.UUIDField(default=uuid4)
    votes_registered = models.PositiveIntegerField(default=0)


class Community(models.Model):

    def community_directory_path(self, filename):
        return f'communities/community_{self.name}/{filename}'

    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT)
    image = models.ImageField(upload_to=community_directory_path, blank=True, null=True)
    name = models.CharField(max_length=255)
    users = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='communities', blank=True)
    uuid = models.UUIDField(default=uuid4)
    


class Poll(models.Model):

    def __str__(self):
        return f"{self.question_text} by {self.user.username}"

    community = models.ForeignKey(Community, related_name='polls', blank=True, null=True, on_delete=models.PROTECT)
    created_at = models.DateTimeField(auto_now_add=True)
    question_text = models.TextField(blank=False)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='polls', on_delete=models.CASCADE)
    updated_at = models.DateTimeField(auto_now=True)
    uuid = models.UUIDField(default=uuid4)

    class Meta:
        unique_together = ['user', 'created_at']  # user cannot create multiple posts at the same time
        ordering = ['-updated_at']  # default ordering for posts is time of last update


class Choice(models.Model):
    choice_text = models.CharField(max_length=255, blank=False)
    poll = models.ForeignKey(Poll, on_delete=models.CASCADE, related_name='choices')
    users = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='choices', blank=True)
    uuid = models.UUIDField(default=uuid4)
    
    def __str__(self):
        return self.choice_text


class Comment(models.Model):
    choice = models.ForeignKey(Choice, on_delete=models.PROTECT, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    comment_text = models.TextField()
    poll = models.ForeignKey(Poll, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='comments')
    uuid = models.UUIDField(default=uuid4)


    def __str__(self):
        return f'{self.comment_text}'


class PollImage(models.Model):

    # specifies upload path for poll images
    def poll_directory_path(self, filename):
        if self.choice:
            return f'users/user_{self.poll.user.id}/poll_{self.poll.id}/choice_{self.choice.id}/{filename}'
        return f'user_{self.poll.user.id}/poll_{self.poll.id}/{filename}'

    image = models.ImageField(upload_to=poll_directory_path)
    poll = models.ForeignKey(Poll, related_name="images", on_delete=models.CASCADE )
    choice = models.OneToOneField(Choice, null=True, on_delete=models.PROTECT)




