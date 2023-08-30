"""
A module implementing interfaces for generating struct method code.
"""

# third-party
from vcorelib.io import IndentedFileWriter

# internal
from ifgen.generation.interface import GenerateTask


def struct_encode(task: GenerateTask, writer: IndentedFileWriter) -> None:
    """Add a method for encoding structs."""

    del task

    with writer.javadoc():
        writer.write("Encode this instance to a buffer.")
        writer.empty()
        writer.write("\\param[out] buffer     Buffer to write.")
        writer.write(
            "\\param[in]  endianness Byte order for encoding elements."
        )

    writer.write(
        (
            "void encode(Buffer &buffer, "
            "std::endian endianness = std::endian::native)"
        )
    )
    with writer.scope():
        writer.write("(void)buffer;")
        writer.write("(void)endianness;")
        writer.cpp_comment("Need to get individual field sizes.")


def struct_decode(task: GenerateTask, writer: IndentedFileWriter) -> None:
    """Add a method for decoding structs."""

    del task

    with writer.javadoc():
        writer.write("Update this instance from a buffer.")
        writer.empty()
        writer.write("\\param[in] buffer     Buffer to read.")
        writer.write(
            "\\param[in] endianness Byte order from decoding elements."
        )

    writer.write("void decode(const Buffer &buffer,")
    writer.write("            std::endian endianness = std::endian::native)")
    with writer.scope():
        writer.write("(void)buffer;")
        writer.write("(void)endianness;")
        writer.cpp_comment("Need to get individual field sizes.")


def struct_methods(task: GenerateTask, writer: IndentedFileWriter) -> None:
    """Write generated-struct methods."""

    writer.write("using Buffer = std::array<uint8_t, size>;")
    writer.empty()

    struct_encode(task, writer)
    writer.empty()
    struct_decode(task, writer)
