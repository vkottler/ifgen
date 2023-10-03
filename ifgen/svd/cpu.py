"""
A module implementing a 'cpu' SVD-element processor.
"""

# built-in
from xml.etree import ElementTree

# third-party
from vcorelib.logging import LoggerType

# internal
from ifgen.svd.model.cpu import Cpu
from ifgen.svd.task import SvdProcessingTask


def process_cpu(
    elem: ElementTree.Element, task: SvdProcessingTask, logger: LoggerType
) -> None:
    """Process a SVD cpu element."""

    cpu = Cpu()
    cpu.log(elem, logger)
    task.model.assign_cpu(cpu)
