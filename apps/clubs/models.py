from django.db import models
from django.conf import settings

# Create your models here.

class BookClub(models.Model):
    club_name = models.CharField(max_length=255)
    slug = models.SlugField(unique=True)
    description = models.TextField(blank=True)
    
    # Links to CustomUser using the official settings wrapper
    creator = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.SET_NULL, 
        null=True, 
        related_name='created_clubs'
    )
    
    # The dedicated member list
    members = models.ManyToManyField(
        settings.AUTH_USER_MODEL, 
        through='Membership',  # Used an intermediary table to track join dates/roles
        related_name='book_clubs'
    )

    PRIVACY_CHOICES = (
    ('PUB', 'Public'),
    ('INV', 'Invite Only'),
    ('PRV', 'Private'),
)
    privacy_level = models.CharField(max_length=3, choices=PRIVACY_CHOICES, default='PUB')

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.club_name


# 3. Intermediary table for Member roles within specific clubs
class Membership(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    book_club = models.ForeignKey(BookClub, on_delete=models.CASCADE)
    date_joined = models.DateField(auto_now_add=True)
    
    # Roles within the club
    ROLE_CHOICES = (
    ('MEMBER', 'Member'),
    ('MOD', 'Moderator'),
    ('ADMIN', 'Admin'),
)
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='MEMBER')

    class Meta:
        unique_together = ('user', 'book_club')
