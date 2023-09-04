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
from ifgen.struct.methods.decode import struct_decode
from ifgen.struct.methods.encode import struct_encode


def protocol_json(task: GenerateTask) -> dict[str, Any]:
    """Get JSON data for this struct task."""

    protocol = task.protocol()

    # use something better for this

    return protocol.export_json()


def struct_buffer_method(
    task: GenerateTask,
    writer: IndentedFileWriter,
    header: bool,
    read_only: bool,
) -> None:
    """Generate a method for raw buffer access."""

    if header:
        with writer.javadoc():
            writer.write(
                (
                    "Get this instance as a "
                    f"{'read-only ' if read_only else ''}"
                    "fixed-size byte array."
                )
            )

    buff_type = task.cpp_namespace("Buffer", header=header)

    if read_only:
        buff_type = "const " + buff_type

    # Returns a pointer.
    method = task.cpp_namespace(
        "raw()" if not read_only else "raw_ro()", prefix="*", header=header
    )
    writer.write(
        f"{buff_type} {method}"
        + (" const" if read_only else "")
        + (";" if header else "")
    )

    if header:
        return

    with writer.scope():
        writer.write(
            "return reinterpret_cast"
            f"<{'const ' if read_only else ''}Buffer *>(this);"
        )


def struct_methods(
    task: GenerateTask, writer: IndentedFileWriter, header: bool
) -> None:
    """Write generated-struct methods."""

    if header:
        writer.write("using Buffer = std::array<byte, size>;")
        with writer.padding():
            writer.write(
                f"auto operator<=>(const {task.name} &) const = default;"
            )

    struct_buffer_method(task, writer, header, False)

    with writer.padding():
        struct_buffer_method(task, writer, header, True)

    struct_encode(task, writer, header)

    writer.empty()
    struct_decode(task, writer, header)

    to_json_method(
        task,
        writer,
        protocol_json(task),
        dumps_indent=task.instance["json_indent"],
        task_name=False,
        static=True,
        definition=header,
    )
