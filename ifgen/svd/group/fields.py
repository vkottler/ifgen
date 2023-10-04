"""
A module for generating configuration data for struct fields.
"""

# built-in
from typing import Any

# internal
from ifgen.svd.model.peripheral import Peripheral


def struct_fields(peripheral: Peripheral) -> list[dict[str, Any]]:
    """Generate data for struct fields."""

    result: list[dict[str, Any]] = []

    del peripheral

    return result
