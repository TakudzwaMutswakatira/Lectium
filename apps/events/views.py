from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse
from django.views import View
from django.views.generic import ListView, DetailView, CreateView
from django.contrib.auth.mixins import LoginRequiredMixin

from apps.clubs.models import BookClub
from .models import Meeting, RSVP


class MeetingListView(ListView):
    model = Meeting
    template_name = 'events/meeting_list.html'
    context_object_name = 'meetings'

    def get_queryset(self):
        self.club = get_object_or_404(BookClub, slug=self.kwargs['slug'])
        return Meeting.objects.filter(book_club=self.club).order_by('meeting_date')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['club'] = self.club
        return context


class MeetingDetailView(DetailView):
    model = Meeting
    template_name = 'events/meeting_detail.html'
    context_object_name = 'meeting'
    pk_url_kwarg = 'meeting_pk'

    def get_queryset(self):
        self.club = get_object_or_404(BookClub, slug=self.kwargs['slug'])
        return Meeting.objects.filter(book_club=self.club)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['club'] = self.club
        context['rsvps'] = self.object.rsvps.select_related('user').all()
        if self.request.user.is_authenticated:
            user_rsvp = RSVP.objects.filter(user=self.request.user, meeting=self.object).first()
            context['user_rsvp'] = user_rsvp.status if user_rsvp else None
        return context


class MeetingCreateView(LoginRequiredMixin, CreateView):
    model = Meeting
    template_name = 'events/meeting_form.html'
    fields = ['title', 'meeting_date', 'is_virtual', 'location', 'meeting_link']

    def dispatch(self, request, *args, **kwargs):
        self.club = get_object_or_404(BookClub, slug=self.kwargs['slug'])
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['club'] = self.club
        return context

    def form_valid(self, form):
        form.instance.book_club = self.club
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('events:meeting_detail', kwargs={
            'slug': self.club.slug,
            'meeting_pk': self.object.pk
        })


class RSVPCreateUpdateView(LoginRequiredMixin, View):
    def post(self, request, slug, meeting_pk):
        club = get_object_or_404(BookClub, slug=slug)
        meeting = get_object_or_404(Meeting, pk=meeting_pk, book_club=club)
        status = request.POST.get('status')
        if status in ['YES', 'NO', 'MAYBE']:
            RSVP.objects.update_or_create(
                user=request.user,
                meeting=meeting,
                defaults={'status': status}
            )
        return redirect('events:meeting_detail', slug=club.slug, meeting_pk=meeting.pk)