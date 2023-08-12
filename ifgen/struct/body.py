"""
A module for writing the body of a struct.
"""

# third-party
from vcorelib.io import IndentedFileWriter

# internal
from ifgen.struct.task import GenerateStructTask


def struct_body(writer: IndentedFileWriter, task: GenerateStructTask) -> None:
    """Write the body of a struct."""

    del task
    writer.cpp_comment("Body.")
