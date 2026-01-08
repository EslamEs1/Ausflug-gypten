"""
User authentication and dashboard views for AusflugAgypten
"""

from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.views.generic import TemplateView, UpdateView
from django.urls import reverse_lazy
from django.db.models import Q
from apps.bookings.models import Booking
from .forms import SignUpForm, LoginForm, UserProfileForm
from .models import UserProfile


def signup_view(request):
    """User registration view"""
    if request.user.is_authenticated:
        return redirect('users:dashboard')
    
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            # Log the user in after successful registration
            login(request, user)
            messages.success(
                request,
                f'Willkommen {user.first_name}! Ihr Konto wurde erfolgreich erstellt.'
            )
            return redirect('users:dashboard')
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"{form.fields[field].label}: {error}")
    else:
        form = SignUpForm()
    
    return render(request, 'users/signup.html', {'form': form})


def login_view(request):
    """User login view"""
    if request.user.is_authenticated:
        return redirect('users:dashboard')
    
    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, f'Willkommen zurück, {user.first_name or user.username}!')
                # Redirect to next page if specified
                next_url = request.GET.get('next', 'users:dashboard')
                return redirect(next_url)
        else:
            messages.error(request, 'Ungültiger Benutzername oder Passwort.')
    else:
        form = LoginForm()
    
    return render(request, 'users/login.html', {'form': form})


@login_required
def logout_view(request):
    """User logout view"""
    logout(request)
    messages.success(request, 'Sie wurden erfolgreich abgemeldet.')
    return redirect('core:home')


class DashboardView(LoginRequiredMixin, TemplateView):
    """User dashboard view"""
    template_name = 'users/dashboard.html'
    login_url = 'users:login'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        
        # Get all user bookings
        bookings = Booking.objects.filter(
            Q(user=user) | Q(customer_email=user.email)
        ).select_related(
            'tour', 'excursion', 'activity', 'transfer'
        ).order_by('-created_at')
        
        context['bookings'] = bookings
        context['total_bookings'] = bookings.count()
        context['pending_bookings'] = bookings.filter(status='pending').count()
        context['confirmed_bookings'] = bookings.filter(status='confirmed').count()
        context['completed_bookings'] = bookings.filter(status='completed').count()
        
        return context


class ProfileView(LoginRequiredMixin, UpdateView):
    """User profile view and edit"""
    model = UserProfile
    form_class = UserProfileForm
    template_name = 'users/profile.html'
    success_url = reverse_lazy('users:profile')
    login_url = 'users:login'
    
    def get_object(self, queryset=None):
        return self.request.user.profile
    
    def form_valid(self, form):
        messages.success(self.request, 'Ihr Profil wurde erfolgreich aktualisiert.')
        return super().form_valid(form)
    
    def form_invalid(self, form):
        messages.error(self.request, 'Bitte korrigieren Sie die Fehler im Formular.')
        return super().form_invalid(form)


class BookingHistoryView(LoginRequiredMixin, TemplateView):
    """User booking history view"""
    template_name = 'users/booking_history.html'
    login_url = 'users:login'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        
        # Filter by status if provided
        status = self.request.GET.get('status', '')
        bookings = Booking.objects.filter(
            Q(user=user) | Q(customer_email=user.email)
        ).select_related('tour', 'excursion', 'activity', 'transfer')
        
        if status:
            bookings = bookings.filter(status=status)
        
        bookings = bookings.order_by('-created_at')
        
        context['bookings'] = bookings
        context['current_status'] = status
        
        return context

