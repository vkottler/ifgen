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


class DerivedMixin(StringKeyValueMixin):
    """A class mixin for instances with a derived attribute."""

    @property
    def derived_elem(self: T) -> T:
        """Get the derived element."""
        return getattr(self, "derived_from")  # type: ignore

    @property
    def name(self) -> str:
        """Get the name of this peripheral."""
        return self.raw_data["name"]

    @property
    def derived(self) -> bool:
        """Whether or not this peripheral is derived from another."""
        return getattr(self, "derived_from", None) is not None

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
