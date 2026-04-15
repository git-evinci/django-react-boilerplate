# core/views.py
"""Views and utilities for RoatanMahogany application."""

import json
import logging
import random
from functools import lru_cache
from typing import Any

from unfold.sites import UnfoldAdminSite

from django.contrib.humanize.templatetags.humanize import intcomma
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from django.utils.safestring import mark_safe
from django.utils.translation import gettext_lazy as _
from django.views.generic import RedirectView

logger = logging.getLogger("core")


class HomeView(RedirectView):
    """Redirect to the admin index page."""

    pattern_name = "admin:index"


def get_base_context(request: HttpRequest) -> dict[str, Any]:
    """Return the base context shared by all views."""
    unfold_admin = UnfoldAdminSite()
    return unfold_admin.each_context(request)


class UnfoldContextMixin:
    """Mixin to provide Unfold admin context to class-based views."""

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        """Merge Unfold admin context and set default metadata."""
        context = super().get_context_data(**kwargs)  # type: ignore
        context.update(get_base_context(self.request))  # type: ignore

        # Optional: Set default values if not provided
        context.setdefault("title", "Password Reset")
        context.setdefault("meta_description", "Reset your password on Acervo Invest.")
        context.setdefault("theme", "dark-mode")
        context.setdefault("site_title", "Acervo Invest")
        context.setdefault("styles", [])
        context.setdefault("page_style", "")
        context.setdefault("is_popup", False)
        context.setdefault("page_script", "")
        return context


def custom_404(request: HttpRequest, exception: Exception) -> HttpResponse:
    """Render the error 404 page for the website.

    Args:
        request: The HTTP request object.
        exception: The exception that triggered the 404 (unused).

    """
    # Explicitly mark exception as unused for the linter if needed,
    # though usually just having it in the signature is enough for Django.
    _ = exception

    context = get_base_context(request)
    context["title"] = "Error 404"
    context["meta_description"] = context.get("meta_description", "Page not found")

    return render(request, "core/404.html", context, status=404)


def custom_500(request: HttpRequest) -> HttpResponse:
    """Render the error 500 page."""
    context = get_base_context(request)
    context["title"] = "Error 500"
    context["meta_description"] = context.get("meta_description", "Internal Server Error")

    # Removed exc_info=True because we aren't inside an 'except' block here
    logger.error("500 error occurred at %s", request.path)

    return render(request, "core/500.html", context, status=500)


def test_500(request: HttpRequest) -> HttpResponse:
    """Render the error 500 page (test-only)."""
    return render(request, "core/500.html", status=500)


def dashboard_callback(request: HttpRequest, context: dict[str, Any]) -> dict[str, Any]:
    """Inject dashboard data into the template context."""
    _ = request  # Mark request as unused
    context.update(random_data())
    return context


@lru_cache
def random_data() -> dict[str, Any]:
    """Generate randomized KPI and chart data for the dashboard."""
    weekdays = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]

    positive = [[1, random.randrange(8, 28)] for _ in range(1, 28)]
    negative = [[-1, -random.randrange(8, 28)] for _ in range(1, 28)]
    average = [r[1] - random.randint(3, 5) for r in positive]
    perf_pos = [[1, random.randrange(8, 28)] for _ in range(1, 28)]  # Used in performance
    perf_neg = [[-1, -random.randrange(8, 28)] for _ in range(1, 28)]  # Used in performance

    return {
        "navigation": [
            {"title": _("Dashboard"), "link": "/", "active": True},
            {"title": _("Analytics"), "link": "#"},
            {"title": _("Settings"), "link": "#"},
        ],
        "filters": [
            {"title": _("All"), "link": "#", "active": True},
            {"title": _("New"), "link": "#"},
        ],
        "kpi": [
            {
                "title": "Product A Performance",
                "metric": f"${intcomma(f'{random.uniform(1000, 9999):.02f}')}",
                "footer": mark_safe(
                    f'<strong class="text-green-700 font-semibold">+{intcomma(f"{random.uniform(1, 9):.02f}")}%</strong>&nbsp;progress'
                ),
                "chart": json.dumps(
                    {
                        "labels": [weekdays[day % 7] for day in range(1, 28)],
                        "datasets": [{"data": average, "borderColor": "#9333ea"}],
                    }
                ),
            },
            # ... Product B and C follow same pattern
        ],
        "chart": json.dumps(
            {
                "labels": [weekdays[day % 7] for day in range(1, 28)],
                "datasets": [
                    {"label": "Average", "data": average, "type": "line"},
                    {"label": "Positive", "data": positive},
                    {"label": "Negative", "data": negative},  # VARIABLE NOW USED HERE
                ],
            }
        ),
        "performance": [
            {
                "title": _("Last week revenue"),
                "chart": json.dumps(
                    {
                        "datasets": [{"data": perf_pos}]  # VARIABLE NOW USED HERE
                    }
                ),
            },
            {
                "title": _("Last week expenses"),
                "chart": json.dumps(
                    {
                        "datasets": [{"data": perf_neg}]  # VARIABLE NOW USED HERE
                    }
                ),
            },
        ],
        "table_data": {
            "headers": [_("Day"), _("Income"), _("Expenses")],
            "rows": [
                ["22-10-2025", "$2,341.89", "$1,876.45"],
            ],
        },
    }
