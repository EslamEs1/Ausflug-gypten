"""
Context processors for global template data
"""

from .models import SiteSettings
from apps.activities.models import ActivityCategory
from apps.tours.models import Location


def site_settings(request):
    """Add site settings and navigation data to all templates"""
    try:
        settings = SiteSettings.load()
    except Exception:
        # Fallback if settings don't exist yet
        settings = SiteSettings()
    
    # Activity categories for header dropdown
    activity_categories = ActivityCategory.objects.filter(
        is_active=True
    ).order_by('order', 'name')[:10]
    
    # Locations for header dropdown
    locations = Location.objects.filter(
        is_active=True
    ).order_by('order', 'name')[:10]
    
    # Popular locations for footer (top 4)
    popular_locations = Location.objects.filter(
        is_active=True
    ).order_by('order', 'name')[:4]
    
    return {
        'site_settings': settings,
        'header_activity_categories': activity_categories,
        'header_locations': locations,
        'footer_popular_locations': popular_locations,
    }


