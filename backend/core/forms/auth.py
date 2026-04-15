# core/forms/auth.py
"""Authentication forms configuration."""

from typing import Any

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Fieldset, Layout
from unfold.forms import AuthenticationForm
from unfold.widgets import (
    UnfoldAdminCheckboxSelectMultiple,
    UnfoldAdminDateWidget,
    UnfoldAdminEmailInputWidget,
    UnfoldAdminExpandableTextareaWidget,
    UnfoldAdminFileFieldWidget,
    UnfoldAdminImageFieldWidget,
    UnfoldAdminIntegerFieldWidget,
    UnfoldAdminMoneyWidget,
    UnfoldAdminRadioSelectWidget,
    UnfoldAdminSelect2Widget,
    UnfoldAdminSplitDateTimeWidget,
    UnfoldAdminTextareaWidget,
    UnfoldAdminTextInputWidget,
    UnfoldAdminTimeWidget,
    UnfoldAdminURLInputWidget,
    UnfoldBooleanSwitchWidget,
)

from django import forms
from django.conf import settings
from django.http import HttpRequest
from django.utils.translation import gettext_lazy as _
from django.views.generic import RedirectView


class HomeView(RedirectView):
    """Redirect to admin index page."""

    pattern_name = "admin:index"


class CustomFormMixin(forms.Form):
    """Mixin class providing common form fields for custom forms.

    This mixin includes fields for user information, preferences, and contact details,
    styled using Unfold admin widgets.
    """

    name = forms.CharField(
        max_length=100,
        label=_("Name"),
        required=True,
        widget=UnfoldAdminTextInputWidget(),
    )
    email = forms.EmailField(
        label=_("Email"),
        required=True,
        widget=UnfoldAdminEmailInputWidget(),
    )
    age = forms.IntegerField(
        label=_("Age"),
        required=True,
        min_value=18,
        max_value=120,
        widget=UnfoldAdminIntegerFieldWidget(),
    )
    url = forms.URLField(
        assume_scheme="https",
        label=_("URL"),
        required=True,
        widget=UnfoldAdminURLInputWidget(),
    )
    salary = forms.DecimalField(
        label=_("Salary"),
        required=True,
        help_text=_("Enter your salary"),
        widget=UnfoldAdminMoneyWidget(),
    )
    title = forms.CharField(
        label=_("Title"),
        required=True,
        widget=UnfoldAdminExpandableTextareaWidget(),
    )
    message = forms.CharField(
        label=_("Message"),
        required=True,
        widget=UnfoldAdminTextareaWidget(),
    )
    subscribe = forms.BooleanField(
        label=_("Subscribe to newsletter"),
        required=True,
        initial=True,
        help_text=_("Toggle to receive our newsletter with updates and offers"),
        widget=UnfoldBooleanSwitchWidget,
    )
    notifications = forms.BooleanField(
        label=_("Receive notifications"),
        required=True,
        initial=False,
        help_text=_("Toggle to receive notifications about your inquiry status"),
        widget=UnfoldBooleanSwitchWidget,
    )
    department = forms.ChoiceField(
        label=_("Department"),
        choices=[
            ("sales", _("Sales")),
            ("marketing", _("Marketing")),
            ("development", _("Development")),
            ("hr", _("Human Resources")),
            ("other", _("Other")),
        ],
        required=True,
        help_text=_("Select the department to contact"),
        widget=UnfoldAdminRadioSelectWidget,
    )
    category = forms.ChoiceField(
        label=_("Category"),
        choices=[
            ("general", _("General Inquiry")),
            ("support", _("Technical Support")),
            ("feedback", _("Feedback")),
            ("other", _("Other")),
        ],
        required=True,
        help_text=_("Select the category of your message"),
        widget=UnfoldAdminCheckboxSelectMultiple,
    )
    priority = forms.TypedChoiceField(
        label=_("Priority"),
        choices=[
            (1, _("Low")),
            (2, _("Medium")),
            (3, _("High")),
        ],
        coerce=int,
        required=True,
        initial=2,
        help_text=_("Select the priority of your message"),
        widget=UnfoldAdminSelect2Widget,
    )
    date = forms.DateField(
        label=_("Date"),
        required=True,
        widget=UnfoldAdminDateWidget,
    )
    time = forms.TimeField(
        label=_("Time"),
        required=True,
        widget=UnfoldAdminTimeWidget,
    )
    datetime = forms.SplitDateTimeField(
        label=_("Date and Time"),
        required=True,
        widget=UnfoldAdminSplitDateTimeWidget,
    )
    file = forms.FileField(
        label=_("File"),
        required=True,
        widget=UnfoldAdminFileFieldWidget,
    )
    image = forms.ImageField(
        label=_("Image"),
        required=True,
        widget=UnfoldAdminImageFieldWidget,
    )


class CustomHorizontalForm(CustomFormMixin):
    """Horizontal layout form with all custom form fields.

    This form extends CustomFormMixin and uses Crispy Forms to render
    all fields in a horizontal layout with organized fieldsets.
    """

    def __init__(self, *args: any, **kwargs: any) -> None:
        """Initialize the form with a horizontal layout and organized fieldsets."""
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_class = "form-horizontal"
        self.helper.layout = Layout(
            Fieldset(
                _("Custom horizontal form"),
                "name",
                "email",
                "age",
                "url",
                "salary",
                "title",
                "message",
                "subscribe",
                "notifications",
                "department",
                "category",
                "date",
                "time",
                "datetime",
            ),
        )


class LoginForm(AuthenticationForm):
    """Login form with optional pre-filled credentials from settings.

    This form extends Django's AuthenticationForm and provides the ability
    to pre-fill username and password fields from Django settings for convenience.
    """

    password = forms.CharField(widget=forms.PasswordInput(render_value=True))

    # Use Optional[HttpRequest] to indicate it can be an HttpRequest or None
    def __init__(self, request: HttpRequest | None = None, *args: Any, **kwargs: Any) -> None:
        """Initialize the LoginForm with optional pre-filled credentials."""
        super().__init__(request, *args, **kwargs)

        if settings.LOGIN_USERNAME and settings.LOGIN_PASSWORD:
            self.fields["username"].initial = settings.LOGIN_USERNAME
            self.fields["password"].initial = settings.LOGIN_PASSWORD
