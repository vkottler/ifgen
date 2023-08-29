"""
A module implementing a generation-environment interface.
"""

# built-in
from enum import StrEnum
from pathlib import Path
from typing import Any

# third-party
from runtimepy.codec.system import TypeSystem
from vcorelib.logging import LoggerMixin
from vcorelib.paths import normalize, rel

# internal
from ifgen.config import Config
from ifgen.paths import combine_if_not_absolute


class Generator(StrEnum):
    """An enumeration declaring all valid kinds of generators."""

    STRUCTS = "structs"
    ENUMS = "enums"


def runtime_enum_data(data: dict[str, Any]) -> dict[str, int]:
    """Get runtime enumeration data."""

    result = {}

    curr_value = 0

    for key, value in data.items():
        if value is None or "value" not in value:
            result[key] = curr_value
            curr_value += 1
        else:
            result[key] = value["value"]
            if value["value"] >= curr_value:
                curr_value = value["value"] + 1

    return result


def type_string(data: str) -> str:
    """Handle some type name conversions."""

    return data.replace("_t", "")


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

        self.types = TypeSystem(*self.config.data["namespace"])
        self._register_enums()
        self._register_structs()

    def _register_enums(self) -> None:
        """Register configuration enums."""

        for name, enum in self.config.data.get("enums", {}).items():
            self.types.enum(
                name,
                runtime_enum_data(enum["enum"]),
                *enum["namespace"],
                primitive=type_string(enum["underlying"]),
            )

            self.logger.info(
                "Registered enum '%s'.",
                self.types.root_namespace.delim.join(
                    enum["namespace"] + [name]
                ),
            )

    def _register_structs(self) -> None:
        """Register configuration structs."""

        for name, struct in self.config.data.get("structs", {}).items():
            self.types.register(name, *struct["namespace"])
            for field in struct["fields"]:
                self.types.add(name, field["name"], type_string(field["type"]))

            self.logger.info(
                "Registered struct '%s' (%d bytes).",
                self.types.root_namespace.delim.join(
                    struct["namespace"] + [name]
                ),
                self.types.size(name, *struct["namespace"]),
            )

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
