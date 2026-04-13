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
    pass


class UnfoldPeriodicTaskForm(PeriodicTaskForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["task"].widget = UnfoldAdminTextInputWidget()
        self.fields["regtask"].widget = UnfoldTaskSelectWidget()


@admin.register(PeriodicTask, site=core_admin_site)
class PeriodicTaskAdmin(BasePeriodicTaskAdmin, ModelAdmin):
    form = UnfoldPeriodicTaskForm


@admin.register(IntervalSchedule, site=core_admin_site)
class IntervalScheduleAdmin(ModelAdmin):
    pass


@admin.register(CrontabSchedule, site=core_admin_site)
class CrontabScheduleAdmin(BaseCrontabScheduleAdmin, ModelAdmin):
    pass


@admin.register(SolarSchedule, site=core_admin_site)
class SolarScheduleAdmin(ModelAdmin):
    pass


@admin.register(ClockedSchedule, site=core_admin_site)
class ClockedScheduleAdmin(BaseClockedScheduleAdmin, ModelAdmin):
    pass