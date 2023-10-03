"""
A module implementing a data model for ARM CMSIS-SVD 'cpu' data.
"""

# built-in
from dataclasses import dataclass
from typing import Iterable

# internal
from ifgen.svd.string import StringKeyVal, StringKeyValueMixin


@dataclass
class Cpu(StringKeyValueMixin):
    """A container for cpu information."""

    @classmethod
    def string_keys(cls) -> Iterable[StringKeyVal]:
        """Get string keys for this instance type."""

        # https://www.keil.com/pack/doc/CMSIS/SVD/html/elem_cpu.html
        return [
            StringKeyVal("name", True),
            StringKeyVal("revision", True),
            StringKeyVal("endian", True),
            StringKeyVal("mpuPresent", True),
            StringKeyVal("fpuPresent", True),
            StringKeyVal("fpuDP", False),
            StringKeyVal("dspPresent", False),
            StringKeyVal("icachePresent", False),
            StringKeyVal("dcachePresent", False),
            StringKeyVal("itcmPresent", False),
            StringKeyVal("dtcmPresent", False),
            StringKeyVal("vtorPresent", False),
            StringKeyVal("nvicPrioBits", True),
            StringKeyVal("vendorSystickConfig", True),
            StringKeyVal("deviceNumInterrupts", False),
            StringKeyVal("sauNumRegions", False),
            # This is an object (not currently implemented).
            # StringKeyVal("sauRegionsConfig", False),
        ]
