"""
A module implementing an interface for generating bit-field methods for
structs.
"""

# built-in
from contextlib import ExitStack
from typing import Any

# third-party
from vcorelib.io.file_writer import IndentedFileWriter

# internal
from ifgen.generation.interface import GenerateTask
from ifgen.struct.methods.bit import bit_field_toggle_method

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


def bit_field_get_method(
    task: GenerateTask,
    parent: dict[str, Any],
    field: dict[str, Any],
    writer: IndentedFileWriter,
    header: bool,
    kind: str,
    method_slug: str,
) -> None:
    """Generate a 'get' method for a bit-field."""

    if not header:
        return

    is_flag = field["width"] == 1

    method = task.cpp_namespace(f"get_{method_slug}()", header=header)
    writer.empty()

    with writer.javadoc():
        writer.write(
            (
                f"Get {parent['name']}'s {field['name']} "
                f"{'field' if field['width'] > 1 else 'bit'}."
            )
        )

    line = f"{kind} " + method

    with ExitStack() as stack:
        if is_flag:
            writer.write(line)
            stack.enter_context(writer.scope())
            stmt = f"{parent['name']} & (1 << {field['index']})"
        else:
            writer.write(line)
            stack.enter_context(writer.scope())
            mask = bit_mask_literal(field["width"])
            stmt = f"({parent['name']} >> {field['index']}u) & {mask}"

        if task.env.is_enum(kind):
            stmt = f"{kind}({stmt})"

        writer.write(f"return {stmt};")


def bit_mask_literal(width: int) -> str:
    """Get a bit-mask literal."""
    return "0b" + ("1" * width) + "u"


def bit_field_set_method(
    task: GenerateTask,
    parent: dict[str, Any],
    field: dict[str, Any],
    writer: IndentedFileWriter,
    header: bool,
    kind: str,
    method_slug: str,
) -> None:
    """Generate a 'set' method for a bit-field."""

    # Generate a toggle method for bit fields.
    if field["width"] == 1:
        bit_field_toggle_method(
            task, parent["name"], field, writer, header, method_slug
        )
    else:
        if not header:
            return

        method = task.cpp_namespace(
            f"set_{method_slug}({kind} value)", header=header
        )
        writer.empty()

        if header:
            with writer.javadoc():
                writer.write(f"Set {parent['name']}'s {field['name']} field.")

        writer.write("inline void " + method)
        with writer.scope():
            writer.write(f"{parent['type']} curr = {parent['name']};")

            mask = bit_mask_literal(field["width"])

            with writer.padding():
                writer.write(f"curr &= ~({mask} << {field['index']}u);")

                val_str = "value"
                if task.env.is_enum(kind):
                    val_str = f"std::to_underlying({val_str})"

                writer.write(
                    f"curr |= ({val_str} & {mask}) << {field['index']}u;"
                )

            writer.write(f"{parent['name']} = curr;")


def bit_field(
    task: GenerateTask,
    parent: dict[str, Any],
    field: dict[str, Any],
    writer: IndentedFileWriter,
    header: bool,
) -> None:
    """Generate for an individual bit-field."""

    kind = bit_field_underlying(field)

    type_size = task.env.size(parent["type"]) * 8

    index = field["index"]
    width = field["width"]

    # Validate field parameters.
    assert index + width < type_size, (index, width, type_size, field)
    assert field["read"] or field["write"], field

    name = parent["name"]
    method_slug = f"{name}_{field['name']}"

    # Generate a 'get' method.
    if field["read"]:
        bit_field_get_method(
            task, parent, field, writer, header, kind, method_slug
        )

    # Generate a 'set' method.
    if field["write"]:
        bit_field_set_method(
            task, parent, field, writer, header, kind, method_slug
        )


def bit_fields(
    task: GenerateTask, writer: IndentedFileWriter, header: bool
) -> None:
    """Generate bit-field lines."""

    for field in task.instance["fields"]:
        for bfield in field.get("fields", []):
            bit_field(task, field, bfield, writer, header)
