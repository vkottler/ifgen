"""
A module implementing interfaces for struct-file generation.
"""

# built-in
from contextlib import contextmanager
from typing import Dict, Iterable, Iterator, Optional, Union

# third-party
from vcorelib.io import IndentedFileWriter

# internal
from ifgen import PKG_NAME
from ifgen.generation.interface import GenerateTask
from ifgen.struct.methods import struct_methods
from ifgen.struct.test import create_struct_test

__all__ = ["create_struct", "create_struct_test"]
FieldConfig = Dict[str, Union[int, str]]


def trailing_comment(data: str) -> str:
    """Wrap some string data in a doxygen comment."""
    return f" /*!< {data} */"


LineWithComment = tuple[str, Optional[str]]
LinesWithComments = list[LineWithComment]


@contextmanager
def trailing_comment_lines(
    writer: IndentedFileWriter,
) -> Iterator[LinesWithComments]:
    """Align indentations for trailing comments."""

    # Collect lines and comments.
    lines_comments: LinesWithComments = []
    yield lines_comments

    longest = 0
    for line, _ in lines_comments:
        length = len(line)
        if len(line) > longest:
            longest = length

    for line, comment in lines_comments:
        padding = " " * (longest - len(line))
        if comment:
            line += padding + trailing_comment(comment)
        writer.write(line)


def struct_line(name: str, value: FieldConfig) -> LineWithComment:
    """Build a string for a struct-field line."""

    return f"{value['type']} {name};", value.get("description")  # type: ignore


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

    result = {
        header_for_type(config["type"], task)
        for config in task.instance["fields"]
    }

    result.add(f'"../{PKG_NAME}/common.h"')
    result.add("<array>")

    return result


def create_struct(task: GenerateTask) -> None:
    """Create a header file based on a struct definition."""

    with task.boilerplate(includes=struct_includes(task), json=True) as writer:
        attributes = ["gnu::packed"]
        writer.write(f"struct [[{', '.join(attributes)}]] {task.name}")
        with writer.scope(suffix=";"):
            with trailing_comment_lines(writer) as lines:
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

            # Fields.
            with writer.padding():
                with trailing_comment_lines(writer) as lines:
                    for field in task.instance["fields"]:
                        lines.append(struct_line(field.pop("name"), field))

            # Methods.
            struct_methods(task, writer)

        writer.empty()

        # Add size assertion.
        writer.write(
            f"static_assert(sizeof({task.name}) == {task.name}::size);"
        )
