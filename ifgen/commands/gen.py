"""
An entry-point for the 'gen' command.
"""

# built-in
from argparse import ArgumentParser as _ArgumentParser
from argparse import Namespace as _Namespace

# third-party
from vcorelib.args import CommandFunction as _CommandFunction
from vcorelib.paths import normalize

# internal
from ifgen import PKG_NAME
from ifgen.config import load
from ifgen.generation import generate
from ifgen.paths import combine_if_not_absolute

DEFAULT_CONFIG = f"{PKG_NAME}.yaml"


def gen_cmd(args: _Namespace) -> int:
    """Execute the gen command."""

    root = normalize(args.root)

    generate(root, load(combine_if_not_absolute(root, DEFAULT_CONFIG)))

    return 0


def add_gen_cmd(parser: _ArgumentParser) -> _CommandFunction:
    """Add gen-command arguments to its parser."""

    parser.add_argument(
        "-r",
        "--root",
        default=".",
        help="root directory to use for relative paths",
    )
    return gen_cmd
