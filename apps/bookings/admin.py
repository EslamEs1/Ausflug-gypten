"""
Admin configuration for Bookings app
"""

from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from django.utils.html import format_html
from django.utils import timezone
from datetime import timedelta
from .models import Booking, Payment


@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    """📅 Bookings - Manage customer reservations"""
    
    list_display = ['confirmation_code', 'customer_name', 'get_booking_type', 'booking_date', 'get_participants_breakdown', 'status', 'get_status_badge', 'is_new_booking', 'created_at']
    list_filter = ['status', 'booking_date', 'created_at']
    search_fields = ['confirmation_code', 'customer_name', 'customer_email', 'customer_phone']
    date_hierarchy = 'booking_date'
    readonly_fields = ['confirmation_code', 'created_at', 'updated_at']
    list_editable = ['status']
    
    fieldsets = (
        ('📋 Booking Information', {
            'fields': ('confirmation_code', 'booking_date', 'adults', 'children', 'babies', 'number_of_participants', 'total_price'),
            'description': 'Booking details and confirmation code'
        }),
        ('🎯 What They Booked', {
            'fields': ('user', 'tour', 'excursion', 'activity', 'transfer'),
            'description': 'Which service was booked (only one will be filled)'
        }),
        ('👤 Customer Information', {
            'fields': ('customer_name', 'customer_email', 'customer_phone'),
            'description': 'Customer contact details'
        }),
        ('✅ Status & Notes', {
            'fields': ('status', 'special_requests', 'admin_notes'),
            'description': 'Update booking status and add internal notes'
        }),
        ('📅 Dates', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('tour', 'excursion', 'activity', 'transfer', 'user')
    
    def get_booking_type(self, obj):
        if obj.tour:
            return f"TOUR: {obj.tour.title}"
        elif obj.excursion:
            return f"EXCURSION: {obj.excursion.title}"
        elif obj.activity:
            return f"ACTIVITY: {obj.activity.title}"
        elif obj.transfer:
            return f"TRANSFER: {obj.transfer.title}"
        return "N/A"
    get_booking_type.short_description = 'Booked Service'
    
    def get_participants_breakdown(self, obj):
        parts = []
        if obj.adults > 0:
            parts.append(f"{obj.adults} Adults")
        if obj.children > 0:
            parts.append(f"{obj.children} Children")
        if obj.babies > 0:
            parts.append(f"{obj.babies} Babies")
        return " / ".join(parts) if parts else f"{obj.number_of_participants} Total"
    get_participants_breakdown.short_description = 'Participants'
    
    def get_status_badge(self, obj):
        """Display status with colored badge"""
        colors = {
            'pending': 'warning',
            'confirmed': 'success',
            'cancelled': 'danger',
            'completed': 'info',
        }
        color = colors.get(obj.status, 'secondary')
        return format_html(
            '<span class="badge badge-{}">{}</span>',
            color,
            obj.get_status_display()
        )
    get_status_badge.short_description = 'Status'
    get_status_badge.admin_order_field = 'status'
    
    def is_new_booking(self, obj):
        """Show if booking is new (within last 7 days)"""
        if obj.status == 'pending' and obj.created_at >= timezone.now() - timedelta(days=7):
            return format_html('<span class="badge badge-danger">🆕 NEW</span>')
        return ''
    is_new_booking.short_description = 'Alert'
    is_new_booking.admin_order_field = 'created_at'
    
    def has_add_permission(self, request):
        return False


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    """💳 Payments - Track payment transactions"""
    
    list_display = ['get_booking_code', 'amount', 'currency', 'status', 'created_at', 'paid_at']
    list_filter = ['status', 'currency', 'created_at']
    search_fields = ['booking__confirmation_code', 'stripe_payment_intent_id']
    readonly_fields = ['booking', 'amount', 'currency', 'stripe_payment_intent_id', 'stripe_charge_id', 'created_at', 'updated_at', 'paid_at']
    date_hierarchy = 'created_at'
    
    fieldsets = (
        ('💳 Payment Information', {
            'fields': ('booking', 'amount', 'currency', 'status'),
            'description': 'Payment details and status'
        }),
        ('🔒 Stripe Details', {
            'fields': ('stripe_payment_intent_id', 'stripe_charge_id'),
            'description': 'Payment gateway transaction IDs'
        }),
        ('📅 Dates', {
            'fields': ('created_at', 'updated_at', 'paid_at'),
            'description': 'When payment was made'
        }),
    )
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('booking')
    
    def get_booking_code(self, obj):
        return obj.booking.confirmation_code if obj.booking else 'N/A'
    get_booking_code.short_description = 'Booking Code'
    
    def has_add_permission(self, request):
        return False
