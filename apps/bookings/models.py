"""
Booking and Payment models for AusflugAgypten
"""

from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from apps.tours.models import Tour
from apps.excursions.models import Excursion
from apps.activities.models import Activity
from apps.transfers.models import Transfer


class Booking(models.Model):
    """Tour booking model"""
    
    STATUS_CHOICES = [
        ('pending', 'Ausstehend'),
        ('confirmed', 'Bestätigt'),
        ('cancelled', 'Storniert'),
        ('completed', 'Abgeschlossen'),
    ]
    
    # User (optional - can be null for guest bookings)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='bookings', verbose_name="Benutzer")
    
    # Tour/Excursion/Activity/Transfer details (at least one must be set)
    tour = models.ForeignKey(Tour, on_delete=models.CASCADE, related_name='bookings', null=True, blank=True)
    excursion = models.ForeignKey(Excursion, on_delete=models.CASCADE, related_name='bookings', null=True, blank=True)
    activity = models.ForeignKey(Activity, on_delete=models.CASCADE, related_name='bookings', null=True, blank=True)
    transfer = models.ForeignKey(Transfer, on_delete=models.CASCADE, related_name='bookings', null=True, blank=True)
    
    # Customer details
    customer_name = models.CharField(max_length=200, verbose_name="Name")
    customer_email = models.EmailField(verbose_name="E-Mail")
    customer_phone = models.CharField(max_length=50, verbose_name="Telefon")
    
    # Booking details
    booking_date = models.DateField(verbose_name="Buchungsdatum")
    number_of_participants = models.PositiveIntegerField(default=1, verbose_name="Anzahl Teilnehmer")
    adults = models.PositiveIntegerField(default=1, verbose_name="Erwachsene")
    children = models.PositiveIntegerField(default=0, verbose_name="Kinder")
    babies = models.PositiveIntegerField(default=0, verbose_name="Babys")
    total_price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Gesamtpreis")
    
    # Status
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending', verbose_name="Status")
    
    # Notes
    special_requests = models.TextField(blank=True, verbose_name="Besondere Wünsche")
    admin_notes = models.TextField(blank=True, verbose_name="Admin-Notizen")
    
    # Confirmation
    confirmation_code = models.CharField(max_length=50, unique=True, blank=True)
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
        verbose_name = "Booking"
        verbose_name_plural = "Bookings"
        indexes = [
            models.Index(fields=['confirmation_code']),
            models.Index(fields=['status', '-created_at']),
        ]
    
    def __str__(self):
        item_title = "N/A"
        if self.tour:
            item_title = self.tour.title
        elif self.excursion:
            item_title = self.excursion.title
        elif self.activity:
            item_title = self.activity.title
        return f"{self.customer_name} - {item_title} - {self.booking_date}"
    
    def get_booked_item(self):
        """Get the booked tour/excursion/activity/transfer"""
        if self.tour:
            return self.tour
        elif self.excursion:
            return self.excursion
        elif self.activity:
            return self.activity
        elif self.transfer:
            return self.transfer
        return None
    
    def save(self, *args, **kwargs):
        if not self.confirmation_code:
            # Generate confirmation code
            import uuid
            self.confirmation_code = f"AE-{uuid.uuid4().hex[:8].upper()}"
        super().save(*args, **kwargs)


class Payment(models.Model):
    """Payment model for Stripe integration"""
    
    PAYMENT_STATUS_CHOICES = [
        ('pending', 'Ausstehend'),
        ('processing', 'In Bearbeitung'),
        ('succeeded', 'Erfolgreich'),
        ('failed', 'Fehlgeschlagen'),
        ('refunded', 'Erstattet'),
    ]
    
    booking = models.OneToOneField(Booking, on_delete=models.CASCADE, related_name='payment')
    
    # Stripe details
    stripe_payment_intent_id = models.CharField(max_length=200, unique=True)
    stripe_charge_id = models.CharField(max_length=200, blank=True)
    
    # Payment details
    amount = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Betrag")
    currency = models.CharField(max_length=3, default='EUR', verbose_name="Währung")
    status = models.CharField(max_length=20, choices=PAYMENT_STATUS_CHOICES, default='pending', verbose_name="Status")
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    paid_at = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        ordering = ['-created_at']
        verbose_name = "Payment"
        verbose_name_plural = "Payments"
    
    def __str__(self):
        return f"Payment for {self.booking.confirmation_code} - {self.status}"

