"""
A module implementing a data model for ARM CMSIS-SVD 'field' data.
"""

# built-in
from dataclasses import dataclass
from typing import Iterable, Optional
from xml.etree import ElementTree

# internal
from ifgen.svd.model.derived import DerivedMixin, derived_from_stack
from ifgen.svd.model.device import ARRAY_PROPERTIES
from ifgen.svd.model.enum import EnumeratedValues, get_enum
from ifgen.svd.string import StringKeyVal


@dataclass
class Field(DerivedMixin):
    """A container for field information."""

    derived_from: Optional["Field"]
    enum: Optional[EnumeratedValues]

    @property
    def access(self) -> str:
        """Get this instance's access property."""
        return self.raw_data["access"]

    @classmethod
    def string_keys(cls) -> Iterable[StringKeyVal]:
        """Get string keys for this instance type."""

        # Not currently handling nested registers or clusters.

        return ARRAY_PROPERTIES + [
            StringKeyVal("name", True),
            StringKeyVal("description", False),
            # Mutually exclusive options:
            # 1 (bitRangeLsbMsbStyle)
            StringKeyVal("bitOffset", False),
            StringKeyVal("bitWidth", False),
            # 2 (bitRangeOffsetWidthStyle)
            StringKeyVal("lsb", False),
            StringKeyVal("msb", False),
            # 3 (bitRangePattern)
            StringKeyVal("bitRange", False),
            # (end mutually exclusive options)
            # is enum
            StringKeyVal("access", False),
            StringKeyVal("modifiedWriteValues", False),
            # is enum
            StringKeyVal("readAction", False),
        ]


FieldMap = dict[str, Field]


def get_fields(registers: ElementTree.Element) -> FieldMap:
    """Get register fields."""

    result: FieldMap = {}
    for field in derived_from_stack(registers.iterfind("field")):
        derived_field = None
        derived = field.attrib.get("derivedFrom")
        if derived is not None:
            derived_field = result[derived]  # pragma: nocover

        # Handle writeConstraint at some point?

        # Handle enumerated values.
        enum = None
        enum_elem = field.find("enumeratedValues")
        if enum_elem is not None:
            enum = get_enum(enum_elem)

        inst = Field.create(field, derived_field, enum)
        result[inst.name] = inst

    return result
