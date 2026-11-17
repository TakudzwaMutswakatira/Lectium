from django.contrib import admin
from .models import Book


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'book_ISBN', 'bisac_code', 'page_count')
    search_fields = ('title', 'author', 'book_ISBN')