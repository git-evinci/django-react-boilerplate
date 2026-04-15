# core/admin/constance.py
"""Admin configuration and utilities for the Core admin constance module.

Includes custom functions for formatting fields.
"""

from constance.admin import Config, ConstanceAdmin

from django.contrib import admin

from core.sites import core_admin_site


@admin.register(Config, site=core_admin_site)
class ConstanceConfigAdmin(ConstanceAdmin):
    """Admin interface for Constance configuration settings."""
