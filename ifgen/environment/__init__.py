"""
A module implementing a generation-environment interface.
"""

# built-in
from enum import StrEnum
from pathlib import Path

# third-party
from vcorelib.logging import LoggerMixin
from vcorelib.namespace import CPP_DELIM, Namespace
from vcorelib.paths import normalize, rel

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
        self.root_path = root
        self.config = config

        self.source = combine_if_not_absolute(
            self.root_path, normalize(*self.config.data["source_dir"])
        )
        self.output = combine_if_not_absolute(
            self.source, normalize(*self.config.data["output_dir"])
        )
        self.test_dir = combine_if_not_absolute(
            self.source, normalize(*self.config.data["test_dir"])
        )

        # Create output directories.
        for subdir in Generator:
            for path in [self.output, self.test_dir]:
                path.joinpath(subdir).mkdir(parents=True, exist_ok=True)

        global_namespace = Namespace(delim=CPP_DELIM)

        # Register global names.

        self.root_namespace = global_namespace.child(
            *self.config.data["namespace"]
        )

        # Register custom names for each generator.

    def make_path(
        self, name: str, generator: Generator, from_output: bool = False
    ) -> Path:
        """Make part of a task's path."""

        result = Path(str(generator), f"{name}.h")

        if from_output:
            result = self.output.joinpath(result)

        return result

    def rel_include(self, name: str, generator: Generator) -> Path:
        """Get an include path to a generated output."""

        return rel(self.output, base=self.source).joinpath(
            self.make_path(name, generator)
        )

    def make_test_path(self, name: str, generator: Generator) -> Path:
        """Make a path to an interface's unit-test suite."""

        return self.test_dir.joinpath(str(generator), f"test_{name}.cc")
