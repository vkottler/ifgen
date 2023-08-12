"""
A module implementing interfaces for enum-file generation.
"""

# internal
from ifgen.generation.interface import GenerateTask


def create_enum(task: GenerateTask) -> None:
    """Create a header file based on an enum definition."""

    with task.boilerplate() as writer:
        assert writer
