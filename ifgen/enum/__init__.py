"""
A module implementing interfaces for enum-file generation.
"""

# built-in
from typing import Dict, Optional, Union

# internal
from ifgen.generation.interface import GenerateTask

EnumConfig = Optional[Dict[str, Union[int, str]]]


def enum_line(name: str, value: EnumConfig) -> str:
    """Build a string representing a line in an enumeration."""

    line = name

    if value and value.get("value"):
        line += f" = {value['value']}"

    if value and value.get("description"):
        line += f" /*!< {value['description']} */"

    return line


def create_enum(task: GenerateTask) -> None:
    """Create a header file based on an enum definition."""

    with task.boilerplate(includes=["<cstdint>"]) as writer:
        writer.write(f"enum class {task.name} : {task.instance['underlying']}")
        with writer.scope(suffix=";"):
            writer.join(
                *(
                    enum_line(enum, value)
                    for enum, value in task.instance.get("enum", {}).items()
                )
            )
