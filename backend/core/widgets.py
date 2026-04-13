# core/widgets.py
"""Custom widgets for use in the Django admin interface."""

import json
from typing import Any

from unfold.widgets import UnfoldAdminTextInputWidget

from django import forms
from django.core.files.uploadedfile import UploadedFile
from django.forms.widgets import ClearableFileInput
from django.template.loader import render_to_string
from django.utils.safestring import mark_safe


class AdminImagePreviewWidget(ClearableFileInput):
    """Custom widget for image preview in Django Admin."""

    def render(
        self,
        name: str,
        value: UploadedFile | str | None,
        attrs: dict | None = None,
        renderer: Any | None = None,
    ) -> str:
        """Render the file input along with an optional image preview if a value (file) exists.

        Args:
            name (str): The name of the field.
            value: The current value of the field (possibly a file).
            attrs (dict | None): HTML attributes for the input field.
            renderer: Renderer instance (required by Django >=2.1).

        Returns:
            str: HTML string containing the input and the image preview (if any).

        """
        html = super().render(name, value, attrs, renderer)

        if value and hasattr(value, "url"):
            preview = f'<br><img src="{value.url}" style="max-height: 150px;" />'
            return mark_safe(html + preview)
        return html


class AdvantageListWidget(forms.Widget):
    """Widget for rendering and editing a JSON list of advantages in the admin."""

    template_name = "admin/widgets/advantage_list.html"

    def value_omitted_from_data(
        self,
        data: dict[str, Any],
        files: dict[str, Any],
        name: str,
    ) -> bool:
        """Return False to indicate the value is always present in form data."""
        return False

    def value_from_datadict(
        self,
        data: dict[str, Any],
        files: dict[str, Any],
        name: str,
    ) -> list[Any]:
        """Extract the JSON-decoded list value from the form data."""
        raw = data.get(name)
        try:
            return json.loads(raw)
        except Exception:
            return []

    def render(
        self,
        name: str,
        value: list[Any] | None,
        attrs: dict[str, Any] | None = None,
        renderer: Any | None = None,
    ) -> str:
        """Render the widget using a template and the current list value."""
        if value is None:
            value = []
        context = {
            "widget": {
                "name": name,
                "value": value,
            }
        }
        return render_to_string(self.template_name, context)


class CommaSeparatedListWidget(UnfoldAdminTextInputWidget):
    """Widget to edit JSONField as comma-separated values."""

    def format_value(self, value: Any) -> str:
        """Convert a list value to a comma-separated string for display."""
        if isinstance(value, list):
            return ", ".join(str(item).strip() for item in value)
        return super().format_value(value)

    def __init__(self, attrs: dict[str, Any] | None = None) -> None:
        """Initialize with a default placeholder, optionally merged with `attrs`."""
        default_attrs = {"placeholder": "Ex: localização, perto do metrô, supermercado"}
        if attrs:
            default_attrs.update(attrs)
        super().__init__(attrs=default_attrs)
