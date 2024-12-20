from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser

class CustomUserAdmin(UserAdmin):
    list_display = ('email', 'username', 'role', 'rating', 'is_staff', 'is_active')
    list_filter = ('role', 'is_staff', 'is_active')
    search_fields = ('username', 'email')
    ordering = ('email',)
    fieldsets = (
        (None, {'fields': ('email', 'password', 'username', 'role', 'rating')}),
        ('Permissions', {'fields': ('is_staff', 'is_superuser', 'is_active', 'groups', 'user_permissions')}),
        ('Dates', {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2', 'username', 'role', 'rating', 'is_staff', 'is_active')}
        ),
    )

admin.site.register(CustomUser, CustomUserAdmin)
