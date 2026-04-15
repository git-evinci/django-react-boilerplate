# core/signals.py
"""Custom JSON encoder module with pretty-printing and sorted keys."""

import json
from typing import Any


class PrettyJSONEncoder(json.JSONEncoder):
    """Custom JSON encoder with pretty-printing and sorted keys."""

    def __init__(
        self,
        *args,  # noqa: ANN002
        indent: int = 4,
        sort_keys: bool = True,
        **kwargs: Any,
    ) -> None:
        """Initialize the PrettyJSONEncoder.

        Args:
        ----
            *args: Positional arguments passed to the superclass.
            indent (int): Indentation level for pretty-printing.
            sort_keys (bool): Whether to sort keys alphabetically.
            **kwargs: Additional keyword arguments.

        """
        super().__init__(*args, indent=indent, sort_keys=sort_keys, **kwargs)
