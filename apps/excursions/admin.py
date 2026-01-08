"""
Admin configuration for Excursions app
"""

from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from .models import Excursion, ExcursionImage, ExcursionItinerary, ExcursionInclusion


class ExcursionImageInline(admin.TabularInline):
    """Add photos of your excursion"""
    model = ExcursionImage
    extra = 2
    fields = ['image', 'caption', 'order']
    verbose_name = 'Photo'
    verbose_name_plural = '📸 Excursion Photos'


class ExcursionItineraryInline(admin.StackedInline):
    """Add schedule/program for the excursion"""
    model = ExcursionItinerary
    extra = 3
    fields = ['time', 'title', 'description', 'order']
    verbose_name = 'Schedule Item'
    verbose_name_plural = '📅 Excursion Schedule'


class ExcursionInclusionInline(admin.TabularInline):
    """What's included/not included"""
    model = ExcursionInclusion
    extra = 3
    fields = ['item', 'is_included', 'order']
    verbose_name = 'Item'
    verbose_name_plural = '✓ Included / ✗ Not Included'


@admin.register(Excursion)
class ExcursionAdmin(admin.ModelAdmin):
    """🏖️ Excursions - Day trips and excursions"""
    
    list_display = ['title', 'location', 'price', 'is_bestseller', 'is_popular', 'is_featured', 'is_active']
    list_filter = ['is_active', 'is_featured', 'is_popular', 'is_bestseller', 'location', 'category']
    list_editable = ['is_bestseller', 'is_popular', 'is_featured', 'is_active']
    search_fields = ['title', 'description']
    prepopulated_fields = {'slug': ('title',)}
    date_hierarchy = 'created_at'
    
    inlines = [ExcursionImageInline, ExcursionItineraryInline, ExcursionInclusionInline]
    
    fieldsets = (
        ('📝 Basic Information', {
            'fields': ('title', 'slug', 'location', 'category', 'featured_image'),
            'description': 'Essential excursion information'
        }),
        ('📄 Description', {
            'fields': ('short_description', 'description'),
            'description': 'Describe your excursion'
        }),
        ('💰 Price', {
            'fields': ('price', 'original_price'),
            'description': 'Set prices'
        }),
        ('ℹ️ Excursion Details', {
            'fields': ('duration', 'group_type', 'max_participants', 'min_age', 'languages'),
            'description': 'Duration, group size, age limits'
        }),
        ('🚗 Pickup & Schedule', {
            'fields': ('pickup_included', 'pickup_time', 'available_days'),
            'description': 'Pickup service and availability'
        }),
        ('✨ Display Options', {
            'fields': ('is_bestseller', 'is_popular', 'is_featured', 'is_active'),
            'description': 'Bestseller=Top seller badge | Popular=Trending | Featured=Homepage | Active=Visible'
        }),
    )
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('location', 'category')


