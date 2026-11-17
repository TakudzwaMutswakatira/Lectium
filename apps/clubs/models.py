from django.db import models
from django.conf import settings
from django.utils.text import slugify


class BookClub(models.Model):
    club_name = models.CharField(max_length=255, unique=True)
    slug = models.SlugField(max_length=255, unique=True, blank=True)
    description = models.TextField()
    creator = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        related_name='created_clubs'
    )
    members = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        through='Membership',
        related_name='book_clubs'
    )

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.club_name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.club_name


class Membership(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    book_club = models.ForeignKey(BookClub, on_delete=models.CASCADE)
    is_moderator = models.BooleanField(default=False)
    joined_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'book_club')

    def __str__(self):
        role = "Moderator" if self.is_moderator else "Member"
        return f"{self.user.username} in {self.book_club.club_name} ({role})"