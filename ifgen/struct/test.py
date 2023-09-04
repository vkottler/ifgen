"""
A module implementing a unit-test output generator for structs.
"""

# third-party
from vcorelib.io import IndentedFileWriter

# internal
from ifgen.generation.interface import GenerateTask
from ifgen.generation.test import (
    unit_test_boilerplate,
    unit_test_main,
    unit_test_method,
    unit_test_method_name,
)


def unit_test_basic_method(
    task: GenerateTask, writer: IndentedFileWriter
) -> None:
    """
    Implement a simple encode-and-decode scenario with endianness as a
    function argument.
    """

    with unit_test_method("encode_decode_basic", task, writer):
        writer.write("(void)endianness;")
        writer.empty()

        writer.cpp_comment(f"{task.name} src;")


def unit_test_body(task: GenerateTask, writer: IndentedFileWriter) -> None:
    """Implement a unit test for a struct."""

    for method in ["encode_decode_basic"]:
        for arg in [
            "std::endian::native",
            "std::endian::little",
            "std::endian::big",
        ]:
            name = unit_test_method_name(method, task)
            writer.write(f"{name}({arg});")

        writer.empty()

    writer.c_comment("Attempt to decode this?")
    writer.write(f"std::cout << {task.name}::json();")


def create_struct_test(task: GenerateTask) -> None:
    """Create a unit test for the enum string-conversion methods."""

    with unit_test_boilerplate(task, main=False) as writer:
        unit_test_basic_method(task, writer)

        writer.empty()

        with unit_test_main(task, writer):
            unit_test_body(task, writer)
