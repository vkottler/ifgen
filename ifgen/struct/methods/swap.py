"""
A module implementing interfaces for byte-swapping method generation.
"""

# third-party
from vcorelib.io import IndentedFileWriter

from ifgen.generation.comments import trailing_comment_lines

# internal
from ifgen.generation.interface import GenerateTask


def swap_fields(task: GenerateTask, writer: IndentedFileWriter) -> None:
    """Perform byte swaps on individual struct fields."""

    writer.write("(void)buffer;")
    writer.empty()

    writer.write("std::size_t offset = 0;")

    with trailing_comment_lines(writer) as lines:
        for field in task.instance["fields"]:
            size = task.env.size(field["type"])
            lines.append(
                (f"offset += {size};", f"{field['name']} {field['type']}")
            )

    writer.empty()
    writer.write("(void)offset;")


def decode_swapped_method(
    task: GenerateTask, writer: IndentedFileWriter
) -> None:
    """Generate a struct-decode method that uses swapped byte order."""

    with writer.javadoc():
        writer.write("Decode using byte-order swapped from native.")
        writer.empty()
        writer.write("\\param[in] buffer Buffer to read.")

    writer.write("inline void decode_swapped(const Buffer &buffer)")
    with writer.scope():
        swap_fields(task, writer)


def encode_swapped_method(
    task: GenerateTask, writer: IndentedFileWriter
) -> None:
    """Generate a struct-encode method that uses swapped byte order."""

    with writer.javadoc():
        writer.write("Encode using byte-order swapped from native.")
        writer.empty()
        writer.write("\\param[out] buffer Buffer to write.")

    writer.write("inline void encode_swapped(Buffer &buffer)")
    with writer.scope():
        swap_fields(task, writer)
