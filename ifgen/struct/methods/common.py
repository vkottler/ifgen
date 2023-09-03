"""
Utilities shared between struct methods.
"""

# third-party
from vcorelib.io import IndentedFileWriter

# internal
from ifgen.generation.interface import GenerateTask


def wrapper_method(
    task: GenerateTask,
    writer: IndentedFileWriter,
    header: bool,
    is_encode: bool = True,
) -> None:
    """Create a generic encode/decode method."""

    method = task.cpp_namespace(
        "encode" if is_encode else "decode", header=header
    )

    line_start = f"void {method}("
    line = line_start + ("const " if not is_encode else "") + "Buffer *buffer,"

    if header and not is_encode:
        writer.write(line)
        line = ""
    else:
        line += " "

    line += (
        " " * len(line_start) if header and not is_encode else ""
    ) + "std::endian endianness"
    if header:
        line += " = std::endian::native"
    line += ")"
    if header:
        line += ";"

    writer.write(line)

    if header:
        return

    with writer.scope():
        writer.write("if (endianness == std::endian::native)")
        with writer.scope():
            writer.write(f"{method}_native(buffer);")
        writer.write("else")
        with writer.scope():
            writer.write(f"{method}_swapped(buffer);")
