"""
A module for generating static map data structures related to enumerations.
"""

# third-party
from vcorelib.io import IndentedFileWriter

# internal
from ifgen.generation.interface import GenerateTask


def enum_to_string_map(task: GenerateTask, writer: IndentedFileWriter) -> None:
    """Create a static map for enum to string conversion."""

    inst = f"{task.name}_to_string"
    writer.write(
        f"static const std::map<{task.name}, const char *> {inst} = " + "{"
    )

    for enum in task.instance.get("enum", {}):
        with writer.indented():
            writer.write("{" + f'{task.name}::{enum}, "{enum}"' + "},")

    writer.write("};")


def enum_from_string_map(
    task: GenerateTask, writer: IndentedFileWriter
) -> None:
    """Create a static map for string to enum conversion."""

    inst = f"{task.name}_from_string"
    writer.write(
        f"static const std::map<const std::string, {task.name}> {inst} = "
        + "{"
    )

    for enum in task.instance.get("enum", {}):
        with writer.indented():
            writer.write("{" + f'"{enum}", {task.name}::{enum}' + "},")

    writer.write("};")
