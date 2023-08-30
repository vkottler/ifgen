"""
A module implementing interfaces for generating struct method code.
"""

# built-in
from typing import Any

# third-party
from vcorelib.io import IndentedFileWriter

# internal
from ifgen.generation.interface import GenerateTask
from ifgen.generation.json import to_json_method


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


def protocol_json(task: GenerateTask) -> dict[str, Any]:
    """Get JSON data for this struct task."""

    protocol = task.env.types.get_protocol(
        task.name, *task.instance.get("namespace", [])
    )

    return protocol.export_json()


def struct_methods(task: GenerateTask, writer: IndentedFileWriter) -> None:
    """Write generated-struct methods."""

    writer.write("using Buffer = std::array<uint8_t, size>;")

    with writer.padding():
        writer.cpp_comment(
            "Add a function for type ID, get it from the TypeSystem?"
        )
        writer.cpp_comment("Underlying type for Type ID?")

    struct_encode(task, writer)

    with writer.padding():
        struct_decode(task, writer)

    to_json_method(
        task,
        writer,
        protocol_json(task),
        dumps_indent=task.instance["json_indent"],
        task_name=False,
        static=True,
    )
