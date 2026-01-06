"""
Activities URL patterns
"""

from django.urls import path
from django.views.generic import TemplateView

app_name = 'activities'

urlpatterns = [
    path('', TemplateView.as_view(template_name='activities/activity_list.html'), name='list'),
    path('<slug:slug>/', TemplateView.as_view(template_name='activities/activity_detail.html'), name='detail'),
]

