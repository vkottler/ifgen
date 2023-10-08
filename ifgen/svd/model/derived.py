"""
A module implementing a class mixin for SVD element types with a derivedFrom
attribute.
"""

# built-in
from typing import Iterable, Iterator, Optional, TypeVar
from xml.etree import ElementTree

# third-party
from vcorelib.logging import LoggerType

# internal
from ifgen.svd.string import StringKeyValueMixin

T = TypeVar("T", bound="DerivedMixin")
DEFAULT_ALTERNATE = "alternateRegister"


class DerivedMixin(StringKeyValueMixin):
    """A class mixin for instances with a derived attribute."""

    @property
    def derived_elem(self: T) -> T:
        """Get the derived element."""

        result = getattr(self, "derived_from", None)
        if result is None:
            result = self
        return result

    @property
    def name(self) -> str:
        """Get the name of this peripheral."""
        return self.raw_data["name"]

    @property
    def derived(self) -> bool:
        """Whether or not this peripheral is derived from another."""
        return getattr(self, "derived_from", None) is not None

    @property
    def alternates(self: T) -> list[T]:
        """Get alternates of this instance."""

        if not hasattr(self, "_alternates"):
            self._alternates: list[T] = []
        return self._alternates

    def is_alternate(self, key: str = DEFAULT_ALTERNATE) -> bool:
        """Determine if this instance is an alternate of another."""
        return isinstance(self.alternate(key=key), str)

    def alternate(self, key: str = DEFAULT_ALTERNATE) -> Optional[str]:
        """Get a possible alternate for this instance."""
        return self.raw_data.get(key)

    def log(
        self, elem: ElementTree.Element, logger: Optional[LoggerType]
    ) -> None:
        """Log information from this instance's raw data."""

        super().log(elem, logger)

        if logger is not None and self.derived:
            logger.info(
                "'%s' derived from '%s'.",
                self.name,
                self.derived_elem.name,
            )


def derived_from_stack(
    elements: Iterable[ElementTree.Element],
) -> Iterator[ElementTree.Element]:
    """Organize elements that are derived after ones that aren't."""

    elem_stack = []

    for elem in elements:
        # Handle derived peripherals last.
        derived = elem.attrib.get("derivedFrom")
        if derived is not None:
            elem_stack.append(elem)
        else:
            elem_stack.insert(0, elem)

    while elem_stack:
        yield elem_stack.pop(0)
