"""
A module implementing 'get' methods for bit-fields.
"""

# built-in
from contextlib import ExitStack
from typing import Any

# third-party
from vcorelib.io.file_writer import IndentedFileWriter

# internal
from ifgen.generation.interface import GenerateTask
from ifgen.struct.methods.fields.common import (
    BitField,
    bit_mask_literal,
    possible_array_arg,
)


def bit_field_get_all_method(
    task: GenerateTask,
    writer: IndentedFileWriter,
    header: bool,
    field: dict[str, Any],
    fields: list[BitField],
    alias: str = None,
) -> None:
    """Generate a 'get' method for multiple bit-field."""

    if not header:
        return

    name = field["name"] if not alias else alias
    writer.c_comment(f"get_{name}")

    print(task)

    print(fields)


def bit_field_get_method(
    task: GenerateTask,
    parent: dict[str, Any],
    field: BitField,
    writer: IndentedFileWriter,
    header: bool,
    kind: str,
    method_slug: str,
    alias: str = None,
) -> None:
    """Generate a 'get' method for a bit-field."""

    if not header:
        return

    is_flag = field["width"] == 1

    inner = possible_array_arg(parent)

    method = task.cpp_namespace(f"get_{method_slug}({inner})", header=header)
    writer.empty()

    with writer.javadoc():
        writer.write(
            (
                f"Get {parent['name']}'s {field['name']} "
                f"{'field' if field['width'] > 1 else 'bit'}."
            )
        )

    line = f"{kind} " + method

    lhs = parent["name"] if not alias else alias
    if inner:
        lhs += "[index]"

    with ExitStack() as stack:
        if is_flag:
            writer.write(line)
            stack.enter_context(writer.scope())
            stmt = f"{lhs} & (1u << {field['index']}u)"
        else:
            writer.write(line)
            stack.enter_context(writer.scope())
            stmt = (
                f"({lhs} >> {field['index']}u) & "
                f"{bit_mask_literal(field['width'])}"
            )

        if task.env.is_enum(kind):
            stmt = f"{kind}({stmt})"

        writer.write(f"return {stmt};")
