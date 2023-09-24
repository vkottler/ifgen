"""
A module for implementing struct stream-related methods.
"""

# third-party
from vcorelib.io.file_writer import IndentedFileWriter

# internal
from ifgen.generation.interface import GenerateTask


def struct_istream(
    task: GenerateTask, writer: IndentedFileWriter, header: bool
) -> None:
    """Generate an input-stream handling method."""

    writer.write(
        (
            "byte_istream &operator>>"
            f"(byte_istream &stream, {task.name} &instance)"
        )
        + (";" if header else "")
    )

    if header:
        return

    with writer.scope():
        writer.write(
            f"stream.read(instance.raw()->data(), {task.name}::size);"
        )
        writer.write("return stream;")


def struct_ostream(
    task: GenerateTask, writer: IndentedFileWriter, header: bool
) -> None:
    """Generate an output-stream handling method."""

    writer.write(
        (
            "byte_ostream &operator<<"
            f"(byte_ostream &stream, const {task.name} &instance)"
        )
        + (";" if header else "")
    )

    if header:
        return

    with writer.scope():
        writer.write(
            f"stream.write(instance.raw_ro()->data(), {task.name}::size);"
        )
        writer.write("return stream;")


def struct_stream_methods(
    task: GenerateTask, writer: IndentedFileWriter, header: bool
) -> None:
    """Generate struct stream read and write methods."""

    writer.c_comment("Stream interfaces.")

    struct_istream(task, writer, header)

    if not header:
        writer.empty()

    struct_ostream(task, writer, header)
