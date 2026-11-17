from django.db import models
from django.conf import settings
from apps.clubs.models import BookClub
from apps.books.models import Book


class Thread(models.Model):
    title = models.CharField(max_length=255)
    book_club = models.ForeignKey(
        BookClub,
        on_delete=models.CASCADE,
        related_name='threads'
    )
    book = models.ForeignKey(
        Book,
        on_delete=models.CASCADE,
        related_name='threads'
    )
    creator = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        related_name='created_threads'
    )
    chapter_focus = models.CharField(max_length=100)
    spoilers_allowed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title} ({self.book_club.club_name})"


class Post(models.Model):
    thread = models.ForeignKey(
        Thread,
        on_delete=models.CASCADE,
        related_name='posts'
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='posts'
    )
    quoted_text = models.TextField(blank=True, help_text="Optional passage quoted from the book")
    content = models.TextField(help_text="Your discussion response")
    contains_spoilers = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Post by {self.user.username} in {self.thread.title}"