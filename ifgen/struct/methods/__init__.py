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


def span_method(
    task: GenerateTask, writer: IndentedFileWriter, header: bool
) -> None:
    """Generate a span method."""

    if not header:
        writer.c_comment("Span method defined in header.")
        return

    with writer.javadoc():
        writer.write(("Get this instance as a byte span."))

    span_type = task.cpp_namespace("Span", header=header)
    method = task.cpp_namespace("span", header=header)

    writer.write(f"inline {span_type} {method}()")

    with writer.scope():
        writer.write("return Span(*raw());")


def struct_buffer_method(
    task: GenerateTask,
    writer: IndentedFileWriter,
    header: bool,
    read_only: bool,
) -> None:
    """Generate a method for raw buffer access."""

    if not header:
        return

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
        f"inline {buff_type} {method}" + (" const" if read_only else "")
    )

    with writer.scope():
        writer.write(
            "return reinterpret_cast"
            f"<{'const ' if read_only else ''}Buffer *>(this);"
        )


def swap_method(
    task: GenerateTask, writer: IndentedFileWriter, header: bool
) -> None:
    """Add an in-place swap method."""

    if not header:
        return

    writer.empty()

    with writer.javadoc():
        writer.write("Swap this instance's bytes in place.")
        writer.empty()
        writer.write(task.command("return", "A reference to the instance."))

    method = task.cpp_namespace("swap", header=header)
    writer.write(f"inline const {task.name} &{method}()")

    with writer.scope():
        writer.write("encode_swapped(raw());")
        writer.write("return *this;")


def struct_methods(
    task: GenerateTask, writer: IndentedFileWriter, header: bool
) -> None:
    """Write generated-struct methods."""

    if header:
        writer.write("using Buffer = byte_array<size>;")
        writer.write("using Span = byte_span<size>;")
        with writer.padding():
            writer.write(
                f"auto operator<=>(const {task.name} &) const = default;"
            )

    struct_buffer_method(task, writer, header, False)

    if header:
        writer.empty()

    span_method(task, writer, header)

    if header:
        writer.empty()

    struct_buffer_method(task, writer, header, True)

    if task.instance["codec"]:
        writer.empty()
        struct_encode(task, writer, header)

        swap_method(task, writer, header)

        struct_decode(task, writer, header)

    if task.instance["json"]:
        to_json_method(
            task,
            writer,
            protocol_json(task),
            dumps_indent=task.instance["json_indent"],
            task_name=False,
            static=True,
            definition=header,
        )
