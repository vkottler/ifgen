"""
A module implementing a data model for ARM CMSIS-SVD 'interrupt' data.
"""

# built-in
from dataclasses import dataclass
from typing import Iterable

# internal
from ifgen.svd.string import StringKeyVal, StringKeyValueMixin


@dataclass
class Interrupt(StringKeyValueMixin):
    """A container for interrupt information."""

    @classmethod
    def string_keys(cls) -> Iterable[StringKeyVal]:
        """Get string keys for this instance type."""

        return [
            StringKeyVal("name", True),
            StringKeyVal("description", False),
            StringKeyVal("value", True),
        ]
