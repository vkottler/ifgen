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

    SvdProcessingTask.svd(path).generate_configs(args.output)

    return 0


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
        "svd_file", type=str, help="path/uri to a CMSIS-SVD file"
    )

    return svd_cmd
