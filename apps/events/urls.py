from django.urls import path
from .views import (
    MeetingListView,
    MeetingDetailView,
    MeetingCreateView,
    RSVPCreateUpdateView,
)

app_name = 'events'

urlpatterns = [
    path('clubs/<slug:slug>/meetings/', MeetingListView.as_view(), name='meeting_list'),
    path('clubs/<slug:slug>/meetings/create/', MeetingCreateView.as_view(), name='meeting_create'),
    path('clubs/<slug:slug>/meetings/<int:meeting_pk>/', MeetingDetailView.as_view(), name='meeting_detail'),
    path('clubs/<slug:slug>/meetings/<int:meeting_pk>/rsvp/', RSVPCreateUpdateView.as_view(), name='meeting_rsvp'),
]