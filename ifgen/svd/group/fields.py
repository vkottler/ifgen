"""
A module for generating configuration data for struct fields.
"""

# built-in
from typing import Any

# internal
from ifgen.svd.model.peripheral import Cluster, Register, RegisterData

StructMap = dict[str, Any]
StructField = dict[str, Any]
DEFAULT_STRUCT = {"stream": False, "codec": False}


def handle_cluster(
    cluster: Cluster, structs: StructMap
) -> tuple[int, StructField]:
    """Handle a cluster element."""

    # Register a struct for this cluster. Should we use a namespace for this?
    cluster_struct: dict[str, Any] = cluster.handle_description()
    size, cluster_struct["fields"] = struct_fields(cluster.children, structs)
    cluster_struct["expected_size"] = size
    cluster_struct.update(DEFAULT_STRUCT)

    # compute expected size?

    structs[cluster.name] = cluster_struct

    # This needs to be an array element somehow. Use a namespace?
    result: StructField = {"name": cluster.name, "expected_size": size}
    cluster.handle_description(result)
    return size, result


def handle_register(register: Register) -> tuple[int, StructField]:
    """Handle a register entry."""

    # handle register is array + get size from peripheral if necessary
    size = register.size
    data = {
        "name": register.name,
        "type": register.c_type,
        "expected_size": size,
    }
    register.handle_description(data)
    return size, data


def struct_fields(
    registers: RegisterData, structs: StructMap, size: int = None
) -> tuple[int, list[StructField]]:
    """Generate data for struct fields."""

    fields = []

    if size is None:
        size = 0

    for item in registers:
        inst_size, field = (
            handle_cluster(item, structs)
            if isinstance(item, Cluster)
            else handle_register(item)
        )
        fields.append(field)
        size += inst_size

    return size, fields
