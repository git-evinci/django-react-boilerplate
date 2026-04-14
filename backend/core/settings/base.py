# core/settings/base.py
"""Base settings for the Django project.

These settings are shared across all environments (development, staging, production).
Environment-specific settings are located in their respective modules.
"""


import logging
import os
from collections import OrderedDict
from pathlib import Path

import sentry_sdk
from dotenv import load_dotenv
from import_export.formats.base_formats import CSV, XLSX
from unfold.contrib.constance.settings import UNFOLD_CONSTANCE_ADDITIONAL_FIELDS

from django.core.management.utils import get_random_secret_key
from django.utils.translation import gettext_lazy as _

from .logging import *  # noqa: F403
from .unfold import *  # noqa: F403

logger = logging.getLogger("core")

######################################################################
# General
######################################################################
BASE_DIR = Path(__file__).resolve().parent.parent.parent
# print(BASE_DIR)
ROOT_DIR = Path(__file__).resolve().parent.parent.parent.parent
# print(ROOT_DIR)
# Load environment variables from .env file
load_dotenv(ROOT_DIR / ".env")  # Explicitly specify the path to the .env file
FRONTEND_DIR = str(BASE_DIR.parent / "frontend" / "dist")

SECRET_KEY = os.getenv("SECRET_KEY", get_random_secret_key())
DEBUG = os.getenv("DEBUG", "False").lower() in ("true", "1", "t")

ROOT_URLCONF = "core.urls"
WSGI_APPLICATION = "core.wsgi.application"

# Default primary key field type
# https://docs.djangoproject.com/en/5.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

DATA_UPLOAD_MAX_NUMBER_FIELDS = 10_000
######################################################################
# Domains
######################################################################
env_hosts = os.getenv("ALLOWED_HOSTS", "localhost,127.0.0.1")
ALLOWED_HOSTS = [host.strip() for host in env_hosts.split(",")]

CSRF_TRUSTED_ORIGINS = os.getenv("CSRF_TRUSTED_ORIGINS", "http://localhost:8000").split(
    ","
)

CSRF_FAILURE_VIEW = "django.views.csrf.csrf_failure"


# Application definition

INSTALLED_APPS = [
    "modeltranslation",
    "unfold",  # before django.contrib.admin
    "unfold.contrib.filters", 
    "unfold.contrib.forms",  
    "unfold.contrib.inlines",  
    "unfold.contrib.import_export", 
    "unfold.contrib.guardian", 
    "unfold.contrib.simple_history", 
    "unfold.contrib.location_field",  
    "unfold.contrib.constance", 
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.humanize",
    "django.contrib.staticfiles",
    "django_extensions",
    #"debug_toolbar",
    "crispy_forms",
    "allauth",
    "allauth.account",
    "import_export",
    "guardian",
    "simple_history",
    "location_field",
    "constance",
    "constance.backends.database",
    "django_celery_beat",
    "djmoney",
    "versatileimagefield",
    "django_vite",
    "rest_framework",
    "corsheaders",
    "drf_spectacular",
    "drf_spectacular_sidecar",  
    "core",
]

UNFOLD_STUDIO = os.getenv("UNFOLD_STUDIO")
if UNFOLD_STUDIO == "1":
    INSTALLED_APPS.insert(0, "unfold_studio")
    logger.info("UNFOLD_STUDIO: %s", UNFOLD_STUDIO)

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",  # Must be directly below SecurityMiddleware
    "django.contrib.sessions.middleware.SessionMiddleware",
    "corsheaders.middleware.CorsMiddleware", # Place this as high as possible
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "allauth.account.middleware.AccountMiddleware",
    "simple_history.middleware.HistoryRequestMiddleware",
    #"debug_toolbar.middleware.DebugToolbarMiddleware",
    "core.middleware.ReadonlyExceptionHandlerMiddleware",
]

# DRF Configuration
REST_FRAMEWORK = {
    "DEFAULT_PERMISSION_CLASSES": [
        "rest_framework.permissions.IsAuthenticatedOrReadOnly",
    ],
    "DEFAULT_AUTHENTICATION_CLASSES": [
        "rest_framework.authentication.SessionAuthentication",
        "rest_framework.authentication.BasicAuthentication",
    ],
    "DEFAULT_SCHEMA_CLASS": "drf_spectacular.openapi.AutoSchema",
}

# CORS Configuration (Adjust for your dev environment)
CORS_ALLOWED_ORIGINS = [
    "http://localhost:5173",
    "http://127.0.0.1:5173",
]

SPECTACULAR_SETTINGS = {
    "TITLE": "Django React Boilerplate API",
    "DESCRIPTION": "Comprehensive API documentation for the Modern Stack Boilerplate",
    "VERSION": "1.0.0",
    "SERVE_INCLUDE_SCHEMA": False,
    # Optional: Change the UI theme
    "SWAGGER_UI_DIST": "SIDECAR",  # Requires 'drf-spectacular-sidecar' if you don't want to use CDN
    "SWAGGER_UI_FAVICON_HREF": "SIDECAR",
}

######################################################################
# Sessions
######################################################################
SESSION_ENGINE = "django.contrib.sessions.backends.signed_cookies"

######################################################################
# Templates
######################################################################
TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
                "core.context_processors.variables",
            ],
        },
    },
]




# Database
# https://docs.djangoproject.com/en/5.2/ref/settings/#databases

# Define the database directory path
DB_DIR = BASE_DIR.parent / "db"

# 🌟 AUTOMATICALLY CREATE THE DIRECTORY IF IT DOESN'T EXIST 🌟
DB_DIR.mkdir(parents=True, exist_ok=True)

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": DB_DIR / "db.sqlite3",
    }
}

AUTHENTICATION_BACKENDS = (
    "django.contrib.auth.backends.ModelBackend",
    "allauth.account.auth_backends.AuthenticationBackend",
    "guardian.backends.ObjectPermissionBackend",
)

# Password validation
# https://docs.djangoproject.com/en/5.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME" : "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME" : "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME" : "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME" : "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]


LOGIN_USERNAME = os.getenv("LOGIN_USERNAME")
LOGIN_PASSWORD = os.getenv("LOGIN_PASSWORD")
#LOGIN_URL = "admin:login"

#LOGIN_REDIRECT_URL = reverse_lazy("admin:index")

# Guardian setting
GUARDIAN_ANONYMOUS_USER_ID = None
ANONYMOUS_USER_NAME = None

# Allauth settings
SITE_ID = 1
SITE_NAME = "Core App"
SITE_DOMAIN = "core.evinci.com.br"
# Deprecated ACCOUNT_AUTHENTICATION_METHOD = "email"  # Use "username_email" if both should work
ACCOUNT_LOGIN_METHODS = ["email", "username"]
ACCOUNT_SIGNUP_FIELDS = [
    "username*",
    "email*",
    "password1*",
    "password2*",
]
ACCOUNT_EMAIL_VERIFICATION =  "none" # Change to 'mandatory' if needed
ACCOUNT_AUTHENTICATED_LOGIN_REDIRECTS = True
ACCOUNT_UNIQUE_EMAIL = True
#LOGIN_REDIRECT_URL = "/app"  # Redirect after login
#LOGIN_URL = "/account/login/"
ACCOUNT_LOGOUT_REDIRECT_URL = "/"  # Redirect after logout
#ACCOUNT_LOGIN_VIEW_CLASS = "core.views.CustomLoginView"
# Custom allauth adapter to control email subjects
ACCOUNT_EMAIL_SUBJECT_PREFIX = None
#ACCOUNT_EMAIL_SUBJECT_PREFIX (default: "[Site] ")
#ACCOUNT_ADAPTER = "core.adapters.CustomAccountAdapter"



# SMTP Configure
EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
#EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"

DEFAULT_FROM_EMAIL = "evinci <no-reply@evinci.com.br>"
SERVER_EMAIL = "server@evinci.com.br"

EMAIL_SUBJECT_PREFIX = None
EMAIL_HOST = "smtp.gmail.com"
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = os.getenv("EMAIL_HOST_USER", "").strip('"').strip("'")
EMAIL_HOST_PASSWORD = os.getenv("EMAIL_HOST_PASSWORD", "").strip('"').strip("'")
DEFAULT_FROM_EMAIL = EMAIL_HOST_USER
CONTACT_EMAIL = os.getenv("CONTACT_EMAIL", "").strip('"').strip("'")

# Internationalization
# https://docs.djangoproject.com/en/5.2/topics/i18n/

LANGUAGE_CODE = "en-us"
TIME_ZONE = "America/Sao_Paulo"
USE_I18N = True
USE_TZ = True
LOCALE_PATHS = [BASE_DIR / "locale"]
LANGUAGES = (
    ("en", _("English")),
    ("es", _("Spanish")),
    # Add more as needed
)


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.2/howto/static-files/
# The URL used to access static files
STATIC_URL = "/static/"
# The destination for 'collectstatic' (Production only)
# This should be a separate folder that is NOT in STATICFILES_DIRS
STATIC_ROOT = BASE_DIR.parent / "collected_static"

# 1. Define the paths
STATIC_DIR = BASE_DIR / "static"
EXTRA_STATIC_DIR = BASE_DIR / "staticfiles"

# 2. Automatically create them if they are missing
STATIC_DIR.mkdir(parents=True, exist_ok=True)
EXTRA_STATIC_DIR.mkdir(parents=True, exist_ok=True)

# 3. Assign them
STATICFILES_DIRS = [
    STATIC_DIR,
    EXTRA_STATIC_DIR,
]


# Vite Integration
VITE_DIST_DIR = BASE_DIR.parent / "frontend" / "dist"

if not DEBUG and VITE_DIST_DIR.exists():
    # We mount the vite build directory so Whitenoise/Django can serve the assets
    STATICFILES_DIRS.append(("vite", VITE_DIST_DIR))

MEDIA_ROOT = BASE_DIR / "media"
MEDIA_URL = "/media/"
# Ensure the directories exist
STATIC_ROOT.mkdir(parents=True, exist_ok=True)
MEDIA_ROOT.mkdir(parents=True, exist_ok=True)

STORAGES = {
    "default": {
        "BACKEND": "django.core.files.storage.FileSystemStorage",
    },
    "staticfiles": {
        "BACKEND": "django.contrib.staticfiles.storage.StaticFilesStorage",
    },
    # "staticfiles": {
    #     "BACKEND": "whitenoise.storage.CompressedManifestStaticFilesStorage",
    # },
}


######################################################################
# Import-Export Settings
######################################################################
IMPORT_FORMATS = [CSV, XLSX]
IMPORT_EXPORT_IMPORT_IGNORE_BLANK_LINES = True



############################################################################
# Debug toolbar
############################################################################
# DEBUG_TOOLBAR_CONFIG = {"SHOW_TOOLBAR_CALLBACK": lambda request: DEBUG}

######################################################################
# Plausible
######################################################################
PLAUSIBLE_DOMAIN = os.getenv("PLAUSIBLE_DOMAIN")

######################################################################
# Sentry: enables automatic reporting of errors and performance data
######################################################################
SENTRY_DSN = os.getenv("SENTRY_DSN")

if SENTRY_DSN:
    sentry_sdk.init(
        dsn=SENTRY_DSN,
        enable_tracing=False,
    )

CELERY_BROKER_URL = os.getenv("CELERY_BROKER_URL", "redis://localhost:6379/0")
CELERY_RESULT_BACKEND = os.getenv("CELERY_RESULT_BACKEND", "redis://localhost:6379/0")

CELERY_ACCEPT_CONTENT = ["json"]
CELERY_TASK_SERIALIZER = "json"

CELERY_BEAT_SCHEDULER = "django_celery_beat.schedulers:DatabaseScheduler"


VERSATILEIMAGEFIELD_SETTINGS = {
    "cache_length": 2592000,
    "cache_name": "versatileimagefield_cache",
    "jpeg_resize_quality": 70,
    "sized_directory_name": "__sized__",
    "filtered_directory_name": "__filtered__",
    "placeholder_directory_name": "__placeholder__",
}

if not DEBUG:
    DJANGO_VITE = {
        "default": {
            "dev_mode": False,
            "manifest_path": ROOT_DIR / "frontend" / "dist" / "manifest.json",
            "static_url_prefix": "vite/",  # or ""
        }
    }
else:  # development
    DJANGO_VITE = {
        "default": {
            "dev_mode": True,
            "dev_server_host": "localhost",
            "dev_server_port": 5173,
            "static_url_prefix": "/",
        }
    }

######################################################################
# Constance
######################################################################
CONSTANCE_BACKEND = "constance.backends.database.DatabaseBackend"

CONSTANCE_CONFIG = {
    "SITE_NAME": ("My Title", _("Website title")),
    "SITE_DESCRIPTION": ("", _("Website description")),
    "THEME": ("light-blue", _("Website theme"), "choice_field"),
    "IN_CONSTRUCTION": (False, _("Website in construction")),
    "SITE_URL": ("", _("Website URL")),
    "SITE_LOGO": ("", _("Website logo"), "image_field"),
    "SITE_FAVICON": ("", _("Website favicon"), "file_field"),
    "SITE_BACKGROUND_IMAGE": ("", _("Website background image"), "image_field"),
    "SITE_BACKGROUND_COLOR": ("#FFFFFF", _("Website background color")),
    "SITE_FONT_SIZE": (16, _("Base font size in pixels")),
    "SITE_ANALYTICS_ID": ("", _("Google Analytics ID")),
    "SITE_MAINTENANCE_MODE": (False, _("Enable maintenance mode")),
    "SITE_MAINTENANCE_MESSAGE": ("", _("Maintenance mode message")),
    "SITE_SOCIAL_LINKS": ("", _("Social media links")),
    "SITE_FOOTER_TEXT": ("", _("Footer text")),
    "SITE_META_KEYWORDS": ("", _("Meta keywords")),
    "SITE_CACHE_TTL": (3600, _("Cache TTL in seconds")),
    "SITE_DATE_FORMAT": ("%Y-%m-%d", _("Date format")),
    "SITE_TIME_ZONE": ("UTC", _("Time zone")),
}

CONSTANCE_CONFIG_FIELDSETS = OrderedDict(
    {
        "General Settings": {
            "fields": (
                "SITE_NAME",
                "SITE_DESCRIPTION",
                "SITE_URL",
            ),
            # "collapse": False,
        },
        "Theme & Design": {
            "fields": (
                "THEME",
                "SITE_FONT_SIZE",
                "SITE_BACKGROUND_COLOR",
                "SITE_BACKGROUND_IMAGE",
            ),
            # "collapse": False,
        },
        "Assets": {
            "fields": (
                "SITE_LOGO",
                "SITE_FAVICON",
            ),
            # "collapse": True,
        },
        "Content": {
            "fields": (
                "SITE_FOOTER_TEXT",
                "SITE_META_KEYWORDS",
                "SITE_SOCIAL_LINKS",
            ),
            # "collapse": True,
        },
        "System": {
            "fields": (
                "IN_CONSTRUCTION",
                "SITE_MAINTENANCE_MODE",
                "SITE_MAINTENANCE_MESSAGE",
                "SITE_CACHE_TTL",
                "SITE_DATE_FORMAT",
                "SITE_TIME_ZONE",
                "SITE_ANALYTICS_ID",
            ),
            # "collapse": True,
        },
    }
)


CONSTANCE_ADDITIONAL_FIELDS = {
    **UNFOLD_CONSTANCE_ADDITIONAL_FIELDS,
    "choice_field": [
        "django.forms.fields.ChoiceField",
        {
            "widget": "unfold.widgets.UnfoldAdminSelectWidget",
            "choices": (
                ("light-blue", "Light blue"),
                ("dark-blue", "Dark blue"),
            ),
        },
    ],
}
