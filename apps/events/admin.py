from django.contrib import admin
from .models import Meeting, RSVP

# Register your models here.

admin.site.register(Meeting)
admin.site.register(RSVP)