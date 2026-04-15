# core/admin/celery_beat.py
"""Admin configuration and utilities for the Core admin celery_beat module.

Includes custom functions for formatting fields.
"""

from django_celery_beat.admin import ClockedScheduleAdmin as BaseClockedScheduleAdmin
from django_celery_beat.admin import CrontabScheduleAdmin as BaseCrontabScheduleAdmin
from django_celery_beat.admin import PeriodicTaskAdmin as BasePeriodicTaskAdmin
from django_celery_beat.admin import PeriodicTaskForm, TaskSelectWidget
from django_celery_beat.models import (
    ClockedSchedule,
    CrontabSchedule,
    IntervalSchedule,
    PeriodicTask,
    SolarSchedule,
)
from unfold.admin import ModelAdmin
from unfold.widgets import (
    UnfoldAdminSelectWidget,
    UnfoldAdminTextInputWidget,
)

from django.contrib import admin

from core.sites import core_admin_site

admin.site.unregister(PeriodicTask)
admin.site.unregister(IntervalSchedule)
admin.site.unregister(CrontabSchedule)
admin.site.unregister(SolarSchedule)
admin.site.unregister(ClockedSchedule)


class UnfoldTaskSelectWidget(UnfoldAdminSelectWidget, TaskSelectWidget):
    """Custom task select widget combining Unfold and Celery Beat functionality."""


class UnfoldPeriodicTaskForm(PeriodicTaskForm):
    """Custom periodic task form with Unfold widget integration."""

    def __init__(self, *args: tuple, **kwargs: dict) -> None:
        """Initialize the form with Unfold widgets for task and regtask fields.

        Args:
            *args: Variable length argument list.
            **kwargs: Arbitrary keyword arguments.

        """
        super().__init__(*args, **kwargs)
        self.fields["task"].widget = UnfoldAdminTextInputWidget()
        self.fields["regtask"].widget = UnfoldTaskSelectWidget()


@admin.register(PeriodicTask, site=core_admin_site)
class PeriodicTaskAdmin(BasePeriodicTaskAdmin, ModelAdmin):
    """Admin interface for PeriodicTask model with Unfold widget integration."""

    form = UnfoldPeriodicTaskForm


@admin.register(IntervalSchedule, site=core_admin_site)
class IntervalScheduleAdmin(ModelAdmin):
    """Admin interface for IntervalSchedule model."""


@admin.register(CrontabSchedule, site=core_admin_site)
class CrontabScheduleAdmin(BaseCrontabScheduleAdmin, ModelAdmin):
    """Admin interface for CrontabSchedule model."""


@admin.register(SolarSchedule, site=core_admin_site)
class SolarScheduleAdmin(ModelAdmin):
    """Admin interface for SolarSchedule model."""


@admin.register(ClockedSchedule, site=core_admin_site)
class ClockedScheduleAdmin(BaseClockedScheduleAdmin, ModelAdmin):
    """Admin interface for ClockedSchedule model."""
