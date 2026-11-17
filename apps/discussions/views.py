from django.shortcuts import get_object_or_404
from django.urls import reverse
from django.views.generic import ListView, DetailView, CreateView
from django.contrib.auth.mixins import LoginRequiredMixin

from apps.clubs.models import BookClub
from .models import Thread, Post


class ClubThreadListView(ListView):
    model = Thread
    template_name = 'discussions/thread_list.html'
    context_object_name = 'threads'

    def get_queryset(self):
        self.club = get_object_or_404(BookClub, slug=self.kwargs['slug'])
        return Thread.objects.filter(book_club=self.club)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['club'] = self.club
        return context


class ThreadDetailView(DetailView):
    model = Thread
    template_name = 'discussions/thread_detail.html'
    context_object_name = 'thread'
    pk_url_kwarg = 'thread_pk'

    def get_queryset(self):
        self.club = get_object_or_404(BookClub, slug=self.kwargs['slug'])
        return Thread.objects.filter(book_club=self.club)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['club'] = self.club
        context['posts'] = self.object.posts.select_related('user').all()
        return context


class ThreadCreateView(LoginRequiredMixin, CreateView):
    model = Thread
    template_name = 'discussions/thread_form.html'
    fields = ['title', 'book', 'chapter_focus', 'spoilers_allowed']

    def dispatch(self, request, *args, **kwargs):
        self.club = get_object_or_404(BookClub, slug=self.kwargs['slug'])
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['club'] = self.club
        return context

    def form_valid(self, form):
        form.instance.book_club = self.club
        form.instance.creator = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('discussions:thread_detail', kwargs={
            'slug': self.club.slug,
            'thread_pk': self.object.pk
        })


class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    fields = ['quoted_text', 'content', 'contains_spoilers']

    def dispatch(self, request, *args, **kwargs):
        self.club = get_object_or_404(BookClub, slug=self.kwargs['slug'])
        self.thread = get_object_or_404(Thread, pk=self.kwargs['thread_pk'], book_club=self.club)
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        form.instance.thread = self.thread
        form.instance.user = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('discussions:thread_detail', kwargs={
            'slug': self.club.slug,
            'thread_pk': self.thread.pk
        })