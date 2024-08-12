"""
A module implementing interfaces for struct-file generation.
"""

# built-in
from contextlib import ExitStack
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
    name: str,
    value: FieldConfig,
    volatile: bool,
    const: bool,
    array_length: int = None,
) -> LineWithComment:
    """Build a string for a struct-field line."""

    line = f"{value['type']} {name}"
    if array_length is not None:
        line += f"[{name}_length]"

    prefix = "volatile " if volatile else ""
    prefix += "const " if const else ""

    if const:
        line += " = {}"

    return prefix + f"{line};", value.get("description")  # type: ignore


def header_for_type(name: str, task: GenerateTask) -> str:
    """Determine the header file to import for a given type."""

    candidate = task.custom_include(name)
    if candidate:
        return f'"{candidate}"'

    return ""


def struct_includes(task: GenerateTask) -> Iterable[str]:
    """Determine headers that need to be included for a given struct."""

    result = set()
    for config in task.instance["fields"]:
        if "type" in config:
            result.add(header_for_type(config["type"], task))

        # Add includes for bit-fields.
        for bit_field in config.get("fields", []):
            if "type" in bit_field:
                result.add(header_for_type(bit_field["type"], task))

        # Add includes for alternates.
        for alternate in config.get("alternates", []):
            for alternate_bit_field in alternate.get("fields", []):
                if "type" in alternate_bit_field:
                    result.add(
                        header_for_type(alternate_bit_field["type"], task)
                    )

    result.add(f'"../{PKG_NAME}/common.h"')

    return result


def struct_fields(task: GenerateTask, writer: IndentedFileWriter) -> None:
    """Generate struct fields."""

    writer.c_comment("Fields.")

    with writer.trailing_comment_lines(style=CommentStyle.C_DOXYGEN) as lines:
        # Fields.
        for field in task.instance["fields"]:
            enforce_expected_size(
                task.env.size(field["type"]) * field.get("array_length", 1),
                field,
                f"{task.name}.{field['name']}",
            )

            if "array_length" in field:
                lines.append(
                    (
                        (
                            f"static constexpr std::size_t "
                            f"{field['name']}_length = "
                            f"{field['array_length']};"
                        ),
                        None,
                    )
                )

            with ExitStack() as stack:
                is_union = field.get("alternates")
                all_fields = [field]
                if is_union:
                    writer.write("union")
                    stack.enter_context(writer.scope(suffix=";"))
                    all_fields.extend(field["alternates"])

                for possible_union in all_fields:
                    if "type" not in possible_union:
                        possible_union["type"] = field["type"]

                    line, comment = struct_line(
                        possible_union["name"],
                        possible_union,
                        possible_union["volatile"],
                        possible_union["const"],
                        array_length=possible_union.get("array_length"),
                    )
                    if is_union:
                        writer.write(
                            line + ("" if not comment else f" /* {comment} */")
                        )
                    else:
                        lines.append((line, comment))

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


def enforce_expected_size(
    size: int, data: dict[str, Any], assert_msg: str
) -> None:
    """Enforce an expected-size field."""

    # If expected size is set, verify it.
    if "expected_size" in data:
        assert data["expected_size"] == size, (
            assert_msg,
            data["expected_size"],
            size,
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
                if task.instance["identifier"]:
                    underlying = task.env.config.data["struct"][
                        "id_underlying"
                    ]
                    lines.append(
                        (
                            "static constexpr "
                            f"{underlying} "
                            f"id = {task.protocol().id};",
                            f"{task.name}'s identifier.",
                        )
                    )

                size = task.env.size(task.name)
                enforce_expected_size(size, task.instance, task.name)

                lines.append(
                    (
                        f"static constexpr std::size_t size = {size};",
                        f"{task.name}'s size in bytes.",
                    )
                )

            writer.empty()
            struct_fields(task, writer)

            # Methods.
            writer.c_comment("Methods.")

            if task.instance["methods"]:
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
