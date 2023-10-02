"""
A module implementing a 'device' SVD-element processor.
"""

# built-in
from xml.etree import ElementTree

# third-party
from vcorelib.logging import LoggerType

# internal
from ifgen.svd.model import Device
from ifgen.svd.task import SvdProcessingTask


def process_device(
    elem: ElementTree.Element, task: SvdProcessingTask, logger: LoggerType
) -> None:
    """Process a SVD device element."""

    # Assign the device.
    assert task.device is None, task.device
    task.device = Device.create(elem)
    task.device.log(elem, logger)

    # Process the CPU metadata.
    cpu = elem.find("cpu")
    if cpu is not None:
        task.process(cpu)
