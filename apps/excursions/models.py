"""
Excursion models for AusflugAgypten
"""

from django.db import models
from django.utils.text import slugify
from django.urls import reverse
from apps.tours.models import Location, TourCategory


class Excursion(models.Model):
    """Excursion model - similar to tours but location-specific"""
    
    # Basic Information
    title = models.CharField(max_length=200, verbose_name="Titel (DE)")
    title_en = models.CharField(max_length=200, verbose_name="Title (EN)")
    slug = models.SlugField(unique=True, blank=True, max_length=250)
    
    # Descriptions
    description = models.TextField(verbose_name="Beschreibung (DE)")
    description_en = models.TextField(verbose_name="Description (EN)")
    short_description = models.CharField(max_length=300, blank=True, verbose_name="Kurzbeschreibung (DE)")
    short_description_en = models.CharField(max_length=300, blank=True, verbose_name="Short Description (EN)")
    
    # Relations
    location = models.ForeignKey(Location, on_delete=models.CASCADE, related_name='excursions')
    category = models.ForeignKey(TourCategory, on_delete=models.SET_NULL, null=True, blank=True, related_name='excursions')
    
    # Images
    featured_image = models.ImageField(upload_to='excursions/', verbose_name="Hauptbild")
    
    # Pricing
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Preis (EUR)")
    original_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, verbose_name="Originalpreis")
    
    # Excursion Details
    duration = models.CharField(max_length=100, verbose_name="Dauer")
    group_type = models.CharField(max_length=50, choices=[
        ('private', 'Privat'),
        ('small_group', 'Kleine Gruppe'),
        ('group', 'Gruppe'),
    ], default='group', verbose_name="Gruppentyp")
    
    max_participants = models.PositiveIntegerField(default=20, verbose_name="Max. Teilnehmer")
    min_age = models.PositiveIntegerField(default=0, verbose_name="Mindestalter")
    
    # Languages
    languages = models.CharField(max_length=200, default="Deutsch, English", verbose_name="Sprachen")
    
    # Availability
    available_days = models.CharField(max_length=200, default="Täglich", verbose_name="Verfügbare Tage")
    pickup_included = models.BooleanField(default=True, verbose_name="Abholung inklusive")
    pickup_time = models.CharField(max_length=100, blank=True, verbose_name="Abholzeit")
    
    # Status
    is_featured = models.BooleanField(default=False, verbose_name="Hervorgehoben")
    is_popular = models.BooleanField(default=False, verbose_name="Beliebt")
    is_bestseller = models.BooleanField(default=False, verbose_name="Bestseller")
    is_active = models.BooleanField(default=True, verbose_name="Aktiv")
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    # SEO
    meta_description = models.CharField(max_length=160, blank=True)
    meta_keywords = models.CharField(max_length=200, blank=True)
    
    class Meta:
        ordering = ['-is_bestseller', '-is_popular', '-is_featured', '-created_at']
        verbose_name = "Ausflug"
        verbose_name_plural = "Ausflüge"
        indexes = [
            models.Index(fields=['slug']),
            models.Index(fields=['is_active', 'is_featured', 'is_popular']),
            models.Index(fields=['location', 'is_active']),
            models.Index(fields=['category', 'is_active']),
        ]
    
    def __str__(self):
        return self.title
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)
    
    def get_absolute_url(self):
        return reverse('excursions:detail', kwargs={'slug': self.slug})
    
    @property
    def average_rating(self):
        """Calculate average rating from reviews"""
        reviews = self.reviews.filter(is_approved=True)
        if reviews.exists():
            return reviews.aggregate(models.Avg('rating'))['rating__avg']
        return 0
    
    @property
    def review_count(self):
        """Count approved reviews"""
        return self.reviews.filter(is_approved=True).count()
    
    @property
    def has_discount(self):
        """Check if excursion has discount"""
        return self.original_price is not None and self.original_price > self.price


class ExcursionImage(models.Model):
    """Additional images for excursions"""
    excursion = models.ForeignKey(Excursion, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='excursions/gallery/')
    caption = models.CharField(max_length=200, blank=True, verbose_name="Bildunterschrift")
    caption_en = models.CharField(max_length=200, blank=True, verbose_name="Caption (EN)")
    order = models.PositiveIntegerField(default=0)
    
    class Meta:
        ordering = ['order']
        verbose_name = "Ausflug-Bild"
        verbose_name_plural = "Ausflug-Bilder"
    
    def __str__(self):
        return f"{self.excursion.title} - Bild {self.order}"


class ExcursionItinerary(models.Model):
    """Excursion itinerary/schedule"""
    excursion = models.ForeignKey(Excursion, on_delete=models.CASCADE, related_name='itinerary')
    time = models.CharField(max_length=50, verbose_name="Zeit")
    title = models.CharField(max_length=200, verbose_name="Titel (DE)")
    title_en = models.CharField(max_length=200, verbose_name="Title (EN)")
    description = models.TextField(verbose_name="Beschreibung (DE)")
    description_en = models.TextField(verbose_name="Description (EN)")
    order = models.PositiveIntegerField(default=0)
    
    class Meta:
        ordering = ['order']
        verbose_name = "Reiseverlauf"
        verbose_name_plural = "Reiseverläufe"
    
    def __str__(self):
        return f"{self.excursion.title} - {self.time}"


class ExcursionInclusion(models.Model):
    """What's included/excluded in the excursion"""
    excursion = models.ForeignKey(Excursion, on_delete=models.CASCADE, related_name='inclusions')
    item = models.CharField(max_length=200, verbose_name="Element (DE)")
    item_en = models.CharField(max_length=200, verbose_name="Item (EN)")
    is_included = models.BooleanField(default=True, verbose_name="Inklusive")
    order = models.PositiveIntegerField(default=0)
    
    class Meta:
        ordering = ['is_included', 'order']
        verbose_name = "Inklusive/Exklusive"
        verbose_name_plural = "Inklusive/Exklusive"
    
    def __str__(self):
        status = "✓" if self.is_included else "✗"
        return f"{status} {self.item}"

