"""
Test the 'commands.gen' module.
"""

# built-in
from subprocess import run
from sys import executable, platform

# module under test
from ifgen import PKG_NAME
from ifgen.entry import main as ifgen_main

# internal
from tests.resources import clean_scenario


def test_ifgen_command_basic():
    """Test the 'gen' command."""

    path = str(clean_scenario("sample"))
    assert ifgen_main([PKG_NAME, "gen", "-r", path]) == 0

    # Attempt to build and run generated tests.
    if platform == "linux":
        run([executable, "-m", "yambs", "-C", path, "native"], check=True)
        run(["ninja", "-C", path, "format-check"], check=True)
