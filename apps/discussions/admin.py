from django.contrib import admin
from .models import Thread, Post


@admin.register(Thread)
class ThreadAdmin(admin.ModelAdmin):
    list_display = ('title', 'book_club', 'book', 'chapter_focus', 'spoilers_allowed')
    list_filter = ('spoilers_allowed', 'book_club')


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('user', 'thread', 'contains_spoilers', 'created_at')
    list_filter = ('contains_spoilers',)