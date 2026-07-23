from django.db import models

# Create your models here.

class Book(models.Model):
    book_title = models.CharField(max_length=255)
    book_subtitle = models.CharField(max_length=255, blank=True, null=True)
    book_ISBN = models.CharField("ISBN", max_length=13, unique=True)
    author = models.CharField(max_length=255)
    publisher = models.CharField(max_length=255)
    cover_url = models.URLField(max_length=500, blank=True, null=True)
    google_books_id = models.CharField(max_length=250, blank=True)

    publication_date = models.DateField()
    page_count = models.PositiveIntegerField()
    language = models.CharField(max_length=50, default='English')
    edition = models.CharField(max_length=50, blank=True, null=True)

    bisac_code = models.CharField("BISAC Code", max_length=20, blank=True, null=True)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.book_title
