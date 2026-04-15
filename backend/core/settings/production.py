# core/settings/production.py
"""Production-specific settings for the Django project.

Inherits from the base settings and extends or overrides specific settings.
"""

import os

from .base import *  # noqa: F403
from .logging import LOGGING

# Disable debugging
DEBUG = False
ALLOWED_HOSTS = os.getenv("ALLOWED_HOSTS", "localhost").split(",")

# Security settings
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
SECURE_SSL_REDIRECT = os.getenv("SECURE_SSL_REDIRECT", "True") == "True"
# SECURE_SSL_REDIRECT = False
SECURE_HSTS_SECONDS = 31536000
SESSION_COOKIE_SECURE = os.getenv("SECURE_SSL_REDIRECT", "False") == "True"
CSRF_COOKIE_SECURE = os.getenv("SECURE_SSL_REDIRECT", "False") == "True"
# SESSION_COOKIE_SECURE = True
# CSRF_COOKIE_SECURE = True

# Retrieve DB_PASS from environment variables and remove any surrounding quotes
DB_ENGINE = os.getenv("DB_ENGINE", None)
DB_HOST = os.getenv("DB_HOST", None)
DB_PORT = os.getenv("DB_PORT", None)
DB_NAME = os.getenv("DB_NAME", None)
DB_USERNAME = os.getenv("DB_USERNAME", None)
DB_PASS = os.getenv("DB_PASS", "").strip('"').strip("'")  # Strips quotes if present

# Database settings for production (example: PostgreSQL)
DATABASES = {
    "default": {
        "ENGINE": f"django.db.backends.{DB_ENGINE}",
        "NAME": DB_NAME,
        "USER": DB_USERNAME,
        "PASSWORD": DB_PASS,
        "HOST": DB_HOST,
        "PORT": DB_PORT,
    },
}

# Cache & Celery: Redis
CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": os.getenv("REDIS_URL", "redis://redis:6379/1"),
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
        },
    }
}

CELERY_BROKER_URL = os.getenv("REDIS_URL", "redis://redis:6379/1")
CELERY_RESULT_BACKEND = os.getenv("REDIS_URL", "redis://redis:6379/1")

LOGGING["handlers"]["file"]["level"] = "INFO"  # type: ignore[index]
LOGGING["loggers"]["core"]["level"] = "INFO"  # type: ignore[index]
LOGGING["loggers"]["django.request"] = {
    "handlers": ["file"],
    "level": "ERROR",
    "propagate": True,
}
