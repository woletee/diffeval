"""importlib.metadata version, or null when missing."""

from importlib.metadata import PackageNotFoundError, version


def version_of(name: str):
    try:
        return version(name)
    except PackageNotFoundError:
        return None
