# core/settings/logging.py
"""Logging configuration for the Django project.

This module defines the logging settings used across the project. It centralizes
the logging configuration to ensure consistency and reusability.
"""

import os
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent.parent.parent.parent

# Logging (can be customized in derived settings files)
LOG_DIR = Path(os.getenv("LOG_DIR", str(ROOT_DIR / "logs")))
LOG_DIR.mkdir(parents=True, exist_ok=True)

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "verbose": {
            "format": "{asctime} | {levelname} | {name} | {message}",
            "style": "{",
        },
        "simple": {
            "format": "{levelname} | {message}",
            "style": "{",
        },
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "level": "DEBUG",  # Log all levels to the console
            "formatter": "verbose",
        },
        "file": {
            "class": "logging.FileHandler",
            "level": "DEBUG",  # Log all levels to the debug.log file
            "filename": LOG_DIR / "debug.log",
            "formatter": "verbose",
        },
    },
    "loggers": {
        "core": {  # Ensure core logs all levels
            "handlers": ["console", "file"],
            "level": "DEBUG",
            "propagate": False,
        },
        "import_export": {
            "handlers": ["console"],
            "level": "INFO",
        },
        "django.request": {
            "handlers": ["file"],
            "level": "ERROR",
            "propagate": True,
        },
        # "django.db.backends": {
        #     "level": "DEBUG",
        #     "handlers": ["console"],
        # },
    },
    "root": {
        "handlers": ["console", "file"],
        "level": "WARNING",
    },
}
