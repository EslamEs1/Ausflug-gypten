"""
Tour models for AusflugAgypten
"""

from django.db import models
from django.utils.text import slugify
from django.urls import reverse
from django.core.validators import MinValueValidator, MaxValueValidator
from django.contrib.contenttypes.fields import GenericRelation
from tinymce.models import HTMLField


class Location(models.Model):
    """Tour locations (Hurghada, Luxor, Cairo, etc.)"""
    name = models.CharField(max_length=100, verbose_name="Name (DE)")
    name_en = models.CharField(max_length=100, verbose_name="Name (EN)")
    slug = models.SlugField(unique=True, blank=True)
    description = HTMLField(blank=True, verbose_name="Beschreibung (DE)")
    description_en = HTMLField(blank=True, verbose_name="Description (EN)")
    image = models.ImageField(upload_to='locations/', blank=True, null=True)
    is_active = models.BooleanField(default=True)
    order = models.PositiveIntegerField(default=0)
    
    class Meta:
        ordering = ['order', 'name']
        verbose_name = "Location"
        verbose_name_plural = "Locations"
    
    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)


class TourCategory(models.Model):
    """Tour categories (Cultural, Snorkeling, Safari, etc.)"""
    name = models.CharField(max_length=100, verbose_name="Name (DE)")
    name_en = models.CharField(max_length=100, verbose_name="Name (EN)")
    slug = models.SlugField(unique=True, blank=True)
    description = HTMLField(blank=True, verbose_name="Beschreibung (DE)")
    description_en = HTMLField(blank=True, verbose_name="Description (EN)")
    icon = models.CharField(max_length=50, blank=True, help_text="CSS class for icon")
    is_active = models.BooleanField(default=True)
    order = models.PositiveIntegerField(default=0)
    
    class Meta:
        ordering = ['order', 'name']
        verbose_name = "Tour Category"
        verbose_name_plural = "Tour Categories"
    
    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)


class Tour(models.Model):
    """Main Tour model"""
    
    # Basic Information
    title = models.CharField(max_length=200, verbose_name="Titel (DE)")
    title_en = models.CharField(max_length=200, verbose_name="Title (EN)")
    slug = models.SlugField(unique=True, blank=True, max_length=250)
    
    # Descriptions
    description = HTMLField(verbose_name="Beschreibung (DE)")
    description_en = HTMLField(verbose_name="Description (EN)")
    short_description = models.CharField(max_length=300, blank=True, verbose_name="Kurzbeschreibung (DE)")
    short_description_en = models.CharField(max_length=300, blank=True, verbose_name="Short Description (EN)")
    
    # Relations
    location = models.ForeignKey(Location, on_delete=models.CASCADE, related_name='tours')
    category = models.ForeignKey(TourCategory, on_delete=models.SET_NULL, null=True, blank=True, related_name='tours')
    
    # Images
    featured_image = models.ImageField(upload_to='tours/', verbose_name="Hauptbild")
    
    # Pricing
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Preis (EUR)")
    original_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, verbose_name="Originalpreis")
    
    # Tour Details
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
    is_active = models.BooleanField(default=True, verbose_name="Aktiv")
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    # SEO
    meta_description = models.CharField(max_length=160, blank=True)
    meta_keywords = models.CharField(max_length=200, blank=True)
    
    # Reviews (GenericRelation for reverse lookup)
    reviews = GenericRelation('reviews.Review', related_query_name='tour')
    
    class Meta:
        ordering = ['-created_at']
        verbose_name = "Tour"
        verbose_name_plural = "Tours"
        indexes = [
            models.Index(fields=['slug']),
            models.Index(fields=['is_active', 'is_featured']),
        ]
    
    def __str__(self):
        return self.title
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)
    
    def get_absolute_url(self):
        return reverse('tours:detail', kwargs={'slug': self.slug})
    
    @property
    def average_rating(self):
        """Calculate average rating from reviews with rating > 3"""
        reviews = self.reviews.filter(is_approved=True, rating__gt=3)
        if reviews.exists():
            return reviews.aggregate(models.Avg('rating'))['rating__avg']
        return None
    
    @property
    def review_count(self):
        """Count approved reviews with rating > 3"""
        return self.reviews.filter(is_approved=True, rating__gt=3).count()


class TourImage(models.Model):
    """Additional images for tours"""
    tour = models.ForeignKey(Tour, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='tours/gallery/')
    caption = models.CharField(max_length=200, blank=True, verbose_name="Bildunterschrift")
    caption_en = models.CharField(max_length=200, blank=True, verbose_name="Caption (EN)")
    order = models.PositiveIntegerField(default=0)
    
    class Meta:
        ordering = ['order']
        verbose_name = "Tour Image"
        verbose_name_plural = "Tour Images"
    
    def __str__(self):
        return f"{self.tour.title} - Bild {self.order}"


class Itinerary(models.Model):
    """Tour itinerary/schedule"""
    tour = models.ForeignKey(Tour, on_delete=models.CASCADE, related_name='itinerary')
    time = models.CharField(max_length=50, verbose_name="Zeit")
    title = models.CharField(max_length=200, verbose_name="Titel (DE)")
    title_en = models.CharField(max_length=200, verbose_name="Title (EN)")
    description = models.TextField(verbose_name="Beschreibung (DE)")
    description_en = models.TextField(verbose_name="Description (EN)")
    order = models.PositiveIntegerField(default=0)
    
    class Meta:
        ordering = ['order']
        verbose_name = "Itinerary"
        verbose_name_plural = "Itineraries"
    
    def __str__(self):
        return f"{self.tour.title} - {self.time}"


class TourInclusion(models.Model):
    """What's included/excluded in the tour"""
    tour = models.ForeignKey(Tour, on_delete=models.CASCADE, related_name='inclusions')
    item = models.CharField(max_length=200, verbose_name="Element (DE)")
    item_en = models.CharField(max_length=200, verbose_name="Item (EN)")
    is_included = models.BooleanField(default=True, verbose_name="Inklusive")
    order = models.PositiveIntegerField(default=0)
    
    class Meta:
        ordering = ['is_included', 'order']
        verbose_name = "Inclusion/Exclusion"
        verbose_name_plural = "Inclusions/Exclusions"
    
    def __str__(self):
        status = "✓" if self.is_included else "✗"
        return f"{status} {self.item}"

