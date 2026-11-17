from django.db import models
from django.conf import settings
from apps.clubs.models import BookClub


class Meeting(models.Model):
    book_club = models.ForeignKey(
        BookClub,
        on_delete=models.CASCADE,
        related_name='meetings'
    )
    title = models.CharField(max_length=255)
    meeting_date = models.DateTimeField(help_text="Format: YYYY-MM-DD HH:MM")
    is_virtual = models.BooleanField(
        default=False,
        help_text="Toggle on if switching to virtual due to loadshedding"
    )
    location = models.CharField(
        max_length=255,
        blank=True,
        help_text="Physical venue address (if in-person or hybrid)"
    )
    meeting_link = models.URLField(
        blank=True,
        help_text="Virtual meeting URL (if virtual or hybrid)"
    )
    attendees = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        through='RSVP',
        related_name='rsvped_meetings'
    )

    def __str__(self):
        mode = "Virtual" if self.is_virtual else "In-Person"
        return f"{self.title} - {self.book_club.club_name} ({mode})"


class RSVP(models.Model):
    STATUS_CHOICES = [
        ('YES', 'Yes'),
        ('NO', 'No'),
        ('MAYBE', 'Maybe'),
    ]
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    meeting = models.ForeignKey(Meeting, on_delete=models.CASCADE, related_name='rsvps')
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='YES')
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('user', 'meeting')

    def __str__(self):
        return f"{self.user.username} - {self.meeting.title}: {self.status}"