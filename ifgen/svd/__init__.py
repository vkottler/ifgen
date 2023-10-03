"""
A module implementing interfaces for working with ARM CMSIS-SVD files.
"""

# internal
from ifgen.svd.cpu import process_cpu
from ifgen.svd.device import process_device
from ifgen.svd.peripherals import process_peripheral, process_peripherals
from ifgen.svd.task import TAG_PROCESSORS


def register_processors() -> None:
    """Register tag-processing methods."""

    TAG_PROCESSORS["device"] = process_device
    TAG_PROCESSORS["cpu"] = process_cpu
    TAG_PROCESSORS["peripheral"] = process_peripheral
    TAG_PROCESSORS["peripherals"] = process_peripherals
