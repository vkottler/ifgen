"""
A module implementing unit-testing related generation utilities.
"""

# built-in
from contextlib import contextmanager
from typing import Iterator, List

# third-party
from vcorelib.io import IndentedFileWriter

# internal
from ifgen.generation.interface import GenerateTask


@contextmanager
def unit_test_boilerplate(
    task: GenerateTask, includes: List[str] = None
) -> Iterator[IndentedFileWriter]:
    """Handle standard unit-test boilerplate."""

    include = task.env.rel_include(task.name, task.generator)

    if includes is None:
        includes = []

    with task.boilerplate(
        includes=["<cassert>", "<cstring>", "<iostream>", f'"{include}"']
        + includes,
        is_test=True,
        use_namespace=False,
        description=f"A unit test for {task.generator} {task.name}.",
    ) as writer:
        writer.write("int main(void)")
        with writer.scope():
            writer.write(f"using namespace {task.namespace()};")
            writer.empty()
            yield writer
            writer.write("return 0;")
