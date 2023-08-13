"""
A module exposing some pathing utilities.
"""

# built-in
from pathlib import Path

# third-party
from vcorelib.paths import Pathlike, normalize


def combine_if_not_absolute(root: Path, candidate: Pathlike) -> Path:
    """Combine a root directory with a path if the path isn't absolute."""

    candidate = normalize(candidate)
    return candidate if candidate.is_absolute() else root.joinpath(candidate)
