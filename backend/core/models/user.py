# core/models/user.py
"""Models for user and user profile extensions.

This module defines a `UserProfile` model to extend Django's built-in User model
with additional fields such as a profile picture.
"""
from typing import Self

from simple_history.models import HistoricalRecords

from django.conf import settings
from django.contrib.auth import get_user_model
from django.db import models
from django.db.models.manager import Manager
from django.utils.translation import gettext_lazy as _

from core.models.base import AuditedModel, user_picture_upload_path

# Exported symbols
__all__ = [
    "User",
    "UserProfile",
]

User = get_user_model()


class UserProfile(AuditedModel):
    """Model extending Django"s default User model with additional fields."""

    objects: Manager

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    picture = models.ImageField(  # type: ignore[misc]
        upload_to=user_picture_upload_path,
        null=True,
        blank=True,
        verbose_name=_("Profile Picture"),
    )
    resume = models.FileField(_("resume"), null=True, blank=True, default=None)
    link = models.URLField(_("link"), default="", blank=True)
    history = HistoricalRecords()

    class Meta:
        """Meta options for the UserProfile model."""

        ordering = ("user",)
        verbose_name = _("User Profile")
        verbose_name_plural = _("User Profile")

    def __str__(self: Self) -> str:
        """Return a string representation of the UserProfile."""
        return f"Profile of {self.user.username}"

    def get_picture_url(self) -> str:
        """Return user picture URL or default avatar."""
        if self.picture:
            return self.picture.url
        return f"{settings.MEDIA_URL}img/avatars/avatar.webp"  # type: ignore[misc]
