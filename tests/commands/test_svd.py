"""
Test the 'commands.svd' module.
"""

# built-in
from tempfile import TemporaryDirectory

# module under test
from ifgen import PKG_NAME
from ifgen.entry import main as ifgen_main


def test_svd_command_basic():
    """Test the 'svd' command."""

    with TemporaryDirectory() as tmpdir:
        for svd in ["XMC4700", "rp2040"]:
            assert (
                ifgen_main(
                    [
                        PKG_NAME,
                        "svd",
                        "-o",
                        str(tmpdir),
                        f"package://{PKG_NAME}/svd/{svd}.svd",
                    ]
                )
                == 0
            )
