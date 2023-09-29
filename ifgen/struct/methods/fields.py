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
    name: str,
    field: dict[str, Any],
    writer: IndentedFileWriter,
    header: bool,
    kind: str,
    method_slug: str,
) -> None:
    """Generate a 'get' method for a bit-field."""

    method = task.cpp_namespace(f"get_{method_slug}()", header=header)
    writer.empty()

    if header:
        with writer.javadoc():
            writer.write(
                (
                    f"Get {name}'s {field['name']} "
                    f"{'field' if field['width'] > 1 else 'bit'}."
                )
            )

    write_method = writer.cpp_comment if not header else writer.write
    write_method(f"{kind} " + method + (";" if header else ""))

    # generate body
    if not header:
        pass


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
        stmt = f"1 << {field['index']}"
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
        stmt = f"~(1 << {field['index']})"
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
        stmt = f"1 << {field['index']}"
        writer.write(f"{name} ^= {stmt};")


def bit_field_set_method(
    task: GenerateTask,
    name: str,
    field: dict[str, Any],
    writer: IndentedFileWriter,
    header: bool,
    kind: str,
    method_slug: str,
) -> None:
    """Generate a 'set' method for a bit-field."""

    # Generate a toggle method for bit fields.
    if field["width"] == 1:
        bit_field_toggle_method(task, name, field, writer, header, method_slug)
    else:
        write_method = writer.cpp_comment if not header else writer.write

        method = task.cpp_namespace(
            f"set_{method_slug}({kind} value)", header=header
        )
        writer.empty()

        if header:
            with writer.javadoc():
                writer.write(f"Set {name}'s {field['name']} field.")

        write_method("void " + method + (";" if header else ""))

        if not header:
            pass


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
            task, name, field, writer, header, kind, method_slug
        )

    # Generate a 'set' method.
    if field["write"]:
        bit_field_set_method(
            task, name, field, writer, header, kind, method_slug
        )


def bit_fields(
    task: GenerateTask, writer: IndentedFileWriter, header: bool
) -> None:
    """Generate bit-field lines."""

    for field in task.instance["fields"]:
        for bfield in field.get("fields", []):
            bit_field(task, field, bfield, writer, header)
