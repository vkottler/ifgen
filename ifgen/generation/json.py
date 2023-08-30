"""
A module for generating methods that store JSON strings.
"""

# built-in
from json import dumps
from os import linesep
from textwrap import wrap
from typing import Any

# third-party
from vcorelib.io import IndentedFileWriter

# internal
from ifgen.generation.interface import GenerateTask


def to_json_method(
    task: GenerateTask,
    writer: IndentedFileWriter,
    data: dict[str, Any],
    task_name: bool = True,
    static: bool = False,
    dumps_indent: int = None,
) -> None:
    """Create a _json() method for a given task."""

    with writer.javadoc():
        writer.write(f"A JSON C string describing {task.name}.")

    method_name = "json"
    if task_name:
        method_name = f"{task.name}_" + method_name

    line = f"const char *{method_name}()"
    if static:
        line = "static " + line

    writer.write(line)
    with writer.scope():
        return_line = "return "
        indent = 0

        raw = dumps(
            data,
            separators=(",", ":"),
            indent=dumps_indent,
            sort_keys=True,
        )

        if dumps_indent is None:
            lines = wrap(raw, 40)
        else:
            lines = raw.split(linesep)

        for line in lines:
            line = line.replace('"', '\\"')

            # Add a newline inside of the output string.
            if dumps_indent is not None:
                line += "\\n"

            return_line += f'{" " * indent}"{line}"{linesep}'

            if indent == 0:
                indent = len("return ")

        writer.write(return_line.rstrip() + ";")
