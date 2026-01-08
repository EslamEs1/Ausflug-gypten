"""
User models for AusflugAgypten
"""

from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


class UserProfile(models.Model):
    """Extended user profile"""
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    
    # Personal information
    phone = models.CharField(max_length=50, blank=True, verbose_name="Telefon")
    country = models.CharField(max_length=100, blank=True, verbose_name="Land")
    city = models.CharField(max_length=100, blank=True, verbose_name="Stadt")
    address = models.TextField(blank=True, verbose_name="Adresse")
    
    # Preferences
    language_preference = models.CharField(
        max_length=2,
        choices=[('de', 'Deutsch'), ('en', 'English')],
        default='de',
        verbose_name="Bevorzugte Sprache"
    )
    newsletter_subscribed = models.BooleanField(default=False, verbose_name="Newsletter abonniert")
    
    # Profile image
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True, verbose_name="Profilbild")
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "User Profile"
        verbose_name_plural = "User Profiles"
    
    def __str__(self):
        return f"{self.user.username}'s Profile"
    
    @property
    def full_name(self):
        """Get user's full name"""
        if self.user.first_name and self.user.last_name:
            return f"{self.user.first_name} {self.user.last_name}"
        return self.user.username
    
    @property
    def booking_count(self):
        """Count total bookings"""
        from apps.bookings.models import Booking
        return Booking.objects.filter(user=self.user).count()


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    """Create UserProfile when User is created"""
    if created:
        UserProfile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    """Save UserProfile when User is saved"""
    if hasattr(instance, 'profile'):
        instance.profile.save()

