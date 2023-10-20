"""
An entry-point for the 'svd' command.
"""

# built-in
from argparse import ArgumentParser as _ArgumentParser
from argparse import Namespace as _Namespace
from logging import getLogger
from pathlib import Path

# third-party
from vcorelib.args import CommandFunction as _CommandFunction
from vcorelib.paths import find_file

# internal
from ifgen import PKG_NAME
from ifgen.svd import register_processors
from ifgen.svd.group import base, enums
from ifgen.svd.task import SvdProcessingTask


def svd_cmd(args: _Namespace) -> int:
    """Execute the svd command."""

    register_processors()

    path = find_file(
        args.svd_file,
        package=PKG_NAME,
        logger=getLogger(__name__),
        include_cwd=True,
    )
    assert path is not None, args.svd_file

    enable_pruning = path.with_suffix("").name in {"XMC4700"}

    # Only enable certain pruning strategies for certain processors.
    enums.PRUNE_ENUMS = enable_pruning
    base.PRUNE_STRUCTS = enable_pruning

    SvdProcessingTask.svd(path, args.min_enum_width).generate_configs(
        args.output
    )

    return 0


DEFAULT_MIN_ENUM_WIDTH = 2


def add_svd_cmd(parser: _ArgumentParser) -> _CommandFunction:
    """Add svd-command arguments to its parser."""

    parser.add_argument(
        "-o",
        "--output",
        type=Path,
        default=f"{PKG_NAME}-out",
        help="output directory for configuration files",
    )

    parser.add_argument(
        "-m",
        "--min-enum-width",
        type=int,
        default=DEFAULT_MIN_ENUM_WIDTH,
        help=(
            "minimum number of enumeration elements to warrant "
            "generating an enumeration definition (default: %(default)s)"
        ),
    )

    parser.add_argument(
        "svd_file", type=str, help="path/uri to a CMSIS-SVD file"
    )

    return svd_cmd
