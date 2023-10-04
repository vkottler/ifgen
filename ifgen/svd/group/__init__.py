"""
A module implementing interfaces for processing a group of peripherals.
"""

# built-in
from pathlib import Path
from typing import Any

# third-party
from vcorelib.io import ARBITER

# internal
from ifgen.svd.group.base import PeripheralGroup, peripheral_groups
from ifgen.svd.group.fields import struct_fields
from ifgen.svd.model.peripheral import Peripheral, peripheral_name

__all__ = ["PeripheralGroup", "peripheral_groups", "handle_group"]


def struct_instance(peripheral: Peripheral) -> dict[str, Any]:
    """Get struct instance data."""

    return {
        "name": peripheral_name(peripheral.name),
        "address": peripheral.raw_data["baseAddress"],
    }


def struct_data(group: PeripheralGroup) -> dict[str, Any]:
    """Get struct data for a peripheral group."""

    data = {
        "instances": [struct_instance(x) for x in group.peripherals],
        "fields": struct_fields(group.root),
        "stream": False,
        "codec": False,
    }

    return data


def handle_group(
    output_dir: Path, group: PeripheralGroup, includes: set[Path]
) -> None:
    """Handle a peripheral group."""

    output = output_dir.joinpath("include.yaml")
    includes.add(output)
    ARBITER.encode(
        output,
        {
            "structs": {
                group.root.base_name: struct_data(group),  # type: ignore
            }
        },
    )
