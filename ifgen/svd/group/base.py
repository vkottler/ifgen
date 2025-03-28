"""
A module implementing base interfaces for processing a group of peripherals.
"""

# built-in
from dataclasses import dataclass
from typing import Iterator, Optional

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


PRUNE_STRUCTS = False


def get_derived(
    peripheral: Peripheral, peripherals: list[Peripheral]
) -> Optional[Peripheral]:
    """Determine if this peripheral is derived from any other peripheral."""

    result = None

    if peripheral.derived:
        result = peripheral.derived_elem

    # Check if this peripheral is equivalent to some other peripheral.
    elif PRUNE_STRUCTS:
        for other in peripherals:
            # Always return None if you get far enough to see yourself in the
            # list. That way this peripheral becomes the effective 'root'.
            if other is peripheral:
                break

            if not other.is_alternate() and not other.derived:
                if other == peripheral:
                    result = other
                    break

    return result


def peripheral_groups(
    peripherals: dict[str, Peripheral],
) -> dict[str, PeripheralGroup]:
    """Organize peripherals into groups."""

    result: dict[str, PeripheralGroup] = {}

    peripherals_list = list(peripherals[x] for x in sorted(peripherals))
    for peripheral in peripherals_list:
        name = peripheral.base_name()

        derived = get_derived(peripheral, peripherals_list)
        if derived is not None:
            name = derived.base_name()

        if name not in result:
            # Validate this later.
            result[name] = PeripheralGroup(None, [])  # type: ignore

        group = result[name]

        if group.root is None:
            group.root = derived if derived is not None else peripheral
        else:
            assert derived is not None
            result[derived.base_name()].derivatives.append(peripheral)

    # Validate groups.
    for name, group in result.items():
        assert group.root is not None, (name, group)

    return result
