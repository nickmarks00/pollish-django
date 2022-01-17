from django.contrib import admin
from .models import User, Profile
from .forms import UserCreationForm
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin


# Register your models here.

class UserAdmin(BaseUserAdmin):
    model = User
    add_form = UserCreationForm


admin.site.register(User, UserAdmin)
admin.site.register(Profile)