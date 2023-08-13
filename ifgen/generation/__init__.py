"""
A module implementing interfaces to facilitate code generation.
"""

# built-in
from multiprocessing.pool import ThreadPool
from pathlib import Path

# internal
from ifgen.config import Config
from ifgen.enum import create_enum
from ifgen.environment import Generator, IfgenEnvironment
from ifgen.generation.interface import GenerateTask, GeneratorMap
from ifgen.struct import create_struct

GENERATORS: GeneratorMap = {
    Generator.STRUCTS: create_struct,
    Generator.ENUMS: create_enum,
}


def generate(root: Path, config: Config) -> None:
    """Generate struct files."""

    env = IfgenEnvironment(root, config)

    with ThreadPool() as pool:
        for generator, method in GENERATORS.items():
            pool.map(
                method,
                (
                    GenerateTask(
                        name,
                        generator,
                        env.make_path(name, generator, from_output=True),
                        data,
                        env,
                    )
                    for name, data in config.data.get(
                        generator.value, {}
                    ).items()
                ),
            )
