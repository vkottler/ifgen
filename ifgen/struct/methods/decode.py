"""
A module for struct-decoding methods.
"""

# third-party
from vcorelib.io import IndentedFileWriter

# internal
from ifgen.generation.interface import GenerateTask
from ifgen.struct.methods.common import wrapper_method


def decode_method(writer: IndentedFileWriter) -> None:
    """Write boilerplate decode method."""

    with writer.javadoc():
        writer.write("Update this instance from a buffer.")
        writer.empty()
        writer.write("\\param[in] buffer     Buffer to read.")
        writer.write(
            "\\param[in] endianness Byte order from decoding elements."
        )

    wrapper_method(writer, is_encode=False)


def decode_native_method(
    task: GenerateTask, writer: IndentedFileWriter
) -> None:
    """Generate a struct-decode method that uses native byte order."""

    with writer.javadoc():
        writer.write("Decode using native byte-order.")
        writer.empty()
        writer.write("\\param[in] buffer Buffer to read.")

    writer.write("inline void decode_native(const Buffer &buffer)")
    with writer.scope():
        writer.write("auto buf = raw();")
        writer.write("*buf = buffer;")

    del task


def decode_swapped_method(
    task: GenerateTask, writer: IndentedFileWriter
) -> None:
    """Generate a struct-decode method that uses swapped byte order."""

    del task

    with writer.javadoc():
        writer.write("Decode using byte-order swapped from native.")
        writer.empty()
        writer.write("\\param[in] buffer Buffer to read.")

    writer.write("inline void decode_swapped(const Buffer &buffer)")
    with writer.scope():
        writer.write("(void)buffer;")
        writer.cpp_comment("Need to get individual field sizes.")


def struct_decode(task: GenerateTask, writer: IndentedFileWriter) -> None:
    """Add a method for decoding structs."""

    decode_native_method(task, writer)

    with writer.padding():
        decode_swapped_method(task, writer)

    decode_method(writer)
