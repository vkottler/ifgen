"""
A module implementing interfaces for enum-file generation.
"""

# built-in
from typing import Dict, Optional, Union

# third-party
from vcorelib.io import IndentedFileWriter

# internal
from ifgen.enum.test import create_enum_test
from ifgen.generation.interface import GenerateTask

EnumConfig = Optional[Dict[str, Union[int, str]]]

__all__ = ["create_enum", "create_enum_test"]


def enum_line(name: str, value: EnumConfig) -> str:
    """Build a string representing a line in an enumeration."""

    line = name

    if value and value.get("value"):
        line += f" = {value['value']}"

    if value and value.get("description"):
        line += f" /*!< {value['description']} */"

    return line


def enum_to_string_function(
    task: GenerateTask, writer: IndentedFileWriter
) -> None:
    """Generate a method for converting enum instances to strings."""

    with writer.javadoc():
        writer.write(f"Converts {task.name} to a C string.")

    writer.write(f"inline const char *to_string({task.name} instance)")
    with writer.scope():
        writer.write(f'const char *result = "UNKNOWN {task.name}";')

        with writer.padding():
            writer.write("switch (instance)")

            with writer.scope(indent=0):
                for enum in task.instance.get("enum", {}):
                    writer.write(f"case {task.name}::{enum}:")
                    with writer.indented():
                        writer.write(f'result = "{enum}";')
                        writer.write("break;")

        writer.write("return result;")


def create_enum(task: GenerateTask) -> None:
    """Create a header file based on an enum definition."""

    with task.boilerplate(includes=["<cstdint>"], json=True) as writer:
        writer.write(f"enum class {task.name} : {task.instance['underlying']}")
        with writer.scope(suffix=";"):
            writer.join(
                *(
                    enum_line(enum, value)
                    for enum, value in task.instance.get("enum", {}).items()
                )
            )

        writer.empty()
        enum_to_string_function(task, writer)
