"""
A module implementing interfaces for struct-file generation.
"""

# built-in
from multiprocessing import Pool
from pathlib import Path
from typing import Any, Dict, NamedTuple

# internal
from ifgen.config import Config

StructConfig = Dict[str, Any]


class GenerateStructTask(NamedTuple):
    """Parameters necessary for struct generation."""

    path: Path
    struct: StructConfig


def create_struct(task: GenerateStructTask) -> None:
    """Create a header file based on a struct definition."""

    print(task)


def generate_structs(output: Path, config: Config) -> None:
    """Generate struct files."""

    pool = Pool()  # pylint: disable=consider-using-with
    try:
        pool.map(
            create_struct,
            (
                GenerateStructTask(output.joinpath(f"{name}.h"), data)
                for name, data in config.data["structs"].items()
            ),
        )
    finally:
        pool.close()
        pool.join()
