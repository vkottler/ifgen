"""
A module implementing an SVD-processing task interface.
"""

# built-in
from dataclasses import dataclass
from logging import getLogger
from pathlib import Path
from typing import Callable, Dict, Optional
from xml.etree import ElementTree

# third-party
from vcorelib.logging import LoggerType

# internal
from ifgen.svd.model import Device
from ifgen.svd.model.cpu import Cpu

TagProcessor = Callable[
    [ElementTree.Element, "SvdProcessingTask", LoggerType], None
]
TagProcessorMap = Dict[str, TagProcessor]
TAG_PROCESSORS: TagProcessorMap = {}


@dataclass
class SvdProcessingTask:
    """A container for SVD-processing state."""

    device: Optional[Device] = None
    cpu: Optional[Cpu] = None

    def process(self, elem: ElementTree.Element) -> None:
        """Process a single element."""
        TAG_PROCESSORS[elem.tag](elem, self, getLogger(elem.tag))

    @staticmethod
    def svd(path: Path) -> "SvdProcessingTask":
        """Process a single SVD file."""

        task = SvdProcessingTask()
        task.process(ElementTree.parse(path).getroot())
        return task
