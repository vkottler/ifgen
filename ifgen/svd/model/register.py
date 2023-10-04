"""
A module implementing a data model for ARM CMSIS-SVD 'register' data.
"""

# built-in
from dataclasses import dataclass
from typing import Iterable, Optional
from xml.etree import ElementTree

# internal
from ifgen.svd.model.derived import DerivedMixin
from ifgen.svd.model.device import ARRAY_PROPERTIES, REGISTER_PROPERTIES
from ifgen.svd.model.field import FieldMap, get_fields
from ifgen.svd.string import StringKeyVal


@dataclass
class Register(DerivedMixin):
    """A container for register information."""

    derived_from: Optional["Register"]
    fields: Optional[FieldMap]

    @classmethod
    def string_keys(cls) -> Iterable[StringKeyVal]:
        """Get string keys for this instance type."""

        return (
            ARRAY_PROPERTIES
            + [
                StringKeyVal("name", True),
                StringKeyVal("displayName", False),
                StringKeyVal("description", False),
                StringKeyVal("alternateGroup", False),
                StringKeyVal("alternateRegister", False),
                StringKeyVal("addressOffset", True),
            ]
            + REGISTER_PROPERTIES
            + [
                # is enum
                StringKeyVal("dataType", False),
                # is enum
                StringKeyVal("modifiedWriteValues", False),
                # is enum
                StringKeyVal("readAction", False),
            ]
        )


RegisterMap = dict[str, Register]


def register(
    element: ElementTree.Element, register_map: RegisterMap
) -> Register:
    """Create a Register instance from an SVD element."""

    derived_register = None
    derived = element.attrib.get("derivedFrom")
    if derived is not None:
        derived_register = register_map[derived]  # pragma: nocover

    # Handle writeConstraint at some point?

    # Load fields.
    fields = None
    fields_elem = element.find("fields")
    if fields_elem is not None:
        fields = get_fields(fields_elem)

    inst = Register.create(element, derived_register, fields)
    register_map[inst.name] = inst
    return inst
