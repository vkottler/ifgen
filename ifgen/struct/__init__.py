"""
A module implementing interfaces for struct-file generation.
"""

# built-in
from typing import Dict, Iterable, Union

# third-party
from vcorelib.io.file_writer import CommentStyle, LineWithComment

# internal
from ifgen import PKG_NAME
from ifgen.generation.interface import GenerateTask
from ifgen.struct.methods import struct_methods
from ifgen.struct.source import create_struct_source
from ifgen.struct.stream import struct_stream_methods
from ifgen.struct.test import create_struct_test

__all__ = ["create_struct", "create_struct_test", "create_struct_source"]
FieldConfig = Dict[str, Union[int, str]]


def struct_line(name: str, value: FieldConfig) -> LineWithComment:
    """Build a string for a struct-field line."""

    return f"{value['type']} {name};", value.get("description")  # type: ignore


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


def create_struct(task: GenerateTask) -> None:
    """Create a header file based on a struct definition."""

    with task.boilerplate(includes=struct_includes(task), json=True) as writer:
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
            writer.c_comment("Fields.")

            with writer.trailing_comment_lines(
                style=CommentStyle.C_DOXYGEN
            ) as lines:
                # Fields.
                for field in task.instance["fields"]:
                    lines.append(struct_line(field["name"], field))

                lines.append(("", None))

            # Methods.
            writer.c_comment("Methods.")
            struct_methods(task, writer, True)

        # Add size assertion.
        with writer.padding():
            writer.write(
                f"static_assert(sizeof({task.name}) == {task.name}::size);"
            )

        struct_stream_methods(task, writer, True)
