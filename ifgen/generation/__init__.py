"""
A module implementing interfaces to facilitate code generation.
"""

# built-in
from multiprocessing.pool import ThreadPool
from pathlib import Path
from typing import Dict, List

# internal
from ifgen.config import Config
from ifgen.enum import create_enum, create_enum_test
from ifgen.environment import Generator, IfgenEnvironment
from ifgen.generation.interface import GenerateTask, InstanceGenerator
from ifgen.struct import create_struct, create_struct_test

GENERATORS: Dict[Generator, List[InstanceGenerator]] = {
    Generator.STRUCTS: [create_struct, create_struct_test],
    Generator.ENUMS: [create_enum, create_enum_test],
}


def generate(root: Path, config: Config) -> None:
    """Generate struct files."""

    env = IfgenEnvironment(root, config)

    with ThreadPool() as pool:
        for generator, methods in GENERATORS.items():
            for method in methods:
                pool.map(
                    method,
                    (
                        GenerateTask(
                            name,
                            generator,
                            env.make_path(name, generator, from_output=True),
                            env.make_test_path(name, generator),
                            data,
                            env,
                        )
                        for name, data in config.data.get(
                            generator.value, {}
                        ).items()
                    ),
                )
