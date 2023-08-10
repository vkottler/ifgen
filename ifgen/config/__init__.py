"""
A module implementing a configuration interface for the package.
"""

# third-party
from vcorelib.dict import merge
from vcorelib.dict.codec import BasicDictCodec as _BasicDictCodec
from vcorelib.io import ARBITER as _ARBITER
from vcorelib.io import DEFAULT_INCLUDES_KEY
from vcorelib.paths import Pathlike, find_file

# internal
from ifgen import PKG_NAME
from ifgen.schemas import IfgenDictCodec


class Config(IfgenDictCodec, _BasicDictCodec):
    """The top-level configuration object for the package."""


def load(path: Pathlike) -> Config:
    """Load a configuration object."""

    src_config = find_file("default.yaml", package=PKG_NAME)
    assert src_config is not None

    data = merge(
        _ARBITER.decode(
            src_config,
            includes_key=DEFAULT_INCLUDES_KEY,
            require_success=True,
        ).data,
        _ARBITER.decode(
            path, includes_key=DEFAULT_INCLUDES_KEY, require_success=True
        ).data,
        # Always allow the project-specific configuration to override package
        # data.
        expect_overwrite=True,
    )

    return Config.create(data)
