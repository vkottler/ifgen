"""
A module implementing interfaces for generating Python sources that aggregate
common resources.
"""

# internal
from ifgen.generation.interface import GenerateTask


def create_python_common(task: GenerateTask) -> None:
    """Create a Python module that aggregates runtime registration tasks."""

    with task.boilerplate() as writer:
        # Add registration function for all generated enumerations. Some base
        # class for structs that registers the generated enumerations?
        writer.empty()
        writer.write("# todo")
