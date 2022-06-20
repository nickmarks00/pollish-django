from django.db import models
from django.contrib.auth.models import AbstractUser

from uuid import uuid4

class User(AbstractUser):
    email = models.EmailField(unique=True)
    uuid = models.UUIDField(default=uuid4)
    following = models.ManyToManyField('User', related_name='followers')


    class Meta:
        ordering = ['id']