"""
ifgen - Test the program's entry-point.
"""

# built-in
from subprocess import check_output
from sys import executable
from unittest.mock import patch

# module under test
from ifgen import PKG_NAME
from ifgen.entry import main as ifgen_main


def test_entry_basic():
    """Test basic argument parsing."""

    args = [PKG_NAME, "noop"]
    assert ifgen_main(args) == 0

    with patch("ifgen.entry.entry", side_effect=SystemExit(1)):
        assert ifgen_main(args) != 0


def test_package_entry():
    """Test the command-line entry through the 'python -m' invocation."""

    check_output([executable, "-m", "ifgen", "-h"])
