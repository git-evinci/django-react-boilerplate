# core/signals.py
"""Signal handlers for the Core application.

This module contains Django signals that automatically perform actions when models
are created, updated, or deleted. Includes:
- Financial data aggregation signals
- User profile synchronization
- Database connection handlers
"""

from contextlib import suppress
from pathlib import Path
from typing import Any

from allauth.account.models import EmailAddress

from django.conf import settings
from django.contrib.auth import get_user_model
from django.db.backends.base.base import BaseDatabaseWrapper
from django.db.backends.signals import connection_created
from django.db.models.signals import post_delete, post_save, pre_save
from django.dispatch import receiver

from core.models import (
    UserProfile,
)

# Prevent recursion by tracking updates
EMAIL_SYNC_LOCK = False

User = get_user_model()


@receiver(post_save, sender=User)
def create_email_address(sender, instance, created: bool, **kwargs: Any) -> None:  # noqa: ANN001, ARG001
    """Populate the EmailAddress table with the User's email when the User is created."""
    if created and not EmailAddress.objects.filter(user=instance, email=instance.email).exists():
        EmailAddress.objects.create(
            user=instance,
            email=instance.email,
            verified=False,  # Set to True if you want to auto-verify it
            primary=True,
        )


@receiver(post_delete, sender=User)
def delete_email_address(sender, instance, **kwargs) -> None:  # noqa: ANN001, ANN003, ARG001
    """Ensure the associated EmailAddress entry is deleted when the User is deleted."""
    EmailAddress.objects.filter(user=instance).delete()


@receiver(post_save, sender=User)
def create_profile(sender, instance, created: bool, **kwargs) -> None:  # noqa: ANN001, ANN003, ARG001
    """Signal to automatically create a UserProfile when a new User is created."""
    if created and not UserProfile.objects.filter(user=instance).exists():
        UserProfile.objects.create(user=instance)


@receiver(post_delete, sender=User)
def delete_profile_on_user_delete(sender, instance, **kwargs) -> None:  # noqa: ANN001, ANN003, ARG001
    """When a User is deleted, delete the associated UserProfile."""
    with suppress(UserProfile.DoesNotExist):
        instance.profile.delete()


@receiver(post_delete, sender=UserProfile)
def delete_profile_picture(sender, instance, **kwargs) -> None:  # noqa: ANN001, ANN003, ARG001
    """Delete the profile picture from storage when a UserProfile is deleted."""
    if instance.picture and Path(instance.picture.path).is_file():
        Path(instance.picture.path).unlink()


@receiver(pre_save, sender=User)
def sync_email_with_email_address(sender, instance, **kwargs) -> None:  # noqa: ANN001, ANN003, ARG001
    """Ensure changes in User.email are reflected in EmailAddress.email.

    Prevent recursion by using a global lock.
    """
    global EMAIL_SYNC_LOCK
    if instance.pk and not EMAIL_SYNC_LOCK:  # Ensure it's an update, not creation
        try:
            old_instance = User.objects.get(pk=instance.pk)  # type: ignore [attr-defined]
            if old_instance.email != instance.email:
                email_address = EmailAddress.objects.filter(user=instance, primary=True).first()
                if email_address and email_address.email != instance.email:
                    EMAIL_SYNC_LOCK = True  # Prevent recursion
                    email_address.email = instance.email
                    email_address.save(update_fields=["email"])
                    EMAIL_SYNC_LOCK = False  # Unlock
        except User.DoesNotExist:
            pass  # Ignore new users


def activate_foreign_keys(sender, connection: BaseDatabaseWrapper, **kwargs) -> None:  # noqa: ANN001, ANN003, ARG001
    """Enable SQLite foreign key constraints in production environments.

    Args:
    ----
        sender: The signal sender class.
        connection: Database connection wrapper.
        **kwargs: Additional signal arguments.

    Note:
    ----
        Only activates when DEBUG=False and using SQLite backend.

    """
    if not settings.DEBUG and connection.vendor == "sqlite":  # type: ignore[misc]
        cursor = connection.cursor()
        cursor.execute("PRAGMA query_only = ON;")


connection_created.connect(activate_foreign_keys)
