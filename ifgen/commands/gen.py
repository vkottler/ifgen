"""
An entry-point for the 'gen' command.
"""

# built-in
from argparse import ArgumentParser as _ArgumentParser
from argparse import Namespace as _Namespace
import sys

# third-party
from vcorelib.args import CommandFunction as _CommandFunction
from vcorelib.paths import normalize

# internal
from ifgen import PKG_NAME
from ifgen.config import load
from ifgen.generation import generate
from ifgen.paths import combine_if_not_absolute


def gen_cmd(args: _Namespace) -> int:
    """Execute the gen command."""

    root = normalize(args.root)

    sys.setrecursionlimit(args.recursion)

    generate(root.resolve(), load(combine_if_not_absolute(root, args.config)))

    return 0


def add_gen_cmd(parser: _ArgumentParser) -> _CommandFunction:
    """Add gen-command arguments to its parser."""

    parser.add_argument(
        "--recursion",
        type=int,
        default=10000,
        help="recursion limit to set (default: '%(default)s')",
    )
    parser.add_argument(
        "-c",
        "--config",
        default=f"{PKG_NAME}.yaml",
        help="configuration file to use (default: '%(default)s')",
    )
    parser.add_argument(
        "-r",
        "--root",
        default=".",
        help=(
            "root directory to use for relative "
            "paths (default: '%(default)s')"
        ),
    )
    return gen_cmd
