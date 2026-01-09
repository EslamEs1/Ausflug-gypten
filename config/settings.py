"""
Django settings for AusflugAgypten project.
"""

from pathlib import Path
import environ
import os

# Build paths
BASE_DIR = Path(__file__).resolve().parent.parent

# Environment variables
env = environ.Env(
    DEBUG=(bool, False)
)
environ.Env.read_env(BASE_DIR / '.env')

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = env('SECRET_KEY', default='django-insecure-CHANGE-THIS-IN-PRODUCTION')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = env('DEBUG')

ALLOWED_HOSTS = env.list('ALLOWED_HOSTS', default=['localhost', '127.0.0.1'])

# Application definition
INSTALLED_APPS = [
    # Modern Admin Interface (must be before django.contrib.admin)
    'jazzmin',
    
    # Django core apps
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',
    
    # Third-party apps
    'crispy_forms',
    'crispy_tailwind',
    
    # Rich Text Editor
    'tinymce',
    
    # File cleanup
    'django_cleanup.apps.CleanupConfig',
    
    # Local apps
    'apps.core',
    'apps.tours',
    'apps.activities',
    'apps.excursions',
    'apps.blog',
    'apps.transfers',
    'apps.reviews',
    'apps.bookings',
    'apps.users',
    'apps.gallery',
]

SITE_ID = 1

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',  # Static files
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',  # i18n
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'config.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'django.template.context_processors.i18n',
                'apps.core.context_processors.site_settings',  # Global site settings
                'apps.core.admin_context.admin_dashboard_stats',  # Admin dashboard stats
            ],
        },
    },
]

WSGI_APPLICATION = 'config.wsgi.application'

# Database
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': env('DB_NAME', default='ausflug_egypt'),
        'USER': env('DB_USER', default='postgres'),
        'PASSWORD': env('DB_PASSWORD', default=''),
        'HOST': env('DB_HOST', default='localhost'),
        'PORT': env('DB_PORT', default='5432'),
    }
}

# For development, you can use SQLite:
if DEBUG:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3',
        }
    }

# Password validation
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

# Internationalization
LANGUAGE_CODE = 'de'
TIME_ZONE = 'Africa/Cairo'
USE_I18N = True
USE_TZ = True

# Supported languages
LANGUAGES = [
    ('de', 'Deutsch'),
    ('en', 'English'),
]

LOCALE_PATHS = [
    BASE_DIR / 'locale',
]

# Static files (CSS, JavaScript, Images)
STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'static'
STATICFILES_DIRS = [
    BASE_DIR / 'staticfiles',
]
# WhiteNoise configuration
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# Media files
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

# Default primary key field type
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Custom User Model (optional)
# AUTH_USER_MODEL = 'users.CustomUser'

# Crispy Forms
CRISPY_ALLOWED_TEMPLATE_PACKS = 'tailwind'
CRISPY_TEMPLATE_PACK = 'tailwind'

# ============ JAZZMIN ADMIN CONFIGURATION ============
JAZZMIN_SETTINGS = {
    "site_title": "AusflugÄgypten Admin",
    "site_header": "AusflugÄgypten",
    "site_brand": "AusflugÄgypten",
    "site_logo": None,  # Add your logo path here: "img/logo/logo.png"
    "site_logo_classes": "img-circle",
    "site_icon": None,  # Add your favicon path here: "img/logo/favicon.png"
    
    # Welcome message
    "welcome_sign": "Willkommen im AusflugÄgypten Admin Panel",
    "copyright": "© 2024 AusflugÄgypten - Alle Rechte vorbehalten",
    
    # Search configuration
    "search_model": ["auth.User", "tours.Tour", "blog.BlogPost", "excursions.Excursion", "activities.Activity", "transfers.Transfer", "bookings.Booking"],
    "user_avatar": None,
    
    # Top menu links
    "topmenu_links": [
        {"name": "Home", "url": "admin:index", "permissions": ["auth.view_user"], "icon": "fas fa-home"},
        {"name": "Website", "url": "/", "new_window": True, "icon": "fas fa-globe"},
        {"name": "Dashboard", "url": "admin:index", "permissions": ["auth.view_user"], "icon": "fas fa-tachometer-alt"},
    ],
    
    # User menu links
    "usermenu_links": [
        {"name": "Website ansehen", "url": "/", "new_window": True, "icon": "fas fa-external-link-alt"},
        {"name": "Support", "url": "/contact", "icon": "fas fa-life-ring"},
    ],
    
    # Sidebar configuration
    "show_sidebar": True,
    "navigation_expanded": True,
    "hide_apps": [],
    "hide_models": [],
    "order_with_respect_to": ["auth", "core", "tours", "excursions", "activities", "transfers", "bookings", "blog", "gallery", "reviews", "users"],
    
    # Icons configuration
    "icons": {
        "auth": "fas fa-users-cog",
        "auth.user": "fas fa-user",
        "auth.Group": "fas fa-users",
        "core.SiteSettings": "fas fa-cog",
        "core.HeroSlide": "fas fa-images",
        "core.ContactMessage": "fas fa-envelope",
        "core.NewsletterSubscriber": "fas fa-newspaper",
        "core.PageHero": "fas fa-heading",
        "tours.Tour": "fas fa-map-marked-alt",
        "tours.TourCategory": "fas fa-tags",
        "tours.Location": "fas fa-map-marker-alt",
        "excursions.Excursion": "fas fa-umbrella-beach",
        "excursions.ExcursionCategory": "fas fa-folder",
        "activities.Activity": "fas fa-running",
        "activities.ActivityCategory": "fas fa-list",
        "transfers.Transfer": "fas fa-car",
        "transfers.TransferType": "fas fa-taxi",
        "transfers.VehicleType": "fas fa-truck",
        "bookings.Booking": "fas fa-calendar-check",
        "bookings.Payment": "fas fa-credit-card",
        "blog.BlogPost": "fas fa-blog",
        "blog.BlogCategory": "fas fa-folder-open",
        "gallery.GalleryImage": "fas fa-photo-video",
        "gallery.GalleryCategory": "fas fa-images",
        "reviews.Review": "fas fa-star",
        "users.UserProfile": "fas fa-user-circle",
    },
    "default_icon_parents": "fas fa-chevron-circle-right",
    "default_icon_children": "fas fa-circle",
    
    # Modal configuration
    "related_modal_active": True,  # Enable modals for better UX
    
    # Custom CSS/JS
    "custom_css": "admin/css/custom_admin.css",  # Custom admin styling
    "custom_js": "admin/js/admin_notifications.js",   # Admin notifications and badges
    
    # Fonts and UI
    "use_google_fonts_cdn": True,
    "show_ui_builder": True,  # Enable UI builder for live customization
    "changeform_format": "horizontal_tabs",
    "changeform_format_overrides": {
        "auth.user": "collapsible",
        "auth.group": "vertical_tabs",
    },
    
    # Language
    "language_chooser": False,
    
    # Additional modern features
    "show_ui_builder_on_load": False,  # Don't show UI builder by default
    "custom_links": {
        "bookings": [{
            "name": "📋 Alle Buchungen",
            "url": "admin:bookings_booking_changelist",
            "icon": "fas fa-list",
            "permissions": ["bookings.view_booking"]
        }, {
            "name": "⏳ Ausstehende Buchungen",
            "url": "admin:bookings_booking_changelist?status__exact=pending",
            "icon": "fas fa-clock",
            "permissions": ["bookings.view_booking"]
        }, {
            "name": "✅ Bestätigte Buchungen",
            "url": "admin:bookings_booking_changelist?status__exact=confirmed",
            "icon": "fas fa-check-circle",
            "permissions": ["bookings.view_booking"]
        }],
        "core": [{
            "name": "📧 Neue Nachrichten",
            "url": "admin:core_contactmessage_changelist?status__exact=new",
            "icon": "fas fa-envelope",
            "permissions": ["core.view_contactmessage"]
        }, {
            "name": "💬 Alle Nachrichten",
            "url": "admin:core_contactmessage_changelist",
            "icon": "fas fa-envelope-open",
            "permissions": ["core.view_contactmessage"]
        }],
        "reviews": [{
            "name": "⏳ Ausstehende Bewertungen",
            "url": "admin:reviews_review_changelist?is_approved__exact=0",
            "icon": "fas fa-star-half-alt",
            "permissions": ["reviews.view_review"]
        }, {
            "name": "⭐ Alle Bewertungen",
            "url": "admin:reviews_review_changelist",
            "icon": "fas fa-star",
            "permissions": ["reviews.view_review"]
        }],
    },
    
    # Custom colors can be set in JAZZMIN_UI_TWEAKS below
}

JAZZMIN_UI_TWEAKS = {
    # Text sizes
    "navbar_small_text": False,
    "footer_small_text": False,
    "body_small_text": False,
    "brand_small_text": False,
    
    # Colors - Modern Blue & Gold Theme matching your brand
    "brand_colour": "navbar-primary",
    "accent": "accent-primary",
    "navbar": "navbar-dark",  # Use "navbar-white" for light navbar
    "no_navbar_border": False,
    
    # Layout options
    "navbar_fixed": True,
    "layout_boxed": False,
    "footer_fixed": False,
    "sidebar_fixed": True,
    "sidebar": "sidebar-dark-primary",  # Options: sidebar-dark-primary, sidebar-dark-warning, sidebar-dark-info, sidebar-dark-success, sidebar-dark-danger, sidebar-light-primary, sidebar-light-warning, sidebar-light-info, sidebar-light-success, sidebar-light-danger
    "sidebar_nav_small_text": False,
    "sidebar_disable_expand": False,
    "sidebar_nav_child_indent": False,
    "sidebar_nav_compact_style": False,
    "sidebar_nav_legacy_style": False,
    "sidebar_nav_flat_style": False,
    "theme": "default",
    "dark_mode_theme": None,
    "button_classes": {
        "primary": "btn-primary",
        "secondary": "btn-secondary",
        "info": "btn-info",
        "warning": "btn-warning",
        "danger": "btn-danger",
        "success": "btn-success"
    }
}

# ============ TINYMCE CONFIGURATION ============
TINYMCE_DEFAULT_CONFIG = {
    'height': 500,
    'width': '100%',
    'cleanup_on_startup': True,
    'custom_undo_redo_levels': 20,
    'selector': 'textarea',
    'theme': 'silver',
    'plugins': '''
        textcolor save link image media preview codesample contextmenu
        table code lists fullscreen  insertdatetime  nonbreaking
        contextmenu directionality searchreplace wordcount visualblocks
        visualchars code fullscreen autolink lists  charmap print  hr
        anchor pagebreak
    ''',
    'toolbar1': '''
        fullscreen preview bold italic underline | fontselect,
        fontsizeselect  | forecolor backcolor | alignleft alignright |
        aligncenter alignjustify | indent outdent | bullist numlist table |
        | link image media | codesample |
    ''',
    'toolbar2': '''
        visualblocks visualchars |
        charmap hr pagebreak nonbreaking anchor |  code |
    ''',
    'contextmenu': 'formats | link image',
    'menubar': True,
    'statusbar': True,
    'image_advtab': True,
    'file_picker_types': 'image',
    'automatic_uploads': True,
    'images_upload_url': '/media/uploads/',
    'relative_urls': False,
    'remove_script_host': False,
    'convert_urls': True,
    'content_style': '''
        body {
            font-family: Arial, sans-serif;
            font-size: 14px;
        }
    ''',
}

# Email Configuration
EMAIL_BACKEND = env('EMAIL_BACKEND', default='django.core.mail.backends.console.EmailBackend')
EMAIL_HOST = env('EMAIL_HOST', default='')
EMAIL_PORT = env.int('EMAIL_PORT', default=587)
EMAIL_USE_TLS = env.bool('EMAIL_USE_TLS', default=True)
EMAIL_HOST_USER = env('EMAIL_HOST_USER', default='')
EMAIL_HOST_PASSWORD = env('EMAIL_HOST_PASSWORD', default='')
DEFAULT_FROM_EMAIL = env('DEFAULT_FROM_EMAIL', default='noreply@ausflugagypten.com')

# Stripe Configuration
STRIPE_PUBLIC_KEY = env('STRIPE_PUBLIC_KEY', default='')
STRIPE_SECRET_KEY = env('STRIPE_SECRET_KEY', default='')
STRIPE_WEBHOOK_SECRET = env('STRIPE_WEBHOOK_SECRET', default='')

# Security Settings (Production)
if not DEBUG:
    SECURE_SSL_REDIRECT = True
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True
    SECURE_BROWSER_XSS_FILTER = True
    SECURE_CONTENT_TYPE_NOSNIFF = True
    X_FRAME_OPTIONS = 'DENY'
    SECURE_HSTS_SECONDS = 31536000
    SECURE_HSTS_INCLUDE_SUBDOMAINS = True
    SECURE_HSTS_PRELOAD = True

# Logging
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
        },
    },
    'root': {
        'handlers': ['console'],
        'level': 'INFO',
    },
}

