"""
A module implementing interfaces for byte-swapping method generation.
"""

# built-in
from contextlib import ExitStack
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
    is_array: bool,
) -> None:
    """Encode or decode a single-byte type."""

    name = field["name"]
    if is_array:
        name += "[i]"

    kind = field["type"]

    is_enum = task.env.is_enum(kind)

    if is_decode:
        line = f"{name} = "
        arg = "buf[idx++]"
        if is_enum:
            arg = f"{kind}({arg})"
        else:
            arg = f"std::to_integer<{kind}>({arg})"

        writer.write(line + arg + ";")
    else:
        writer.write(f"buf[idx++] = std::byte({name});")


def swap_struct(
    field: dict[str, Any],
    is_decode: bool,
    task: GenerateTask,
    writer: IndentedFileWriter,
    is_array: bool,
) -> None:
    """Perform a byte swap for a struct type."""

    del task

    name = field["name"]
    if is_array:
        name += "[i]"

    kind = field["type"]

    writer.write(
        f"idx += {name}.{'decode' if is_decode else 'encode'}_swapped("
    )
    pointer = f"{kind}::Buffer *"
    if is_decode:
        pointer = "const " + pointer

    arg = f"reinterpret_cast<{pointer}>"
    arg += "(&(*buffer)[idx])"
    writer.write(f"    {arg});")


def assignment(writer: IndentedFileWriter, lhs: str, rhs: str) -> None:
    """Write an assignment line."""

    line = f"{lhs} = {rhs};"

    if len(line) + 4 > 79:
        start = lhs + " ="
        writer.write(start)
        writer.write("    " + rhs + ";")
    else:
        writer.write(line)


def to_integral(kind: str) -> str:
    """Convert certain types to their corresponding integral types."""

    lazy = {"float": "uint32_t", "double": "uint64_t"}
    return lazy.get(kind, kind)


def swap_enum(
    field: dict[str, Any],
    is_decode: bool,
    task: GenerateTask,
    writer: IndentedFileWriter,
    is_array: bool,
) -> None:
    """Perform a byte swap for an enumeration type."""

    underlying = task.env.get_enum(field["type"]).primitive + "_t"

    name = field["name"]
    if is_array:
        name += "[i]"

    if is_decode:
        lhs = name
        underlying = to_integral(underlying)
        rhs = (
            f"{field['type']}(std::byteswap(*reinterpret_cast<const "
            f"{underlying} *>(&buf[idx])))"
        )

    else:
        lhs = f"*reinterpret_cast<{underlying} *>(&buf[idx])"
        underlying = to_integral(underlying)
        rhs = f"std::byteswap(std::to_underlying({name}))"

    assignment(writer, lhs, rhs)


def encode_primitive_swap(
    field: dict[str, Any], writer: IndentedFileWriter, is_array: bool
) -> None:
    """Encode a primitive-sized element by swapping byte order."""

    underlying = field["type"]
    integral = to_integral(underlying)

    name = field["name"]
    if is_array:
        name += "[i]"

    rhs = "std::byteswap("
    if field["type"] == integral:
        lhs = f"*reinterpret_cast<{underlying} *>(&buf[idx])"
        rhs += f"{name})"
    else:
        lhs = f"*reinterpret_cast<{integral} *>(&buf[idx])"
        rhs += f"std::bit_cast<{integral}>({name}))"

    assignment(writer, lhs, rhs)


def decode_primitive_swap(
    field: dict[str, Any], writer: IndentedFileWriter, is_array: bool
) -> None:
    """Decode a primitive-sized element by swapping byte order."""

    lhs = f"{field['name']}"
    if is_array:
        lhs += "[i]"

    underlying = field["type"]
    integral = to_integral(underlying)
    reinterp = f"reinterpret_cast<const {integral} *>"

    if integral == underlying:
        rhs = f"std::byteswap(*{reinterp}" f"(&buf[idx]))"
        assignment(writer, lhs, rhs)
    else:
        # assignment(
        #     writer, "auto val", f"std::byteswap(*{reinterp}(&buf[idx]))"
        # )
        assignment(
            writer,
            lhs,
            f"std::bit_cast<{underlying}>("
            f"std::byteswap(*{reinterp}(&buf[idx])))",
        )


def swap_fields(
    task: GenerateTask, writer: IndentedFileWriter, is_decode: bool = True
) -> None:
    """Perform byte swaps on individual struct fields."""

    writer.write("std::size_t idx = 0;")
    writer.write("auto buf = buffer->data();")

    for field in task.instance["fields"]:
        writer.empty()

        name = field["name"]
        kind = field["type"]
        writer.c_comment(f"{kind} {name}")

        with ExitStack() as stack:
            is_array = "array_length" in field
            if is_array:
                array_cmp = task.cpp_namespace(f"{name}_length")
                writer.write(f"for (std::size_t i = 0; i < {array_cmp}; i++)")
                stack.enter_context(writer.scope())

            size = task.env.size(kind)

            # Handle padding.
            if field["padding"]:
                writer.c_comment(f"Advance for padding field '{name}'.")
                writer.write(f"idx += {size};")
                continue

            if size == 1:
                no_swap(field, is_decode, task, writer, is_array)
            elif task.env.is_struct(kind):
                swap_struct(field, is_decode, task, writer, is_array)
            elif task.env.is_enum(kind):
                swap_enum(field, is_decode, task, writer, is_array)
                writer.write(f"idx += {size};")
            else:
                if is_decode:
                    decode_primitive_swap(field, writer, is_array)
                else:
                    encode_primitive_swap(field, writer, is_array)
                writer.write(f"idx += {size};")

    writer.empty()
    writer.write("return idx;")


def decode_swapped_method(
    task: GenerateTask, writer: IndentedFileWriter, header: bool
) -> None:
    """Generate a struct-decode method that uses swapped byte order."""

    if header:
        with writer.javadoc():
            writer.write("Decode using byte-order swapped from native.")
            writer.empty()
            writer.write(task.command("param[in]", "buffer Buffer to read."))
            writer.write(
                task.command(
                    "return", "          The number of bytes decoded."
                )
            )

    writer.write(
        f"std::size_t {task.cpp_namespace('decode_swapped', header=header)}"
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
            writer.write(task.command("param[out]", "buffer Buffer to write."))
            writer.write(
                task.command(
                    "return", "           The number of bytes encoded."
                )
            )

    method = task.cpp_namespace("encode_swapped", header=header)
    writer.write(
        f"std::size_t {method}(Buffer *buffer) const" + (";" if header else "")
    )

    if header:
        return

    with writer.scope():
        swap_fields(task, writer, is_decode=False)
