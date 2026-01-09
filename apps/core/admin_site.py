"""
Custom Admin Site with Dashboard Stats and Notifications
"""
from django.contrib import admin
from django.contrib.admin import AdminSite
from django.utils.html import format_html
from django.urls import path, reverse
from django.shortcuts import render
from django.db.models import Count, Q, Sum
from datetime import datetime, timedelta
from django.utils import timezone


class AusflugAgyptenAdminSite(AdminSite):
    site_header = "AusflugÄgypten Administration"
    site_title = "AusflugÄgypten Admin"
    index_title = "Dashboard"

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('dashboard-stats/', self.admin_view(self.dashboard_stats_view), name='dashboard_stats'),
        ]
        return custom_urls + urls

    def index(self, request, extra_context=None):
        """
        Override index to add dashboard stats and notifications
        """
        extra_context = extra_context or {}
        
        # Import models dynamically to avoid circular imports
        try:
            from apps.bookings.models import Booking
            from apps.reviews.models import Review
            from apps.core.models import ContactMessage
            from apps.tours.models import Tour
            from apps.excursions.models import Excursion
            from apps.activities.models import Activity
            from apps.transfers.models import Transfer
            from apps.blog.models import BlogPost
            from apps.gallery.models import GalleryImage
            from django.contrib.auth.models import User
        except ImportError:
            Booking = None
            Review = None
            ContactMessage = None
            Tour = None
            Excursion = None
            Activity = None
            Transfer = None
            BlogPost = None
            GalleryImage = None
            User = None

        # Calculate stats
        today = timezone.now().date()
        last_7_days = today - timedelta(days=7)
        last_30_days = today - timedelta(days=30)
        
        stats = {}
        notifications = {}
        
        # Bookings Stats
        if Booking:
            stats['bookings'] = {
                'total': Booking.objects.count(),
                'pending': Booking.objects.filter(status='pending').count(),
                'confirmed': Booking.objects.filter(status='confirmed').count(),
                'today': Booking.objects.filter(created_at__date=today).count(),
                'last_7_days': Booking.objects.filter(created_at__date__gte=last_7_days).count(),
                'last_30_days': Booking.objects.filter(created_at__date__gte=last_30_days).count(),
                'revenue': Booking.objects.filter(status__in=['confirmed', 'completed']).aggregate(
                    total=Sum('total_price')
                )['total'] or 0,
            }
            notifications['bookings'] = Booking.objects.filter(
                status='pending',
                created_at__date__gte=last_7_days
            ).count()
        
        # Contact Messages Stats
        if ContactMessage:
            stats['contacts'] = {
                'total': ContactMessage.objects.count(),
                'new': ContactMessage.objects.filter(status='new', is_read=False).count(),
                'read': ContactMessage.objects.filter(is_read=True).count(),
                'today': ContactMessage.objects.filter(created_at__date=today).count(),
                'last_7_days': ContactMessage.objects.filter(created_at__date__gte=last_7_days).count(),
            }
            notifications['contacts'] = ContactMessage.objects.filter(
                status='new',
                is_read=False
            ).count()
        
        # Reviews Stats
        if Review:
            stats['reviews'] = {
                'total': Review.objects.count(),
                'pending': Review.objects.filter(is_approved=False).count(),
                'approved': Review.objects.filter(is_approved=True).count(),
                'today': Review.objects.filter(created_at__date=today).count(),
                'last_7_days': Review.objects.filter(created_at__date__gte=last_7_days).count(),
                'avg_rating': Review.objects.filter(is_approved=True).aggregate(
                    avg=Sum('rating') / Count('id')
                ) or 0,
            }
            notifications['reviews'] = Review.objects.filter(is_approved=False).count()
        
        # Content Stats
        if Tour:
            stats['tours'] = Tour.objects.filter(is_active=True).count()
        if Excursion:
            stats['excursions'] = Excursion.objects.filter(is_active=True).count()
        if Activity:
            stats['activities'] = Activity.objects.filter(is_active=True).count()
        if Transfer:
            stats['transfers'] = Transfer.objects.filter(is_active=True).count()
        if BlogPost:
            stats['blog_posts'] = BlogPost.objects.filter(is_published=True).count()
        if GalleryImage:
            stats['gallery_images'] = GalleryImage.objects.filter(is_active=True).count()
        if User:
            stats['users'] = User.objects.filter(is_active=True).count()
        
        # Calculate total notifications
        total_notifications = (
            notifications.get('bookings', 0) +
            notifications.get('contacts', 0) +
            notifications.get('reviews', 0)
        )
        
        extra_context.update({
            'dashboard_stats': stats,
            'notifications': notifications,
            'total_notifications': total_notifications,
            'today': today,
            'last_7_days': last_7_days,
            'last_30_days': last_30_days,
        })
        
        return super().index(request, extra_context)
    
    def dashboard_stats_view(self, request):
        """AJAX endpoint for dashboard stats"""
        # Same stats calculation as above
        return render(request, 'admin/dashboard_stats.html', {})

# Create custom admin site instance
admin_site = AusflugAgyptenAdminSite(name='ausflugagypten_admin')

