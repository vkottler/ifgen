"""
A module implementing an interface for generating bit-field methods for
structs.
"""

# built-in
from typing import Any

# third-party
from vcorelib.io.file_writer import IndentedFileWriter

# internal
from ifgen.generation.interface import GenerateTask
from ifgen.struct.methods.fields.common import BitField
from ifgen.struct.methods.fields.getter import (
    bit_field_get_all_method,
    bit_field_get_method,
)
from ifgen.struct.methods.fields.setter import (
    bit_field_set_all_method,
    bit_field_set_method,
)

STANDARD_INTS = [
    ("uint8_t", 8),
    ("uint16_t", 16),
    ("uint32_t", 32),
    ("uint64_t", 64),
]


def bit_field_underlying(field: dict[str, Any]) -> str:
    """Get the underlying type for a bit field."""

    kind = field.get("type")

    # Automatically determine a sane primitive-integer type to use if one isn't
    # specified.
    if kind is None:
        width = field["width"]

        if width == 1:
            kind = "bool"
        else:
            for candidate, bit_width in STANDARD_INTS:
                if field["width"] <= bit_width:
                    kind = candidate
                    break

    assert kind is not None, kind
    return kind


def bit_field(
    task: GenerateTask,
    parent: dict[str, Any],
    field: BitField,
    writer: IndentedFileWriter,
    header: bool,
    read_fields: list[BitField],
    write_fields: list[BitField],
    alias: str = None,
) -> None:
    """Generate for an individual bit-field."""

    kind = bit_field_underlying(field)

    type_size = task.env.size(parent["type"]) * 8

    index = field["index"]
    width = field["width"]

    # Validate field parameters.
    assert index + width <= type_size, (index, width, type_size, field)
    assert field["read"] or field["write"], field

    name = parent["name"] if not alias else alias
    method_slug = f"{name}_{field['name']}"

    # Generate a 'get' method.
    if field["read"]:
        bit_field_get_method(
            task, parent, field, writer, header, kind, method_slug, alias=alias
        )
        read_fields.append(field)

    # Generate a 'set' method.
    if field["write"]:
        bit_field_set_method(
            task, parent, field, writer, header, kind, method_slug, alias=alias
        )
        write_fields.append(field)


def handle_atomic_fields_methods(
    task: GenerateTask,
    writer: IndentedFileWriter,
    header: bool,
    field: dict[str, Any],
    read_fields: list[BitField],
    write_fields: list[BitField],
    alias: str = None,
) -> None:
    """Handle additional bit-field methods."""

    if len(read_fields) > 1:
        writer.empty()
        bit_field_get_all_method(
            task, writer, header, field, read_fields, alias=alias
        )

    if len(write_fields) > 1:
        writer.empty()
        bit_field_set_all_method(
            task, writer, header, field, write_fields, alias=alias
        )


def bit_fields(
    task: GenerateTask, writer: IndentedFileWriter, header: bool
) -> None:
    """Generate bit-field lines."""

    for field in task.instance["fields"]:
        read_fields: list[BitField] = []
        write_fields: list[BitField] = []

        for bfield in field.get("fields", []):
            bit_field(
                task, field, bfield, writer, header, read_fields, write_fields
            )
        handle_atomic_fields_methods(
            task, writer, header, field, read_fields, write_fields
        )

        for alternate in field.get("alternates", []):
            read_fields = []
            write_fields = []

            for bfield in alternate.get("fields", []):
                bit_field(
                    task,
                    field,
                    bfield,
                    writer,
                    header,
                    read_fields,
                    write_fields,
                    alias=alternate["name"],
                )
            handle_atomic_fields_methods(
                task,
                writer,
                header,
                field,
                read_fields,
                write_fields,
                alias=alternate["name"],
            )
