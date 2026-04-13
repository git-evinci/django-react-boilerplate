# core/apps.py
"""App configuration for the core Django app."""

from django.apps import AppConfig


class CoreConfig(AppConfig):
    """AppConfig for the core app."""

    default_auto_field = "django.db.models.BigAutoField"
    name = "core"
    default = True

    def ready(self) -> None:
        """Import admin and signal modules to ensure proper registration."""
        # Ensures all admin submodules and signals are loaded
        import core.admin  # Modular admin registration
        import core.signals  # Model signal handlers  # noqa: F401
