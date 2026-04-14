# core/settings/development.py
"""Development-specific settings for the Django project.

Inherits from the base settings and extends or overrides specific settings
to support development, such as enabling the debug toolbar.
"""
from .base import *  # noqa: F403

# Enable debugging
DEBUG = True
ALLOWED_HOSTS += [  # noqa: F405
    "localhost",
    "127.0.0.1",
    "192.168.15.11",
    "192.168.15.12",
    "testserver",
]
# Silence the specific django_vite manifest warning
SILENCED_SYSTEM_CHECKS = ["django_vite.W001"]

# Additional apps and middleware for development
# INSTALLED_APPS += [
#     "debug_toolbar",
# ]

# MIDDLEWARE += [
#     "debug_toolbar.middleware.DebugToolbarMiddleware",
# ]

# Debug Toolbar configuration
# DEBUG_TOOLBAR_CONFIG = {
#     "SHOW_TOOLBAR_CALLBACK": lambda request: DEBUG,
#     "IS_RUNNING_TESTS": os.getenv("RUNNING_TESTS", "False").lower() == "true",
# }

# Internal IPs for Debug Toolbar
INTERNAL_IPS = [
    "127.0.0.1",
    "::1",
]

# Development email backend
# EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"

LOGGING["handlers"]["file"]["level"] = "DEBUG"  # type: ignore # noqa: F405
