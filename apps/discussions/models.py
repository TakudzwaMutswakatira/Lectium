from django.db import models
from django.conf import settings
from apps.clubs.models import BookClub
from apps.books.models import Book

class Thread(models.Model):
    title = models.CharField(max_length=255)
    
    # Relationships
    club = models.ForeignKey(BookClub, on_delete=models.CASCADE, related_name='threads')
    book = models.ForeignKey(Book, on_delete=models.SET_NULL, null=True, blank=True, related_name='threads')
    creator = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    
    # Spoiler and Organization controls
    chapter_focus = models.CharField(max_length=100, blank=True, null=True, help_text="e.g., 'Chapters 1-5' or 'Full Book'")
    spoilers_allowed = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.title} ({self.club.club_name})"

class Post(models.Model):
    thread = models.ForeignKey(Thread, on_delete=models.CASCADE, related_name='posts')
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    
    content = models.TextField()
    
    # Feature: Annotations & Highlights
    quoted_text = models.TextField(blank=True, null=True, help_text="Highlighted text straight from the book")
    
    # Feature: Granular Spoiler Control (for UI blurring)
    contains_spoilers = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['created_at']  # Ensures posts display chronologically 

    def __str__(self):
        return f"Post by {self.author.username} in {self.thread.title}"