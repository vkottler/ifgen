"""
An entry-point for the 'gen' command.
"""

# built-in
from argparse import ArgumentParser as _ArgumentParser
from argparse import Namespace as _Namespace
from pathlib import Path

# third-party
from vcorelib.args import CommandFunction as _CommandFunction
from vcorelib.paths import Pathlike, normalize

# internal
from ifgen import PKG_NAME
from ifgen.config import load
from ifgen.generation import generate

DEFAULT_CONFIG = f"{PKG_NAME}.yaml"


def combine_if_not_absolute(root: Path, candidate: Pathlike) -> Path:
    """Combine a root directory with a path if the path isn't absolute."""

    candidate = normalize(candidate)
    return candidate if candidate.is_absolute() else root.joinpath(candidate)


def gen_cmd(args: _Namespace) -> int:
    """Execute the gen command."""

    root = normalize(args.root)

    config = load(combine_if_not_absolute(root, DEFAULT_CONFIG))

    output = combine_if_not_absolute(
        root, normalize(*config.data["output_dir"])
    )

    generate(root, output, config)

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
