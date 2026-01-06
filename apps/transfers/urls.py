"""
Transfers URL patterns
"""

from django.urls import path
from django.views.generic import TemplateView

app_name = 'transfers'

urlpatterns = [
    path('', TemplateView.as_view(template_name='transfers/transfer_list.html'), name='list'),
]

