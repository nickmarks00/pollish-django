from django.contrib import admin
from .models import User
from .forms import PollishUserCreationForm
from django.contrib.auth.admin import UserAdmin

# Register your models here.

class PollishUserAdmin(UserAdmin):
    model = User
    add_form = PollishUserCreationForm

    readonly_fields = ['updated']

    fieldsets = (
        *UserAdmin.fieldsets,
        (
            'User meta',
            {
                'fields': (
                    'avatar',
                    'bio',
                    'updated',
                )
            }
        )
    )

admin.site.register(User, PollishUserAdmin)
