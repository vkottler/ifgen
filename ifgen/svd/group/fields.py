"""
A module for generating configuration data for struct fields.
"""

# built-in
from typing import Any

# internal
from ifgen.svd.model.cluster import Cluster, RegisterData
from ifgen.svd.model.register import Register

StructMap = dict[str, Any]
StructField = dict[str, Any]
DEFAULT_STRUCT = {"stream": False, "codec": False}


def handle_cluster(cluster: Cluster, structs: StructMap) -> StructField:
    """Handle a cluster element."""

    # Register a struct for this cluster. Should we use a namespace for this?
    cluster_struct: dict[str, Any] = cluster.handle_description()
    cluster_struct["fields"] = struct_fields(cluster.children, structs)
    cluster_struct.update(DEFAULT_STRUCT)

    # compute expected size?

    structs[cluster.name] = cluster_struct

    # This needs to be an array element somehow. Use a namespace?
    result: StructField = {"name": cluster.name}
    cluster.handle_description(result)
    return result


def handle_register(register: Register) -> StructField:
    """Handle a register entry."""

    data = {"name": register.name}
    register.handle_description(data)
    return data


def struct_fields(
    registers: RegisterData, structs: StructMap
) -> list[StructField]:
    """Generate data for struct fields."""

    return [
        handle_cluster(item, structs)
        if isinstance(item, Cluster)
        else handle_register(item)
        for item in registers
    ]
