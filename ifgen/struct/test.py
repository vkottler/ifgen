"""
A module implementing a unit-test output generator for structs.
"""

# third-party
from vcorelib.io import IndentedFileWriter

# internal
from ifgen.generation.interface import GenerateTask
from ifgen.generation.test import unit_test_boilerplate


def unit_test_body(task: GenerateTask, writer: IndentedFileWriter) -> None:
    """Implement a unit test for a struct."""

    writer.c_comment("Attempt to decode this?")
    writer.write(f"std::cout << {task.name}::json();")


def create_struct_test(task: GenerateTask) -> None:
    """Create a unit test for the enum string-conversion methods."""

    with unit_test_boilerplate(task) as writer:
        unit_test_body(task, writer)
        writer.empty()
