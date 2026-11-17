from django.contrib import admin
from .models import Meeting, RSVP


@admin.register(Meeting)
class MeetingAdmin(admin.ModelAdmin):
    list_display = ('title', 'book_club', 'meeting_date', 'is_virtual', 'location')
    list_filter = ('is_virtual', 'book_club')


@admin.register(RSVP)
class RSVPAdmin(admin.ModelAdmin):
    list_display = ('user', 'meeting', 'status', 'updated_at')
    list_filter = ('status',)