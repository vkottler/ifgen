"""
A module implementing interfaces for enum-file generation.
"""

# internal
from ifgen.enum.header import enum_header
from ifgen.enum.source import create_enum_source
from ifgen.enum.test import create_enum_test
from ifgen.generation.interface import GenerateTask

__all__ = ["create_enum", "create_enum_source", "create_enum_test"]


def create_enum(task: GenerateTask) -> None:
    """Create a header file based on an enum definition."""

    includes = ["<cstdint>"]
    if not task.instance["use_map"]:
        includes.append("<cstring>")

    with task.boilerplate(
        includes=includes, json=task.instance["json"]
    ) as writer:
        enum_header(task, writer)
