"""
Test the 'commands.svd' module.
"""

# built-in
from tempfile import TemporaryDirectory

# module under test
from ifgen import PKG_NAME
from ifgen.entry import main as ifgen_main


def handle_proc(proc: str) -> None:
    """Test that we can generate code from an SVD processor."""

    with TemporaryDirectory() as tmpdir:
        # Generate configurations.
        assert (
            ifgen_main(
                [
                    PKG_NAME,
                    "svd",
                    "-o",
                    str(tmpdir),
                    f"package://{PKG_NAME}/svd/{proc}.svd",
                ]
            )
            == 0
        )

        # Generate code.
        assert ifgen_main([PKG_NAME, "-C", str(tmpdir), "gen"]) == 0


def test_svd_command_basic():
    """Test the 'svd' command."""

    # Coverage not working with this.
    # procs = ["XMC4700", "rp2040", "mimxrt1176_cm7", "mimxrt1176_cm4"]
    # with Pool(len(procs)) as pool:
    #     pool.map(handle_proc, procs)

    for proc in ["mimxrt1176_cm7", "XMC4700", "rp2040"]:
        handle_proc(proc)
