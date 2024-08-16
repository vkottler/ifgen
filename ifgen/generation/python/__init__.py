"""
A module implementing code-generation interfaces for Python.
"""

# built-in
from contextlib import contextmanager
from typing import Iterator

# third-party
from vcorelib.io import IndentedFileWriter

PythonImports = dict[str, list[str]]


def write_imports(
    writer: IndentedFileWriter,
    label: str,
    imports: PythonImports,
) -> None:
    """Write a group of Python imports to a file."""

    writer.empty()
    writer.write(f"# {label}")
    for key, values in imports.items():
        writer.write(f"from {key} import {', '.join(values)}")


def python_imports(
    writer: IndentedFileWriter, third_party: PythonImports = None
) -> None:
    """Write Python-module imports."""

    if third_party:
        write_imports(writer, "third-party", third_party)


@contextmanager
def python_class(
    writer: IndentedFileWriter,
    name: str,
    docstring: str,
    parents: list[str] = None,
) -> Iterator[None]:
    """Write class definition contents."""

    line = f"class {name}"
    if parents:
        line += f"({', '.join(parents)})"
    line += ":"

    writer.write(line)
    with writer.indented():
        writer.write(f'"""{docstring}"""')
        writer.empty()
        yield
