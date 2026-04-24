"""
A module implementing a configuration interface for the package.
"""

# built-in
import re
from typing import Iterator

# third-party
from vcorelib.dict import merge, GenericStrDict
from vcorelib.dict.codec import BasicDictCodec as _BasicDictCodec
from vcorelib.io import ARBITER as _ARBITER
from vcorelib.io import DEFAULT_INCLUDES_KEY
from vcorelib.io.types import JsonObject as _JsonObject
from vcorelib.paths import Pathlike, find_file

# internal
from ifgen import PKG_NAME
from ifgen.schemas import IfgenDictCodec
from ifgen.enums import Generator


def check_patterns(method: str, name: str, *patterns: str) -> bool:
    """
    Determine if a regular expression method matches any pattern against name.
    """

    matched = False

    for pattern in patterns:
        if getattr(re, method)(pattern, name) is not None:
            matched = True
            break

    return matched


class Config(IfgenDictCodec, _BasicDictCodec):
    """The top-level configuration object for the package."""

    def init(self, data: _JsonObject) -> None:
        """Initialize this instance."""

        super().init(data)

        common = ["identifier", "unit_test"]

        # Load name-matching data.
        self.names: dict[str, list[str]] = data.get(  # type: ignore
            "names", {}
        )
        self.names.setdefault("search", [".*"])

        # Forward enum settings.
        enum_forwards = common + ["use_map"]
        enum: GenericStrDict
        for enum in data.get("enums", {}).values():  # type: ignore
            for forward in enum_forwards:
                enum.setdefault(
                    forward,
                    data["enum"][forward],  # type: ignore
                )

        # Forward struct settings.
        struct_forwards = common + [
            "codec",
            "stream",
            "methods",
            "default_endianness",
            "packed",
        ]
        struct: GenericStrDict
        for struct in data.get("structs", {}).values():  # type: ignore
            for forward in struct_forwards:
                struct.setdefault(
                    forward,
                    data["struct"][forward],  # type: ignore
                )

    def check_name(self, name: str) -> bool:
        """Determine if a provided name is included via search patterns."""

        result = False

        for method, patterns in self.names.items():
            if check_patterns(method, name, *patterns):
                result = True
                break

        return result

    def generator_tasks(
        self, generator: Generator
    ) -> Iterator[tuple[str, GenericStrDict]]:
        """Handle configured exclusions."""

        for name, data in self.data.get(generator.value, {}).items():
            if generator.always() or self.check_name(name):
                yield name, data


def load(path: Pathlike) -> Config:
    """Load a configuration object."""

    src_config = find_file("default.yaml", package=PKG_NAME)
    assert src_config is not None

    data = merge(
        _ARBITER.decode(
            src_config,
            includes_key=DEFAULT_INCLUDES_KEY,
            require_success=True,
        ).data,
        _ARBITER.decode(
            path, includes_key=DEFAULT_INCLUDES_KEY, require_success=True
        ).data,
        # Always allow the project-specific configuration to override package
        # data.
        expect_overwrite=True,
    )

    return Config.create(data)
