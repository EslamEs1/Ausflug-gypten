"""
Review models for AusflugAgypten
"""

from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.core.validators import MinValueValidator, MaxValueValidator


class Review(models.Model):
    """Generic review model for tours/activities"""
    # Generic relation to allow reviews for any model
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')
    
    # Review details
    name = models.CharField(max_length=100, verbose_name="Name")
    email = models.EmailField(verbose_name="E-Mail")
    rating = models.PositiveIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)],
        verbose_name="Bewertung"
    )
    title = models.CharField(max_length=200, verbose_name="Titel")
    comment = models.TextField(verbose_name="Kommentar")
    
    # Status
    is_approved = models.BooleanField(default=False, verbose_name="Genehmigt")
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created_at']
        verbose_name = "Bewertung"
        verbose_name_plural = "Bewertungen"
        indexes = [
            models.Index(fields=['content_type', 'object_id']),
            models.Index(fields=['is_approved', '-created_at']),
        ]
    
    def __str__(self):
        return f"{self.name} - {self.rating}★"

