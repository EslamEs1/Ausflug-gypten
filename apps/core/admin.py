"""
Admin configuration for Core app
"""

from django.contrib import admin
from .models import SiteSettings, ContactMessage


@admin.register(SiteSettings)
class SiteSettingsAdmin(admin.ModelAdmin):
    """Admin for site settings - singleton"""
    
    def has_add_permission(self, request):
        # Only allow one instance
        return not SiteSettings.objects.exists()
    
    def has_delete_permission(self, request, obj=None):
        # Prevent deletion
        return False
    
    fieldsets = (
        ('Grundinformationen', {
            'fields': ('site_name', 'site_title', 'site_description', 'site_keywords')
        }),
        ('Logo & Favicon', {
            'fields': ('logo', 'logo_alt', 'favicon', 'og_image')
        }),
        ('Kontaktinformationen', {
            'fields': ('address', 'phone', 'email', 'whatsapp')
        }),
        ('Social Media', {
            'fields': ('facebook_url', 'instagram_url', 'twitter_url', 'youtube_url', 'linkedin_url')
        }),
        ('Öffnungszeiten', {
            'fields': ('opening_hours_monday_friday', 'opening_hours_saturday', 'opening_hours_sunday')
        }),
        ('Footer', {
            'fields': ('footer_text', 'copyright_text')
        }),
    )


@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'subject', 'status', 'is_read', 'created_at']
    list_filter = ['status', 'is_read', 'subject', 'created_at']
    list_editable = ['status', 'is_read']
    search_fields = ['name', 'email', 'message']
    readonly_fields = ['created_at', 'updated_at']
    date_hierarchy = 'created_at'
    
    fieldsets = (
        ('Kontaktinformationen', {
            'fields': ('name', 'email', 'phone')
        }),
        ('Nachricht', {
            'fields': ('subject', 'message')
        }),
        ('Status', {
            'fields': ('status', 'is_read', 'admin_notes')
        }),
        ('Zeitstempel', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def get_queryset(self, request):
        return super().get_queryset(request).order_by('-created_at')

