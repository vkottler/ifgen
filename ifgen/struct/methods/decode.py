"""
A module for struct-decoding methods.
"""

# third-party
from vcorelib.io import IndentedFileWriter

# internal
from ifgen.generation.interface import GenerateTask
from ifgen.struct.methods.common import wrapper_method
from ifgen.struct.methods.swap import decode_swapped_method


def decode_method(
    task: GenerateTask, writer: IndentedFileWriter, header: bool
) -> None:
    """Write boilerplate decode method."""

    if header:
        with writer.javadoc():
            writer.write("Update this instance from a buffer.")
            writer.empty()
            writer.write(
                task.command("param[in]", "buffer     Buffer to read.")
            )
            writer.write(
                task.command(
                    "param[in]",
                    "endianness Byte order from decoding elements.",
                )
            )
            writer.write(
                task.command(
                    "return", "              The number of bytes decoded."
                )
            )

    wrapper_method(task, writer, header, is_encode=False)


def struct_decode(
    task: GenerateTask, writer: IndentedFileWriter, header: bool
) -> None:
    """Add a method for decoding structs."""

    with writer.padding():
        decode_swapped_method(task, writer, header)

    decode_method(task, writer, header)
