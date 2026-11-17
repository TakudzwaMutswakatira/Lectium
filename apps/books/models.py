from django.db import models


class Book(models.Model):
    title = models.CharField(max_length=255)
    author = models.CharField(max_length=255)
    book_ISBN = models.CharField(max_length=20, unique=True)
    bisac_code = models.CharField(max_length=50)
    page_count = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.title} by {self.author} (ISBN: {self.book_ISBN})"