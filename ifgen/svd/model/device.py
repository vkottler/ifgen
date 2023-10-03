"""
A module implementing a data model for ARM CMSIS-SVD 'device' data.
"""

# built-in
from dataclasses import dataclass
from typing import Iterable

# internal
from ifgen.svd.string import StringKeyVal, StringKeyValueMixin

# https://www.keil.com/pack/doc/CMSIS/SVD/html/
#     elem_special.html#registerPropertiesGroup_gr
REGISTER_PROPERTIES = [
    StringKeyVal("size", False),
    StringKeyVal("access", False),
    StringKeyVal("protection", False),
    StringKeyVal("resetValue", False),
    StringKeyVal("resetMask", False),
]
ARRAY_PROPERTIES = [
    StringKeyVal("dim", False),
    StringKeyVal("dimIncrement", False),
    StringKeyVal("dimIndex", False),
    StringKeyVal("dimName", False),
    # This is an object.
    # StringKeyVal("dimArrayIndex", False),
]


@dataclass
class Device(StringKeyValueMixin):
    """A container for device information."""

    @classmethod
    def string_keys(cls) -> Iterable[StringKeyVal]:
        """Get string keys for this instance type."""

        # https://www.keil.com/pack/doc/CMSIS/SVD/html/elem_device.html
        return [
            StringKeyVal("vendor", False),
            StringKeyVal("vendorID", False),
            StringKeyVal("name", True),
            StringKeyVal("series", False),
            StringKeyVal("version", True),
            StringKeyVal("description", True),
            StringKeyVal("licenseText", False),
            StringKeyVal("headerSystemFilename", False),
            StringKeyVal("headerDefinitionsPrefix", False),
            StringKeyVal("addressUnitBits", True),
            StringKeyVal("width", True),
        ] + REGISTER_PROPERTIES
