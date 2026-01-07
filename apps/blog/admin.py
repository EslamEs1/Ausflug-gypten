"""
Admin configuration for Blog app
"""

from django.contrib import admin
from ckeditor_uploader.widgets import CKEditorUploadingWidget
from django import forms
from .models import BlogCategory, BlogPost


class BlogPostAdminForm(forms.ModelForm):
    content = forms.CharField(widget=CKEditorUploadingWidget(), required=False)
    content_en = forms.CharField(widget=CKEditorUploadingWidget(), required=False)
    
    class Meta:
        model = BlogPost
        fields = '__all__'


@admin.register(BlogCategory)
class BlogCategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'name_en', 'slug', 'is_active']
    list_editable = ['is_active']
    list_filter = ['is_active']
    search_fields = ['name', 'name_en']
    prepopulated_fields = {'slug': ('name',)}


@admin.register(BlogPost)
class BlogPostAdmin(admin.ModelAdmin):
    form = BlogPostAdminForm
    list_display = ['title', 'category', 'author', 'is_published', 'published_at', 'created_at']
    list_filter = ['is_published', 'category', 'created_at']
    list_editable = ['is_published']
    search_fields = ['title', 'title_en', 'content']
    prepopulated_fields = {'slug': ('title',)}
    date_hierarchy = 'published_at'
    
    fieldsets = (
        ('Grundinformationen', {
            'fields': ('title', 'title_en', 'slug', 'category', 'author')
        }),
        ('Inhalt', {
            'fields': ('excerpt', 'excerpt_en', 'content', 'content_en', 'featured_image')
        }),
        ('Veröffentlichung', {
            'fields': ('is_published', 'published_at', 'reading_time')
        }),
        ('SEO', {
            'fields': ('meta_description', 'meta_keywords'),
            'classes': ('collapse',)
        }),
    )
    
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.select_related('category', 'author')

