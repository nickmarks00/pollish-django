from django import forms
from django.contrib.auth.forms import UserCreationForm as BaseUserCreationForm
from .models import User

class UserCreationForm(BaseUserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")