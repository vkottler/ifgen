"""
A module implementing a data model for ARM CMSIS-SVD 'peripheral' data.
"""

# built-in
from dataclasses import dataclass
from typing import Iterable, Optional

# internal
from ifgen.svd.string import StringKeyVal, StringKeyValueMixin


@dataclass
class Peripheral(StringKeyValueMixin):
    """A container for cpu information."""

    derived_from: Optional["Peripheral"]

    @property
    def name(self) -> str:
        """Get the name of this peripheral."""
        return self.raw_data["name"]

    @classmethod
    def string_keys(cls) -> Iterable[StringKeyVal]:
        """Get string keys for this instance type."""

        return [
            StringKeyVal("dim", False),
            StringKeyVal("dimIncrement", False),
            StringKeyVal("dimIndex", False),
            StringKeyVal("dimName", False),
            # This is an object.
            # StringKeyVal("dimArrayIndex", False),
            StringKeyVal("name", True),
            StringKeyVal("version", False),
            StringKeyVal("description", False),
            StringKeyVal("alternatePeripheral", False),
            StringKeyVal("groupName", False),
            StringKeyVal("prependToName", False),
            StringKeyVal("appendToName", False),
            StringKeyVal("headerStructName", False),
            StringKeyVal("disableCondition", False),
            StringKeyVal("baseAddress", True),
            # https://www.keil.com/pack/doc/CMSIS/SVD/html/
            #    elem_special.html#registerPropertiesGroup_gr
            StringKeyVal("size", False),
            StringKeyVal("access", False),
            StringKeyVal("protection", False),
            StringKeyVal("resetValue", False),
            StringKeyVal("resetMask", False),
        ]
