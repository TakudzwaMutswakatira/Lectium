from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    READING_PACE_CHOICES = [
        ('SLOW', 'Slow (1-2 chapters/week)'),
        ('MODERATE', 'Moderate (3-5 chapters/week)'),
        ('FAST', 'Fast (6+ chapters/week)'),
    ]
    bio = models.TextField(blank=True)
    reading_pace = models.CharField(
        max_length=20,
        choices=READING_PACE_CHOICES,
        default='MODERATE'
    )

    def __str__(self):
        return self.username