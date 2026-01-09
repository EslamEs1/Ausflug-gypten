"""
Admin Context Processor for Dashboard Stats and Notifications
"""
from django.db.models import Count, Q, Sum
from datetime import datetime, timedelta
from django.utils import timezone


def admin_dashboard_stats(request):
    """
    Context processor to add dashboard stats to admin pages
    Only adds context if user is in admin and is staff
    """
    # Only process for admin pages and staff users
    if not request.path.startswith('/admin/'):
        return {}
    
    if not hasattr(request, 'user') or not request.user.is_staff:
        return {}
    
    if not request.user.is_authenticated:
        return {}
    
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
        return {}
    
    # Calculate stats with timezone-aware dates
    now = timezone.now()
    today_start = now.replace(hour=0, minute=0, second=0, microsecond=0)
    today = today_start.date()
    last_7_days_start = today_start - timedelta(days=7)
    last_30_days_start = today_start - timedelta(days=30)
    
    stats = {}
    notifications = {}
    
    # Bookings Stats
    try:
        bookings_pending = Booking.objects.filter(status='pending')
        bookings_new = bookings_pending.filter(created_at__gte=last_7_days_start)
        
        stats['bookings'] = {
            'total': Booking.objects.count(),
            'pending': bookings_pending.count(),
            'confirmed': Booking.objects.filter(status='confirmed').count(),
            'today': Booking.objects.filter(created_at__gte=today_start).count(),
            'last_7_days': Booking.objects.filter(created_at__gte=last_7_days_start).count(),
            'last_30_days': Booking.objects.filter(created_at__gte=last_30_days_start).count(),
            'revenue': float(Booking.objects.filter(status__in=['confirmed', 'completed']).aggregate(
                total=Sum('total_price')
            )['total'] or 0),
        }
        notifications['bookings'] = bookings_new.count()
    except Exception:
        pass
    
    # Contact Messages Stats
    try:
        contacts_new = ContactMessage.objects.filter(status='new', is_read=False)
        
        stats['contacts'] = {
            'total': ContactMessage.objects.count(),
            'new': contacts_new.count(),
            'read': ContactMessage.objects.filter(is_read=True).count(),
            'today': ContactMessage.objects.filter(created_at__gte=today_start).count(),
            'last_7_days': ContactMessage.objects.filter(created_at__gte=last_7_days_start).count(),
        }
        notifications['contacts'] = contacts_new.count()
    except Exception:
        pass
    
    # Reviews Stats
    try:
        reviews_pending = Review.objects.filter(is_approved=False)
        
        stats['reviews'] = {
            'total': Review.objects.count(),
            'pending': reviews_pending.count(),
            'approved': Review.objects.filter(is_approved=True).count(),
            'today': Review.objects.filter(created_at__gte=today_start).count(),
            'last_7_days': Review.objects.filter(created_at__gte=last_7_days_start).count(),
        }
        notifications['reviews'] = reviews_pending.count()
    except Exception:
        pass
    
    # Content Stats
    try:
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
    except Exception:
        pass
    
    # Calculate total notifications
    total_notifications = (
        notifications.get('bookings', 0) +
        notifications.get('contacts', 0) +
        notifications.get('reviews', 0)
    )
    
    return {
        'dashboard_stats': stats,
        'notifications': notifications if total_notifications > 0 else None,
        'total_notifications': total_notifications,
    }

