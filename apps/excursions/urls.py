"""
Excursions URL patterns
"""

from django.urls import path
from . import views

app_name = 'excursions'

urlpatterns = [
    path('', views.ExcursionListView.as_view(), name='list'),
    path('<slug:slug>/', views.ExcursionDetailView.as_view(), name='detail'),
]

