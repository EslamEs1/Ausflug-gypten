"""
Activity models for AusflugAgypten
"""

from django.db import models
from django.utils.text import slugify
from django.urls import reverse
from django.core.validators import MinValueValidator, MaxValueValidator
from django.contrib.contenttypes.fields import GenericRelation
from apps.tours.models import Location
from tinymce.models import HTMLField


class ActivityCategory(models.Model):
    """Activity categories (Snorkeling, Cultural, Safari, etc.)"""
    name = models.CharField(max_length=100, verbose_name="Name (DE)")
    name_en = models.CharField(max_length=100, verbose_name="Name (EN)")
    slug = models.SlugField(unique=True, blank=True)
    description = HTMLField(blank=True, verbose_name="Beschreibung (DE)")
    description_en = HTMLField(blank=True, verbose_name="Description (EN)")
    icon = models.CharField(max_length=50, blank=True, help_text="Emoji or icon class (e.g., 🏊, 🏛️, 🏜️)")
    image = models.ImageField(upload_to='activity_categories/', blank=True, null=True)
    gradient_color = models.CharField(
        max_length=50, 
        default='primary-blue',
        help_text="CSS gradient color class (primary-blue, primary-gold, orange-600)"
    )
    is_active = models.BooleanField(default=True)
    order = models.PositiveIntegerField(default=0)
    
    class Meta:
        ordering = ['order', 'name']
        verbose_name = "Activity Category"
        verbose_name_plural = "Activity Categories"
    
    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)
    
    def get_absolute_url(self):
        return reverse('activities:category', kwargs={'slug': self.slug})


class Activity(models.Model):
    """Activity model"""
    # Basic Information
    title = models.CharField(max_length=200, verbose_name="Titel (DE)")
    title_en = models.CharField(max_length=200, verbose_name="Title (EN)")
    slug = models.SlugField(unique=True, blank=True, max_length=250)
    
    # Content
    short_description = models.CharField(max_length=300, blank=True, verbose_name="Kurzbeschreibung (DE)")
    short_description_en = models.CharField(max_length=300, blank=True, verbose_name="Short Description (EN)")
    description = HTMLField(verbose_name="Beschreibung (DE)")
    description_en = HTMLField(verbose_name="Description (EN)")
    
    # Relations
    category = models.ForeignKey(ActivityCategory, on_delete=models.SET_NULL, null=True, related_name='activities')
    location = models.ForeignKey(Location, on_delete=models.SET_NULL, null=True, blank=True, related_name='activities')
    
    # Images
    featured_image = models.ImageField(upload_to='activities/', verbose_name="Hauptbild")
    
    # Pricing
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Preis (EUR)")
    price_per_person = models.BooleanField(default=True, verbose_name="Preis pro Person")
    discount_price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True, verbose_name="Rabattpreis")
    
    # Details
    duration_hours = models.PositiveIntegerField(default=4, verbose_name="Dauer (Stunden)")
    group_size = models.CharField(
        max_length=50,
        default='Klein',
        choices=[
            ('Privat', 'Privat'),
            ('Klein', 'Klein (2-8 Personen)'),
            ('Mittel', 'Mittel (9-15 Personen)'),
            ('Groß', 'Groß (16+ Personen)'),
        ],
        verbose_name="Gruppengröße"
    )
    languages = models.CharField(
        max_length=200,
        default='DE, EN',
        help_text="Komma-getrennte Liste (z.B. 'DE, EN, FR')",
        verbose_name="Verfügbare Sprachen"
    )
    pickup_included = models.BooleanField(default=True, verbose_name="Abholung inklusive")
    
    # Status & Features
    is_active = models.BooleanField(default=True, verbose_name="Aktiv")
    is_featured = models.BooleanField(default=False, verbose_name="Empfohlen")
    is_popular = models.BooleanField(default=False, verbose_name="Beliebt")
    
    # SEO
    meta_description = models.CharField(max_length=160, blank=True)
    meta_keywords = models.CharField(max_length=200, blank=True)
    
    # Reviews (GenericRelation for reverse lookup)
    reviews = GenericRelation('reviews.Review', related_query_name='activity')
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-is_featured', '-is_popular', 'title']
        verbose_name = "Activity"
        verbose_name_plural = "Activities"
        indexes = [
            models.Index(fields=['slug']),
            models.Index(fields=['is_active', 'is_featured']),
            models.Index(fields=['category', 'is_active']),
        ]
    
    def __str__(self):
        return self.title
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)
    
    def get_absolute_url(self):
        return reverse('activities:detail', kwargs={'slug': self.slug})
    
    @property
    def display_price(self):
        """Returns the price to display (discount if available)"""
        return self.discount_price if self.discount_price else self.price
    
    @property
    def has_discount(self):
        """Check if activity has discount"""
        return self.discount_price is not None and self.discount_price < self.price
    
    @property
    def average_rating(self):
        """Calculate average rating from reviews with rating > 3"""
        reviews = self.reviews.filter(is_approved=True, rating__gt=3)
        if reviews.exists():
            return reviews.aggregate(models.Avg('rating'))['rating__avg']
        return None
    
    @property
    def total_reviews(self):
        """Count approved reviews with rating > 3"""
        return self.reviews.filter(is_approved=True, rating__gt=3).count()


class ActivityImage(models.Model):
    """Additional images for activities"""
    activity = models.ForeignKey(Activity, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='activities/gallery/')
    alt_text = models.CharField(max_length=200, blank=True)
    order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)
    
    class Meta:
        ordering = ['order', 'id']
        verbose_name = "Activity Image"
        verbose_name_plural = "Activity Images"
    
    def __str__(self):
        return f"{self.activity.title} - Image {self.order}"


class ActivityInclusion(models.Model):
    """What's included in the activity"""
    activity = models.ForeignKey(Activity, on_delete=models.CASCADE, related_name='inclusions')
    title = models.CharField(max_length=200, verbose_name="Titel (DE)")
    title_en = models.CharField(max_length=200, verbose_name="Title (EN)")
    order = models.PositiveIntegerField(default=0)
    
    class Meta:
        ordering = ['order', 'id']
        verbose_name = "Inclusion"
        verbose_name_plural = "Inclusions"
    
    def __str__(self):
        return f"{self.activity.title} - {self.title}"


class ActivityImportantInfo(models.Model):
    """Important information for the activity"""
    activity = models.ForeignKey(Activity, on_delete=models.CASCADE, related_name='important_info')
    info = models.CharField(max_length=300, verbose_name="Information (DE)")
    info_en = models.CharField(max_length=300, verbose_name="Information (EN)")
    order = models.PositiveIntegerField(default=0)
    
    class Meta:
        ordering = ['order', 'id']
        verbose_name = "Important Information"
        verbose_name_plural = "Important Information"
    
    def __str__(self):
        return f"{self.activity.title} - {self.info}"


