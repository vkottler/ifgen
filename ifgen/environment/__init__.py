"""
A module implementing a generation-environment interface.
"""

# built-in
from enum import StrEnum
from pathlib import Path

# third-party
from vcorelib.logging import LoggerMixin
from vcorelib.paths import normalize

# internal
from ifgen.config import Config
from ifgen.paths import combine_if_not_absolute


class Generator(StrEnum):
    """An enumeration declaring all valid kinds of generators."""

    STRUCTS = "structs"
    ENUMS = "enums"


class IfgenEnvironment(LoggerMixin):
    """A class for managing stateful information while generating outputs."""

    def __init__(self, root: Path, config: Config) -> None:
        """Initialize this instance."""

        super().__init__()
        self.root = root
        self.config = config

        self.output = combine_if_not_absolute(
            self.root, normalize(*self.config.data["output_dir"])
        )

        # Create output directories.
        for subdir in Generator:
            self.output.joinpath(subdir).mkdir(parents=True, exist_ok=True)

    def make_path(
        self, name: str, generator: Generator, from_output: bool = False
    ) -> Path:
        """Make part of a task's path."""

        result = Path(str(generator), f"{name}.h")

        if from_output:
            result = self.output.joinpath(result)

        return result
