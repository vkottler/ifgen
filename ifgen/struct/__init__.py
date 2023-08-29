"""
A module implementing interfaces for struct-file generation.
"""

# built-in
from typing import Dict, Iterable, Union

# internal
from ifgen.generation.interface import GenerateTask
from ifgen.struct.test import create_struct_test

__all__ = ["create_struct", "create_struct_test"]
FieldConfig = Dict[str, Union[int, str]]


def struct_line(name: str, value: FieldConfig) -> str:
    """Build a string for a struct-field line."""

    result = f"{value['type']} {name};"

    if value.get("description"):
        result += f" /*!< {value['description']} */"

    return result


TYPE_LOOKUP: Dict[str, str] = {}
for _item in [
    "int8_t",
    "int16_t",
    "int32_t",
    "int64_t",
    "uint8_t",
    "uint16_t",
    "uint32_t",
    "uint64_t",
]:
    TYPE_LOOKUP[_item] = "<cstdint>"


def header_for_type(name: str, task: GenerateTask) -> str:
    """Determine the header file to import for a given type."""

    if name in TYPE_LOOKUP:
        return TYPE_LOOKUP[name]

    candidate = task.custom_include(name)
    if candidate:
        return f'"{candidate}"'

    return ""


def struct_includes(task: GenerateTask) -> Iterable[str]:
    """Determine headers that need to be included for a given struct."""

    return {
        header_for_type(config["type"], task)
        for config in task.instance["fields"]
    }


def create_struct(task: GenerateTask) -> None:
    """Create a header file based on a struct definition."""

    with task.boilerplate(includes=struct_includes(task), json=True) as writer:
        attributes = ["gnu::packed"]
        writer.write(f"struct [[{', '.join(attributes)}]] {task.name}")
        with writer.scope(suffix=";"):
            for field in task.instance["fields"]:
                writer.write(struct_line(field.pop("name"), field))

        writer.empty()

        # Add size assertion.
        writer.write(
            (
                f"static_assert(sizeof({task.name}) "
                f"== {task.env.types.size(task.name)});"
            )
        )
