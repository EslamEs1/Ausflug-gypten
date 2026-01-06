"""
URL configuration for AusflugAgypten project.
"""

from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls.i18n import i18n_patterns

urlpatterns = [
    path('admin/', admin.site.urls),
]

# Internationalized URLs
urlpatterns += i18n_patterns(
    path('', include('apps.core.urls')),
    path('touren/', include('apps.tours.urls', namespace='tours')),
    path('aktivitaeten/', include('apps.activities.urls', namespace='activities')),
    path('blog/', include('apps.blog.urls', namespace='blog')),
    path('transfer/', include('apps.transfers.urls', namespace='transfers')),
    path('buchungen/', include('apps.bookings.urls', namespace='bookings')),
    prefix_default_language=True,
)

# Serve media files in development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

