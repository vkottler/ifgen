"""
Test the 'commands.svd' module.
"""

# module under test
from ifgen import PKG_NAME
from ifgen.entry import main as ifgen_main

# internal
from tests.resources import resource


def test_svd_command_basic():
    """Test the 'svd' command."""

    assert (
        ifgen_main([PKG_NAME, "svd", str(resource("svd", "XMC4700.svd"))]) == 0
    )
