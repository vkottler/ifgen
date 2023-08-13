"""
A module implementing interfaces to facilitate code generation.
"""

# built-in
from multiprocessing.pool import ThreadPool
from pathlib import Path

# internal
from ifgen.config import Config
from ifgen.enum import create_enum
from ifgen.generation.interface import GenerateTask, GeneratorMap
from ifgen.struct import create_struct

GENERATORS: GeneratorMap = {
    "structs": create_struct,
    "enums": create_enum,
}


def generate(root: Path, output: Path, config: Config) -> None:
    """Generate struct files."""

    # Create output directories.
    for subdir in GENERATORS:
        output.joinpath(subdir).mkdir(parents=True, exist_ok=True)

    pool = ThreadPool()  # pylint: disable=consider-using-with
    for gen_name, generator in GENERATORS.items():
        pool.map(
            generator,
            (
                GenerateTask(
                    name,
                    root,
                    output.joinpath(gen_name, f"{name}.h"),
                    data,
                    config.data,
                )
                for name, data in config.data.get(gen_name, {}).items()
            ),
        )
    pool.close()
    pool.join()
