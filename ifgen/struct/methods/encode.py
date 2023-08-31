"""
A module for struct-encoding methods.
"""

# third-party
from vcorelib.io import IndentedFileWriter

# internal
from ifgen.generation.interface import GenerateTask
from ifgen.struct.methods.common import wrapper_method


def encode_native_method(
    task: GenerateTask, writer: IndentedFileWriter
) -> None:
    """Generate a struct-encode method that uses native byte order."""

    with writer.javadoc():
        writer.write("Encode using native byte-order.")
        writer.empty()
        writer.write("\\param[out] buffer Buffer to write.")

    writer.write("inline void encode_native(Buffer &buffer)")
    with writer.scope():
        writer.write("buffer = *raw();")

    del task


def encode_swapped_method(
    task: GenerateTask, writer: IndentedFileWriter
) -> None:
    """Generate a struct-encode method that uses swapped byte order."""

    with writer.javadoc():
        writer.write("Encode using byte-order swapped from native.")
        writer.empty()
        writer.write("\\param[out] buffer Buffer to write.")

    writer.write("inline void encode_swapped(Buffer &buffer)")
    with writer.scope():
        writer.write("(void)buffer;")
        writer.cpp_comment("Need to get individual field sizes.")

    del task


def encode_method(writer: IndentedFileWriter) -> None:
    """Write boilerplate encode method."""

    with writer.javadoc():
        writer.write("Encode this instance to a buffer.")
        writer.empty()
        writer.write("\\param[out] buffer     Buffer to write.")
        writer.write(
            "\\param[in]  endianness Byte order for encoding elements."
        )

    wrapper_method(writer)


def struct_encode(task: GenerateTask, writer: IndentedFileWriter) -> None:
    """Add a method for encoding structs."""

    encode_native_method(task, writer)

    with writer.padding():
        encode_swapped_method(task, writer)

    encode_method(writer)
