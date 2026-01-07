"""
Transfer models for AusflugAgypten
"""

from django.db import models
from django.utils.text import slugify
from django.urls import reverse
from django.core.validators import MinValueValidator, MaxValueValidator
from apps.tours.models import Location


class TransferType(models.Model):
    """Transfer types (Airport, Hotel, Private, etc.)"""
    name = models.CharField(max_length=100, verbose_name="Name (DE)")
    name_en = models.CharField(max_length=100, verbose_name="Name (EN)")
    slug = models.SlugField(unique=True, blank=True)
    description = models.TextField(blank=True, verbose_name="Beschreibung (DE)")
    description_en = models.TextField(blank=True, verbose_name="Description (EN)")
    icon = models.CharField(max_length=50, blank=True, help_text="Emoji or icon (e.g., ✈️, 🚗, 🏨)")
    is_active = models.BooleanField(default=True)
    order = models.PositiveIntegerField(default=0)
    
    class Meta:
        ordering = ['order', 'name']
        verbose_name = "Transfer-Typ"
        verbose_name_plural = "Transfer-Typen"
    
    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)


class VehicleType(models.Model):
    """Vehicle types (Sedan, SUV, Minivan, Bus, etc.)"""
    name = models.CharField(max_length=100, verbose_name="Name (DE)")
    name_en = models.CharField(max_length=100, verbose_name="Name (EN)")
    slug = models.SlugField(unique=True, blank=True)
    capacity = models.PositiveIntegerField(verbose_name="Kapazität (Personen)")
    luggage_capacity = models.PositiveIntegerField(default=2, verbose_name="Koffer-Kapazität")
    description = models.TextField(blank=True)
    icon = models.CharField(max_length=50, blank=True)
    is_active = models.BooleanField(default=True)
    order = models.PositiveIntegerField(default=0)
    
    class Meta:
        ordering = ['order', 'capacity']
        verbose_name = "Fahrzeugtyp"
        verbose_name_plural = "Fahrzeugtypen"
    
    def __str__(self):
        return f"{self.name} ({self.capacity} Pers.)"
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)


class Transfer(models.Model):
    """Transfer service model"""
    # Basic Information
    title = models.CharField(max_length=200, verbose_name="Titel (DE)")
    title_en = models.CharField(max_length=200, verbose_name="Title (EN)")
    slug = models.SlugField(unique=True, blank=True, max_length=250)
    
    # Content
    short_description = models.CharField(max_length=300, blank=True, verbose_name="Kurzbeschreibung (DE)")
    short_description_en = models.CharField(max_length=300, blank=True, verbose_name="Short Description (EN)")
    description = models.TextField(verbose_name="Beschreibung (DE)")
    description_en = models.TextField(verbose_name="Description (EN)")
    
    # Relations
    transfer_type = models.ForeignKey(TransferType, on_delete=models.SET_NULL, null=True, related_name='transfers')
    vehicle_type = models.ForeignKey(VehicleType, on_delete=models.SET_NULL, null=True, related_name='transfers')
    from_location = models.ForeignKey(Location, on_delete=models.SET_NULL, null=True, blank=True, related_name='transfers_from', verbose_name="Von")
    to_location = models.ForeignKey(Location, on_delete=models.SET_NULL, null=True, blank=True, related_name='transfers_to', verbose_name="Nach")
    
    # Images
    featured_image = models.ImageField(upload_to='transfers/', verbose_name="Hauptbild", blank=True, null=True)
    
    # Pricing
    base_price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Grundpreis (EUR)")
    price_per_person = models.BooleanField(default=False, verbose_name="Preis pro Person")
    price_per_km = models.BooleanField(default=False, verbose_name="Preis pro Kilometer")
    discount_price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True, verbose_name="Rabattpreis")
    
    # Details
    duration_minutes = models.PositiveIntegerField(default=30, verbose_name="Dauer (Minuten)")
    availability = models.CharField(
        max_length=50,
        default='24/7',
        choices=[
            ('24/7', '24/7 Verfügbar'),
            ('Täglich', 'Täglich'),
            ('Wochentags', 'Wochentags'),
            ('Nach Vereinbarung', 'Nach Vereinbarung'),
        ],
        verbose_name="Verfügbarkeit"
    )
    languages = models.CharField(
        max_length=200,
        default='DE, EN',
        help_text="Komma-getrennte Liste (z.B. 'DE, EN, AR')",
        verbose_name="Verfügbare Sprachen"
    )
    free_cancellation = models.BooleanField(default=True, verbose_name="Kostenlose Stornierung")
    free_waiting_time = models.PositiveIntegerField(default=60, verbose_name="Kostenlose Wartezeit (Minuten)")
    flight_monitoring = models.BooleanField(default=False, verbose_name="Flugüberwachung")
    meet_greet = models.BooleanField(default=True, verbose_name="Meet & Greet Service")
    
    # Status & Features
    is_active = models.BooleanField(default=True, verbose_name="Aktiv")
    is_featured = models.BooleanField(default=False, verbose_name="Empfohlen")
    is_popular = models.BooleanField(default=False, verbose_name="Beliebt")
    
    # SEO
    meta_description = models.CharField(max_length=160, blank=True)
    meta_keywords = models.CharField(max_length=200, blank=True)
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-is_featured', '-is_popular', 'title']
        verbose_name = "Transfer"
        verbose_name_plural = "Transfers"
        indexes = [
            models.Index(fields=['slug']),
            models.Index(fields=['is_active', 'is_featured']),
            models.Index(fields=['transfer_type', 'is_active']),
        ]
    
    def __str__(self):
        return self.title
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)
    
    def get_absolute_url(self):
        return reverse('transfers:detail', kwargs={'slug': self.slug})
    
    @property
    def display_price(self):
        """Returns the price to display (discount if available)"""
        return self.discount_price if self.discount_price else self.base_price
    
    @property
    def has_discount(self):
        """Check if transfer has discount"""
        return self.discount_price is not None and self.discount_price < self.base_price


class TransferImage(models.Model):
    """Additional images for transfers"""
    transfer = models.ForeignKey(Transfer, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='transfers/gallery/')
    alt_text = models.CharField(max_length=200, blank=True)
    order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)
    
    class Meta:
        ordering = ['order', 'id']
        verbose_name = "Transfer-Bild"
        verbose_name_plural = "Transfer-Bilder"
    
    def __str__(self):
        return f"{self.transfer.title} - Image {self.order}"


class TransferInclusion(models.Model):
    """What's included in the transfer"""
    transfer = models.ForeignKey(Transfer, on_delete=models.CASCADE, related_name='inclusions')
    title = models.CharField(max_length=200, verbose_name="Titel (DE)")
    title_en = models.CharField(max_length=200, verbose_name="Title (EN)")
    order = models.PositiveIntegerField(default=0)
    
    class Meta:
        ordering = ['order', 'id']
        verbose_name = "Inklusion"
        verbose_name_plural = "Inklusionen"
    
    def __str__(self):
        return f"{self.transfer.title} - {self.title}"


class TransferImportantInfo(models.Model):
    """Important information for the transfer"""
    transfer = models.ForeignKey(Transfer, on_delete=models.CASCADE, related_name='important_info')
    info = models.CharField(max_length=300, verbose_name="Information (DE)")
    info_en = models.CharField(max_length=300, verbose_name="Information (EN)")
    order = models.PositiveIntegerField(default=0)
    
    class Meta:
        ordering = ['order', 'id']
        verbose_name = "Wichtige Information"
        verbose_name_plural = "Wichtige Informationen"
    
    def __str__(self):
        return f"{self.transfer.title} - {self.info}"


class TransferRoute(models.Model):
    """Common transfer routes"""
    transfer = models.ForeignKey(Transfer, on_delete=models.CASCADE, related_name='routes')
    from_location = models.ForeignKey(Location, on_delete=models.CASCADE, related_name='transfer_routes_from')
    to_location = models.ForeignKey(Location, on_delete=models.CASCADE, related_name='transfer_routes_to')
    distance_km = models.PositiveIntegerField(blank=True, null=True, verbose_name="Entfernung (km)")
    estimated_duration = models.PositiveIntegerField(verbose_name="Geschätzte Dauer (Minuten)")
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Preis (EUR)")
    is_active = models.BooleanField(default=True)
    order = models.PositiveIntegerField(default=0)
    
    class Meta:
        ordering = ['order', 'from_location', 'to_location']
        verbose_name = "Transfer-Route"
        verbose_name_plural = "Transfer-Routen"
        unique_together = ['transfer', 'from_location', 'to_location']
    
    def __str__(self):
        return f"{self.from_location.name} → {self.to_location.name}"

