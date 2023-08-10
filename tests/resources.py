"""
A module for working with test data.
"""

# built-in
from pathlib import Path
from shutil import rmtree


def resource(resource_name: str, *parts: str, valid: bool = True) -> Path:
    """Locate the path to a test resource."""

    return Path(__file__).parent.joinpath(
        "data", "valid" if valid else "invalid", resource_name, *parts
    )


def clean_scenario(name: str) -> Path:
    """
    Get the path to a scenario directory and ensure outputs are cleaned before
    running.
    """

    base = resource("scenarios", name)

    # Clean things that can affect tests.
    for path in ["src"]:
        rmtree(base.joinpath(path), ignore_errors=True)

    return base
