# core/models/base.py
"""Base models and utility functions for the Core application."""

from typing import Self

from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.utils.translation import gettext_lazy as _

# Exported symbols
__all__ = [
    "AuditedModel",
    "Tag",
    "user_picture_upload_path",
]


def model_picture_upload_path(
    instance: models.Model,
    filename: str,
    directory: str = "img/avatars",
    field: str = "username",
) -> str:
    """Generate a consistent upload path for model images.

    Args:
        instance: The model instance.
        filename: The original uploaded filename.
        directory: Base directory to store images.
        field: Model field name to use for the filename (e.g., 'username', 'slug', 'id').

    Returns:
        str: Path in the form '{directory}/{instance.id}/{filename_based_on_field.ext}'

    """
    ext = filename.split(".")[-1]
    base_name = getattr(instance, field, None)

    # Fallback to instance.pk if the field doesn't exist
    if base_name is None:
        base_name = instance.pk

    safe_filename = f"{base_name}.{ext}"
    return f"{directory}/{base_name}/{safe_filename}"


def user_picture_upload_path(instance: models.Model, filename: str) -> str:
    """Generate upload path for a user's profile picture."""
    user = instance.user  # type: ignore[attr-defined]
    return model_picture_upload_path(
        user, filename, directory="img/avatars", field="username"
    )


class AuditedModel(models.Model):
    """Abstract model that provides automatic timestamp tracking."""

    modified_at = models.DateTimeField(_("Modificada em"), auto_now=True)
    created_at = models.DateTimeField(_("Criada em"), auto_now_add=True)

    class Meta:
        """Meta options for the abstract AuditedModel."""

        abstract = True


class Tag(AuditedModel):
    """Tag model to associate tags with any other model via GenericForeignKey."""

    title = models.CharField(_("title"), max_length=255)
    slug = models.CharField(_("slug"), max_length=255)
    content_type = models.ForeignKey(
        ContentType, on_delete=models.CASCADE, verbose_name=_("content type")
    )
    object_id = models.PositiveIntegerField(_("object id"))
    content_object = GenericForeignKey("content_type", "object_id")

    class Meta:
        """Meta options for the Tag model."""

        db_table = "tags"
        verbose_name = _("tag")
        verbose_name_plural = _("tags")
        indexes = (models.Index(fields=["content_type", "object_id"]),)
        abstract = True

    def __str__(self: Self) -> str:
        """Return a string representation of the Tag."""
        return str(self.title)
