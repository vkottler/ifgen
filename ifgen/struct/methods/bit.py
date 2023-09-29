"""
A module implementing interfaces for generating bit-field methods.
"""

# built-in
from typing import Any

# third-party
from vcorelib.io.file_writer import IndentedFileWriter

# internal
from ifgen.generation.interface import GenerateTask


def set_bit_method(
    task: GenerateTask,
    name: str,
    field: dict[str, Any],
    writer: IndentedFileWriter,
    header: bool,
    method_slug: str,
) -> None:
    """Generate a 'set' method for a bit-field."""

    if not header:
        return

    method = task.cpp_namespace(f"set_{method_slug}()", header=header)
    writer.empty()

    with writer.javadoc():
        writer.write(f"Set {name}'s {field['name']} bit.")

    writer.write("inline void " + method)

    with writer.scope():
        stmt = f"1u << {field['index']}u"
        writer.write(f"{name} |= {stmt};")


def clear_bit_method(
    task: GenerateTask,
    name: str,
    field: dict[str, Any],
    writer: IndentedFileWriter,
    header: bool,
    method_slug: str,
) -> None:
    """Generate a 'clear' method for a bit-field."""

    if not header:
        return

    method = task.cpp_namespace(f"clear_{method_slug}()", header=header)
    writer.empty()

    with writer.javadoc():
        writer.write(f"Clear {name}'s {field['name']} bit.")

    writer.write("inline void " + method)

    with writer.scope():
        stmt = f"~(1u << {field['index']}u)"
        writer.write(f"{name} &= {stmt};")


def bit_field_toggle_method(
    task: GenerateTask,
    name: str,
    field: dict[str, Any],
    writer: IndentedFileWriter,
    header: bool,
    method_slug: str,
) -> None:
    """Generate a 'toggle' method for a bit-field."""

    set_bit_method(task, name, field, writer, header, method_slug)
    clear_bit_method(task, name, field, writer, header, method_slug)

    if not header:
        return

    method = task.cpp_namespace(f"toggle_{method_slug}()", header=header)
    writer.empty()

    with writer.javadoc():
        writer.write(f"Toggle {name}'s {field['name']} bit.")

    writer.write("inline void " + method)

    with writer.scope():
        stmt = f"1u << {field['index']}u"
        writer.write(f"{name} ^= {stmt};")
