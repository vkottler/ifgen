"""
A module defining a struct-task interface.
"""

# built-in
from pathlib import Path
from typing import Any, Dict, NamedTuple

StructConfig = Dict[str, Any]


class GenerateStructTask(NamedTuple):
    """Parameters necessary for struct generation."""

    root: Path
    path: Path
    struct: StructConfig
    config: Dict[str, Any]

    def command(self, command: str, data: str = "", space: str = " ") -> str:
        """Get a command string."""
        return (
            str(self.config["command"])
            + command
            + (space if data else "")
            + data
        )
