"""
A module implementing a unit-test output generator for enums.
"""

# third-party
from vcorelib.io import IndentedFileWriter

# internal
from ifgen.generation.interface import GenerateTask
from ifgen.generation.test import unit_test_boilerplate


def unit_test_body(task: GenerateTask, writer: IndentedFileWriter) -> None:
    """Implement a simple unit test for the enumeration."""

    for enum in task.instance.get("enum", {}):
        to_string = f"to_string({task.name}::{enum})"
        writer.write(f"std::cout << {to_string} << std::endl;")
        writer.write(f'assert(!strcmp({to_string}, "{enum}"));')
        writer.empty()


def create_enum_test(task: GenerateTask) -> None:
    """Create a unit test for the enum string-conversion methods."""

    with unit_test_boilerplate(task) as writer:
        unit_test_body(task, writer)
