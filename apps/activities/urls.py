"""
Activities URL patterns
"""

from django.urls import path
from . import views

app_name = 'activities'

urlpatterns = [
    path('', views.ActivityListView.as_view(), name='list'),
    path('<slug:slug>/', views.ActivityDetailView.as_view(), name='detail'),
]

