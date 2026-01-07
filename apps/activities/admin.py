"""
Admin configuration for Activities app
"""

from django.contrib import admin
from .models import ActivityCategory, Activity, ActivityImage, ActivityInclusion, ActivityImportantInfo


@admin.register(ActivityCategory)
class ActivityCategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'name_en', 'slug', 'icon', 'is_active', 'order']
    list_editable = ['is_active', 'order']
    list_filter = ['is_active']
    search_fields = ['name', 'name_en']
    prepopulated_fields = {'slug': ('name',)}


class ActivityImageInline(admin.TabularInline):
    model = ActivityImage
    extra = 1
    fields = ['image', 'alt_text', 'order', 'is_active']


class ActivityInclusionInline(admin.TabularInline):
    model = ActivityInclusion
    extra = 1
    fields = ['title', 'title_en', 'order']


class ActivityImportantInfoInline(admin.TabularInline):
    model = ActivityImportantInfo
    extra = 1
    fields = ['info', 'info_en', 'order']


@admin.register(Activity)
class ActivityAdmin(admin.ModelAdmin):
    list_display = ['title', 'category', 'location', 'price', 'is_active', 'is_featured', 'is_popular', 'created_at']
    list_filter = ['is_active', 'is_featured', 'is_popular', 'category', 'location', 'created_at']
    list_editable = ['is_active', 'is_featured', 'is_popular']
    search_fields = ['title', 'title_en', 'description']
    prepopulated_fields = {'slug': ('title',)}
    date_hierarchy = 'created_at'
    
    fieldsets = (
        ('Grundinformationen', {
            'fields': ('title', 'title_en', 'slug', 'category', 'location')
        }),
        ('Inhalt', {
            'fields': ('short_description', 'short_description_en', 'description', 'description_en', 'featured_image')
        }),
        ('Preise', {
            'fields': ('price', 'price_per_person', 'discount_price')
        }),
        ('Details', {
            'fields': ('duration_hours', 'group_size', 'languages', 'pickup_included')
        }),
        ('Status & Features', {
            'fields': ('is_active', 'is_featured', 'is_popular')
        }),
        ('SEO', {
            'fields': ('meta_description', 'meta_keywords'),
            'classes': ('collapse',)
        }),
    )
    
    inlines = [ActivityImageInline, ActivityInclusionInline, ActivityImportantInfoInline]
    
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.select_related('category', 'location')

