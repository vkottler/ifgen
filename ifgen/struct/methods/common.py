"""
Utilities shared between struct methods.
"""

# third-party
from vcorelib.io import IndentedFileWriter


def wrapper_method(writer: IndentedFileWriter, is_encode: bool = True) -> None:
    """Create a generic encode/decode method."""

    method = "encode" if is_encode else "decode"

    line = f"inline void {method}("

    writer.write(
        line
        + ("const " if not is_encode else "")
        + "Buffer "
        + ("&" if not is_encode else "")
        + "&buffer,"
    )
    writer.write(
        " " * len(line) + "std::endian endianness = std::endian::native)"
    )
    with writer.scope():
        writer.write("if (endianness == std::endian::native)")
        with writer.scope():
            writer.write(f"{method}_native(buffer);")
        writer.write("else")
        with writer.scope():
            writer.write(f"{method}_swapped(buffer);")
