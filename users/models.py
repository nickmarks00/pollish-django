from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class User(AbstractUser):

   avatar = models.ImageField(upload_to='users', default='no_picture.png')
   updated = models.DateTimeField(auto_now=True)
   bio = models.TextField(max_length=250, default="", blank=True)