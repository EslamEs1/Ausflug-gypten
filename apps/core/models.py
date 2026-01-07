"""
Core models for AusflugAgypten
"""

from django.db import models
from django.utils.text import slugify


class SiteSettings(models.Model):
    """Global site settings - singleton model"""
    
    # Site Information
    site_name = models.CharField(max_length=200, default="AusflugÄgypten", verbose_name="Seitenname")
    site_title = models.CharField(max_length=200, default="AusflugÄgypten - Touren, Ausflüge & Aktivitäten in Ägypten", verbose_name="Seitentitel")
    site_description = models.TextField(default="Entdecken Sie die besten Touren und Ausflüge in Ägypten", verbose_name="Seitenbeschreibung")
    site_keywords = models.CharField(max_length=500, default="Ägypten Touren, Hurghada Ausflüge, Luxor, Kairo", verbose_name="Keywords")
    
    # Logo
    logo = models.ImageField(upload_to='site/', null=True, blank=True, verbose_name="Logo")
    logo_alt = models.CharField(max_length=200, default="AusflugÄgypten Logo", verbose_name="Logo Alt Text")
    favicon = models.ImageField(upload_to='site/', null=True, blank=True, verbose_name="Favicon")
    
    # Contact Information
    address = models.CharField(max_length=500, default="Hurghada, Ägypten", verbose_name="Adresse")
    phone = models.CharField(max_length=50, default="+20 123 456 7890", verbose_name="Telefon")
    email = models.EmailField(default="info@ausflugagypten.com", verbose_name="E-Mail")
    whatsapp = models.CharField(max_length=50, default="+201234567890", verbose_name="WhatsApp")
    
    # Social Media
    facebook_url = models.URLField(blank=True, verbose_name="Facebook URL")
    instagram_url = models.URLField(blank=True, verbose_name="Instagram URL")
    twitter_url = models.URLField(blank=True, verbose_name="Twitter URL")
    youtube_url = models.URLField(blank=True, verbose_name="YouTube URL")
    linkedin_url = models.URLField(blank=True, verbose_name="LinkedIn URL")
    
    # Opening Hours
    opening_hours_monday_friday = models.CharField(max_length=100, default="08:00 - 20:00", verbose_name="Montag - Freitag")
    opening_hours_saturday = models.CharField(max_length=100, default="09:00 - 18:00", verbose_name="Samstag")
    opening_hours_sunday = models.CharField(max_length=100, default="10:00 - 16:00", verbose_name="Sonntag")
    
    # Footer
    footer_text = models.TextField(default="Erleben Sie unvergessliche Abenteuer in Ägypten mit unseren maßgeschneiderten Touren und Ausflügen.", verbose_name="Footer Text")
    copyright_text = models.CharField(max_length=200, default="© 2024 AusflugÄgypten. Alle Rechte vorbehalten.", verbose_name="Copyright Text")
    
    # SEO
    og_image = models.ImageField(upload_to='site/', null=True, blank=True, verbose_name="Open Graph Bild")
    
    class Meta:
        verbose_name = "Seiteneinstellungen"
        verbose_name_plural = "Seiteneinstellungen"
    
    def __str__(self):
        return self.site_name
    
    def save(self, *args, **kwargs):
        # Ensure only one instance exists
        self.pk = 1
        super().save(*args, **kwargs)
    
    @classmethod
    def load(cls):
        """Get or create the singleton instance"""
        obj, created = cls.objects.get_or_create(pk=1)
        return obj


class ContactMessage(models.Model):
    """Contact form messages"""
    
    SUBJECT_CHOICES = [
        ('tour_booking', 'Tourbuchung'),
        ('general_inquiry', 'Allgemeine Anfrage'),
        ('complaint', 'Beschwerden'),
        ('other', 'Sonstiges'),
    ]
    
    STATUS_CHOICES = [
        ('new', 'Neu'),
        ('read', 'Gelesen'),
        ('replied', 'Beantwortet'),
        ('archived', 'Archiviert'),
    ]
    
    # Contact Information
    name = models.CharField(max_length=200, verbose_name="Name")
    email = models.EmailField(verbose_name="E-Mail")
    phone = models.CharField(max_length=50, blank=True, verbose_name="Telefon")
    
    # Message
    subject = models.CharField(max_length=50, choices=SUBJECT_CHOICES, verbose_name="Betreff")
    message = models.TextField(verbose_name="Nachricht")
    
    # Status
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='new', verbose_name="Status")
    is_read = models.BooleanField(default=False, verbose_name="Gelesen")
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Erstellt am")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Aktualisiert am")
    
    # Admin Notes
    admin_notes = models.TextField(blank=True, verbose_name="Admin Notizen")
    
    class Meta:
        ordering = ['-created_at']
        verbose_name = "Kontaktnachricht"
        verbose_name_plural = "Kontaktnachrichten"
        indexes = [
            models.Index(fields=['status', '-created_at']),
            models.Index(fields=['is_read', '-created_at']),
        ]
    
    def __str__(self):
        return f"{self.name} - {self.get_subject_display()} ({self.created_at.strftime('%d.%m.%Y')})"

