"""
A module implementing interfaces to facilitate code generation.
"""

# built-in
from multiprocessing.pool import ThreadPool
from pathlib import Path

# internal
from ifgen.config import Config
from ifgen.enum import create_enum
from ifgen.generation.interface import GenerateTask, Generator, GeneratorMap
from ifgen.struct import create_struct

GENERATORS: GeneratorMap = {
    Generator.STRUCTS: create_struct,
    Generator.ENUMS: create_enum,
}


def generate(root: Path, output: Path, config: Config) -> None:
    """Generate struct files."""

    # Create output directories.
    for subdir in Generator:
        output.joinpath(subdir).mkdir(parents=True, exist_ok=True)

    with ThreadPool() as pool:
        for generator, method in GENERATORS.items():
            pool.map(
                method,
                (
                    GenerateTask(
                        name,
                        generator,
                        root,
                        output.joinpath(
                            GenerateTask.make_path(name, generator)
                        ),
                        data,
                        config.data,
                    )
                    for name, data in config.data.get(
                        generator.value, {}
                    ).items()
                ),
            )
