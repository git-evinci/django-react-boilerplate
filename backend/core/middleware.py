# core/middleware.py
"""Middleware for handling readonly database exceptions."""

from collections.abc import Callable

from django.contrib import messages
from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _


class ReadonlyExceptionHandlerMiddleware:
    """Middleware to catch and handle ReadonlyException gracefully."""

    def __init__(self, get_response: Callable[[HttpRequest], HttpResponse]) -> None:
        """Initialize middleware.

        Args:
            get_response: A callable that takes an HttpRequest and returns an HttpResponse.

        """
        self.get_response = get_response

    def __call__(self, request: HttpRequest) -> HttpResponse:
        """Process the request and return the response.

        Args:
            request: The HTTP request.

        Returns:
            The HTTP response from the next middleware or view.

        """
        return self.get_response(request)

    def process_exception(
        self, request: HttpRequest, exception: Exception
    ) -> HttpResponse | None:
        """Handle specific exceptions like ReadonlyException.

        Args:
            request: The HTTP request.
            exception: The exception raised during processing.

        Returns:
            An HTTP redirect response or None if not handled.

        """
        if (
            exception
            and repr(exception)
            == "ReadonlyException('Database is operating in readonly mode. Not possible to save any data.')"
        ):
            messages.warning(
                request,
                _(
                    "Database is operating in readonly mode. Not possible to save any data."
                ),
            )
            return redirect(
                request.META.get("HTTP_REFERER", reverse_lazy("admin:login"))
            )

        return None
