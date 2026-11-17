from django.urls import path
from .views import (
    ClubThreadListView,
    ThreadDetailView,
    ThreadCreateView,
    PostCreateView,
)

app_name = 'discussions'

urlpatterns = [
    path('clubs/<slug:slug>/threads/', ClubThreadListView.as_view(), name='thread_list'),
    path('clubs/<slug:slug>/threads/create/', ThreadCreateView.as_view(), name='thread_create'),
    path('clubs/<slug:slug>/threads/<int:thread_pk>/', ThreadDetailView.as_view(), name='thread_detail'),
    path('clubs/<slug:slug>/threads/<int:thread_pk>/posts/create/', PostCreateView.as_view(), name='post_create'),
]