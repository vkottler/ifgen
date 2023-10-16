"""
A module implementing 'set' methods for bit-fields.
"""

# built-in
from typing import Any

# third-party
from vcorelib.io.file_writer import IndentedFileWriter

# internal
from ifgen.generation.interface import GenerateTask
from ifgen.struct.methods.bit import bit_field_toggle_method
from ifgen.struct.methods.fields.common import (
    BitField,
    bit_mask_literal,
    possible_array_arg,
)


def bit_field_set_all_method(
    task: GenerateTask,
    writer: IndentedFileWriter,
    header: bool,
    field: dict[str, Any],
    fields: list[BitField],
    alias: str = None,
) -> None:
    """Generate a 'set' method for multiple bit-field."""

    if not header:
        return

    name = field["name"] if not alias else alias
    writer.c_comment(f"set_{name}")

    print(task)

    print(fields)


def bit_field_set_method(
    task: GenerateTask,
    parent: dict[str, Any],
    field: BitField,
    writer: IndentedFileWriter,
    header: bool,
    kind: str,
    method_slug: str,
    alias: str = None,
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

        inner = possible_array_arg(parent)
        if inner:
            inner += ", "
        inner += f"{kind} value"

        method = task.cpp_namespace(
            f"set_{method_slug}({inner})", header=header
        )
        writer.empty()

        if header:
            with writer.javadoc():
                writer.write(f"Set {parent['name']}'s {field['name']} field.")

        writer.write("inline void " + method)
        with writer.scope():
            rhs = parent["name"] if not alias else alias
            if "index" in inner:
                rhs += "[index]"

            writer.write(f"{parent['type']} curr = {rhs};")

            mask = bit_mask_literal(field["width"])

            with writer.padding():
                writer.write(f"curr &= ~({mask} << {field['index']}u);")

                val_str = "value"
                if task.env.is_enum(kind):
                    val_str = f"std::to_underlying({val_str})"

                writer.write(
                    f"curr |= ({val_str} & {mask}) << {field['index']}u;"
                )

            writer.write(f"{rhs} = curr;")
