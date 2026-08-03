from django.urls import path
from .views import ClubListView, ClubDetailView, ClubCreateView

urlpatterns = [
    # Route: /clubs/
    path('', ClubListView.as_view(), name='club-list'),
    
    # Route: /clubs/create/
    # Note: This must come BEFORE the <slug> route, otherwise Django will think 'create' is a slug!
    path('create/', ClubCreateView.as_view(), name='club-create'),
    
    # Route: /clubs/
    path('<slug:slug>/', ClubDetailView.as_view(), name='club-detail'),

    path('<slug:slug>/join/', JoinClubView.as_view(), name='club-join'),
    path('<slug:slug>/leave/', LeaveClubView.as_view(), name='club-leave'),
]