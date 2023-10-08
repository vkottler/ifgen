"""
A module for common enum-generation utilities.
"""

# third-party
from vcorelib.io import IndentedFileWriter

# internal
from ifgen.enum.map import enum_from_string_map, enum_to_string_map
from ifgen.generation.interface import GenerateTask


def enum_to_string(
    task: GenerateTask, writer: IndentedFileWriter, use_map: bool
) -> None:
    """
    Implement an enumeration to string method without using the static map.
    """

    writer.write(f'const char *result = "UNKNOWN {task.name}";')

    with writer.padding():
        if not use_map:
            writer.write("switch (instance)")

            with writer.scope(indent=0):
                for enum in task.instance.get("enum", {}):
                    writer.write(f"case {task.name}::{enum}:")
                    with writer.indented():
                        writer.write(f'result = "{enum}";')
                        writer.write("break;")
        else:
            map_inst = f"{task.name}_to_string"
            writer.write(f"if ({map_inst}.contains(instance))")
            with writer.scope():
                writer.write(f"result = {map_inst}.at(instance);")

    writer.write("return result;")


def enum_to_string_function(
    task: GenerateTask,
    writer: IndentedFileWriter,
    use_map: bool,
    definition: bool = False,
) -> None:
    """Generate a method for converting enum instances to strings."""

    if definition:
        with writer.javadoc():
            writer.write(f"Converts {task.name} to a C string.")
            writer.empty()
            writer.write(
                task.command("param[in]", data="instance Value to convert.")
            )
            writer.write(
                task.command(
                    "return",
                    "            A C string representation of the value.",
                )
            )

    if not definition and use_map:
        enum_to_string_map(task, writer)
        writer.empty()

    line = ""
    if not use_map:
        line = "inline "
    line += f"const char *to_string({task.name} instance)"

    if definition and use_map:
        line += ";"

    writer.write(line)

    if definition and use_map:
        return

    with writer.scope():
        enum_to_string(task, writer, use_map)


def enum_from_string(
    task: GenerateTask, writer: IndentedFileWriter, use_map: bool
) -> None:
    """
    Implement an string to enumeration method without using the static map.
    """

    if not use_map:
        writer.write("bool result = false;")

        with writer.padding():
            first = True
            for enum in task.instance.get("enum", {}):
                line = f'if ((result = !strncmp(data, "{enum}", {len(enum)})))'

                if not first:
                    line = "else " + line
                else:
                    first = False

                writer.write(line)
                with writer.scope():
                    writer.write(f"output = {task.name}::{enum};")

    else:
        map_inst = f"{task.name}_from_string"
        writer.write(f"bool result = {map_inst}.contains(data);")

        with writer.padding():
            writer.write("if (result)")
            with writer.scope():
                writer.write(f"output = {map_inst}.at(data);")

    writer.write("return result;")


def string_to_enum_function(
    task: GenerateTask,
    writer: IndentedFileWriter,
    use_map: bool,
    definition: bool = False,
) -> None:
    """Generate a method for converting string instances to enums."""

    if definition:
        with writer.javadoc():
            writer.write(f"Converts a C string to {task.name}.")
            writer.empty()
            writer.write(
                task.command("param[in]", " data   A C string to convert.")
            )
            writer.write(
                task.command(
                    "param[out]",
                    "output The enumeration element to write.",
                )
            )
            writer.write(
                task.command(
                    "return",
                    "           Whether or not the output was written.",
                )
            )

    if not definition and use_map:
        enum_from_string_map(task, writer)
        writer.empty()

    line = ""
    if not use_map:
        line = "inline "

    line += f"bool from_string(const char *data, {task.name} &output)"

    if definition and use_map:
        line += ";"

    writer.write(line)

    if definition and use_map:
        return

    with writer.scope():
        enum_from_string(task, writer, use_map)
