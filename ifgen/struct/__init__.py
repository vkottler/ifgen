"""
A module implementing interfaces for struct-file generation.
"""

# internal
from ifgen.generation.interface import GenerateTask


def create_struct(task: GenerateTask) -> None:
    """Create a header file based on a struct definition."""

    with task.boilerplate() as writer:
        writer.write(f"struct {task.name}")
        with writer.scope(suffix=";"):
            writer.cpp_comment("Body.")
