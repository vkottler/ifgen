# =====================================
# generator=datazen
# version=3.2.0
# hash=3bac2a3bc0b9200d68535b5383b9886e
# =====================================

"""
ifgen - Package definition for distribution.
"""

# third-party
try:
    from setuptools_wrapper.setup import setup
except (ImportError, ModuleNotFoundError):
    from ifgen_bootstrap.setup import setup  # type: ignore

# internal
from ifgen import DESCRIPTION, PKG_NAME, VERSION

author_info = {
    "name": "Vaughn Kottler",
    "email": "vaughnkottler@gmail.com",
    "username": "vkottler",
}
pkg_info = {
    "name": PKG_NAME,
    "slug": PKG_NAME.replace("-", "_"),
    "version": VERSION,
    "description": DESCRIPTION,
    "versions": [
        "3.12",
    ],
}
setup(
    pkg_info,
    author_info,
)
