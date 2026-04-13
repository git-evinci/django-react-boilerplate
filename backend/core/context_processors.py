"""Custom context processors for the Core project."""

from django.conf import settings
from django.http import HttpRequest


def variables(request: HttpRequest) -> dict[str, str]:  # noqa: ARG001
    """Expose Plausible Analytics domain to templates."""
    return {"plausible_domain": settings.PLAUSIBLE_DOMAIN}  # type: ignore[misc]


def languages(request: HttpRequest) -> dict[str, object]:  # noqa: ARG001
    """Expose language settings and BIDI flag to templates."""
    return {
        "LANGUAGES": settings.LANGUAGES,  # type: ignore[misc]
        "LANGUAGE_CODE": settings.LANGUAGE_CODE,  # type: ignore[misc]
        "LANGUAGE_BIDI": settings.LANGUAGE_CODE.split("-")[1].lower()  # type: ignore[misc]
        in {
            "ar",
            "he",
            "fa",
            "ur",
        },  # RTL (bidirectional) languages #type: ignore[misc]
    }
