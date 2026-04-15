# core/admin/base.py
"""Admin configuration and utilities for the Core admin base module.

Includes custom functions for formatting.
"""

import io
import logging
import unicodedata
from collections.abc import Callable
from typing import Any

import chardet
from import_export.admin import ImportExportModelAdmin
from unfold.admin import ModelAdmin

from django.core.files.uploadedfile import InMemoryUploadedFile
from django.http import HttpRequest
from django.template.response import TemplateResponse

# Exported symbols
__all__ = [
    "CustomImportExportAdmin",
    "JustReadAdmin",
]
logger = logging.getLogger("core")


class CustomImportExportAdmin(ImportExportModelAdmin):
    """Custom ImportExportAdmin."""

    """
    - Automatically detect file encoding.
    - Normalize special characters.
    - Convert files to UTF-8 before importing.
    """

    def import_action(self, request: HttpRequest, **kwargs: Any) -> TemplateResponse:
        """Override import_action to process file encoding before importing."""
        if "import_file" in request.FILES:
            import_file = request.FILES["import_file"]  # Get uploaded file
            file_name = import_file.name  # File name
            file_size = import_file.size  # File size

            logger.info("Uploaded file: %s (%s bytes)", file_name, file_size)

            # Read a sample of the file to detect encoding
            raw_sample = import_file.read(4096)
            detected_encoding = chardet.detect(raw_sample).get("encoding", "utf-8")

            # Fallback if detection fails
            if not detected_encoding or detected_encoding.lower() in [
                "ascii",
                "unknown",
            ]:
                detected_encoding = "utf-8"

            logger.info("Detected encoding: %s", detected_encoding)

            # Reset file pointer before full reading
            import_file.seek(0)

            try:
                # Read entire file content safely
                file_content = import_file.read().decode(detected_encoding, errors="ignore")
            except UnicodeDecodeError as err:
                logger.exception("Encoding conversion failed")
                msg = f"Failed to decode file with detected encoding: {detected_encoding}"
                raise ValueError(msg) from err

            # Normalize Unicode (using NFC to preserve correct characters)
            if detected_encoding == "utf-8":
                normalized_content = file_content
                logger.info("File encoding already UTF-8 — skipping normalization.")
            else:
                normalized_content = unicodedata.normalize("NFC", file_content)
                logger.info("File normalized using NFC.")

            # Convert the normalized content into an in-memory file
            utf_file = io.BytesIO()
            utf_file.write(normalized_content.encode("utf-8"))
            utf_file.seek(0)  # Reset pointer

            # Replace the uploaded file with the UTF-8 converted version
            request.FILES["import_file"] = InMemoryUploadedFile(
                utf_file,  # File object
                "import_file",  # Field name
                file_name,  # File name
                "text/csv",  # Set proper content type
                utf_file.getbuffer().nbytes,  # File size
                "utf-8",  # Charset
            )

        # logger.info("Updated Request.FILES['import_file'] with UTF-8 content.")

        # Proceed with the default import action
        return super().import_action(request, **kwargs)


class JustReadAdmin(ModelAdmin):
    """Read-only admin class that disables add, change, and delete actions in the admin interface."""

    actions_on_top = True
    actions_on_bottom = False

    def has_add_permission(self, _request: HttpRequest) -> bool:
        """Disable the 'add' button in admin since records are auto-generated."""
        return False

    def has_change_permission(self, _request: HttpRequest) -> bool:
        """Disable manual editing of summary records in admin."""
        return False

    def has_delete_permission(self, _request: HttpRequest) -> bool:
        """Prevent deletion of summary records from the admin."""
        return False

    def get_actions(self, request: HttpRequest) -> dict[str, Callable]:
        """Get the default actions. It used to customize the list of actions available in the admin interface."""
        return super().get_actions(request)
