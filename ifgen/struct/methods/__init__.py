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


def struct_methods(task: GenerateTask, writer: IndentedFileWriter) -> None:
    """Write generated-struct methods."""

    writer.write("using Buffer = std::array<uint8_t, size>;")
    writer.empty()

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
