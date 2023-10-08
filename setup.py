# =====================================
# generator=datazen
# version=3.1.4
# hash=8c4d99f635c21da173b8be87123faba3
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
        "3.11",
        "3.12",
    ],
}
setup(
    pkg_info,
    author_info,
)
