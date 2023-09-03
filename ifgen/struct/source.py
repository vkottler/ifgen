"""
A module for generating struct source files.
"""

# internal
from ifgen.generation.interface import GenerateTask
from ifgen.struct.methods import struct_methods


def create_struct_source(task: GenerateTask) -> None:
    """Create a header file based on a struct definition."""

    with task.source_boilerplate([]) as writer:
        struct_methods(task, writer, False)
