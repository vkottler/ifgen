"""
A module implementing an SVD-command configuration interface for the package.
"""

# third-party
from vcorelib.dict.codec import BasicDictCodec as _BasicDictCodec

# internal
from ifgen.schemas import IfgenDictCodec


class SvdConfig(IfgenDictCodec, _BasicDictCodec):
    """The top-level configuration object for the package."""
