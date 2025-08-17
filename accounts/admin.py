from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User

class UserAdmin(BaseUserAdmin):
    ordering = ['user_id']
    list_display = ['user_id', 'name', 'role', 'is_staff']
    search_fields = ['user_id', 'name']
    
    fieldsets = (
        (None, {'fields': ('user_id', 'password')}),
        ('Personal Info', {'fields': ('name', 'email', 'phone_number', 'program', 'country')}),
        ('Permissions', {'fields': ('role', 'is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login',)}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': (
                'user_id',
                'name',
                'email',
                'phone_number',
                'program',
                'country',
                'role',
                'password1',
                'password2',
            ),
        }),
    )

admin.site.register(User, UserAdmin)
