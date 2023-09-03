"""
A module for struct-decoding methods.
"""

# third-party
from vcorelib.io import IndentedFileWriter

# internal
from ifgen.generation.interface import GenerateTask
from ifgen.struct.methods.common import wrapper_method
from ifgen.struct.methods.swap import decode_swapped_method


def decode_method(
    task: GenerateTask, writer: IndentedFileWriter, header: bool
) -> None:
    """Write boilerplate decode method."""

    if header:
        with writer.javadoc():
            writer.write("Update this instance from a buffer.")
            writer.empty()
            writer.write("\\param[in] buffer     Buffer to read.")
            writer.write(
                "\\param[in] endianness Byte order from decoding elements."
            )

    wrapper_method(task, writer, header, is_encode=False)


def decode_native_method(
    task: GenerateTask, writer: IndentedFileWriter, header
) -> None:
    """Generate a struct-decode method that uses native byte order."""

    if header:
        with writer.javadoc():
            writer.write("Decode using native byte-order.")
            writer.empty()
            writer.write("\\param[in] buffer Buffer to read.")

    method = task.cpp_namespace("decode_native", header=header)
    writer.write(
        f"void {method}(const Buffer *buffer)" + (";" if header else "")
    )

    if header:
        return

    with writer.scope():
        writer.write("auto buf = raw();")
        writer.write("*buf = *buffer;")

    del task


def struct_decode(
    task: GenerateTask, writer: IndentedFileWriter, header: bool
) -> None:
    """Add a method for decoding structs."""

    decode_native_method(task, writer, header)

    with writer.padding():
        decode_swapped_method(task, writer, header)

    decode_method(task, writer, header)
