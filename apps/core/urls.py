"""
Core URL patterns
"""

from django.urls import path
from . import views

app_name = 'core'

urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    path('about/', views.AboutView.as_view(), name='about'),
    path('faq/', views.FAQView.as_view(), name='faq'),
    path('contact/', views.ContactView.as_view(), name='contact'),
    path('newsletter/', views.NewsletterView.as_view(), name='newsletter'),
    path('privacy/', views.PrivacyView.as_view(), name='privacy'),
    path('impressum/', views.ImpressumView.as_view(), name='impressum'),
    path('terms/', views.TermsView.as_view(), name='terms'),
]

