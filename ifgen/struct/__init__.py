"""
A module implementing interfaces for struct-file generation.
"""

# built-in
from typing import Any, Dict, Iterable, Union

# third-party
from vcorelib.io.file_writer import (
    CommentStyle,
    IndentedFileWriter,
    LineWithComment,
)

# internal
from ifgen import PKG_NAME
from ifgen.generation.interface import GenerateTask
from ifgen.struct.methods import struct_methods
from ifgen.struct.methods.fields import bit_fields
from ifgen.struct.source import create_struct_source
from ifgen.struct.stream import struct_stream_methods
from ifgen.struct.test import create_struct_test

__all__ = ["create_struct", "create_struct_test", "create_struct_source"]
FieldConfig = Dict[str, Union[int, str]]


def struct_line(
    name: str, value: FieldConfig, volatile: bool
) -> LineWithComment:
    """Build a string for a struct-field line."""

    return ("volatile " if volatile else "") + (  # type: ignore
        f"{value['type']} {name};"
    ), value.get("description")


def header_for_type(name: str, task: GenerateTask) -> str:
    """Determine the header file to import for a given type."""

    candidate = task.custom_include(name)
    if candidate:
        return f'"{candidate}"'

    return ""


def struct_includes(task: GenerateTask) -> Iterable[str]:
    """Determine headers that need to be included for a given struct."""

    result = {
        header_for_type(config["type"], task)
        for config in task.instance["fields"]
    }

    result.add(f'"../{PKG_NAME}/common.h"')

    return result


def struct_fields(task: GenerateTask, writer: IndentedFileWriter) -> None:
    """Generate struct fields."""

    writer.c_comment("Fields.")

    with writer.trailing_comment_lines(style=CommentStyle.C_DOXYGEN) as lines:
        # Fields.
        for field in task.instance["fields"]:
            lines.append(struct_line(field["name"], field, field["volatile"]))

        lines.append(("", None))


def struct_instance(
    task: GenerateTask, writer: IndentedFileWriter, instance: dict[str, Any]
) -> None:
    """Generate struct instances."""

    writer.empty()

    if instance.get("description"):
        with writer.javadoc():
            writer.write(instance["description"])

    type_base = f"{task.name} *"
    writer.write(
        (
            "static "
            + ("volatile " if instance["volatile"] else "")
            + f"{type_base}const "
            f"{instance['name']} = "
            f"reinterpret_cast<{type_base}>({instance['address']});"
        )
    )


def create_struct(task: GenerateTask) -> None:
    """Create a header file based on a struct definition."""

    with task.boilerplate(
        includes=struct_includes(task), json=task.instance.get("json", False)
    ) as writer:
        attributes = ["gnu::packed"]
        writer.write(f"struct [[{', '.join(attributes)}]] {task.name}")
        with writer.scope(suffix=";"):
            writer.c_comment("Constant attributes.")
            with writer.trailing_comment_lines(
                style=CommentStyle.C_DOXYGEN
            ) as lines:
                lines.append(
                    (
                        "static constexpr "
                        f"{task.env.config.data['struct_id_underlying']} "
                        f"id = {task.protocol().id};",
                        f"{task.name}'s identifier.",
                    )
                )
                lines.append(
                    (
                        f"static constexpr std::size_t size = "
                        f"{task.env.types.size(task.name)};",
                        f"{task.name}'s size in bytes.",
                    )
                )

            writer.empty()
            struct_fields(task, writer)

            # Methods.
            writer.c_comment("Methods.")
            struct_methods(task, writer, True)
            bit_fields(task, writer, True)

        # Add size assertion.
        writer.empty()
        writer.write(
            f"static_assert(sizeof({task.name}) == {task.name}::size);"
        )

        if task.instance["stream"]:
            writer.empty()
            struct_stream_methods(task, writer, True)

        for instance in task.instance.get("instances", []):
            struct_instance(task, writer, instance)
