"""
An entry-point for the 'svd' command.
"""

# built-in
from argparse import ArgumentParser as _ArgumentParser
from argparse import Namespace as _Namespace
from pathlib import Path

# third-party
from vcorelib.args import CommandFunction as _CommandFunction

# internal
from ifgen.svd import register_processors
from ifgen.svd.task import SvdProcessingTask


def svd_cmd(args: _Namespace) -> int:
    """Execute the svd command."""

    register_processors()
    task = SvdProcessingTask.svd(args.svd_file)

    # generate output files etc. ?
    assert task

    return 0


def add_svd_cmd(parser: _ArgumentParser) -> _CommandFunction:
    """Add svd-command arguments to its parser."""

    parser.add_argument("svd_file", type=Path, help="path to a CMSIS-SVD file")

    return svd_cmd
