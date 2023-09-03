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

    with task.boilerplate(includes=["<bit>"]) as writer:
        writer.c_comment("Enforce that this isn't a mixed-endian system.")
        writer.write(
            "static_assert(std::endian::native == std::endian::big or"
        )
        writer.write(
            "              std::endian::native == std::endian::little);"
        )
