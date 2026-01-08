"""
Gallery models for AusflugAgypten
"""

from django.db import models
from django.utils.text import slugify
from django.urls import reverse
from apps.tours.models import Location


class GalleryCategory(models.Model):
    """Gallery categories (Hurghada, Luxor, Safari, Snorkeling, etc.)"""
    name = models.CharField(max_length=100, verbose_name="Name (DE)")
    name_en = models.CharField(max_length=100, verbose_name="Name (EN)")
    slug = models.SlugField(unique=True, blank=True)
    description = models.TextField(blank=True, verbose_name="Beschreibung (DE)")
    description_en = models.TextField(blank=True, verbose_name="Description (EN)")
    icon = models.CharField(max_length=50, blank=True, help_text="Emoji or icon (e.g., 🏖️, 🏛️, 🏜️)")
    is_active = models.BooleanField(default=True)
    order = models.PositiveIntegerField(default=0)
    
    class Meta:
        ordering = ['order', 'name']
        verbose_name = "Gallery Category"
        verbose_name_plural = "Gallery Categories"
    
    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)


class GalleryImage(models.Model):
    """Gallery image model"""
    # Basic Information
    title = models.CharField(max_length=200, verbose_name="Titel (DE)")
    title_en = models.CharField(max_length=200, blank=True, verbose_name="Title (EN)")
    description = models.TextField(blank=True, verbose_name="Beschreibung (DE)")
    description_en = models.TextField(blank=True, verbose_name="Description (EN)")
    
    # Image
    image = models.ImageField(upload_to='gallery/', verbose_name="Bild")
    thumbnail = models.ImageField(upload_to='gallery/thumbnails/', blank=True, null=True, verbose_name="Vorschaubild")
    
    # Relations
    category = models.ForeignKey(GalleryCategory, on_delete=models.SET_NULL, null=True, blank=True, related_name='images')
    location = models.ForeignKey(Location, on_delete=models.SET_NULL, null=True, blank=True, related_name='gallery_images')
    
    # Metadata
    photographer = models.CharField(max_length=200, blank=True, verbose_name="Fotograf")
    taken_at = models.DateField(blank=True, null=True, verbose_name="Aufgenommen am")
    alt_text = models.CharField(max_length=200, blank=True, verbose_name="Alt-Text")
    
    # Status
    is_featured = models.BooleanField(default=False, verbose_name="Hervorgehoben")
    is_active = models.BooleanField(default=True, verbose_name="Aktiv")
    
    # Ordering
    order = models.PositiveIntegerField(default=0, verbose_name="Reihenfolge")
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['order', '-is_featured', '-created_at']
        verbose_name = "Gallery Image"
        verbose_name_plural = "Gallery Images"
        indexes = [
            models.Index(fields=['is_active', 'is_featured']),
            models.Index(fields=['category', 'is_active']),
            models.Index(fields=['location', 'is_active']),
        ]
    
    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        return reverse('gallery:detail', kwargs={'pk': self.pk})
    
    @property
    def display_title(self):
        """Returns title based on current language"""
        # This would need i18n middleware to work properly
        return self.title
    
    @property
    def display_description(self):
        """Returns description based on current language"""
        return self.description


