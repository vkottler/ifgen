"""
A module implementing a struct-padding manager.
"""

# built-in
from typing import Any, Iterator

StructField = dict[str, Any]


def type_string(data: str) -> str:
    """Handle some type name conversions."""

    if "int" in data:
        data = data.replace("_t", "")
    return data


class PaddingManager:
    """A class implementing basic padding management."""

    base_name = "reserved_padding"

    def __init__(self) -> None:
        """Initialize this instance."""
        self.reset()

    def _new_field(self) -> StructField:
        """Create a new padding field."""

        field: StructField = {
            "padding": True,
            "volatile": False,
            "const": True,
            "name": f"{self.base_name}{self.index}",
        }
        self.index += 1

        return field

    def add_padding(self, num_bytes: int) -> Iterator[StructField]:
        """Add padding field(s)."""

        words, single_bytes = divmod(num_bytes, 4)

        for size, kind in (words, "uint32_t"), (single_bytes, "uint8_t"):
            if size > 0:
                field = self._new_field()
                field["type"] = kind

                if size >= 2:
                    field["array_length"] = size

                yield field

    def reset(self) -> None:
        """Reset the padding-element index."""
        self.index = 0
