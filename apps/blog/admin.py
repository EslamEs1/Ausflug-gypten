"""
Admin configuration for Blog app
"""

from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from .models import BlogCategory, BlogPost


@admin.register(BlogCategory)
class BlogCategoryAdmin(admin.ModelAdmin):
    """📂 Blog Categories - Topics for blog posts"""
    
    list_display = ['name', 'is_active']
    list_editable = ['is_active']
    list_filter = ['is_active']
    search_fields = ['name', 'name_en']
    prepopulated_fields = {'slug': ('name',)}
    
    fieldsets = (
        ('Category Details', {
            'fields': ('name', 'name_en', 'slug', 'description', 'is_active')
        }),
    )


@admin.register(BlogPost)
class BlogPostAdmin(admin.ModelAdmin):
    """📝 Blog Posts - Write articles and news"""
    
    list_display = ['title', 'category', 'author', 'is_published', 'published_at']
    list_filter = ['is_published', 'category', 'created_at']
    list_editable = ['is_published']
    search_fields = ['title', 'content']
    prepopulated_fields = {'slug': ('title',)}
    date_hierarchy = 'published_at'
    
    fieldsets = (
        ('📝 Post Information', {
            'fields': ('title', 'slug', 'category', 'author', 'featured_image'),
            'description': 'Basic blog post information'
        }),
        ('📄 Content', {
            'fields': ('excerpt', 'content'),
            'description': 'Excerpt = Short preview shown in lists | Content = Full article'
        }),
        ('📅 Publication', {
            'fields': ('is_published', 'published_at', 'reading_time'),
            'description': 'Published = Visible on website | Reading time = minutes to read'
        }),
    )
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('category', 'author')
    
    def save_model(self, request, obj, form, change):
        if not obj.author_id:
            obj.author = request.user
        super().save_model(request, obj, form, change)
