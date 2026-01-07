"""
Gallery URL patterns
"""

from django.urls import path
from . import views

app_name = 'gallery'

urlpatterns = [
    path('', views.GalleryListView.as_view(), name='list'),
    path('<int:pk>/', views.GalleryDetailView.as_view(), name='detail'),
]

