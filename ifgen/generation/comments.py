"""
A module for working with comments.
"""

# built-in
from contextlib import contextmanager
from typing import Iterator, Optional

# third-party
from vcorelib.io import IndentedFileWriter


def trailing_comment(data: str) -> str:
    """Wrap some string data in a doxygen comment."""
    return f" /*!< {data} */"


LineWithComment = tuple[str, Optional[str]]
LinesWithComments = list[LineWithComment]


@contextmanager
def trailing_comment_lines(
    writer: IndentedFileWriter,
) -> Iterator[LinesWithComments]:
    """Align indentations for trailing comments."""

    # Collect lines and comments.
    lines_comments: LinesWithComments = []
    yield lines_comments

    longest = 0
    for line, _ in lines_comments:
        length = len(line)
        if len(line) > longest:
            longest = length

    for line, comment in lines_comments:
        padding = " " * (longest - len(line))
        if comment:
            line += padding + trailing_comment(comment)
        writer.write(line)
