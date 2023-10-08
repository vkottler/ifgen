"""
A module implementing a generation-environment interface.
"""

# built-in
from enum import StrEnum
from pathlib import Path
from shutil import rmtree
from typing import Any

# third-party
from runtimepy.codec.protocol import Protocol
from runtimepy.codec.system import TypeSystem
from runtimepy.enum import RuntimeEnum
from vcorelib.logging import LoggerMixin
from vcorelib.paths import normalize, rel

# internal
from ifgen import PKG_NAME
from ifgen.config import Config
from ifgen.environment.field import process_field
from ifgen.environment.padding import PaddingManager, type_string
from ifgen.paths import combine_if_not_absolute


class Generator(StrEnum):
    """An enumeration declaring all valid kinds of generators."""

    STRUCTS = "structs"
    ENUMS = "enums"
    IFGEN = PKG_NAME


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

        self.generated: set[Path] = set()

        # Create output directories.
        for subdir in Generator:
            for path in [self.output, self.test_dir]:
                dest = path.joinpath(subdir)
                rmtree(dest, ignore_errors=True)
                dest.mkdir(parents=True, exist_ok=True)

        self.types = TypeSystem(*self.config.data["namespace"])
        self.padding = PaddingManager()
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
            namespace = [*struct["namespace"]]
            self.types.register(name, *namespace)

            field_groups = []

            self.padding.reset()
            for field in struct["fields"]:
                padding = list(
                    process_field(
                        name, self.padding, self.types, field, namespace
                    )
                )
                if padding:
                    field_groups.append(padding)
                field_groups.append([field])

            # Re-assign fields structure.
            struct["fields"] = []
            for group in field_groups:
                for field in group:
                    struct["fields"].append(field)

            self.logger.info(
                "Registered struct '%s' (%d bytes).",
                self.types.root_namespace.delim.join(
                    struct["namespace"] + [name]
                ),
                self.types.size(name, *struct["namespace"]),
            )

    def make_path(
        self,
        name: str,
        generator: Generator,
        from_output: bool = False,
        track: bool = True,
    ) -> Path:
        """Make part of a task's path."""

        result = Path(str(generator), f"{name}.h")

        if from_output:
            result = self.output.joinpath(result)

        if track:
            self.generated.add(result)

        return result

    def rel_include(self, name: str, generator: Generator) -> Path:
        """Get an include path to a generated output."""

        return rel(self.output, base=self.source).joinpath(
            self.make_path(name, generator, track=False)
        )

    def make_test_path(self, name: str, generator: Generator) -> Path:
        """Make a path to an interface's unit-test suite."""

        result = self.test_dir.joinpath(str(generator), f"test_{name}.cc")
        self.generated.add(result)
        return result

    def get_protocol(self, name: str, exact: bool = False) -> Protocol:
        """Get the protocol instance for a given struct."""

        return self.types.get_protocol(
            name, self.config.data["structs"].get("namespace", []), exact=exact
        )

    def is_struct(self, name: str) -> bool:
        """Determine if a field is a struct or not."""

        try:
            self.get_protocol(type_string(name))
            return True
        except KeyError:
            return False

    def size(self, type_name: str, exact: bool = False) -> int:
        """Get the size of a given type."""
        return self.types.size(type_string(type_name), exact=exact)

    def get_enum(self, name: str, exact: bool = False) -> RuntimeEnum:
        """Get a runtime enum instance for a given enumeration."""

        return self.types.get_enum(
            name, *self.config.data["enums"].get("namespace", []), exact=exact
        )

    def is_enum(self, name: str, exact: bool = False) -> bool:
        """Determine if a field is an enumeration or not."""

        try:
            self.get_enum(type_string(name), exact=exact)
            return True
        except KeyError:
            return False
