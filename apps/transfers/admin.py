"""
Admin configuration for Transfers app
"""

from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from .models import (
    TransferType, VehicleType, Transfer, 
    TransferImage, TransferInclusion, TransferImportantInfo, TransferRoute
)


@admin.register(TransferType)
class TransferTypeAdmin(admin.ModelAdmin):
    """📂 Transfer Types - Airport, Hotel, City, etc."""
    
    list_display = ['name', 'is_active', 'order']
    list_editable = ['is_active', 'order']
    list_filter = ['is_active']
    search_fields = ['name', 'name_en']
    prepopulated_fields = {'slug': ('name',)}
    
    fieldsets = (
        ('Transfer Type Details', {
            'fields': ('name', 'name_en', 'slug', 'description', 'icon', 'is_active', 'order')
        }),
    )


@admin.register(VehicleType)
class VehicleTypeAdmin(admin.ModelAdmin):
    """🚗 Vehicle Types - Car, Van, Bus, etc."""
    
    list_display = ['name', 'capacity', 'luggage_capacity', 'is_active', 'order']
    list_editable = ['is_active', 'order']
    list_filter = ['is_active', 'capacity']
    search_fields = ['name', 'name_en']
    prepopulated_fields = {'slug': ('name',)}
    
    fieldsets = (
        ('Vehicle Details', {
            'fields': ('name', 'name_en', 'slug', 'description', 'capacity', 'luggage_capacity', 'image', 'is_active', 'order'),
            'description': 'Capacity = number of passengers, Luggage = number of bags'
        }),
    )


class TransferImageInline(admin.TabularInline):
    """Add photos of vehicles"""
    model = TransferImage
    extra = 1
    fields = ['image', 'alt_text', 'order', 'is_active']
    verbose_name = 'Photo'
    verbose_name_plural = '📸 Transfer Photos'


class TransferInclusionInline(admin.TabularInline):
    """What's included in the service"""
    model = TransferInclusion
    extra = 2
    fields = ['title', 'order']
    verbose_name = 'Service'
    verbose_name_plural = '✓ Included Services'


class TransferImportantInfoInline(admin.TabularInline):
    """Important information for customers"""
    model = TransferImportantInfo
    extra = 2
    fields = ['info', 'order']
    verbose_name = 'Important Note'
    verbose_name_plural = 'ℹ️ Important Information'


class TransferRouteInline(admin.TabularInline):
    """Different routes and their prices"""
    model = TransferRoute
    extra = 1
    fields = ['from_location', 'to_location', 'distance_km', 'estimated_duration', 'price', 'is_active', 'order']
    verbose_name = 'Route'
    verbose_name_plural = '🗺️ Available Routes'


@admin.register(Transfer)
class TransferAdmin(admin.ModelAdmin):
    """🚕 Transfers - Transportation services"""
    
    list_display = ['title', 'transfer_type', 'vehicle_type', 'base_price', 'is_featured', 'is_popular', 'is_active']
    list_filter = ['is_active', 'is_featured', 'is_popular', 'transfer_type', 'vehicle_type', 'availability']
    list_editable = ['is_featured', 'is_popular', 'is_active']
    search_fields = ['title', 'description']
    prepopulated_fields = {'slug': ('title',)}
    date_hierarchy = 'created_at'
    
    fieldsets = (
        ('📝 Basic Information', {
            'fields': ('title', 'slug', 'transfer_type', 'vehicle_type', 'featured_image'),
            'description': 'Essential transfer information'
        }),
        ('📄 Description', {
            'fields': ('short_description', 'description'),
            'description': 'Describe your transfer service'
        }),
        ('💰 Price', {
            'fields': ('base_price', 'price_per_person', 'price_per_km', 'discount_price'),
            'description': 'Set prices (base + per person + per km options)'
        }),
        ('ℹ️ Service Details', {
            'fields': ('duration_minutes', 'availability', 'languages', 'free_cancellation', 'free_waiting_time'),
            'description': 'Duration in minutes, availability (24/7, Daytime, etc.)'
        }),
        ('✈️ Extra Services', {
            'fields': ('flight_monitoring', 'meet_greet'),
            'description': 'Track flight delays, meet & greet service'
        }),
        ('✨ Display Options', {
            'fields': ('is_featured', 'is_popular', 'is_active'),
            'description': 'Featured=Homepage | Popular=Trending badge | Active=Visible'
        }),
    )
    
    inlines = [TransferImageInline, TransferInclusionInline, TransferImportantInfoInline, TransferRouteInline]
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('transfer_type', 'vehicle_type', 'from_location', 'to_location')
