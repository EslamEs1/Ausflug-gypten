"""
Admin configuration for Activities app
"""

from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from .models import ActivityCategory, Activity, ActivityImage, ActivityInclusion, ActivityImportantInfo


@admin.register(ActivityCategory)
class ActivityCategoryAdmin(admin.ModelAdmin):
    """📂 Activity Categories - Types of activities"""
    
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


class ActivityImageInline(admin.TabularInline):
    """Add photos of your activity"""
    model = ActivityImage
    extra = 2
    fields = ['image', 'alt_text', 'order', 'is_active']
    verbose_name = 'Photo'
    verbose_name_plural = '📸 Activity Photos'


class ActivityInclusionInline(admin.TabularInline):
    """What's included in the activity"""
    model = ActivityInclusion
    extra = 3
    fields = ['title', 'order']
    verbose_name = 'Inclusion'
    verbose_name_plural = '✓ What\'s Included'


class ActivityImportantInfoInline(admin.TabularInline):
    """Important information for customers"""
    model = ActivityImportantInfo
    extra = 2
    fields = ['info', 'order']
    verbose_name = 'Important Note'
    verbose_name_plural = 'ℹ️ Important Information'


@admin.register(Activity)
class ActivityAdmin(admin.ModelAdmin):
    """🏊 Activities - Water sports, adventures, etc."""
    
    list_display = ['title', 'category', 'location', 'price', 'is_featured', 'is_popular', 'is_active']
    list_filter = ['is_active', 'is_featured', 'is_popular', 'category', 'location']
    list_editable = ['is_featured', 'is_popular', 'is_active']
    search_fields = ['title', 'description']
    prepopulated_fields = {'slug': ('title',)}
    date_hierarchy = 'created_at'
    
    inlines = [ActivityImageInline, ActivityInclusionInline, ActivityImportantInfoInline]
    
    fieldsets = (
        ('📝 Basic Information', {
            'fields': ('title', 'slug', 'category', 'location', 'featured_image'),
            'description': 'Essential activity information'
        }),
        ('📄 Description', {
            'fields': ('short_description', 'description'),
            'description': 'Describe your activity'
        }),
        ('💰 Price', {
            'fields': ('price', 'price_per_person', 'discount_price'),
            'description': 'Set prices (price_per_person = per person pricing)'
        }),
        ('ℹ️ Activity Details', {
            'fields': ('duration_hours', 'group_size', 'languages', 'pickup_included'),
            'description': 'Duration in hours, max group size, available languages'
        }),
        ('✨ Display Options', {
            'fields': ('is_featured', 'is_popular', 'is_active'),
            'description': 'Featured=Homepage | Popular=Trending badge | Active=Visible on website'
        }),
    )
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('category', 'location')
