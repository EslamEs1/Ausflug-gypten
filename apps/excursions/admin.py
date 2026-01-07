"""
Admin configuration for Excursions app
"""

from django.contrib import admin
from .models import Excursion, ExcursionImage, ExcursionItinerary, ExcursionInclusion


class ExcursionImageInline(admin.TabularInline):
    model = ExcursionImage
    extra = 3
    fields = ['image', 'caption', 'caption_en', 'order']


class ExcursionItineraryInline(admin.StackedInline):
    model = ExcursionItinerary
    extra = 5
    fields = ['time', 'title', 'title_en', 'description', 'description_en', 'order']


class ExcursionInclusionInline(admin.TabularInline):
    model = ExcursionInclusion
    extra = 5
    fields = ['item', 'item_en', 'is_included', 'order']


@admin.register(Excursion)
class ExcursionAdmin(admin.ModelAdmin):
    list_display = ['title', 'location', 'category', 'price', 'is_bestseller', 'is_popular', 'is_featured', 'is_active', 'created_at']
    list_filter = ['is_active', 'is_featured', 'is_popular', 'is_bestseller', 'location', 'category', 'group_type', 'created_at']
    list_editable = ['is_bestseller', 'is_popular', 'is_featured', 'is_active']
    search_fields = ['title', 'title_en', 'description']
    prepopulated_fields = {'slug': ('title',)}
    date_hierarchy = 'created_at'
    
    inlines = [ExcursionImageInline, ExcursionItineraryInline, ExcursionInclusionInline]
    
    fieldsets = (
        ('Grundinformationen', {
            'fields': ('title', 'title_en', 'slug', 'location', 'category')
        }),
        ('Beschreibungen', {
            'fields': ('description', 'description_en', 'short_description', 'short_description_en')
        }),
        ('Medien', {
            'fields': ('featured_image',)
        }),
        ('Preise', {
            'fields': ('price', 'original_price')
        }),
        ('Ausflug-Details', {
            'fields': ('duration', 'group_type', 'max_participants', 'min_age', 'languages')
        }),
        ('Verfügbarkeit', {
            'fields': ('available_days', 'pickup_included', 'pickup_time')
        }),
        ('Status', {
            'fields': ('is_bestseller', 'is_popular', 'is_featured', 'is_active')
        }),
        ('SEO', {
            'fields': ('meta_description', 'meta_keywords'),
            'classes': ('collapse',)
        }),
    )
    
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.select_related('location', 'category')

