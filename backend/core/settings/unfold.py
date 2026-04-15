# core/settings/unfold.py
"""Unfold configuration settings.

This module defines all settings related to the Unfold admin panel integration.
"""

from django.templatetags.static import static
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _

UNFOLD = {
    "SITE_HEADER": _("Admin Panel"),
    "SITE_TITLE": _("Game"),
    # "SITE_URL": "/",
    "SITE_ICON": {
        "light": lambda request: static("core/img/icons/icon-light.svg"),  # light mode
        "dark": lambda request: static("core/img/icons/icon-dark.svg"),  # dark mode
    },
    "SITE_DROPDOWN": [
        {
            "icon": "diamond",
            "title": _("Unfold theme repository"),
            "link": "https://github.com/unfoldadmin/django-unfold",
        },
        {
            "icon": "rocket_launch",
            "title": _("Turbo boilerplate repository"),
            "link": "https://github.com/unfoldadmin/turbo",
        },
        {
            "icon": "description",
            "title": _("Technical documentation"),
            "link": "https://unfoldadmin.com/docs/",
        },
    ],
    "SITE_SYMBOL": "settings",
    "SHOW_LANGUAGES": True,
    "SHOW_HISTORY": True,
    # "THEME": "dark",
    "ENVIRONMENT": "core.utils.environment_callback",
    "DASHBOARD_CALLBACK": "core.views.dashboard_callback",
    "LOGIN": {
        "image": lambda request: static("core/img/backgrounds/login-xl.png"),
    },
    "STYLES": [
        lambda request: static("core/css/core.css"),
    ],
    "SCRIPTS": [
        # lambda request: static("js/chart.min.js"),
    ],
    "SITE_FAVICONS": [
        {
            "rel": "shortcut icon",
            "type": "image/x-icon",
            "href": lambda request: static("core/img/icons/favicon.ico"),
        },
        # Apple Touch Icons (PNG only)
        {
            "rel": "apple-touch-icon",
            "type": "image/png",
            "sizes": "57x57",
            "href": lambda request: static("core/img/icons/apple-icon-57x57.png"),
        },
        {
            "rel": "apple-touch-icon",
            "type": "image/png",
            "sizes": "60x60",
            "href": lambda request: static("core/img/icons/apple-icon-60x60.png"),
        },
        {
            "rel": "apple-touch-icon",
            "type": "image/png",
            "sizes": "72x72",
            "href": lambda request: static("core/img/icons/apple-icon-72x72.png"),
        },
        {
            "rel": "apple-touch-icon",
            "type": "image/png",
            "sizes": "76x76",
            "href": lambda request: static("core/img/icons/apple-icon-76x76.png"),
        },
        {
            "rel": "apple-touch-icon",
            "type": "image/png",
            "sizes": "114x114",
            "href": lambda request: static("core/img/icons/apple-icon-114x114.png"),
        },
        {
            "rel": "apple-touch-icon",
            "type": "image/png",
            "sizes": "120x120",
            "href": lambda request: static("core/img/icons/apple-icon-120x120.png"),
        },
        {
            "rel": "apple-touch-icon",
            "type": "image/png",
            "sizes": "144x144",
            "href": lambda request: static("core/img/icons/apple-icon-144x144.png"),
        },
        {
            "rel": "apple-touch-icon",
            "type": "image/png",
            "sizes": "152x152",
            "href": lambda request: static("core/img/icons/apple-icon-152x152.png"),
        },
        {
            "rel": "apple-touch-icon",
            "type": "image/png",
            "sizes": "180x180",
            "href": lambda request: static("core/img/icons/apple-icon-180x180.png"),
        },
        # Android / General Icons
        {
            "rel": "icon",
            "type": "image/png",
            "sizes": "36x36",
            "href": lambda request: static("core/img/icons/android-icon-36x36.webp"),
        },
        {
            "rel": "icon",
            "type": "image/png",
            "sizes": "48x48",
            "href": lambda request: static("core/img/icons/android-icon-48x48.webp"),
        },
        {
            "rel": "icon",
            "type": "image/png",
            "sizes": "72x72",
            "href": lambda request: static("core/img/icons/android-icon-72x72.webp"),
        },
        {
            "rel": "icon",
            "type": "image/png",
            "sizes": "96x96",
            "href": lambda request: static("core/img/icons/android-icon-96x96.webp"),
        },
        {
            "rel": "icon",
            "type": "image/png",
            "sizes": "144x144",
            "href": lambda request: static("core/img/icons/android-icon-144x144.webp"),
        },
        {
            "rel": "icon",
            "type": "image/png",
            "sizes": "192x192",
            "href": lambda request: static("core/img/icons/android-icon-192x192.webp"),
        },
        {
            "rel": "icon",
            "type": "image/png",
            "sizes": "512x512",
            "href": lambda request: static("core/img/icons/android-icon-512x512.webp"),
        },
        # Favicon sizes
        {
            "rel": "icon",
            "type": "image/webp",
            "sizes": "512x512",
            "href": lambda request: static("core/img/icons/favicon-512x512.webp"),
        },
        # Manifest
        {
            "rel": "manifest",
            "href": lambda request: static("manifest.json"),
        },
        # Second fallback favicon
        {
            "rel": "shortcut icon",
            "type": "image/ico",
            "href": lambda request: static("core/img/icons/favicon.ico"),
        },
        # Microsoft Tiles (Windows)
        {
            "rel": "icon",
            "type": "image/png",
            "sizes": "70x70",
            "href": lambda request: static("core/img/icons/ms-icon-70x70.png"),
        },
        {
            "rel": "icon",
            "type": "image/png",
            "sizes": "144x144",
            "href": lambda request: static("core/img/icons/ms-icon-144x144.png"),
        },
        {
            "rel": "icon",
            "type": "image/png",
            "sizes": "150x150",
            "href": lambda request: static("core/img/icons/ms-icon-150x150.png"),
        },
        {
            "rel": "icon",
            "type": "image/png",
            "sizes": "310x310",
            "href": lambda request: static("core/img/icons/ms-icon-310x310.png"),
        },
        {
            "rel": "mask-icon",
            "type": "image/svg+xml",
            "color": "#000000",
            "href": lambda request: static("core/img/icons/safari-pinned-tab.svg"),
        },
    ],
    "COLORS": {
        "font": {
            "subtle-light": "#6d6d6d",
            "subtle-dark": "#888888",
            "default-light": "#5d5d5d",
            "default-dark": "#b0b0b0",
            "important-light": "#3d3d3d",
            "important-dark": "#e7e7e7",
        },
        "primary": {
            "50": "#fef5ee",
            "100": "#fde7d7",
            "200": "#fbcbad",
            "300": "#f8a779",
            "400": "#f47843",
            "500": "#f15a25",
            "600": "#e23c14",
            "700": "#bb2b13",
            "800": "#952417",
            "900": "#782016",
            "950": "#410d09",
        },
        "acv_graphite": {
            50: "#f2f2f2",
            100: "#e7e7e7",
            200: "#d1d1d1",
            300: "#b0b0b0",
            400: "#888888",
            500: "#6d6d6d",
            600: "#5d5d5d",
            700: "#4f4f4f",
            800: "#454545",
            900: "#3d3d3d",
            950: "#252525",
        },
        "acv_orange": {
            50: "#fef5ee",
            100: "#fde7d7",
            200: "#fbcbad",
            300: "#f8a779",
            400: "#f47843",
            500: "#f15a25",
            600: "#e23c14",
            700: "#bb2b13",
            800: "#952417",
            900: "#782016",
            950: "#410d09",
        },
        "acv_burned_earth": {
            50: "#fff7ed",
            100: "#feedd6",
            200: "#fcd8ac",
            300: "#f9bb78",
            400: "#f69541",
            500: "#f3761c",
            600: "#e45c12",
            700: "#bd4511",
            800: "#993816",
            900: "#792f15",
            950: "#411609",
        },
    },
    "TABS": [
        # {
        #     "page": "django_celery_beat_clockedschedule",
        #     "models": [
        #         "django_celery_beat.clockedschedule",
        #         "django_celery_beat.crontabschedule",
        #         "django_celery_beat.intervalschedule",
        #         "django_celery_beat.periodictask",
        #         "django_celery_beat.solarschedule",
        #     ],
        #     "items": [
        #         {
        #             "title": _("Horários fixos"),
        #             "icon": "hourglass_bottom",
        #             "link": reverse_lazy("admin:django_celery_beat_clockedschedule_changelist"),
        #         },
        #         {
        #             "title": _("Personalizados (Crontabs)"),
        #             "icon": "update",
        #             "link": reverse_lazy("admin:django_celery_beat_crontabschedule_changelist"),
        #         },
        #         {
        #             "title": _("Intervalos"),
        #             "icon": "timer",
        #             "link": reverse_lazy("admin:django_celery_beat_intervalschedule_changelist"),
        #         },
        #         {
        #             "title": _("Definir Tarefas periódicas"),
        #             "icon": "task",
        #             "link": reverse_lazy("admin:django_celery_beat_periodictask_changelist"),
        #         },
        #         {
        #             "title": _("Eventos naturais"),
        #             "icon": "event",
        #             "link": reverse_lazy("admin:django_celery_beat_solarschedule_changelist"),
        #         },
        #     ],
        # },
        {
            "page": "users",
            "models": ["auth.user", "core.userprofile", "account.emailaddress"],
            "items": [
                {
                    "title": _("Usuários"),
                    "icon": "person",
                    "link": reverse_lazy("admin:auth_user_changelist"),
                },
                {
                    "title": _("Perfil Usuários"),
                    "icon": "profile",
                    "link": reverse_lazy("admin:core_userprofile_changelist"),
                },
                {
                    "title": _("Endereços E-mail"),
                    "icon": "email",
                    "link": reverse_lazy("admin:account_emailaddress_changelist"),
                },
            ],
        },
    ],
    "SIDEBAR": {
        "show_search": True,
        "show_all_applications": True,
        "navigation": [
            {
                "title": _("Resumo"),
                "items": [
                    {
                        "title": _("Dashboard"),
                        "icon": "dashboard",
                        "link": reverse_lazy("admin:index"),
                    },
                ],
            },
            {
                "title": _("Sistema"),
                "collapsible": True,
                "items": [
                    {
                        "title": _("Usuário"),
                        "icon": "person",
                        "link": reverse_lazy("admin:auth_user_changelist"),
                    },
                    {
                        "title": _("Grupo (permissões)"),
                        "icon": "group",
                        "link": reverse_lazy("admin:auth_group_changelist"),
                    },
                    {
                        "title": _("Constance"),
                        "icon": "settings",
                        "link": reverse_lazy("admin:constance_config_changelist"),
                    },
                ],
            },
            {
                "title": _("Celery Tasks"),
                "collapsible": True,
                "items": [
                    {
                        "title": _("Clocked"),
                        "icon": "hourglass_bottom",
                        "link": reverse_lazy("admin:django_celery_beat_clockedschedule_changelist"),
                    },
                    {
                        "title": _("Crontabs"),
                        "icon": "update",
                        "link": reverse_lazy("admin:django_celery_beat_crontabschedule_changelist"),
                    },
                    {
                        "title": _("Intervals"),
                        "icon": "timer",
                        "link": reverse_lazy("admin:django_celery_beat_intervalschedule_changelist"),
                    },
                    {
                        "title": _("Periodic tasks"),
                        "icon": "task",
                        "link": reverse_lazy("admin:django_celery_beat_periodictask_changelist"),
                    },
                    {
                        "title": _("Solar events"),
                        "icon": "event",
                        "link": reverse_lazy("admin:django_celery_beat_solarschedule_changelist"),
                    },
                ],
            },
        ],
    },
}

UNFOLD_STUDIO_DEFAULT_FRAGMENT = "color-schemes"

UNFOLD_STUDIO_ENABLE_SAVE = False

UNFOLD_STUDIO_ENABLE_FILEUPLOAD = False

UNFOLD_STUDIO_ALWAYS_OPEN = True

UNFOLD_STUDIO_ENABLE_RESET_PASSWORD = True
