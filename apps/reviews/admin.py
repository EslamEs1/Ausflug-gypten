"""
Admin configuration for Reviews app
"""

from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from .models import Review


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    """⭐ Customer Reviews - Approve/manage reviews"""
    
    list_display = ['name', 'rating', 'get_review_type', 'is_approved', 'created_at']
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
    
    def has_add_permission(self, request):
        return False
