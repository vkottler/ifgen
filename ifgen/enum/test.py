"""
A module implementing a unit-test output generator for enums.
"""

# third-party
from vcorelib.io import IndentedFileWriter

# internal
from ifgen.generation.interface import GenerateTask


def unit_test_body(task: GenerateTask, writer: IndentedFileWriter) -> None:
    """Implement a simple unit test for the enumeration."""

    writer.write(f"using namespace {task.namespace()};")

    writer.empty()

    for enum in task.instance.get("enum", {}):
        to_string = f"to_string({task.name}::{enum})"
        writer.write(f"std::cout << {to_string} << std::endl;")
        writer.write(f'assert(!strcmp({to_string}, "{enum}"));')
        writer.empty()


def create_enum_test(task: GenerateTask) -> None:
    """Create a unit test for the enum string-conversion methods."""

    include = task.env.rel_include(task.name, task.generator)

    with task.boilerplate(
        includes=["<cassert>", "<cstring>", "<iostream>", f'"{include}"'],
        is_test=True,
        use_namespace=False,
        description=f"A unit test for {task.generator} {task.name}.",
    ) as writer:
        writer.write("int main(void)")
        with writer.scope():
            unit_test_body(task, writer)
            writer.write("return 0;")
