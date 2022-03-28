from django.core.validators import MinValueValidator
from django.conf import settings
from django.db import models
from uuid import uuid4


class Profile(models.Model):

    def __str__(self):
        return f'{self.user.username}'
    
    # can't access the instance.username, because this action  occurs before Django has access to that data
    def upload_to(instance, filename):
        return f'profiles/{instance}/{filename}'


    #TODO change the upload_to property
    avatar = models.ImageField(upload_to=upload_to, default='no_picture.png')
    bio = models.TextField(max_length=250, default="", null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    # removes dependency of Profile on specific User model
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='profile')
    uuid = models.UUIDField(default=uuid4)

    


class Poll(models.Model):

    def __str__(self):
        return f"{self.question_text} by {self.user.username}"

    created_at = models.DateTimeField(auto_now_add=True)
    question_text = models.TextField(blank=False, default="")
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='polls', on_delete=models.CASCADE)
    updated_at = models.DateTimeField(auto_now=True)
    uuid = models.UUIDField(default=uuid4)



    class Meta:
        unique_together = ['user', 'created_at']  # user cannot create multiple posts at the same time
        ordering = ['-updated_at']  # default ordering for posts is time of last update


class Choice(models.Model):
    choice_text = models.CharField(max_length=255, blank=False, default="")
    poll = models.ForeignKey(Poll, on_delete=models.CASCADE, related_name='choices')
    # I've added blank here so that the field is not required on form submisson -- not working currently
    users = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='choices', blank=True)
    uuid = models.UUIDField(default=uuid4)
    votes = models.IntegerField(default=0, blank=False, validators=[MinValueValidator(0)])


    def __str__(self):
        return "{} --- {}".format(self.poll.question_text,self.choice_text)


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
            return f'user_{self.poll.user.id}/poll_{self.poll.id}/choice_{self.choice.id}/{filename}'
        return f'user_{self.poll.user.id}/poll_{self.poll.id}/{filename}'

    image = models.ImageField(upload_to=poll_directory_path)
    poll = models.ForeignKey(Poll, related_name="images", on_delete=models.CASCADE )
    choice = models.OneToOneField(Choice, null=True, on_delete=models.PROTECT)

    class Meta:
        # unique_together = ['poll', 'choice']
        pass


