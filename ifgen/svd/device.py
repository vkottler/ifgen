"""
A module implementing a 'device' SVD-element processor.
"""

# built-in
from xml.etree import ElementTree

# third-party
from vcorelib.logging import LoggerType

# internal
from ifgen.svd.model.device import Device
from ifgen.svd.task import SvdProcessingTask


def process_device(
    elem: ElementTree.Element, task: SvdProcessingTask, logger: LoggerType
) -> None:
    """Process a SVD device element."""

    # Assign the device.
    dev = Device.create(elem)
    dev.log(elem, logger)
    task.model.assign_device(dev)

    # Process the CPU metadata.
    cpu = elem.find("cpu")
    if cpu is not None:
        task.process(cpu)

    # Process peripherals.
    peripherals = elem.find("peripherals")
    if peripherals is not None:
        task.process(peripherals)
