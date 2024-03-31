from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin

from .forms import UserCreateForm, UserUpdateForm

User = get_user_model()


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    add_form = UserCreateForm
    form = UserUpdateForm

    list_display = (
        'email', 'username', 'avatar', 'is_active', 'is_superuser', 'descriptions', 'sex', 'balance',
        'avatar')

    fieldsets = (
        (None, {'fields': ('email', 'is_staff', 'is_superuser', 'email_not')}),
        ('Personal info',
         {'fields': ('username', 'is_active', 'sex', 'descriptions', 'avatar', 'balance')}),
        ('Groups', {'fields': ('groups',)}),
        ('Permissions', {'fields': ('user_permissions',)}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'password1', 'password2'),
        }),
    )
