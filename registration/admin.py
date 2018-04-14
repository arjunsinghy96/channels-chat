from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from registration.models import User
from registration.forms import UserChangeForm, UserCreationForm

@admin.register(User)
class UserAdmin(BaseUserAdmin):
    """
    Register the custom User model to django admin.
    """
    form = UserChangeForm
    add_form = UserCreationForm

    list_display = ('username', 'email', 'is_staff')
    list_filter = ('is_staff', )

    fieldsets = (
            (None, {'fields': ('username' ,'email', 'password')}),
            ('Personal Info', {'fields': ('first_name', 'last_name', 'phone_no', 'avatar')}),
            ('Permissions', {'fields': ('is_staff', 'is_active', 'groups',
                                        'user_permissions')}),
            ('Important Dates', {'fields': ('last_login', 'date_joined')})
            )

    add_fieldsets = (
            (None, {
                'classes': ('wide',),
                'fields': ('username' ,'email', 'password'),
            }),
        )

    search_fields = ('email', )
    ordering = ('email', )
