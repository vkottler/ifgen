"""
A module implementing unit-testing related generation utilities.
"""

from contextlib import contextmanager

# built-in
from os import linesep
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

    linesep.join([f"A unit test for {task.generator} {task.name}."])

    with task.boilerplate(
        includes=["<cassert>", "<cstring>", "<iostream>", f'"{include}"']
        + includes,
        is_test=True,
        use_namespace=False,
        description=linesep.join(
            [
                f"A unit test for {task.generator} {task.name}.",
                "",
                "\\return 0 on success.",
            ]
        ),
    ) as writer:
        writer.write("int main(void)")
        with writer.scope():
            writer.write(f"using namespace {task.namespace()};")
            writer.empty()
            yield writer
            writer.write("return 0;")
