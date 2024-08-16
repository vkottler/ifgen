"""
A module implementing Python enum-generation interfaces.
"""

# third-party
from vcorelib.io import IndentedFileWriter

# internal
from ifgen.generation.interface import GenerateTask
from ifgen.generation.python import python_class, python_imports


def python_enum_header(task: GenerateTask, writer: IndentedFileWriter) -> None:
    """Create a Python module for an enumeration."""

    # Write imports.
    python_imports(
        writer, third_party={"runtimepy.enum.registry": ["RuntimeIntEnum"]}
    )

    writer.empty()
    writer.empty()

    with python_class(
        writer, task.name, docstring="TODO.", parents=["RuntimeIntEnum"]
    ):
        # Add members.
        writer.write("# todo")
