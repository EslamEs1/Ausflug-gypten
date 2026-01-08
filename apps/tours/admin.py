"""
Admin configuration for Tours app
"""

from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from .models import Location, TourCategory, Tour, TourImage, Itinerary, TourInclusion


class TourImageInline(admin.TabularInline):
    """Add photos of your tour"""
    model = TourImage
    extra = 2
    fields = ['image', 'caption', 'order']
    verbose_name = 'Photo'
    verbose_name_plural = '📸 Tour Photos'


class ItineraryInline(admin.StackedInline):
    """Add schedule/program for the tour"""
    model = Itinerary
    extra = 3
    fields = ['time', 'title', 'description', 'order']
    verbose_name = 'Schedule Item'
    verbose_name_plural = '📅 Tour Schedule'


class TourInclusionInline(admin.TabularInline):
    """What's included/not included in the tour"""
    model = TourInclusion
    extra = 3
    fields = ['item', 'is_included', 'order']
    verbose_name = 'Item'
    verbose_name_plural = '✓ Included / ✗ Not Included'


@admin.register(Location)
class LocationAdmin(admin.ModelAdmin):
    """📍 Locations - Cities and areas where tours are offered"""
    
    list_display = ['name', 'is_active', 'order']
    list_editable = ['is_active', 'order']
    list_filter = ['is_active']
    search_fields = ['name', 'name_en']
    prepopulated_fields = {'slug': ('name',)}
    
    fieldsets = (
        ('Location Details', {
            'fields': ('name', 'name_en', 'slug', 'description', 'image', 'is_active', 'order')
        }),
    )


@admin.register(TourCategory)
class TourCategoryAdmin(admin.ModelAdmin):
    """📂 Tour Categories - Types of tours (Cultural, Adventure, etc.)"""
    
    list_display = ['name', 'is_active', 'order']
    list_editable = ['is_active', 'order']
    list_filter = ['is_active']
    search_fields = ['name', 'name_en']
    prepopulated_fields = {'slug': ('name',)}
    
    fieldsets = (
        ('Category Details', {
            'fields': ('name', 'name_en', 'slug', 'description', 'icon', 'is_active', 'order')
        }),
    )


@admin.register(Tour)
class TourAdmin(admin.ModelAdmin):
    """🎯 Tours - Manage your tour packages"""
    
    list_display = ['title', 'location', 'price', 'is_featured', 'is_active']
    list_filter = ['is_active', 'is_featured', 'location', 'category']
    list_editable = ['is_featured', 'is_active']
    search_fields = ['title', 'description']
    prepopulated_fields = {'slug': ('title',)}
    date_hierarchy = 'created_at'
    
    inlines = [TourImageInline, ItineraryInline, TourInclusionInline]
    
    fieldsets = (
        ('📝 Basic Information', {
            'fields': ('title', 'slug', 'location', 'category', 'featured_image'),
            'description': 'Essential tour information'
        }),
        ('📄 Description', {
            'fields': ('short_description', 'description'),
            'description': 'Describe your tour (short description shows in lists)'
        }),
        ('💰 Price', {
            'fields': ('price', 'original_price'),
            'description': 'Set tour prices. Original price shows as crossed out if different'
        }),
        ('ℹ️ Tour Details', {
            'fields': ('duration', 'group_type', 'max_participants', 'min_age', 'languages'),
            'description': 'Duration, group size, age limits, available languages'
        }),
        ('🚗 Pickup & Schedule', {
            'fields': ('pickup_included', 'pickup_time', 'available_days'),
            'description': 'Pickup service and tour availability'
        }),
        ('✨ Display Options', {
            'fields': ('is_featured', 'is_active'),
            'description': 'Featured = Show on homepage | Active = Visible on website'
        }),
    )
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('location', 'category')


# Note: Individual admin classes hidden - manage everything from the Tour edit page above

