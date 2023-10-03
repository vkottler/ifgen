"""
A module implementing an SVD-processing task interface.
"""

# built-in
from dataclasses import dataclass
from logging import getLogger
from pathlib import Path
from typing import Callable, Dict
from xml.etree import ElementTree

# third-party
from vcorelib.io import ARBITER
from vcorelib.logging import LoggerType

# internal
from ifgen.svd.model import SvdModel

TagProcessor = Callable[
    [ElementTree.Element, "SvdProcessingTask", LoggerType], None
]
TagProcessorMap = Dict[str, TagProcessor]
TAG_PROCESSORS: TagProcessorMap = {}


@dataclass
class SvdProcessingTask:
    """A container for SVD-processing state."""

    model: SvdModel

    def process(self, elem: ElementTree.Element) -> None:
        """Process a single element."""
        TAG_PROCESSORS[elem.tag](elem, self, getLogger(elem.tag))

    @staticmethod
    def svd(path: Path) -> "SvdProcessingTask":
        """Process a single SVD file."""

        task = SvdProcessingTask(SvdModel({}))
        task.process(ElementTree.parse(path).getroot())
        return task

    def generate_configs(self, path: Path) -> None:
        """Generate output configuration files."""

        path.mkdir(exist_ok=True, parents=True)

        # Write metadata that doesn't currently get used for generation.
        ARBITER.encode(path.joinpath("metadata.json"), self.model.metadata())

        # generate outputs
