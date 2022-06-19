from django.contrib import admin
from .models import User
from .forms import UserCreationForm
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin


# Register your models here.

class UserAdmin(BaseUserAdmin):
    model = User
    add_form = UserCreationForm

    # fieldsets = (
    #     *BaseUserAdmin.fieldsets,
    #     (
    #         'User profile',
    #         {
    #             'fields': [
    #                 'profile',
    #             ]
    #         }
    #     )
    # )


admin.site.register(User, UserAdmin)


