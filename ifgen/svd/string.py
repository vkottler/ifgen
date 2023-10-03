"""
A module implementing interfaces for string-data elements.
"""

# built-in
from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Iterable, Optional
from xml.etree import ElementTree

# third-party
from vcorelib.logging import LoggerType


@dataclass
class StringKeyVal:
    """Name of key and whether or not it's required."""

    key: str
    required: bool = True


class StringKeyValueMixin(ABC):
    """A mixin for SVD data model classes."""

    _raw: dict[str, str]

    @classmethod
    @abstractmethod
    def string_keys(cls) -> Iterable[StringKeyVal]:
        """Get string keys for this instance type."""

    def raw(self, elem: ElementTree.Element) -> dict[str, str]:
        """Get raw data for this instance based on string keys."""

        result = getattr(self, "_raw", None)
        if result is None:
            self._raw = self.get_values(elem)
            result = self._raw

        assert result is not None
        return result

    def log(
        self, elem: ElementTree.Element, logger: Optional[LoggerType]
    ) -> None:
        """Log information from this instance's raw data."""

        if logger is not None:
            for key, value in self.raw(elem).items():
                for line in value.splitlines():
                    line = line.strip().replace("\\n", "")
                    if line:
                        logger.info("%s: %s", key, line)

    @classmethod
    def get_values(cls, elem: ElementTree.Element) -> dict[str, str]:
        """Get string values for this instance."""

        return get_string_values(elem, cls.string_keys())


def get_string_values(
    elem: ElementTree.Element, keys: Iterable[StringKeyVal]
) -> dict[str, str]:
    """Get string values from an element's children."""

    result = {}

    for item in keys:
        key = item.key
        required = item.required

        new_elem = elem.find(key)
        assert (
            new_elem is not None or not required
        ), f"'{key}' required but not found!"
        if new_elem is not None:
            result[key] = new_elem.text or ""

    return result
