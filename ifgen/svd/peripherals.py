"""
A module implementing a 'peripherals' SVD-element processor.
"""

# built-in
from xml.etree import ElementTree

# third-party
from vcorelib.logging import LoggerType

# internal
from ifgen.svd.task import SvdProcessingTask


def process_peripherals(
    elem: ElementTree.Element, task: SvdProcessingTask, logger: LoggerType
) -> None:
    """Process a SVD peripherals element."""

    # iterate over peripherals and register individual periphs
    print(elem)
    del task
    del logger
