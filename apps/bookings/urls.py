"""
Bookings URL patterns
"""

from django.urls import path
from . import views

app_name = 'bookings'

urlpatterns = [
    path('create-checkout-session/', views.CreateCheckoutSessionView.as_view(), name='create_checkout'),
    path('webhook/', views.StripeWebhookView.as_view(), name='stripe_webhook'),
    path('success/', views.BookingSuccessView.as_view(), name='success'),
    path('cancel/', views.BookingCancelView.as_view(), name='cancel'),
    path('inquiry/', views.BookingInquiryView.as_view(), name='inquiry'),
    path('inquiry/success/<str:confirmation_code>/', views.BookingInquirySuccessView.as_view(), name='inquiry_success'),
]

