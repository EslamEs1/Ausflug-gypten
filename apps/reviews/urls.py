"""
URL patterns for Reviews app
"""

from django.urls import path
from . import views

app_name = 'reviews'

urlpatterns = [
    path('submit/', views.SubmitReviewView.as_view(), name='submit'),
]

