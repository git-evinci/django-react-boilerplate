# core/sites.py
"""Custom admin site configuration for Core."""

from unfold.sites import UnfoldAdminSite

from core.forms import LoginForm


class CoreAdminSite(UnfoldAdminSite):
    """Custom admin site for Core using a custom login form."""

    login_form = LoginForm


core_admin_site = CoreAdminSite(name="core_admin_site")
