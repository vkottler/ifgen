"""
A module implementing a data model for ARM CMSIS-SVD 'peripheral' data.
"""

# built-in
from dataclasses import dataclass
from typing import Iterable, List, Optional
from xml.etree import ElementTree

# third-party
from vcorelib.logging import LoggerType

# internal
from ifgen.svd.model.interrupt import Interrupt
from ifgen.svd.string import StringKeyVal, StringKeyValueMixin


@dataclass
class Peripheral(StringKeyValueMixin):
    """A container for peripheral information."""

    derived_from: Optional["Peripheral"]
    interrupts: List[Interrupt]

    def handle_registers(self, registers: ElementTree.Element) -> None:
        """Handle the 'registers' element."""

        print(registers)

    def handle_address_block(self, address_block: ElementTree.Element) -> None:
        """Handle an 'address_block' element."""

        print(address_block)

    def handle_interrupt(self, interrupt: ElementTree.Element) -> None:
        """Handle an 'interrupt' element."""
        self.interrupts.append(Interrupt.create(interrupt))

    @property
    def derived(self) -> bool:
        """Whether or not this peripheral is derived from another."""
        return self.derived_from is not None

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

    def log(
        self, elem: ElementTree.Element, logger: Optional[LoggerType]
    ) -> None:
        """Log information from this instance's raw data."""

        super().log(elem, logger)

        if logger is not None and self.derived:
            assert self.derived_from is not None
            logger.info(
                "Peripheral '%s' derived from '%s'.",
                self.name,
                self.derived_from.name,
            )
