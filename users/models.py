from django.db import models

# Create your models here.
class User(models.Model):
   name = models.CharField(max_length=50, blank=False,unique=True)
   username = models.CharField(max_length=50, blank=False, unique=True, default='username')
   image = models.ImageField(upload_to='users', default='no_picture.png')
   created = models.DateTimeField(auto_now_add=True)

   def __str__(self):
      return f"{self.username}"