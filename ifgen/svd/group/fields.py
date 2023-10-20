"""
A module for generating configuration data for struct fields.
"""

# built-in
from typing import Any, Iterable

# internal
from ifgen.svd.group.enums import ENUM_DEFAULTS, get_enum_name, translate_enums
from ifgen.svd.model.peripheral import Cluster, Register, RegisterData

StructMap = dict[str, Any]
StructField = dict[str, Any]
DEFAULT_STRUCT = {
    "stream": False,
    "codec": False,
    "methods": False,
    "unit_test": False,
    "identifier": False,
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


EnumMap = dict[str, Any]


def handle_cluster(
    cluster: Cluster,
    structs: StructMap,
    enums: EnumMap,
    peripheral: str,
    min_enum_members: int,
) -> tuple[int, StructField]:
    """Handle a cluster element."""

    # Ensure that a correct result will be produced.
    check_not_handled_fields(cluster.raw_data, ["alernateCluster"])

    # Register a struct for this cluster. Should we use a namespace for this?
    cluster_struct: dict[str, Any] = cluster.handle_description()
    size, cluster_struct["fields"] = struct_fields(
        cluster.children, structs, enums, peripheral, min_enum_members
    )

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


RegisterMap = dict[str, Register]


def process_bit_fields(
    register: Register,
    output: dict[str, Any],
    enums: EnumMap,
    peripheral: str,
    min_enum_width: int,
) -> None:
    """Get bit-field declarations for a given register."""

    if register.fields is None:
        return

    result: list[dict[str, Any]] = []

    # Process fields.
    for name, field in register.fields.items():
        field_data: dict[str, Any] = {"name": name}
        field_data.update(field.ifgen_data)
        result.append(field_data)

        # Handle creating an enumeration.
        if field.enum is not None:
            # Register enumeration.
            raw = translate_enums(field.enum)

            if field_data["width"] >= min_enum_width:
                new_enum: dict[str, Any] = {"enum": raw}
                new_enum.update(ENUM_DEFAULTS)

                # Increase size of underlying if necessary.
                if field_data["width"] > 8:
                    new_enum["underlying"] = "uint16_t"

                # Check if enum is unique.
                enum_name = get_enum_name(
                    f"{peripheral}_{register.name}_{name}".replace("[%s]", ""),
                    peripheral,
                    raw,
                )
                field_data["type"] = enum_name
                if enum_name not in enums:
                    enums[enum_name] = new_enum

    if result:
        output["fields"] = result


def handle_register(
    register: Register,
    register_map: RegisterMap,
    enums: EnumMap,
    peripheral: str,
    min_enum_width: int,
) -> tuple[int, StructField]:
    """Handle a register entry."""

    # Handle adding a union entry to the main field and handle this register's
    # bit fields.
    if "alternateRegister" in register.raw_data:
        return 0, {}

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

    # Handle bit fields.
    process_bit_fields(register, data, enums, peripheral, min_enum_width)

    # Handle alternates.
    alts = register.alternates
    if alts:
        alts_data: list[dict[str, Any]] = []

        for item in alts:
            alt_data: dict[str, Any] = {"name": item.name}
            if item.access == "read-only":
                alt_data["const"] = True
            item.handle_description(alt_data, prefix=f"({item.access}) ")

            process_bit_fields(
                register_map[item.name],
                alt_data,
                enums,
                peripheral,
                min_enum_width,
            )

            # Forward array information (might be necessary at some point).
            # if "array_length" in data:
            #     alt_data["array_length"] = data["array_length"]

            alts_data.append(alt_data)

        data["alternates"] = alts_data

    return size, data


def struct_fields(
    registers: RegisterData,
    structs: StructMap,
    enums: EnumMap,
    peripheral: str,
    min_enum_width: int,
    size: int = None,
) -> tuple[int, list[StructField]]:
    """Generate data for struct fields."""

    fields = []

    if size is None:
        size = 0

    # Create a string mapping of registers.
    register_map: RegisterMap = {}
    for item in registers:
        if isinstance(item, Register):
            register_map[item.name] = item

    for item in registers:
        inst_size, field = (
            handle_cluster(item, structs, enums, peripheral, min_enum_width)
            if isinstance(item, Cluster)
            else handle_register(
                item, register_map, enums, peripheral, min_enum_width
            )
        )
        if inst_size > 0:
            fields.append(field)
            size += inst_size

    return size, fields
