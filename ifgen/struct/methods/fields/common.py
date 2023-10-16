"""
Common utilities for generating bit-field related struct methods.
"""

# built-in
from typing import Any, Optional

BitField = dict[str, Any]


def bit_mask_literal(width: int) -> str:
    """Get a bit-mask literal."""
    return "0b" + ("1" * width) + "u"


def possible_array_arg(parent: dict[str, Any]) -> str:
    """Determine if a method needs an array-index argument."""

    array_length: Optional[int] = parent.get("array_length")
    inner = ""
    if array_length:
        inner = "std::size_t index"

    return inner
