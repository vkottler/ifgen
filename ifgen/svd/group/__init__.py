"""
A module implementing interfaces for processing a group of peripherals.
"""

# built-in
from pathlib import Path

# third-party
from vcorelib.io import ARBITER

# internal
from ifgen.svd.group.base import PeripheralGroup, peripheral_groups
from ifgen.svd.model.peripheral import peripheral_name

__all__ = ["PeripheralGroup", "peripheral_groups", "handle_group"]


def handle_group(
    output_dir: Path, name: str, group: PeripheralGroup, includes: set[Path]
) -> None:
    """Handle a peripheral group."""

    output = output_dir.joinpath("include.yaml")
    includes.add(output)

    ARBITER.encode(
        output,
        {
            "name": peripheral_name(name),
            "derivatives": [
                peripheral_name(x.name) for x in group.derivatives
            ],
        },
    )
