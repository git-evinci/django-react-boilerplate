# core/admin/dashboard.py
"""Admin configuration and utilities for the Core admin dashboard module.

Includes custom functions for formatting fields.
"""

import random
from functools import lru_cache

from unfold.components import BaseComponent, register_component

from django.utils.timezone import now, timedelta


@lru_cache
def tracker_random_data() -> list:
    """Generate random tracker data for display.

    Returns
    -------
    list
        A list of dictionaries with color and tooltip values.

    """
    data = []

    for _i in range(1, 64):
        has_value = random.choice([True, True, True, True, False])
        color = None
        tooltip = None

        if has_value:
            value = random.randint(2, 6)
            color = "bg-primary-500"
            tooltip = f"Value {value}"

        data.append(
            {
                "color": color,
                "tooltip": tooltip,
            }
        )

    return data


@register_component
class TrackerComponent(BaseComponent):
    """Component for displaying tracker data with random values.

    Renders a tracker visualization with randomly generated data including
    color coding and tooltips for each data point.
    """

    def get_context_data(self, **kwargs: dict) -> dict:
        """Get context data for the tracker component.

        Returns
        -------
        dict
            Context dictionary containing tracker data.

        """
        context = super().get_context_data(**kwargs)
        context["data"] = tracker_random_data()
        return context


@lru_cache
def cohort_random_data() -> dict:
    """Generate random cohort analysis data for display.

    Returns
    -------
    dict
        A dictionary containing headers and rows with cohort data including
        values, colors, and subtitles for each cell.

    """
    rows = []
    headers = []
    cols = []

    dates = reversed([(now() - timedelta(days=x)).strftime("%B %d, %Y") for x in range(8)])
    groups = range(1, 10)

    for row_index, date in enumerate(dates):
        cols = []

        for col_index, _col in enumerate(groups):
            color_index = 8 - row_index - col_index
            col_classes = []

            if color_index > 0:
                col_classes.append(f"bg-primary-{color_index}00 dark:bg-primary-{9 - color_index}00")

            if color_index >= 4:
                col_classes.append("text-white")

            if color_index >= 6:
                col_classes.append("dark:text-base-800")

            value = random.randint(
                4000 - (col_index * row_index * 225),
                5000 - (col_index * row_index * 225),
            )

            subtitle = f"{random.randint(10, 100)}%"

            if value <= 0:
                value = 0
                subtitle = None

            cols.append(
                {
                    "value": value,
                    "color": " ".join(col_classes),
                    "subtitle": subtitle,
                }
            )

        rows.append(
            {
                "header": {
                    "title": date,
                    "subtitle": f"Total {sum(col['value'] for col in cols):,}",
                },
                "cols": cols,
            }
        )

    for index, group in enumerate(groups):
        total = sum(row["cols"][index]["value"] for row in rows)

        headers.append(
            {
                "title": f"Group #{group}",
                "subtitle": f"Total {total:,}",
            }
        )

    return {
        "headers": headers,
        "rows": rows,
    }


@register_component
class CohortComponent(BaseComponent):
    """Component for displaying cohort analysis data.

    Renders a cohort analysis table with randomly generated data including
    color coding, values, and subtitles for each cell.
    """

    def get_context_data(self, **kwargs: dict) -> dict:
        """Get context data for the cohort component.

        Returns
        -------
        dict
            Context dictionary containing cohort analysis data.

        """
        context = super().get_context_data(**kwargs)
        context["data"] = cohort_random_data()
        return context
