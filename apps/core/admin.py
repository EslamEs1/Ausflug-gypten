"""
Admin configuration for Core app
"""

from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from django.utils.html import format_html
from django.utils import timezone
from datetime import timedelta
from .models import SiteSettings, ContactMessage, HeroSlide, NewsletterSubscriber, PageHero, PageHeroBadge


@admin.register(SiteSettings)
class SiteSettingsAdmin(admin.ModelAdmin):
    """Website Settings - Configure your site information"""
    
    def has_add_permission(self, request):
        return not SiteSettings.objects.exists()
    
    def has_delete_permission(self, request, obj=None):
        return False
    
    fieldsets = (
        ('🌐 Basic Information', {
            'fields': ('site_name', 'site_title', 'site_description', 'site_keywords'),
            'description': 'Basic information about your website'
        }),
        ('🖼️ Logo & Images', {
            'fields': ('logo', 'logo_alt', 'favicon', 'og_image'),
            'description': 'Upload your website logo and favicon'
        }),
        ('📞 Contact Information', {
            'fields': ('address', 'phone', 'email', 'whatsapp'),
            'description': 'Your business contact details'
        }),
        ('📱 Social Media Links', {
            'fields': ('facebook_url', 'instagram_url', 'twitter_url', 'youtube_url', 'linkedin_url'),
            'description': 'Add your social media profile links'
        }),
        ('🕒 Opening Hours', {
            'fields': ('opening_hours_monday_friday', 'opening_hours_saturday', 'opening_hours_sunday'),
            'description': 'Set your business hours'
        }),
        ('📄 Footer Text', {
            'fields': ('footer_text', 'copyright_text'),
            'description': 'Text displayed at the bottom of your website'
        }),
    )


@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    """Customer Messages - View and respond to customer inquiries"""
    
    list_display = ['name', 'email', 'get_subject_display', 'status', 'is_read', 'get_status_badge', 'is_new_message', 'created_at']
    list_filter = ['status', 'is_read', 'subject', 'created_at']
    list_editable = ['status', 'is_read']
    search_fields = ['name', 'email', 'message']
    readonly_fields = ['name', 'email', 'phone', 'subject', 'message', 'created_at', 'updated_at']
    date_hierarchy = 'created_at'
    
    fieldsets = (
        ('👤 Customer Information', {
            'fields': ('name', 'email', 'phone')
        }),
        ('💬 Message Details', {
            'fields': ('subject', 'message')
        }),
        ('✅ Status & Notes', {
            'fields': ('status', 'is_read', 'admin_notes'),
            'description': 'Update status and add your internal notes'
        }),
        ('📅 Dates', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def get_queryset(self, request):
        return super().get_queryset(request).order_by('-created_at')
    
    def get_status_badge(self, obj):
        """Display status with colored badge"""
        from django.utils.html import format_html
        from django.utils import timezone
        from datetime import timedelta
        
        colors = {
            'new': 'danger',
            'read': 'info',
            'replied': 'success',
            'archived': 'secondary',
        }
        color = colors.get(obj.status, 'secondary')
        
        badge = format_html(
            '<span class="badge badge-{}">{}</span>',
            color,
            obj.get_status_display()
        )
        
        if not obj.is_read:
            badge += format_html(' <span class="badge badge-warning">Ungelesen</span>')
        
        return badge
    get_status_badge.short_description = 'Status'
    get_status_badge.admin_order_field = 'status'
    
    def is_new_message(self, obj):
        """Show if message is new and unread"""
        from django.utils.html import format_html
        from django.utils import timezone
        from datetime import timedelta
        
        if obj.status == 'new' and not obj.is_read:
            return format_html('<span class="badge badge-danger">🆕 NEW</span>')
        return ''
    is_new_message.short_description = 'Alert'
    is_new_message.admin_order_field = 'created_at'
    
    def has_add_permission(self, request):
        return False


@admin.register(HeroSlide)
class HeroSlideAdmin(admin.ModelAdmin):
    """Homepage Slider - Manage slideshow on homepage"""
    
    list_display = ['title', 'order', 'is_active', 'button_1_text', 'button_2_text']
    list_filter = ['is_active']
    list_editable = ['order', 'is_active']
    search_fields = ['title', 'subtitle']
    
    fieldsets = (
        ('🖼️ Slide Content', {
            'fields': ('title', 'subtitle', 'image'),
            'description': 'Main content for this slide'
        }),
        ('🔘 First Button (Optional)', {
            'fields': ('button_1_text', 'button_1_url', 'button_1_style'),
            'description': 'Add a button to your slide'
        }),
        ('🔘 Second Button (Optional)', {
            'fields': ('button_2_text', 'button_2_url', 'button_2_style'),
            'description': 'Add a second button to your slide'
        }),
        ('⚙️ Display Settings', {
            'fields': ('order', 'is_active'),
            'description': 'Order: Lower numbers show first. Active: Check to show this slide'
        }),
    )
    
    def get_queryset(self, request):
        return super().get_queryset(request).order_by('order')


@admin.register(NewsletterSubscriber)
class NewsletterSubscriberAdmin(admin.ModelAdmin):
    """Newsletter Subscribers - Manage email list"""
    
    list_display = ['email', 'is_active', 'subscribed_at']
    list_filter = ['is_active', 'subscribed_at']
    list_editable = ['is_active']
    search_fields = ['email']
    readonly_fields = ['email', 'subscribed_at', 'unsubscribed_at']
    date_hierarchy = 'subscribed_at'
    
    fieldsets = (
        ('📧 Email Subscription', {
            'fields': ('email', 'is_active', 'subscribed_at', 'unsubscribed_at'),
            'description': 'Subscriber details and status'
        }),
    )
    
    def get_queryset(self, request):
        return super().get_queryset(request).order_by('-subscribed_at')
    
    def has_add_permission(self, request):
        return False


class PageHeroBadgeInline(admin.TabularInline):
    """Add feature badges (e.g., "Certified", "Best Price")"""
    model = PageHeroBadge
    extra = 1
    fields = ['text', 'text_en', 'icon', 'order']
    ordering = ['order']
    verbose_name = 'Badge'
    verbose_name_plural = 'Feature Badges'


@admin.register(PageHero)
class PageHeroAdmin(admin.ModelAdmin):
    """Page Headers - Customize headers for different pages"""
    
    list_display = ['get_page_display', 'title', 'is_active']
    list_filter = ['is_active', 'page']
    list_editable = ['is_active']
    search_fields = ['title', 'subtitle']
    inlines = [PageHeroBadgeInline]
    
    fieldsets = (
        ('📄 Page Selection', {
            'fields': ('page', 'is_active'),
            'description': 'Choose which page this header is for'
        }),
        ('🖼️ Header Content', {
            'fields': ('title', 'subtitle', 'background_image'),
            'description': 'Main content for the page header'
        }),
        ('🎨 Appearance (Optional)', {
            'fields': ('breadcrumb_text', 'height', 'overlay_opacity'),
            'classes': ('collapse',),
            'description': 'Advanced display settings'
        }),
    )
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related().prefetch_related('badges')


