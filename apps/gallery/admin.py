"""
Admin configuration for Gallery app
"""

from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from .models import GalleryCategory, GalleryImage


@admin.register(GalleryCategory)
class GalleryCategoryAdmin(admin.ModelAdmin):
    """📂 Gallery Categories - Albums/collections"""
    
    list_display = ['name', 'icon', 'is_active', 'order']
    list_editable = ['is_active', 'order']
    list_filter = ['is_active']
    search_fields = ['name', 'name_en']
    prepopulated_fields = {'slug': ('name',)}
    
    fieldsets = (
        ('Category Details', {
            'fields': ('name', 'name_en', 'slug', 'description', 'icon', 'is_active', 'order'),
            'description': 'Create photo albums/collections'
        }),
    )


@admin.register(GalleryImage)
class GalleryImageAdmin(admin.ModelAdmin):
    """📸 Gallery Photos - Manage your photo gallery"""
    
    list_display = ['title', 'category', 'location', 'is_featured', 'is_active', 'order']
    list_filter = ['is_active', 'is_featured', 'category', 'location', 'created_at']
    list_editable = ['is_featured', 'is_active', 'order']
    search_fields = ['title', 'description']
    date_hierarchy = 'created_at'
    
    fieldsets = (
        ('📸 Photo Information', {
            'fields': ('title', 'category', 'location', 'image', 'alt_text'),
            'description': 'Upload photo and add details'
        }),
        ('📄 Description', {
            'fields': ('description',),
            'description': 'Describe the photo (optional)'
        }),
        ('📋 Photo Details (Optional)', {
            'fields': ('photographer', 'taken_at'),
            'classes': ('collapse',),
            'description': 'Who took the photo and when'
        }),
        ('✨ Display Options', {
            'fields': ('is_featured', 'is_active', 'order'),
            'description': 'Featured=Show prominently | Active=Visible | Order=Display sequence'
        }),
    )
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('category', 'location')
