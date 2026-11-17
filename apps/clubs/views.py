from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse
from django.views import View
from django.views.generic import ListView, DetailView, CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import BookClub, Membership


class ClubListView(ListView):
    model = BookClub
    template_name = 'clubs/bookclub_list.html'
    context_object_name = 'clubs'


class ClubDetailView(DetailView):
    model = BookClub
    template_name = 'clubs/bookclub_detail.html'
    context_object_name = 'club'
    slug_url_kwarg = 'slug'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['member_count'] = self.object.members.count()
        context['threads'] = self.object.threads.all()
        context['meetings'] = self.object.meetings.all()
        if self.request.user.is_authenticated:
            context['is_member'] = Membership.objects.filter(
                user=self.request.user,
                book_club=self.object
            ).exists()
        else:
            context['is_member'] = False
        return context


class ClubCreateView(LoginRequiredMixin, CreateView):
    model = BookClub
    template_name = 'clubs/bookclub_form.html'
    fields = ['club_name', 'slug', 'description']

    def form_valid(self, form):
        form.instance.creator = self.request.user
        response = super().form_valid(form)
        # Auto-generate moderator Membership for the creator
        Membership.objects.create(
            user=self.request.user,
            book_club=self.object,
            is_moderator=True
        )
        return response

    def get_success_url(self):
        return reverse('clubs:club_detail', kwargs={'slug': self.object.slug})


class ClubJoinLeaveView(LoginRequiredMixin, View):
    def post(self, request, slug):
        club = get_object_or_404(BookClub, slug=slug)
        membership = Membership.objects.filter(user=request.user, book_club=club).first()
        if membership:
            membership.delete()
        else:
            Membership.objects.create(user=request.user, book_club=club, is_moderator=False)
        return redirect('clubs:club_detail', slug=club.slug)