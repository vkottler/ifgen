"""
A module implementing interfaces for generating Python sources that aggregate
common resources.
"""

# internal
from ifgen.generation.interface import GenerateTask
from ifgen.generation.python import python_function, python_imports


def create_python_common(task: GenerateTask) -> None:
    """Create a Python module that aggregates runtime registration tasks."""

    with task.boilerplate() as writer:
        # Write imports.
        python_imports(
            writer, third_party={"runtimepy.enum.registry": ["EnumRegistry"]}
        )

        with python_function(
            writer,
            "register_enums",
            "Register generated enumerations.",
            params="registry: EnumRegistry",
        ):
            writer.write("# iterate over all custom enums, register each")
            writer.empty()
            writer.write("del registry")

        writer.write("# base class for structs that auto registers enums?")
