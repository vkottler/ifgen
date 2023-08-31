"""
A module implementing interfaces for byte-swapping method generation.
"""

# third-party
from vcorelib.io import IndentedFileWriter

# internal
from ifgen.generation.interface import GenerateTask


def swap_fields(
    task: GenerateTask, writer: IndentedFileWriter, is_decode: bool = True
) -> None:
    """Perform byte swaps on individual struct fields."""

    writer.write("std::size_t offset = 0;")
    writer.write("(void)buffer;")
    writer.write("(void)offset;")

    for field in task.instance["fields"]:
        size = task.env.size(field["type"])
        name = field["name"]
        kind = field["type"]

        writer.empty()
        writer.c_comment(f"{kind} {name}")

        if task.env.is_struct(kind):
            writer.write(
                f"{name}.{'decode' if is_decode else 'encode'}_swapped("
            )

            pointer = f"{kind}::Buffer *"
            if is_decode:
                pointer = "const " + pointer

            arg = f"*reinterpret_cast<{pointer}>"
            arg += "(&buffer[offset])"
            writer.write(f"    {arg});")

        writer.write(f"offset += {size};")


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
        swap_fields(task, writer, is_decode=False)
