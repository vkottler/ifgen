"""
A module for struct-encoding methods.
"""

# third-party
from vcorelib.io import IndentedFileWriter

# internal
from ifgen.generation.interface import GenerateTask
from ifgen.struct.methods.common import wrapper_method
from ifgen.struct.methods.swap import encode_swapped_method


def encode_method(
    task: GenerateTask, writer: IndentedFileWriter, header: bool
) -> None:
    """Write boilerplate encode method."""

    if header:
        with writer.javadoc():
            writer.write("Encode this instance to a buffer.")
            writer.empty()
            writer.write(
                task.command("param[out]", "buffer     Buffer to write.")
            )
            writer.write(
                task.command(
                    "param[in]",
                    " endianness Byte order for encoding elements.",
                )
            )
            writer.write(
                task.command(
                    "return", "               The number of bytes encoded."
                )
            )

    wrapper_method(task, writer, header)


def struct_encode(
    task: GenerateTask, writer: IndentedFileWriter, header: bool
) -> None:
    """Add a method for encoding structs."""

    encode_swapped_method(task, writer, header)
    writer.empty()
    encode_method(task, writer, header)
