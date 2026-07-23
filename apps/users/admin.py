from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser

class CustomUserAdmin(UserAdmin):
    model = CustomUser
    
    # This tells the admin panel to include your custom fields on the user edit page
    fieldsets = UserAdmin.fieldsets + (
        ('Book Club Profile', {'fields': ('bio', 'reading_pace')}),
    )

# Register the model and the admin class
admin.site.register(CustomUser, CustomUserAdmin)