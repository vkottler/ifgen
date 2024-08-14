"""
A module implementing Python enum-generation interfaces.
"""

# third-party
from vcorelib.io import IndentedFileWriter

# internal
from ifgen.generation.interface import GenerateTask


def python_enum_header(task: GenerateTask, writer: IndentedFileWriter) -> None:
    """Create a Python module for an enumeration."""

    writer.empty()

    del task
    writer.write("# todo")
