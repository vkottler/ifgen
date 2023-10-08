"""
A module for generating configuration data for struct fields.
"""

# built-in
from typing import Any, Iterable

# internal
from ifgen.svd.model.peripheral import Cluster, Register, RegisterData

StructMap = dict[str, Any]
StructField = dict[str, Any]
DEFAULT_STRUCT = {
    "stream": False,
    "codec": False,
    "methods": False,
    "unit_test": False,
}


def parse_offset(data: dict[str, str]) -> int:
    """Parse a hex string to get decimal address offset."""

    return int(data["addressOffset"], 16)


def check_not_handled_fields(
    data: dict[str, Any], fields: Iterable[str]
) -> None:
    """Ensure that some keys aren't present in data."""

    for field in fields:
        assert (
            field not in data
        ), f"Field '{field}' isn't currently handled: {data}."


def handle_cluster(
    cluster: Cluster, structs: StructMap
) -> tuple[int, StructField]:
    """Handle a cluster element."""

    # Ensure that a correct result will be produced.
    check_not_handled_fields(cluster.raw_data, ["alernateCluster"])

    # Register a struct for this cluster. Should we use a namespace for this?
    cluster_struct: dict[str, Any] = cluster.handle_description()
    size, cluster_struct["fields"] = struct_fields(cluster.children, structs)

    # Too difficult due to padding (may need to comment out).
    cluster_struct["expected_size"] = size

    cluster_struct.update(DEFAULT_STRUCT)

    raw_name = cluster.name.replace("[%s]", "")

    cluster_name = cluster.raw_data.get(
        "headerStructName", f"{raw_name}_instance"
    )
    structs[cluster_name] = cluster_struct

    # This needs to be an array element somehow. Use a namespace?
    array_dim = int(cluster.raw_data.get("dim", 1))
    size *= array_dim
    result: StructField = {
        "name": raw_name,
        "type": cluster_name,
        # Too difficult due to padding (may need to comment out).
        "expected_size": size,
        "expected_offset": parse_offset(cluster.raw_data),
    }
    if array_dim > 1:
        result["array_length"] = array_dim

    cluster.handle_description(result)
    return size, result


def handle_register(register: Register) -> tuple[int, StructField]:
    """Handle a register entry."""

    # Ensure that a correct result will be produced.
    check_not_handled_fields(register.raw_data, ["alternateGroup"])

    array_dim = int(register.raw_data.get("dim", 1))

    size = register.size * array_dim
    data = {
        "name": register.name.replace("[%s]", ""),
        "type": register.c_type,
        "expected_size": size,
        "expected_offset": parse_offset(register.raw_data),
    }
    if array_dim > 1:
        data["array_length"] = array_dim

    access = register.access
    if access == "read-only":
        data["const"] = True

    notes = [access]

    register.handle_description(data, prefix=f"({', '.join(notes)}) ")
    return size, data


def struct_fields(
    registers: RegisterData, structs: StructMap, size: int = None
) -> tuple[int, list[StructField]]:
    """Generate data for struct fields."""

    fields = []

    if size is None:
        size = 0

    for item in registers:
        # Figure out how to handle this some other way.
        if "alternateRegister" not in item.raw_data:
            inst_size, field = (
                handle_cluster(item, structs)
                if isinstance(item, Cluster)
                else handle_register(item)
            )
            fields.append(field)
            size += inst_size

    return size, fields
