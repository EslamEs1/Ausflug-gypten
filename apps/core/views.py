"""
Core views for AusflugAgypten
"""

from django.views.generic import TemplateView, FormView
from django.contrib import messages
from django.urls import reverse_lazy
from django.shortcuts import redirect, render
from django.http import HttpResponseBadRequest, HttpResponseForbidden, HttpResponseNotFound, HttpResponseServerError
from django.contrib.contenttypes.models import ContentType
from apps.tours.models import Tour, Location
from apps.excursions.models import Excursion
from apps.activities.models import Activity, ActivityCategory
from apps.reviews.models import Review
from apps.blog.models import BlogPost
from .models import ContactMessage, HeroSlide
from .forms import ContactForm, NewsletterForm


class HomeView(TemplateView):
    """Homepage view"""
    template_name = 'core/index.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Hero slides
        context['hero_slides'] = HeroSlide.objects.filter(
            is_active=True
        ).order_by('order', 'created_at')
        
        # Popular tours (for "Beliebte Ausflüge" section)
        context['popular_tours'] = Tour.objects.filter(
            is_active=True,
            is_featured=True
        ).select_related('location', 'category').prefetch_related('images', 'reviews')[:3]
        
        # Featured tours (if needed separately)
        context['featured_tours'] = Tour.objects.filter(
            is_active=True,
            is_featured=True
        ).select_related('location', 'category')[:6]
        
        # Locations for categories section
        context['locations'] = Location.objects.filter(
            is_active=True
        ).order_by('order', 'name')[:4]
        
        # Activity categories for activities section
        context['activity_categories'] = ActivityCategory.objects.filter(
            is_active=True
        ).order_by('order', 'name')[:4]
        
        # Featured activities (if needed)
        context['featured_activities'] = Activity.objects.filter(
            is_active=True,
            is_featured=True
        ).select_related('category', 'location').prefetch_related('images')[:4]
        
        # Reviews/Testimonials - get approved reviews with rating > 3 for tours
        tour_content_type = ContentType.objects.get_for_model(Tour)
        context['reviews'] = Review.objects.filter(
            is_approved=True,
            content_type=tour_content_type,
            rating__gt=3
        ).select_related('content_type')[:6]
        
        # Latest blog posts
        context['latest_posts'] = BlogPost.objects.filter(
            is_published=True
        ).select_related('category', 'author')[:3]
        
        return context


class AboutView(TemplateView):
    """About page"""
    template_name = 'core/about.html'


class FAQView(TemplateView):
    """FAQ page"""
    template_name = 'core/faq.html'


class PrivacyView(TemplateView):
    """Privacy policy page"""
    template_name = 'core/privacy.html'


class ImpressumView(TemplateView):
    """Impressum page"""
    template_name = 'core/impressum.html'


class TermsView(TemplateView):
    """Terms and conditions page"""
    template_name = 'core/terms.html'


class ContactView(FormView):
    """Contact page with form handling"""
    template_name = 'core/contact.html'
    form_class = ContactForm
    success_url = reverse_lazy('core:contact')
    
    def form_valid(self, form):
        # Save the contact message
        contact_message = form.save()
        
        # Add success message
        messages.success(
            self.request,
            f'Vielen Dank, {contact_message.name}! Ihre Nachricht wurde erfolgreich gesendet. Wir werden uns bald bei Ihnen melden.'
        )
        
        return redirect(self.success_url)
    
    def form_invalid(self, form):
        messages.error(
            self.request,
            'Bitte überprüfen Sie Ihre Eingaben und versuchen Sie es erneut.'
        )
        return super().form_invalid(form)


class NewsletterView(FormView):
    """Newsletter subscription view"""
    form_class = NewsletterForm
    http_method_names = ['post']
    
    def form_valid(self, form):
        subscriber = form.save()
        messages.success(
            self.request,
            f'Vielen Dank! Ihre E-Mail-Adresse ({subscriber.email}) wurde erfolgreich für unseren Newsletter angemeldet.'
        )
        # Redirect back to the referring page or home
        referer = self.request.META.get('HTTP_REFERER', '/')
        return redirect(referer)
    
    def form_invalid(self, form):
        # Get the first error message
        error_message = 'Bitte überprüfen Sie Ihre E-Mail-Adresse und versuchen Sie es erneut.'
        if form.errors:
            first_error = list(form.errors.values())[0][0]
            error_message = first_error
        
        messages.error(self.request, error_message)
        # Redirect back to the referring page or home
        referer = self.request.META.get('HTTP_REFERER', '/')
        return redirect(referer)


# Error Handler Views
def bad_request_view(request, exception):
    """400 Bad Request error handler"""
    return render(request, '400.html', status=400)


def permission_denied_view(request, exception):
    """403 Forbidden error handler"""
    return render(request, '403.html', status=403)


def page_not_found_view(request, exception):
    """404 Page Not Found error handler"""
    return render(request, '404.html', status=404)


def server_error_view(request):
    """500 Server Error error handler"""
    return render(request, '500.html', status=500)

