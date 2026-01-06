"""
Core views for AusflugAgypten
"""

from django.views.generic import TemplateView
from apps.tours.models import Tour
from apps.blog.models import BlogPost


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


class ContactView(TemplateView):
    """Contact page"""
    template_name = 'pages/contact.html'

