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

def get_base_context(request: HttpRequest) -> dict:
    """Return the base context shared by all views."""
    unfold_admin = UnfoldAdminSite()
    return unfold_admin.each_context(request)


class UnfoldContextMixin:
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(get_base_context(self.request))  # Merge Unfold admin context

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
        request (HttpRequest): The HTTP request object.
        exception (Exception): The exception that triggered the 404 error.

    Returns:
        HttpResponse: The rendered error 404 page HTML.

    """
    context = get_base_context(request)
    context["title"] = "Error 404"
    context["meta_description"] = context.get(
        "meta_description", "Page not found on the site"
    )

    return render(request, "core/404.html", context, status=404)


def custom_500(request: HttpRequest) -> HttpResponse:
    """Render the error 500 page."""
    context = get_base_context(request)
    context["title"] = "Error 500"
    context["meta_description"] = context.get(
        "meta_description", "Internal Server Error"
    )
    logger.error("500 error occurred", exc_info=True)
    return render(request, "core/500.html", context, status=500)


def test_500(request: HttpRequest) -> HttpResponse:
    """Render the error 500 page (test-only)."""
    return render(request, "core/500.html", status=500)


def dashboard_callback(request: HttpRequest, context: dict[str, Any]) -> dict[str, Any]:
    """Inject dashboard data into the template context."""
    context.update(random_data())
    return context

@lru_cache
def random_data():
    WEEKDAYS = [
        "Mon",
        "Tue",
        "Wed",
        "Thu",
        "Fri",
        "Sat",
        "Sun",
    ]

    positive = [[1, random.randrange(8, 28)] for i in range(1, 28)]
    negative = [[-1, -random.randrange(8, 28)] for i in range(1, 28)]
    average = [r[1] - random.randint(3, 5) for r in positive]
    performance_positive = [[1, random.randrange(8, 28)] for i in range(1, 28)]
    performance_negative = [[-1, -random.randrange(8, 28)] for i in range(1, 28)]

    return {
        "navigation": [
            {"title": _("Dashboard"), "link": "/", "active": True},
            {"title": _("Analytics"), "link": "#"},
            {"title": _("Settings"), "link": "#"},
        ],
        "filters": [
            {"title": _("All"), "link": "#", "active": True},
            {
                "title": _("New"),
                "link": "#",
            },
        ],
        "kpi": [
            {
                "title": "Product A Performance",
                "metric": f"${intcomma(f'{random.uniform(1000, 9999):.02f}')}",
                "footer": mark_safe(
                    f'<strong class="text-green-700 font-semibold dark:text-green-400">+{intcomma(f"{random.uniform(1, 9):.02f}")}%</strong>&nbsp;progress from last week'
                ),
                "chart": json.dumps(
                    {
                        "labels": [WEEKDAYS[day % 7] for day in range(1, 28)],
                        "datasets": [{"data": average, "borderColor": "#9333ea"}],
                    }
                ),
            },
            {
                "title": "Product B Performance",
                "metric": f"${intcomma(f'{random.uniform(1000, 9999):.02f}')}",
                "footer": mark_safe(
                    f'<strong class="text-green-700 font-semibold dark:text-green-400">+{intcomma(f"{random.uniform(1, 9):.02f}")}%</strong>&nbsp;progress from last week'
                ),
            },
            {
                "title": "Product C Performance",
                "metric": f"${intcomma(f'{random.uniform(1000, 9999):.02f}')}",
                "footer": mark_safe(
                    f'<strong class="text-green-700 font-semibold dark:text-green-400">+{intcomma(f"{random.uniform(1, 9):.02f}")}%</strong>&nbsp;progress from last week'
                ),
            },
        ],
        "progress": [
            {
                "title": "Social marketing e-book",
                "description": f"${intcomma(f'{random.uniform(1000, 9999):.02f}')}",
                "value": random.randint(10, 90),
            },
            {
                "title": "Freelancing tasks",
                "description": f"${intcomma(f'{random.uniform(1000, 9999):.02f}')}",
                "value": random.randint(10, 90),
            },
            {
                "title": "Development coaching",
                "description": f"${intcomma(f'{random.uniform(1000, 9999):.02f}')}",
                "value": random.randint(10, 90),
            },
            {
                "title": "Product consulting",
                "description": f"${intcomma(f'{random.uniform(1000, 9999):.02f}')}",
                "value": random.randint(10, 90),
            },
            {
                "title": "Other income",
                "description": f"${intcomma(f'{random.uniform(1000, 9999):.02f}')}",
                "value": random.randint(10, 90),
            },
            {
                "title": "Course sales",
                "description": f"${intcomma(f'{random.uniform(1000, 9999):.02f}')}",
                "value": random.randint(10, 90),
            },
            {
                "title": "Ads revenue",
                "description": f"${intcomma(f'{random.uniform(1000, 9999):.02f}')}",
                "value": random.randint(10, 90),
            },
            {
                "title": "Customer Retention Rate",
                "description": f"${intcomma(f'{random.uniform(1000, 9999):.02f}')}",
                "value": random.randint(10, 90),
            },
        ],
        "chart": json.dumps(
            {
                "labels": [WEEKDAYS[day % 7] for day in range(1, 28)],
                "datasets": [
                    {
                        "label": "Example 1",
                        "type": "line",
                        "data": average,
                        "borderColor": "var(--color-primary-500)",
                    },
                    {
                        "label": "Example 2",
                        "data": positive,
                        "backgroundColor": "var(--color-primary-700)",
                    },
                    {
                        "label": "Example 3",
                        "data": negative,
                        "backgroundColor": "var(--color-primary-300)",
                    },
                ],
            }
        ),
        "performance": [
            {
                "title": _("Last week revenue"),
                "metric": "$1,234.56",
                "footer": mark_safe(
                    '<strong class="text-green-600 font-medium">+3.14%</strong>&nbsp;progress from last week'
                ),
                "chart": json.dumps(
                    {
                        "labels": [WEEKDAYS[day % 7] for day in range(1, 28)],
                        "datasets": [
                            {
                                "data": performance_positive,
                                "borderColor": "var(--color-primary-700)",
                            }
                        ],
                    }
                ),
            },
            {
                "title": _("Last week expenses"),
                "metric": "$1,234.56",
                "footer": mark_safe(
                    '<strong class="text-green-600 font-medium">+3.14%</strong>&nbsp;progress from last week'
                ),
                "chart": json.dumps(
                    {
                        "labels": [WEEKDAYS[day % 7] for day in range(1, 28)],
                        "datasets": [
                            {
                                "data": performance_negative,
                                "borderColor": "var(--color-primary-300)",
                            }
                        ],
                    }
                ),
            },
        ],
        "table_data": {
            "headers": [_("Day"), _("Income"), _("Expenses")],
            "rows": [
                ["22-10-2025", "$2,341.89", "$1,876.45"],
                ["23-10-2025", "$1,987.23", "$2,109.67"],
                ["24-10-2025", "$3,456.78", "$1,543.21"],
                ["25-10-2025", "$1,765.43", "$2,987.65"],
                ["26-10-2025", "$2,876.54", "$1,234.56"],
                ["27-10-2025", "$1,543.21", "$2,765.43"],
                ["28-10-2025", "$3,210.98", "$1,987.65"],
            ],
        },
    }