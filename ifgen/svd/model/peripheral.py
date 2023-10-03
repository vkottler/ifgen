"""
A module implementing a data model for ARM CMSIS-SVD 'peripheral' data.
"""

# built-in
from dataclasses import dataclass
from typing import Iterable, List, Optional, Tuple
from xml.etree import ElementTree

# internal
from ifgen.svd.model.address_block import AddressBlock
from ifgen.svd.model.cluster import ClusterMap, get_clusters
from ifgen.svd.model.derived import DerivedMixin
from ifgen.svd.model.device import ARRAY_PROPERTIES, REGISTER_PROPERTIES
from ifgen.svd.model.interrupt import Interrupt
from ifgen.svd.model.register import RegisterMap, get_registers
from ifgen.svd.string import StringKeyVal

RegisterData = Tuple[ClusterMap, RegisterMap]


@dataclass
class Peripheral(DerivedMixin):
    """A container for peripheral information."""

    derived_from: Optional["Peripheral"]
    interrupts: List[Interrupt]
    address_blocks: List[AddressBlock]
    registers: List[RegisterData]

    def handle_registers(self, registers: ElementTree.Element) -> None:
        """Handle the 'registers' element."""

        self.registers.append(
            (get_clusters(registers), get_registers(registers))
        )

    def handle_address_block(self, address_block: ElementTree.Element) -> None:
        """Handle an 'address_block' element."""
        self.address_blocks.append(AddressBlock.create(address_block))

    def handle_interrupt(self, interrupt: ElementTree.Element) -> None:
        """Handle an 'interrupt' element."""
        self.interrupts.append(Interrupt.create(interrupt))

    @classmethod
    def string_keys(cls) -> Iterable[StringKeyVal]:
        """Get string keys for this instance type."""

        return (
            ARRAY_PROPERTIES
            + [
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
            ]
            + REGISTER_PROPERTIES
        )
