"""
Admin configuration for Transfers app
"""

from django.contrib import admin
from .models import (
    TransferType, VehicleType, Transfer, 
    TransferImage, TransferInclusion, TransferImportantInfo, TransferRoute
)


@admin.register(TransferType)
class TransferTypeAdmin(admin.ModelAdmin):
    list_display = ['name', 'name_en', 'slug', 'icon', 'is_active', 'order']
    list_editable = ['is_active', 'order']
    list_filter = ['is_active']
    search_fields = ['name', 'name_en']
    prepopulated_fields = {'slug': ('name',)}


@admin.register(VehicleType)
class VehicleTypeAdmin(admin.ModelAdmin):
    list_display = ['name', 'name_en', 'capacity', 'luggage_capacity', 'is_active', 'order']
    list_editable = ['is_active', 'order']
    list_filter = ['is_active', 'capacity']
    search_fields = ['name', 'name_en']
    prepopulated_fields = {'slug': ('name',)}


class TransferImageInline(admin.TabularInline):
    model = TransferImage
    extra = 1
    fields = ['image', 'alt_text', 'order', 'is_active']


class TransferInclusionInline(admin.TabularInline):
    model = TransferInclusion
    extra = 1
    fields = ['title', 'title_en', 'order']


class TransferImportantInfoInline(admin.TabularInline):
    model = TransferImportantInfo
    extra = 1
    fields = ['info', 'info_en', 'order']


class TransferRouteInline(admin.TabularInline):
    model = TransferRoute
    extra = 1
    fields = ['from_location', 'to_location', 'distance_km', 'estimated_duration', 'price', 'is_active', 'order']


@admin.register(Transfer)
class TransferAdmin(admin.ModelAdmin):
    list_display = ['title', 'transfer_type', 'vehicle_type', 'base_price', 'is_active', 'is_featured', 'is_popular', 'created_at']
    list_filter = ['is_active', 'is_featured', 'is_popular', 'transfer_type', 'vehicle_type', 'availability', 'created_at']
    list_editable = ['is_active', 'is_featured', 'is_popular']
    search_fields = ['title', 'title_en', 'description']
    prepopulated_fields = {'slug': ('title',)}
    date_hierarchy = 'created_at'
    
    fieldsets = (
        ('Grundinformationen', {
            'fields': ('title', 'title_en', 'slug', 'transfer_type', 'vehicle_type')
        }),
        ('Routen', {
            'fields': ('from_location', 'to_location'),
            'classes': ('collapse',)
        }),
        ('Inhalt', {
            'fields': ('short_description', 'short_description_en', 'description', 'description_en', 'featured_image')
        }),
        ('Preise', {
            'fields': ('base_price', 'price_per_person', 'price_per_km', 'discount_price')
        }),
        ('Details', {
            'fields': ('duration_minutes', 'availability', 'languages', 'free_cancellation', 'free_waiting_time')
        }),
        ('Services', {
            'fields': ('flight_monitoring', 'meet_greet'),
            'classes': ('collapse',)
        }),
        ('Status & Features', {
            'fields': ('is_active', 'is_featured', 'is_popular')
        }),
        ('SEO', {
            'fields': ('meta_description', 'meta_keywords'),
            'classes': ('collapse',)
        }),
    )
    
    inlines = [TransferImageInline, TransferInclusionInline, TransferImportantInfoInline, TransferRouteInline]
    
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.select_related('transfer_type', 'vehicle_type', 'from_location', 'to_location')

