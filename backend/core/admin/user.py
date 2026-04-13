# core/admin/user.py
"""Admin configuration for user-related models such as User, EmailAddress, and UserProfile."""
import logging
from contextlib import suppress
from typing import Any

from allauth.account.models import EmailAddress
from import_export.admin import ImportExportActionModelAdmin, ImportExportModelAdmin
from unfold.admin import ModelAdmin
from unfold.contrib.import_export.forms import ExportForm, ImportForm
from unfold.decorators import display
from unfold.forms import AdminPasswordChangeForm, UserChangeForm, UserCreationForm

from django.contrib import admin
from django.contrib.auth.admin import GroupAdmin as BaseGroupAdmin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import Group, User
from django.http import HttpRequest
from django.template.response import TemplateResponse
from django.utils.html import format_html
from django.utils.translation import gettext_lazy as _

from core.models import UserProfile
from core.resources import UserResource
from core.sites import core_admin_site

for model in (User, Group, EmailAddress):
    with suppress(admin.sites.NotRegistered):
        admin.site.unregister(model)

__all__ = [
    "EmailAddressAdmin",
    "GroupAdmin",
    "UserAdmin",
    "UserProfileAdmin",
]

logger = logging.getLogger("core")


@admin.register(User, site=core_admin_site)
class UserAdmin(
    BaseUserAdmin, ModelAdmin, ImportExportModelAdmin, ImportExportActionModelAdmin
):
    """Admin configuration for User model with import/export capabilities."""

    form = UserChangeForm
    add_form = UserCreationForm
    change_password_form = AdminPasswordChangeForm

    resource_class = UserResource
    export_form_class = ExportForm
    import_form_class = ImportForm

    list_display = (
        "id",
        "username",
        "email",
        "first_name",
        "last_name",
        "is_active",
        "is_staff",
        "is_superuser",
    )
    list_display_links = ("id", "username", "email", "first_name", "last_name")
    list_filter = ("is_staff", "is_superuser", "is_active", "groups")
    search_fields = ("username", "email")
    ordering = ("id", "username")
    readonly_fields = ("date_joined", "last_login")
    filter_horizontal = ("groups", "user_permissions")
    fieldsets = (
        (None, {"fields": ("username", "password")}),
        (
            _("Personal info"),
            {
                "fields": (("first_name", "last_name"), "email"),
                "classes": ["tab"],
            },
        ),
        (
            _("Permissions"),
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                ),
                "classes": ["tab"],
            },
        ),
        (
            _("Important dates"),
            {
                "fields": ("last_login", "date_joined"),
                "classes": ["tab"],
            },
        ),
    )

    @display(description=_("Usuário"))
    def display_header(self, instance: User) -> str:
        """Return the username of the user instance."""
        return instance.username

    @display(description=_("Staff"), boolean=True)
    def display_staff(self, instance: User) -> str:
        """Return whether the user has staff privileges."""
        return instance.is_staff

    @display(description=_("Superusuário"), boolean=True)
    def display_superuser(self, instance: User) -> str:
        """Return whether the user has superuser privileges."""
        return instance.is_superuser

    @display(description=_("Criado"))
    def display_created(self, instance: User) -> str:
        """Return the creation date of the user instance."""
        return instance.created_at


@admin.register(EmailAddress, site=core_admin_site)
class EmailAddressAdmin(ModelAdmin):
    """Admin configuration for EmailAddress model."""

    list_display = (
        "email",
        "user",
        "verified",
        "primary",
    )  # Customize fields displayed in the list view
    search_fields = ("email", "user__username")  # Add search functionality
    list_filter = ("verified", "primary")  # Add filters


@admin.register(Group, site=core_admin_site)
class GroupAdmin(BaseGroupAdmin, ModelAdmin):
    """Admin configuration for Group model."""

    def changelist_view(
        self, request: HttpRequest, extra_context: dict[str, Any] | None = None
    ) -> TemplateResponse:
        """Render the changelist view for the Group admin."""
        return super().changelist_view(request, extra_context=extra_context)


@admin.register(UserProfile, site=core_admin_site)
class UserProfileAdmin(ModelAdmin):
    """Admin configuration for UserProfile, managing additional fields for Django's User model."""

    list_display = (
        "id",
        "picture_display",
        "get_username",
        "get_email",
        "get_last_login",
        "get_created_on",
    )
    list_display_links = list_display
    ordering = ("id", "user__username")
    search_fields = (
        "user__username",
        "user__email",
        "user__first_name",
        "user__last_name",
    )
    list_filter = (
        "user__is_staff",
        "user__is_superuser",
        "user__is_active",
    )
    readonly_fields = ("user",)

    fieldsets = ((None, {"fields": ("user", "picture")}),)

    @display(ordering="user__username", description="Username")
    def get_username(self, obj: UserProfile) -> str:
        """Retrieve the username from the related User model."""
        return obj.user.username

    @display(ordering="user__email", description="Email")
    def get_email(self, obj: UserProfile) -> str:
        """Retrieve the email from the related User model."""
        return obj.user.email

    @display(ordering="user__last_login", description="Last Login")
    def get_last_login(self, obj: UserProfile) -> str:
        """Retrieve the last login timestamp from the related User model."""
        return obj.user.last_login if obj.user.last_login else "Never Logged In"

    @display(ordering="user__date_joined", description="Created On")
    def get_created_on(self, obj: UserProfile) -> str:
        """Retrieve the account creation date from the related User model."""
        return (
            obj.user.date_joined.strftime("%Y-%m-%d %H:%M:%S")
            if obj.user.date_joined
            else "Desconhecido"
        )

    @display(description="Avatar")
    def picture_display(self, obj: UserProfile) -> str:
        """Display the user's profile picture as a small avatar in the admin list view."""
        try:
            picture_url = obj.get_picture_url()
            return format_html(
                '<img class="w-8 h-8 rounded-full border-2 border-solid border-acv_burned_earth-800" '
                'src="{}" alt="Profile Picture">',
                picture_url,
            )
        except Exception:
            return format_html(
                '<span class="text-xs text-red-600 italic">No Image</span>'
            )
