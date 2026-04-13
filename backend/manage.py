#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys


def main() -> None:
    """Run administrative tasks."""
    # Supported environments
    valid_environments = ["development", "production", "test"]

    # Determine the environment (default to development)
    environment = os.getenv("DJANGO_ENV", "development")

    if environment not in valid_environments:
        msg = (
            f"Invalid DJANGO_ENV: '{environment}'. Must be one of {valid_environments}."
        )
        raise ValueError(msg)

    # Set the settings module dynamically
    settings_module = f"core.settings.{environment}"

    os.environ.setdefault("DJANGO_SETTINGS_MODULE", settings_module)

    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)


if __name__ == "__main__":
    main()
