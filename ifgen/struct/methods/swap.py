"""
A module implementing interfaces for byte-swapping method generation.
"""

# built-in
from typing import Any

# third-party
from vcorelib.io import IndentedFileWriter

# internal
from ifgen.generation.interface import GenerateTask


def no_swap(
    field: dict[str, Any],
    is_decode: bool,
    task: GenerateTask,
    writer: IndentedFileWriter,
) -> None:
    """Encode or decode a single-byte type."""

    name = field["name"]
    kind = field["type"]

    is_enum = task.env.is_enum(kind)

    if is_decode:
        line = f"{name} = "
        arg = "(*buffer)[offset]"
        if is_enum:
            arg = f"{kind}({arg})"

        writer.write(line + arg + ";")
    else:
        arg = name
        if is_enum:
            arg = f"uint8_t({arg})"
        writer.write(f"(*buffer)[offset] = {arg};")


def swap_struct(
    field: dict[str, Any],
    is_decode: bool,
    task: GenerateTask,
    writer: IndentedFileWriter,
) -> None:
    """Perform a byte swap for a struct type."""

    del task

    name = field["name"]
    kind = field["type"]

    writer.write(f"{name}.{'decode' if is_decode else 'encode'}_swapped(")
    pointer = f"{kind}::Buffer *"
    if is_decode:
        pointer = "const " + pointer

    arg = f"reinterpret_cast<{pointer}>"
    arg += "(&(*buffer)[offset])"
    writer.write(f"    {arg});")


def swap_enum(
    field: dict[str, Any],
    is_decode: bool,
    task: GenerateTask,
    writer: IndentedFileWriter,
) -> None:
    """Perform a byte swap for an enumeration type."""

    writer.cpp_comment("IS ENUM")

    del field
    del is_decode
    del task


def swap_fields(
    task: GenerateTask, writer: IndentedFileWriter, is_decode: bool = True
) -> None:
    """Perform byte swaps on individual struct fields."""

    writer.write("std::size_t offset = 0;")

    for field in task.instance["fields"]:
        writer.empty()

        name = field["name"]
        kind = field["type"]
        writer.c_comment(f"{kind} {name}")

        size = task.env.size(kind)
        if size == 1:
            no_swap(field, is_decode, task, writer)
        elif task.env.is_struct(kind):
            swap_struct(field, is_decode, task, writer)
        elif task.env.is_enum(kind):
            swap_enum(field, is_decode, task, writer)

        writer.write(f"offset += {size};")


def decode_swapped_method(
    task: GenerateTask, writer: IndentedFileWriter, header: bool
) -> None:
    """Generate a struct-decode method that uses swapped byte order."""

    if header:
        with writer.javadoc():
            writer.write("Decode using byte-order swapped from native.")
            writer.empty()
            writer.write("\\param[in] buffer Buffer to read.")

    writer.write(
        f"void {task.cpp_namespace('decode_swapped', header=header)}"
        "(const Buffer *buffer)" + (";" if header else "")
    )

    if header:
        return

    with writer.scope():
        swap_fields(task, writer)


def encode_swapped_method(
    task: GenerateTask, writer: IndentedFileWriter, header: bool
) -> None:
    """Generate a struct-encode method that uses swapped byte order."""

    if header:
        with writer.javadoc():
            writer.write("Encode using byte-order swapped from native.")
            writer.empty()
            writer.write("\\param[out] buffer Buffer to write.")

    method = task.cpp_namespace("encode_swapped", header=header)
    writer.write(f"void {method}(Buffer *buffer)" + (";" if header else ""))

    if header:
        return

    with writer.scope():
        swap_fields(task, writer, is_decode=False)
