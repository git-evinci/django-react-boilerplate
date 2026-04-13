# core/resources.py
"""Resource classes for importing and exporting data in the Core application.

This module provides resource classes for handling import/export operations between
various data formats (CSV, Excel, etc.) and Django models, with custom widgets for
data conversion and validation.
"""

import logging

from import_export import resources

from django.contrib.auth import get_user_model

logger = logging.getLogger("import_export")

User = get_user_model()


# Exported symbols
__all__ = [
    "UserResource",
]


class UserResource(resources.ModelResource):
    """Resource class for handling User model import/export."""

    class Meta:
        """Configuration options for UserResource."""

        model = User
        fields = (
            "id",
            "username",
            "email",
            "first_name",
            "last_name",
            "is_active",
            "is_staff",
            "is_superuser",
            "date_joined",
            "last_login",
        )
        skip_unchanged = True
        report_skipped = True

