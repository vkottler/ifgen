"""
A module implementing an interface for generating bit-field methods for
structs.
"""

# built-in
from typing import Any

# third-party
from vcorelib.io.file_writer import IndentedFileWriter

# internal
from ifgen.generation.interface import GenerateTask


def bit_field(
    task: GenerateTask,
    field: dict[str, Any],
    writer: IndentedFileWriter,
    header: bool,
) -> None:
    """Generate for an individual bit-field."""

    del task
    del writer
    del header

    # validate index + width + type ?

    # type
    # index
    # width

    assert field["read"] or field["write"], field

    # Generate a 'get' method.
    if field["read"]:
        method = f"get_{field['name']}"
        print(method)

    # Generate a 'set' method.
    if field["write"]:
        method = f"set_{field['name']}"
        print(method)


def bit_fields(
    task: GenerateTask, writer: IndentedFileWriter, header: bool
) -> None:
    """Generate bit-field lines."""

    for field in task.instance["fields"]:
        for bfield in field.get("fields", []):
            bit_field(task, bfield, writer, header)
