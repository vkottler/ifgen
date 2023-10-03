"""
A module implementing a data model for ARM CMSIS-SVD 'addressBlock' data.
"""

# built-in
from dataclasses import dataclass
from typing import Iterable

# internal
from ifgen.svd.string import StringKeyVal, StringKeyValueMixin


@dataclass
class AddressBlock(StringKeyValueMixin):
    """A container for address-block information."""

    @classmethod
    def string_keys(cls) -> Iterable[StringKeyVal]:
        """Get string keys for this instance type."""

        return [
            StringKeyVal("offset", True),
            StringKeyVal("size", True),
            StringKeyVal("usage", True),  # registers, buffer, reserved
            StringKeyVal("protection", False),
        ]
