"""
Blog models for AusflugAgypten
"""

from django.db import models
from django.utils.text import slugify
from django.urls import reverse
from django.contrib.auth import get_user_model
from ckeditor_uploader.fields import RichTextUploadingField

User = get_user_model()


class BlogCategory(models.Model):
    """Blog post categories"""
    name = models.CharField(max_length=100, verbose_name="Name (DE)")
    name_en = models.CharField(max_length=100, verbose_name="Name (EN)")
    slug = models.SlugField(unique=True, blank=True)
    description = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)
    
    class Meta:
        verbose_name = "Blog-Kategorie"
        verbose_name_plural = "Blog-Kategorien"
    
    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)


class BlogPost(models.Model):
    """Blog post model"""
    title = models.CharField(max_length=200, verbose_name="Titel (DE)")
    title_en = models.CharField(max_length=200, verbose_name="Title (EN)")
    slug = models.SlugField(unique=True, blank=True, max_length=250)
    
    content = RichTextUploadingField(verbose_name="Inhalt (DE)")
    content_en = RichTextUploadingField(verbose_name="Content (EN)")
    excerpt = models.CharField(max_length=300, blank=True, verbose_name="Auszug (DE)")
    excerpt_en = models.CharField(max_length=300, blank=True, verbose_name="Excerpt (EN)")
    
    featured_image = models.ImageField(upload_to='blog/', verbose_name="Hauptbild")
    category = models.ForeignKey(BlogCategory, on_delete=models.SET_NULL, null=True, related_name='posts')
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='blog_posts')
    
    # SEO
    meta_description = models.CharField(max_length=160, blank=True)
    meta_keywords = models.CharField(max_length=200, blank=True)
    
    # Status
    is_published = models.BooleanField(default=False, verbose_name="Veröffentlicht")
    published_at = models.DateTimeField(null=True, blank=True)
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    # Reading time
    reading_time = models.PositiveIntegerField(default=5, verbose_name="Lesezeit (Minuten)")
    
    class Meta:
        ordering = ['-published_at']
        verbose_name = "Blog-Artikel"
        verbose_name_plural = "Blog-Artikel"
        indexes = [
            models.Index(fields=['slug']),
            models.Index(fields=['is_published', '-published_at']),
        ]
    
    def __str__(self):
        return self.title
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)
    
    def get_absolute_url(self):
        return reverse('blog:detail', kwargs={'slug': self.slug})

