from django.urls import path
from .views import (
    ClubListView,
    ClubDetailView,
    ClubCreateView,
    ClubJoinLeaveView,
)

app_name = 'clubs'

urlpatterns = [
    path('', ClubListView.as_view(), name='club_list'),
    path('create/', ClubCreateView.as_view(), name='club_create'),
    path('<slug:slug>/', ClubDetailView.as_view(), name='club_detail'),
    path('<slug:slug>/join/', ClubJoinLeaveView.as_view(), name='club_join_leave'),
]