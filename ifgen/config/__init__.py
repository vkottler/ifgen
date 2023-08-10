"""
A module implementing a configuration interface for the package.
"""

# third-party
from vcorelib.dict.codec import BasicDictCodec as _BasicDictCodec

# internal
from ifgen.schemas import IfgenDictCodec


class Config(IfgenDictCodec, _BasicDictCodec):
    """The top-level configuration object for the package."""
