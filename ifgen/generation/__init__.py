"""
A module implementing interfaces to facilitate code generation.
"""

# built-in
from importlib import import_module
from logging import getLogger
from multiprocessing.pool import ThreadPool
from pathlib import Path
import re
import sys
from typing import Iterator

# third-party
from vcorelib.names import import_str_and_item

# internal
from ifgen.common import create_common, create_common_test
from ifgen.config import Config
from ifgen.enum import create_enum, create_enum_source, create_enum_test
from ifgen.enums import Generator, Language
from ifgen.environment import IfgenEnvironment
from ifgen.generation.interface import (
    GenerateTask,
    InstanceConfig,
    InstanceGenerator,
)
from ifgen.plugins import internal_plugin_entry
from ifgen.struct import (
    create_struct,
    create_struct_test,
)

CodeGenerators = dict[Generator, list[InstanceGenerator]]
GENERATORS: CodeGenerators = {
    Generator.STRUCTS: [create_struct, create_struct_test],
    Generator.ENUMS: [create_enum, create_enum_test, create_enum_source],
    Generator.IFGEN: [],
    Generator.CUSTOM: [internal_plugin_entry],
}
LOG = getLogger(__name__)


def resolve_generators(env: IfgenEnvironment) -> CodeGenerators:
    """
    Populate any custom generator interfaces defined in the configuration.
    """

    path = str(env.root_path.resolve())
    if path not in sys.path:
        sys.path.append(path)

    generators = GENERATORS.copy()

    if env.config.data["common"]:
        generators[Generator.IFGEN].append(create_common)
    if env.config.data["common_test"]:
        generators[Generator.IFGEN].append(create_common_test)

    for custom in env.config.data.get("plugins", []):
        module, app = import_str_and_item(custom)
        generators[Generator.CUSTOM].append(
            getattr(import_module(module), app)
        )

    return generators


def check_patterns(method: str, name: str, *patterns: str) -> bool:
    """
    Determine if a regular expression method matches any pattern against name.
    """

    matched = False

    for pattern in patterns:
        if getattr(re, method)(pattern, name) is not None:
            matched = True
            break

    return matched


def generator_tasks(
    generator: Generator, config: Config
) -> Iterator[tuple[str, InstanceConfig]]:
    """Handle configured exclusions."""

    for name, data in config.data.get(generator.value, {}).items():
        for method, patterns in config.names.items():
            if check_patterns(method, name, *patterns):
                yield name, data
                break


def generate(root: Path, config: Config) -> None:
    """Generate struct files."""

    env = IfgenEnvironment(root, config)

    # Search for language configurations.
    languages = [x for x in Language if config.data.get(x.cfg_dir_name)]
    LOG.info("Generating for languages: %s.", languages)

    with ThreadPool() as pool:
        for language in languages:
            for generator, methods in resolve_generators(env).items():
                for method in methods:
                    pool.map(
                        method,
                        (
                            GenerateTask(
                                name,
                                generator,
                                language,
                                env.make_path(
                                    name,
                                    generator,
                                    language,
                                    from_output=True,
                                ),
                                env.make_test_path(name, generator, language),
                                data,
                                env,
                            )
                            for name, data in generator_tasks(
                                generator, config
                            )
                        ),
                    )

    env.prune_empty()
