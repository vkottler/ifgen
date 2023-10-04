"""
A module for generating configuration data for struct fields.
"""

# built-in
from typing import Any

# internal
from ifgen.svd.model.cluster import Cluster
from ifgen.svd.model.peripheral import Peripheral


def struct_fields(peripheral: Peripheral) -> list[dict[str, Any]]:
    """Generate data for struct fields."""

    result: list[dict[str, Any]] = []

    for item in peripheral.registers:
        # check if this is an array?
        if isinstance(item, Cluster):
            for child in item.children:
                result.append({"name": child.name})
        else:
            result.append({"name": item.name})

    return result
