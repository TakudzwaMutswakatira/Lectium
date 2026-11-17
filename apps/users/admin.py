from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser


@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    fieldsets = UserAdmin.fieldsets + (
        ('Librarium Profile', {'fields': ('bio', 'reading_pace')}),
    )
    list_display = ('username', 'email', 'reading_pace', 'is_staff')