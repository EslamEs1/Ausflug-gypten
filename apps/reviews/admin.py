"""
Admin configuration for Reviews app
"""

from django.contrib import admin
from .models import Review


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ['name', 'rating', 'content_type', 'object_id', 'is_approved', 'created_at']
    list_filter = ['is_approved', 'rating', 'content_type', 'created_at']
    list_editable = ['is_approved']
    search_fields = ['name', 'email', 'title', 'comment']
    date_hierarchy = 'created_at'
    readonly_fields = ['created_at']
    
    fieldsets = (
        ('Bewertungsinformationen', {
            'fields': ('content_type', 'object_id', 'rating', 'title')
        }),
        ('Kundendaten', {
            'fields': ('name', 'email')
        }),
        ('Kommentar', {
            'fields': ('comment',)
        }),
        ('Status', {
            'fields': ('is_approved', 'created_at')
        }),
    )
    
    actions = ['approve_reviews', 'disapprove_reviews']
    
    def approve_reviews(self, request, queryset):
        queryset.update(is_approved=True)
    approve_reviews.short_description = "Ausgewählte Bewertungen genehmigen"
    
    def disapprove_reviews(self, request, queryset):
        queryset.update(is_approved=False)
    disapprove_reviews.short_description = "Ausgewählte Bewertungen ablehnen"

