from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import BookClub, Membership
from django.shortcuts import get_object_or_404, redirect
from django.views import View
from django.contrib import messages

class ClubListView(ListView):
    """Fetches all clubs from the database to display on a dashboard."""
    model = BookClub
    context_object_name = 'clubs'
    
    def get_queryset(self):
        # Add filtering here later (e.g., only show public clubs)
        return BookClub.objects.all().order_by('-created_at')

class ClubDetailView(DetailView):
    """Fetches a single club's data based on its slug."""
    model = BookClub
    context_object_name = 'club'
    
    def get_context_data(self, **kwargs):
        # Inject extra backend data here for the template to use later
        context = super().get_context_data(**kwargs)
        context['member_count'] = self.object.members.count()
        return context

class ClubCreateView(LoginRequiredMixin, CreateView):
    """Handles the form to create a new club and assigns backend relationships."""
    model = BookClub
    fields = ['club_name', 'slug', 'description'] 
    # LoginRequiredMixin ensures unauthenticated users are booted to the login page
    
    def form_valid(self, form):
        # 1. Intercept the form submission before saving to the DB
        form.instance.creator = self.request.user
        
        # 2. Save the new club to the database
        response = super().form_valid(form)
        
        # 3. Automatically create a Membership record so the creator 
        # is both a member and a moderator of their new club
        Membership.objects.create(
            user=self.request.user,
            book_club=self.object,
            IS_MODERATOR=True # Note: Change to 'is_moderator' if you updated the PEP8 naming!
        )
        
        return response
        
    def get_success_url(self):
        # Redirect the user to the club's detail page after successful creation
        from django.urls import reverse
        return reverse('club-detail', kwargs={'slug': self.object.slug})


class JoinClubView(LoginRequiredMixin, View):
    """Backend logic to process a user joining a club."""
    def post(self, request, slug):
        # 1. Find the club based on the URL slug
        club = get_object_or_404(BookClub, slug=slug)
        
        # 2. Add the user to the Membership table (get_or_create prevents duplicates)
        Membership.objects.get_or_create(
            user=request.user, 
            book_club=club,
            defaults={'IS_MODERATOR': False} # Note: match your PEP8 casing here
        )
        
        # 3. Queue up a success message for the frontend
        messages.success(request, f"You have successfully joined {club.club_name}!")
        
        # 4. Redirect them right back to the club's detail page
        return redirect('club-detail', slug=slug)


class LeaveClubView(LoginRequiredMixin, View):
    """Backend logic to process a user leaving a club."""
    def post(self, request, slug):
        club = get_object_or_404(BookClub, slug=slug)
        
        # Find the specific membership row and delete it
        Membership.objects.filter(user=request.user, book_club=club).delete()
        
        messages.warning(request, f"You have left {club.club_name}.")
        return redirect('club-list')