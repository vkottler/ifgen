"""
An entry-point for the 'gen' command.
"""

# built-in
from argparse import ArgumentParser as _ArgumentParser
from argparse import Namespace as _Namespace

# third-party
from vcorelib.args import CommandFunction as _CommandFunction
from vcorelib.dict import merge
from vcorelib.io import ARBITER as _ARBITER
from vcorelib.io import DEFAULT_INCLUDES_KEY
from vcorelib.paths import Pathlike, find_file, normalize

# internal
from ifgen import PKG_NAME
from ifgen.config import Config

DEFAULT_CONFIG = f"{PKG_NAME}.yaml"


def load_config(path: Pathlike) -> Config:
    """Load a configuration object."""

    src_config = find_file("default.yaml", package=PKG_NAME)
    assert src_config is not None

    path = normalize(DEFAULT_CONFIG)

    data = merge(
        _ARBITER.decode(
            src_config,
            includes_key=DEFAULT_INCLUDES_KEY,
            require_success=True,
        ).data,
        _ARBITER.decode(path, includes_key=DEFAULT_INCLUDES_KEY).data,
        # Always allow the project-specific configuration to override
        # package data.
        expect_overwrite=True,
    )

    return Config.create(data)


def gen_cmd(args: _Namespace) -> int:
    """Execute the gen command."""

    del args

    config = load_config(DEFAULT_CONFIG)
    print(config)

    return 0


def add_gen_cmd(parser: _ArgumentParser) -> _CommandFunction:
    """Add gen-command arguments to its parser."""

    del parser
    return gen_cmd
