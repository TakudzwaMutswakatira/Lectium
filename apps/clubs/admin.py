from django.contrib import admin
from .models import BookClub, Membership


@admin.register(BookClub)
class BookClubAdmin(admin.ModelAdmin):
    list_display = ('club_name', 'slug', 'creator')
    prepopulated_fields = {'slug': ('club_name',)}


@admin.register(Membership)
class MembershipAdmin(admin.ModelAdmin):
    list_display = ('user', 'book_club', 'is_moderator', 'joined_at')
    list_filter = ('is_moderator', 'book_club')