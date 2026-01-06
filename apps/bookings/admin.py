"""
Admin configuration for Bookings app
"""

from django.contrib import admin
from .models import Booking, Payment


@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ['confirmation_code', 'customer_name', 'tour', 'booking_date', 'number_of_participants', 'total_price', 'status', 'created_at']
    list_filter = ['status', 'booking_date', 'created_at']
    search_fields = ['confirmation_code', 'customer_name', 'customer_email', 'customer_phone']
    date_hierarchy = 'booking_date'
    readonly_fields = ['confirmation_code', 'created_at', 'updated_at']
    
    fieldsets = (
        ('Tour-Informationen', {
            'fields': ('tour', 'booking_date', 'number_of_participants', 'total_price')
        }),
        ('Kundeninformationen', {
            'fields': ('customer_name', 'customer_email', 'customer_phone')
        }),
        ('Status', {
            'fields': ('status', 'confirmation_code')
        }),
        ('Notizen', {
            'fields': ('special_requests', 'admin_notes')
        }),
        ('Zeitstempel', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.select_related('tour')


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ['booking', 'amount', 'currency', 'status', 'stripe_payment_intent_id', 'created_at', 'paid_at']
    list_filter = ['status', 'currency', 'created_at']
    search_fields = ['booking__confirmation_code', 'stripe_payment_intent_id', 'stripe_charge_id']
    readonly_fields = ['stripe_payment_intent_id', 'stripe_charge_id', 'created_at', 'updated_at', 'paid_at']
    date_hierarchy = 'created_at'
    
    fieldsets = (
        ('Buchung', {
            'fields': ('booking',)
        }),
        ('Zahlungsinformationen', {
            'fields': ('amount', 'currency', 'status')
        }),
        ('Stripe-Details', {
            'fields': ('stripe_payment_intent_id', 'stripe_charge_id')
        }),
        ('Zeitstempel', {
            'fields': ('created_at', 'updated_at', 'paid_at'),
            'classes': ('collapse',)
        }),
    )
    
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.select_related('booking', 'booking__tour')

