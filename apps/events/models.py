from django.db import models
from django.conf import settings
from apps.clubs.models import BookClub

# Create your models here.

class Meeting(models.Model):
    club = models.ForeignKey(BookClub, on_delete=models.CASCADE, related_name='meetings')
    organizer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    
    title = models.CharField(max_length=255, help_text="e.g., Chapter 1-5 Discussion & Wine Night")
    description = models.TextField(blank=True, null=True)
    date_time = models.DateTimeField()
    
    # Online,Offline  & Hybrid Pivot Controls
    is_virtual = models.BooleanField(default=False, help_text="Check if meeting is online (or switched due to loadshedding)")
    location = models.CharField(max_length=255, blank=True, null=True, help_text="Physical address for in-person meetups")
    meeting_link = models.URLField(max_length=500, blank=True, null=True, help_text="Zoom/Google Meet link")
    
    # Tracking attendance
    attendees = models.ManyToManyField(
        settings.AUTH_USER_MODEL, 
        through='RSVP', 
        related_name='club_meetings'
    )
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['date_time'] # Displays upcoming meetings first chronologically

    def __str__(self):
        return f"{self.title} - {self.club.club_name}"


class RSVP(models.Model):
    STATUS_CHOICES = (
        ('YES', 'Going'),
        ('NO', 'Not Going'),
        ('MAYBE', 'Maybe'),
    )
    
    meeting = models.ForeignKey(Meeting, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    status = models.CharField(max_length=5, choices=STATUS_CHOICES, default='YES')
    response_date = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('meeting', 'user') # Prevents duplicate RSVPs from the same user

    def __str__(self):
        return f"{self.user.username} - {self.get_status_display()} for {self.meeting.title}"