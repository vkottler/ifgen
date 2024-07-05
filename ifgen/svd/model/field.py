"""
A module implementing a data model for ARM CMSIS-SVD 'field' data.
"""

# built-in
from dataclasses import dataclass
from functools import cached_property
from typing import Any, Iterable, Optional
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

    def __eq__(self, other) -> bool:
        """Determine if two fields are equivalent."""

        result = False

        if isinstance(other, Field):
            our_data = self.ifgen_data
            their_data = other.ifgen_data

            result = (
                our_data["index"] == their_data["index"]
                and our_data["width"] == their_data["width"]
                and our_data["read"] == their_data["read"]
                and our_data["write"] == their_data["write"]
            )

        return result

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

    @cached_property
    def ifgen_data(self) -> dict[str, Any]:
        """Populate bit-field data."""

        output: dict[str, Any] = {}

        self.handle_description(output)

        # We don't currently handle arrays of bit-fields.
        assert "dim" not in self.raw_data

        lsb = -1
        msb = -1
        if "bitRange" in self.raw_data:
            msb_str, lsb_str = self.raw_data["bitRange"].split(":")
            lsb = int(lsb_str.replace("]", ""))
            msb = int(msb_str.replace("[", ""))
        elif "lsb" in self.raw_data:
            lsb = int(self.raw_data["lsb"])
            msb = int(self.raw_data["msb"])
        elif "bitOffset" in self.raw_data:
            lsb = int(self.raw_data["bitOffset"])
            msb = lsb + (int(self.raw_data["bitWidth"]) - 1)

        assert lsb != -1 and msb != -1, self.raw_data

        output["index"] = lsb

        width = (msb - lsb) + 1
        assert width >= 1, (msb, lsb, self.name)
        output["width"] = width

        output["read"] = "read" in self.access
        output["write"] = "write" in self.access

        return output


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
