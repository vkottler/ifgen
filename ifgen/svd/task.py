"""
A module implementing an SVD-processing task interface.
"""

# built-in
from dataclasses import dataclass
from logging import getLogger
from pathlib import Path
from typing import Callable
from xml.etree import ElementTree

# third-party
from vcorelib.io import ARBITER
from vcorelib.logging import LoggerType
from vcorelib.paths import rel

# internal
from ifgen.svd.group import handle_group, peripheral_groups
from ifgen.svd.model import SvdModel

TagProcessor = Callable[
    [ElementTree.Element, "SvdProcessingTask", LoggerType], None
]
TagProcessorMap = dict[str, TagProcessor]
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

        meta = self.model.metadata()

        # Write metadata that doesn't currently get used for generation.
        ARBITER.encode(path.joinpath("metadata.json"), meta)

        includes: set[Path] = set()

        # Organize peripherals into groups based on ones derived from others
        # and process them.
        for group in peripheral_groups(self.model.peripherals).values():
            output_dir = path.joinpath(group.root.base_name())
            output_dir.mkdir(exist_ok=True)
            handle_group(output_dir, group, includes)

        ARBITER.encode(
            path.joinpath("ifgen.yaml"),
            {
                "includes": sorted(  # type: ignore
                    str(rel(x.resolve(), base=path)) for x in includes
                ),
                "namespace": [meta["device"]["name"]],
            },
        )
