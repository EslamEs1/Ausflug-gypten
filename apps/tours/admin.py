"""
Admin configuration for Tours app
"""

from django.contrib import admin
from .models import Location, TourCategory, Tour, TourImage, Itinerary, TourInclusion


class TourImageInline(admin.TabularInline):
    model = TourImage
    extra = 3
    fields = ['image', 'caption', 'caption_en', 'order']


class ItineraryInline(admin.StackedInline):
    model = Itinerary
    extra = 5
    fields = ['time', 'title', 'title_en', 'description', 'description_en', 'order']


class TourInclusionInline(admin.TabularInline):
    model = TourInclusion
    extra = 5
    fields = ['item', 'item_en', 'is_included', 'order']


@admin.register(Location)
class LocationAdmin(admin.ModelAdmin):
    list_display = ['name', 'name_en', 'slug', 'is_active', 'order']
    list_editable = ['is_active', 'order']
    list_filter = ['is_active']
    search_fields = ['name', 'name_en']
    prepopulated_fields = {'slug': ('name',)}


@admin.register(TourCategory)
class TourCategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'name_en', 'slug', 'is_active', 'order']
    list_editable = ['is_active', 'order']
    list_filter = ['is_active']
    search_fields = ['name', 'name_en']
    prepopulated_fields = {'slug': ('name',)}


@admin.register(Tour)
class TourAdmin(admin.ModelAdmin):
    list_display = ['title', 'location', 'category', 'price', 'is_featured', 'is_active', 'created_at']
    list_filter = ['is_active', 'is_featured', 'location', 'category', 'group_type']
    list_editable = ['is_featured', 'is_active']
    search_fields = ['title', 'title_en', 'description']
    prepopulated_fields = {'slug': ('title',)}
    date_hierarchy = 'created_at'
    
    inlines = [TourImageInline, ItineraryInline, TourInclusionInline]
    
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
        ('Tour-Details', {
            'fields': ('duration', 'group_type', 'max_participants', 'min_age', 'languages')
        }),
        ('Verfügbarkeit', {
            'fields': ('available_days', 'pickup_included', 'pickup_time')
        }),
        ('Status', {
            'fields': ('is_featured', 'is_active')
        }),
        ('SEO', {
            'fields': ('meta_description', 'meta_keywords'),
            'classes': ('collapse',)
        }),
    )
    
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.select_related('location', 'category')


@admin.register(TourImage)
class TourImageAdmin(admin.ModelAdmin):
    list_display = ['tour', 'caption', 'order']
    list_filter = ['tour']
    search_fields = ['tour__title', 'caption']


@admin.register(Itinerary)
class ItineraryAdmin(admin.ModelAdmin):
    list_display = ['tour', 'time', 'title', 'order']
    list_filter = ['tour']
    search_fields = ['tour__title', 'title']


@admin.register(TourInclusion)
class TourInclusionAdmin(admin.ModelAdmin):
    list_display = ['tour', 'item', 'is_included', 'order']
    list_filter = ['tour', 'is_included']
    search_fields = ['tour__title', 'item']

