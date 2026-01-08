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
    # TinyMCE URLs
    path('tinymce/', include('tinymce.urls')),
]

# Internationalized URLs
urlpatterns += i18n_patterns(
    path('', include('apps.core.urls')),
    path('touren/', include('apps.tours.urls', namespace='tours')),
    path('aktivitaeten/', include('apps.activities.urls', namespace='activities')),
    path('ausfluege/', include('apps.excursions.urls', namespace='excursions')),
    path('blog/', include('apps.blog.urls', namespace='blog')),
    path('transfer/', include('apps.transfers.urls', namespace='transfers')),
    path('galerie/', include('apps.gallery.urls', namespace='gallery')),
    path('buchungen/', include('apps.bookings.urls', namespace='bookings')),
    path('bewertungen/', include('apps.reviews.urls', namespace='reviews')),
    path('konto/', include('apps.users.urls', namespace='users')),
    prefix_default_language=True,
)

# Serve media files in development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)


# Error Handlers
handler400 = 'apps.core.views.bad_request_view'
handler403 = 'apps.core.views.permission_denied_view'
handler404 = 'apps.core.views.page_not_found_view'
handler500 = 'apps.core.views.server_error_view'

