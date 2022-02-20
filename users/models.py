from django.conf import settings
from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class User(AbstractUser):
    email = models.EmailField(unique=True)

class Profile(models.Model):
    # removes dependency of Profile on specific User model
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='profile')
    #TODO change the upload_to property
    avatar = models.ImageField(upload_to='users', default='no_picture.png')
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)
    bio = models.TextField(max_length=250, default="", null=True, blank=True)

    def __str__(self):
        return f'{self.user.username}'