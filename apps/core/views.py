"""
Core views for AusflugAgypten
"""

from django.views.generic import TemplateView, FormView
from django.contrib import messages
from django.urls import reverse_lazy
from django.shortcuts import redirect, render
from django.http import HttpResponseBadRequest, HttpResponseForbidden, HttpResponseNotFound, HttpResponseServerError
from apps.tours.models import Tour
from apps.blog.models import BlogPost
from .models import ContactMessage
from .forms import ContactForm


class HomeView(TemplateView):
    """Homepage view"""
    template_name = 'pages/home.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Featured tours
        context['featured_tours'] = Tour.objects.filter(
            is_active=True,
            is_featured=True
        ).select_related('location', 'category')[:6]
        
        # Latest blog posts
        context['latest_posts'] = BlogPost.objects.filter(
            is_published=True
        ).select_related('category', 'author')[:3]
        
        return context


class AboutView(TemplateView):
    """About page"""
    template_name = 'pages/about.html'


class FAQView(TemplateView):
    """FAQ page"""
    template_name = 'pages/faq.html'


class PrivacyView(TemplateView):
    """Privacy policy page"""
    template_name = 'pages/privacy.html'


class ImpressumView(TemplateView):
    """Impressum page"""
    template_name = 'pages/impressum.html'


class TermsView(TemplateView):
    """Terms and conditions page"""
    template_name = 'pages/terms.html'


class ContactView(FormView):
    """Contact page with form handling"""
    template_name = 'apps/core/templates/core/contact.html'
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

