"""
Transfers URL patterns
"""

from django.urls import path
from . import views

app_name = 'transfers'

urlpatterns = [
    path('', views.TransferListView.as_view(), name='list'),
    path('<slug:slug>/', views.TransferDetailView.as_view(), name='detail'),
]

