"""
A module implementing base interfaces for processing a group of peripherals.
"""

# built-in
from dataclasses import dataclass
from typing import Iterator

# internal
from ifgen.svd.model.peripheral import Peripheral


@dataclass
class PeripheralGroup:
    """A container for peripherals that have the same register layout."""

    root: Peripheral
    derivatives: list[Peripheral]

    @property
    def peripherals(self) -> Iterator[Peripheral]:
        """Get all peripheral instances."""
        yield self.root
        yield from self.derivatives


def peripheral_groups(
    peripherals: dict[str, Peripheral]
) -> dict[str, PeripheralGroup]:
    """Organize peripherals into groups."""

    result: dict[str, PeripheralGroup] = {}

    for name, peripheral in peripherals.items():
        if name not in result and not peripheral.derived:
            # Validate this later.
            result[name] = PeripheralGroup(None, [])  # type: ignore

        if peripheral.derived:
            result[peripheral.derived_elem.name].derivatives.append(peripheral)
        else:
            assert result[name].root is None, result[name].root
            result[name].root = peripheral

    # Validate groups.
    for name, group in result.items():
        assert group.root is not None, (name, group)

    return result
