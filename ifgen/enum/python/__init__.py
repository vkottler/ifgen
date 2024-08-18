"""
A module implementing Python enum-generation interfaces.
"""

# third-party
from runtimepy.enum.registry import DEFAULT_ENUM_PRIMITIVE
from vcorelib.io import IndentedFileWriter

# internal
from ifgen.generation.interface import GenerateTask
from ifgen.generation.python import (
    python_class,
    python_function,
    python_imports,
)


def strip_t_suffix(data: str) -> str:
    """Strip a possible '_t' suffix from a string."""
    return data.replace("_t", "") if data.endswith("_t") else data


def uses_auto(task: GenerateTask) -> bool:
    """
    Determine if a generation task will require 'auto' from the enum module.
    """

    result = False

    for value in task.instance.get("enum", {}).values():
        if not value or "value" not in value:
            result = True
            break

    return result


def to_enum_name(data: str) -> str:
    """Ensure a candidate name string is suitable as an enumeration name."""
    return data.upper()


def python_enum_header(task: GenerateTask, writer: IndentedFileWriter) -> None:
    """Create a Python module for an enumeration."""

    built_in = {}
    if uses_auto(task):
        built_in["enum"] = ["auto"]

    # Write imports.
    python_imports(
        writer,
        third_party={"runtimepy.enum.registry": ["RuntimeIntEnum"]},
        built_in=built_in,
    )

    with python_class(
        writer,
        task.name,
        task.resolve_description() or "No description.",
        parents=["RuntimeIntEnum"],
        final_empty=0,
    ):
        underlying = strip_t_suffix(task.instance["underlying"])

        if underlying != DEFAULT_ENUM_PRIMITIVE:
            with python_function(
                writer,
                "primitive",
                "The underlying primitive type for this runtime enumeration.",
                params="cls",
                return_type="str",
                final_empty=1,
                decorators=["classmethod"],
            ):
                writer.write(f'return "{underlying}"')

        for enum, value in task.instance.get("enum", {}).items():
            final = "auto()"
            if value:
                final = value.get("value", final)

            line = f"{to_enum_name(enum)} = {final}"
            if value and "description" in value:
                line += f"  # {value['description']}"

            writer.write(line)
