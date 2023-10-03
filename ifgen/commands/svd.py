"""
An entry-point for the 'svd' command.
"""

# built-in
from argparse import ArgumentParser as _ArgumentParser
from argparse import Namespace as _Namespace
from logging import getLogger

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

    task = SvdProcessingTask.svd(path)

    # generate output files etc. ?
    assert task

    return 0


def add_svd_cmd(parser: _ArgumentParser) -> _CommandFunction:
    """Add svd-command arguments to its parser."""

    parser.add_argument(
        "svd_file", type=str, help="path/uri to a CMSIS-SVD file"
    )

    return svd_cmd
