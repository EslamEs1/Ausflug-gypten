"""
Context processors for global template data
"""

from .models import SiteSettings


def site_settings(request):
    """Add site settings to all templates"""
    try:
        settings = SiteSettings.load()
    except Exception:
        # Fallback if settings don't exist yet
        settings = SiteSettings()
    
    return {
        'site_settings': settings,
    }

