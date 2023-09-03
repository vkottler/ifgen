"""
A module for struct-encoding methods.
"""

# third-party
from vcorelib.io import IndentedFileWriter

# internal
from ifgen.generation.interface import GenerateTask
from ifgen.struct.methods.common import wrapper_method
from ifgen.struct.methods.swap import encode_swapped_method


def encode_native_method(
    task: GenerateTask, writer: IndentedFileWriter, header: bool
) -> None:
    """Generate a struct-encode method that uses native byte order."""

    if header:
        with writer.javadoc():
            writer.write("Encode using native byte-order.")
            writer.empty()
            writer.write("\\param[out] buffer Buffer to write.")

    method = task.cpp_namespace("encode_native", header=header)
    buffer_type = task.cpp_namespace("Buffer")
    writer.write(
        f"void {method}({buffer_type} *buffer)" + (";" if header else "")
    )

    if header:
        return

    with writer.scope():
        writer.write("*buffer = *raw();")

    del task


def encode_method(
    task: GenerateTask, writer: IndentedFileWriter, header: bool
) -> None:
    """Write boilerplate encode method."""

    if header:
        with writer.javadoc():
            writer.write("Encode this instance to a buffer.")
            writer.empty()
            writer.write("\\param[out] buffer     Buffer to write.")
            writer.write(
                "\\param[in]  endianness Byte order for encoding elements."
            )

    wrapper_method(task, writer, header)


def struct_encode(
    task: GenerateTask, writer: IndentedFileWriter, header: bool
) -> None:
    """Add a method for encoding structs."""

    encode_native_method(task, writer, header)

    with writer.padding():
        encode_swapped_method(task, writer, header)

    encode_method(task, writer, header)
