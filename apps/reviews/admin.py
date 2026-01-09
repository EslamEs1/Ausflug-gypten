"""
Admin configuration for Reviews app
"""

from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from django.utils.html import format_html
from .models import Review


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    """⭐ Customer Reviews - Approve/manage reviews"""
    
    list_display = ['name', 'get_rating_stars', 'get_review_type', 'is_approved', 'get_approval_badge', 'needs_approval', 'created_at']
    list_filter = ['is_approved', 'rating', 'content_type', 'created_at']
    list_editable = ['is_approved']
    search_fields = ['name', 'email', 'title', 'comment']
    date_hierarchy = 'created_at'
    readonly_fields = ['name', 'email', 'content_type', 'object_id', 'rating', 'title', 'comment', 'created_at']
    
    fieldsets = (
        ('⭐ Review Details', {
            'fields': ('rating', 'title', 'comment'),
            'description': 'What the customer wrote'
        }),
        ('👤 Customer Information', {
            'fields': ('name', 'email'),
            'description': 'Who wrote this review'
        }),
        ('📝 Review For', {
            'fields': ('content_type', 'object_id'),
            'description': 'Which tour/excursion/activity this review is for'
        }),
        ('✅ Approval Status', {
            'fields': ('is_approved', 'created_at'),
            'description': 'Check "Approved" to show this review on your website'
        }),
    )
    
    actions = ['approve_reviews', 'disapprove_reviews']
    
    def approve_reviews(self, request, queryset):
        updated = queryset.update(is_approved=True)
        self.message_user(request, f'{updated} review(s) approved and will now be visible on the website.')
    approve_reviews.short_description = "✅ Approve selected reviews"
    
    def disapprove_reviews(self, request, queryset):
        updated = queryset.update(is_approved=False)
        self.message_user(request, f'{updated} review(s) hidden from the website.')
    disapprove_reviews.short_description = "❌ Hide selected reviews"
    
    def get_review_type(self, obj):
        return obj.content_type.model.upper()
    get_review_type.short_description = 'Type'
    
    def get_rating_stars(self, obj):
        """Display rating as stars"""
        stars = '★' * obj.rating + '☆' * (5 - obj.rating)
        color = '#ffc107' if obj.rating >= 4 else '#ff9800' if obj.rating >= 3 else '#f44336'
        return format_html(
            '<span style="color: {}; font-size: 1.2em;">{}</span> <strong>({})</strong>',
            color,
            stars,
            obj.rating
        )
    get_rating_stars.short_description = 'Rating'
    get_rating_stars.admin_order_field = 'rating'
    
    def get_approval_badge(self, obj):
        """Display approval status with badge"""
        if obj.is_approved:
            return format_html('<span class="badge badge-success">✓ Genehmigt</span>')
        else:
            return format_html('<span class="badge badge-warning">⏳ Ausstehend</span>')
    get_approval_badge.short_description = 'Status'
    get_approval_badge.admin_order_field = 'is_approved'
    
    def needs_approval(self, obj):
        """Show alert if review needs approval"""
        if not obj.is_approved:
            return format_html('<span class="badge badge-danger">⚠️ Prüfen</span>')
        return ''
    needs_approval.short_description = 'Alert'
    needs_approval.admin_order_field = 'is_approved'
    
    def has_add_permission(self, request):
        return False
