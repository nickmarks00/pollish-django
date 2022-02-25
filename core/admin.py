from django.contrib import admin
from .models import User, Profile
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

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    # Change form
    autocomplete_fields = ['user']
    fields = ['user', 'created_at', 'updated_at', 'avatar', 'bio']
    readonly_fields = ['updated_at', 'created_at']

    # Change list
    list_display = ['user', 'updated_at', 'avatar',  'bio']
    list_editable = []
    list_per_page = 25

    search_fields = ['user__username']
