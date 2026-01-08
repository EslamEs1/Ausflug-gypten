"""
Core models for AusflugAgypten
"""

from django.db import models
from django.utils.text import slugify
from django.urls import reverse, NoReverseMatch


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
        verbose_name = "Site Settings"
        verbose_name_plural = "Site Settings"
    
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


class HeroSlide(models.Model):
    """Hero slider slides for homepage"""
    
    BUTTON_STYLE_CHOICES = [
        ('primary', 'Primary Button'),
        ('outline', 'Outline Button'),
    ]
    
    # Slide Content
    image = models.ImageField(upload_to='hero/', verbose_name="Hintergrundbild")
    title = models.CharField(max_length=200, verbose_name="Titel")
    subtitle = models.TextField(verbose_name="Untertitel")
    
    # Button 1
    button_1_text = models.CharField(max_length=100, blank=True, verbose_name="Button 1 Text")
    button_1_url = models.CharField(max_length=500, blank=True, verbose_name="Button 1 URL", help_text="URL oder Django URL Name (z.B. 'excursions:list')")
    button_1_style = models.CharField(max_length=20, choices=BUTTON_STYLE_CHOICES, default='primary', verbose_name="Button 1 Stil")
    
    # Button 2
    button_2_text = models.CharField(max_length=100, blank=True, verbose_name="Button 2 Text")
    button_2_url = models.CharField(max_length=500, blank=True, verbose_name="Button 2 URL", help_text="URL oder Django URL Name (z.B. 'core:contact')")
    button_2_style = models.CharField(max_length=20, choices=BUTTON_STYLE_CHOICES, default='outline', verbose_name="Button 2 Stil")
    
    # Display Settings
    order = models.PositiveIntegerField(default=0, verbose_name="Reihenfolge", help_text="Niedrigere Zahlen werden zuerst angezeigt")
    is_active = models.BooleanField(default=True, verbose_name="Aktiv")
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Erstellt am")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Aktualisiert am")
    
    class Meta:
        ordering = ['order', 'created_at']
        verbose_name = "Hero Slide"
        verbose_name_plural = "Hero Slides"
        indexes = [
            models.Index(fields=['is_active', 'order']),
        ]
    
    def __str__(self):
        return f"{self.title} (Order: {self.order})"
    
    def get_button_1_url(self):
        """Resolve button 1 URL - returns Django URL or direct URL"""
        if not self.button_1_url:
            return '#'
        # Check if it's a direct URL (starts with http://, https://, or /)
        if self.button_1_url.startswith(('http://', 'https://', '/')):
            return self.button_1_url
        # Otherwise, try to resolve as Django URL name
        try:
            return reverse(self.button_1_url)
        except NoReverseMatch:
            # If reverse fails, return as-is (might be a relative URL)
            return self.button_1_url
    
    def get_button_2_url(self):
        """Resolve button 2 URL - returns Django URL or direct URL"""
        if not self.button_2_url:
            return '#'
        # Check if it's a direct URL (starts with http://, https://, or /)
        if self.button_2_url.startswith(('http://', 'https://', '/')):
            return self.button_2_url
        # Otherwise, try to resolve as Django URL name
        try:
            return reverse(self.button_2_url)
        except NoReverseMatch:
            # If reverse fails, return as-is (might be a relative URL)
            return self.button_2_url


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
        verbose_name = "Contact Message"
        verbose_name_plural = "Contact Messages"
        indexes = [
            models.Index(fields=['status', '-created_at']),
            models.Index(fields=['is_read', '-created_at']),
        ]
    
    def __str__(self):
        return f"{self.name} - {self.get_subject_display()} ({self.created_at.strftime('%d.%m.%Y')})"


class NewsletterSubscriber(models.Model):
    """Newsletter subscription model"""
    
    email = models.EmailField(unique=True, verbose_name="E-Mail")
    is_active = models.BooleanField(default=True, verbose_name="Aktiv")
    subscribed_at = models.DateTimeField(auto_now_add=True, verbose_name="Abonniert am")
    unsubscribed_at = models.DateTimeField(null=True, blank=True, verbose_name="Abgemeldet am")
    
    class Meta:
        ordering = ['-subscribed_at']
        verbose_name = "Newsletter Subscriber"
        verbose_name_plural = "Newsletter Subscribers"
        indexes = [
            models.Index(fields=['email', 'is_active']),
        ]
    
    def __str__(self):
        return self.email


class PageHero(models.Model):
    """Hero section for different pages"""
    
    PAGE_CHOICES = [
        ('excursions', 'Ausflüge & Touren'),
        ('blog', 'Blog'),
        ('gallery', 'Galerie'),
        ('transfers', 'Transfer Service'),
        ('activities', 'Aktivitäten'),
    ]
    
    # Page Identification
    page = models.CharField(max_length=50, choices=PAGE_CHOICES, unique=True, verbose_name="Seite")
    
    # Hero Content
    background_image = models.ImageField(upload_to='hero/pages/', verbose_name="Hintergrundbild")
    title = models.CharField(max_length=200, verbose_name="Titel")
    subtitle = models.TextField(verbose_name="Untertitel/Beschreibung")
    breadcrumb_text = models.CharField(max_length=100, blank=True, verbose_name="Breadcrumb Text", help_text="Falls leer, wird der Seitentitel verwendet")
    
    # Display Settings
    height = models.CharField(max_length=20, default="450px", verbose_name="Höhe", help_text="z.B. '450px' oder '500px'")
    overlay_opacity = models.CharField(max_length=20, default="0.7", verbose_name="Overlay Opacity", help_text="z.B. '0.7' für 70% Deckkraft")
    
    # Status
    is_active = models.BooleanField(default=True, verbose_name="Aktiv")
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Erstellt am")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Aktualisiert am")
    
    class Meta:
        ordering = ['page']
        verbose_name = "Page Hero"
        verbose_name_plural = "Page Heroes"
        indexes = [
            models.Index(fields=['page', 'is_active']),
        ]
    
    def __str__(self):
        return f"{self.get_page_display()} - {self.title}"


class PageHeroBadge(models.Model):
    """Badge items for hero sections (e.g., "Zertifiziert", "Sofortige Bestätigung")"""
    
    page_hero = models.ForeignKey(PageHero, on_delete=models.CASCADE, related_name='badges', verbose_name="Seiten Hero")
    icon = models.CharField(max_length=100, blank=True, verbose_name="Icon", help_text="SVG Path oder Emoji")
    text = models.CharField(max_length=100, verbose_name="Text")
    order = models.PositiveIntegerField(default=0, verbose_name="Reihenfolge")
    
    class Meta:
        ordering = ['order', 'id']
        verbose_name = "Hero Badge"
        verbose_name_plural = "Hero Badges"
    
    def __str__(self):
        return f"{self.page_hero.get_page_display()} - {self.text}"


