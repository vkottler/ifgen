"""
A module implementing a data model for ARM CMSIS-SVD 'enumeratedValue' data.
"""

# built-in
from dataclasses import dataclass
from typing import Iterable, Optional
from xml.etree import ElementTree

# internal
from ifgen.svd.model.derived import DerivedMixin
from ifgen.svd.string import StringKeyVal, StringKeyValueMixin


@dataclass
class EnumeratedValue(StringKeyValueMixin):
    """A container for enumerated-value information."""

    @classmethod
    def string_keys(cls) -> Iterable[StringKeyVal]:
        """Get string keys for this instance type."""

        return [
            StringKeyVal("name", False),
            StringKeyVal("description", False),
            # Some kind of parsing needed for this field maybe.
            StringKeyVal("value", False),
            StringKeyVal("isDefault", False),
        ]


EnumValueMap = dict[str, EnumeratedValue]


@dataclass
class EnumeratedValues(DerivedMixin):
    """A container for enum information."""

    derived_from: Optional["EnumeratedValues"]
    enum: EnumValueMap

    @classmethod
    def string_keys(cls) -> Iterable[StringKeyVal]:
        """Get string keys for this instance type."""

        return [
            StringKeyVal("name", False),
            StringKeyVal("headerEnumName", False),
            StringKeyVal("usage", False),
        ]


def get_enum(enumerated_values: ElementTree.Element) -> EnumeratedValues:
    """Get register clusters."""

    # Handle values.
    vals = {}
    for enum in enumerated_values.iterfind("enumeratedValue"):
        val_inst = EnumeratedValue.create(enum)
        vals[val_inst.raw_data["name"]] = val_inst

    # No handling for derived enumerations yet.
    derived = enumerated_values.attrib.get("derivedFrom")
    assert derived is None, derived

    return EnumeratedValues.create(enumerated_values, None, vals)
