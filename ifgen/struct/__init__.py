"""
A module implementing interfaces for struct-file generation.
"""

# built-in
from multiprocessing import Pool
from pathlib import Path
from typing import Any, Dict, NamedTuple

# third-party
from vcorelib.io import IndentedFileWriter

# internal
from ifgen.config import Config

StructConfig = Dict[str, Any]


class GenerateStructTask(NamedTuple):
    """Parameters necessary for struct generation."""

    root: Path
    path: Path
    struct: StructConfig


def create_struct(task: GenerateStructTask) -> None:
    """Create a header file based on a struct definition."""

    with IndentedFileWriter.from_path(task.path, per_indent=4) as writer:
        with writer.javadoc():
            writer.write("Test.")


def generate_structs(root: Path, output: Path, config: Config) -> None:
    """Generate struct files."""

    output.mkdir(parents=True, exist_ok=True)

    pool = Pool()  # pylint: disable=consider-using-with
    try:
        pool.map(
            create_struct,
            (
                GenerateStructTask(root, output.joinpath(f"{name}.h"), data)
                for name, data in config.data["structs"].items()
            ),
        )
    finally:
        pool.close()
        pool.join()
