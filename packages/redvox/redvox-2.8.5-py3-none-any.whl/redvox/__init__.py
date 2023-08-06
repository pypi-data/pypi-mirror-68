"""
Provides library level metadata and constants.
"""

NAME = "redvox"
VERSION = "2.8.5"


def version() -> str:
    """Returns the version number of this library."""
    return VERSION


def print_version():
    """Prints the version number of this library"""
    print(version())
