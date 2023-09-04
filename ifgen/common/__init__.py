"""
A module for generating shared headers and sources.
"""

# internal
from ifgen.generation.interface import GenerateTask
from ifgen.generation.test import unit_test_boilerplate


def create_common_test(task: GenerateTask) -> None:
    """Create a unit test for the enum string-conversion methods."""

    with unit_test_boilerplate(task) as writer:
        writer.cpp_comment("TODO.")


def create_common(task: GenerateTask) -> None:
    """Create a unit test for the enum string-conversion methods."""

    streams = task.stream_implementation

    includes = ["<cstdint>", "<bit>"]
    if streams:
        includes.extend(["<streambuf>", "<istream>", "<ostream>"])

    with task.boilerplate(includes=includes) as writer:
        writer.c_comment("Enforce that this isn't a mixed-endian system.")
        writer.write(
            "static_assert(std::endian::native == std::endian::big or"
        )
        writer.write(
            "              std::endian::native == std::endian::little);"
        )

        writer.empty()

        writer.write("using byte = uint8_t;")
        if streams:
            writer.write("using byte_streambuf = std::basic_streambuf<byte>;")
            writer.write("using byte_istream = std::basic_istream<byte>;")
            writer.write("using byte_ostream = std::basic_ostream<byte>;")
