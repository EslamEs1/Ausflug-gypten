"""
Admin configuration for Gallery app
"""

from django.contrib import admin
from .models import GalleryCategory, GalleryImage


@admin.register(GalleryCategory)
class GalleryCategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'name_en', 'slug', 'icon', 'is_active', 'order']
    list_editable = ['is_active', 'order']
    list_filter = ['is_active']
    search_fields = ['name', 'name_en']
    prepopulated_fields = {'slug': ('name',)}


@admin.register(GalleryImage)
class GalleryImageAdmin(admin.ModelAdmin):
    list_display = ['title', 'category', 'location', 'is_featured', 'is_active', 'order', 'created_at']
    list_filter = ['is_active', 'is_featured', 'category', 'location', 'created_at']
    list_editable = ['is_featured', 'is_active', 'order']
    search_fields = ['title', 'title_en', 'description', 'description_en']
    date_hierarchy = 'created_at'
    
    fieldsets = (
        ('Grundinformationen', {
            'fields': ('title', 'title_en', 'category', 'location')
        }),
        ('Bild', {
            'fields': ('image', 'thumbnail', 'alt_text')
        }),
        ('Beschreibung', {
            'fields': ('description', 'description_en')
        }),
        ('Metadaten', {
            'fields': ('photographer', 'taken_at'),
            'classes': ('collapse',)
        }),
        ('Status', {
            'fields': ('is_featured', 'is_active', 'order')
        }),
    )
    
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.select_related('category', 'location')

