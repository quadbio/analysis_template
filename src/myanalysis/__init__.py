from importlib.metadata import version

from ._constants import DatasetPaths, FilePaths
from .plotting import qc_violin

__all__ = ["DatasetPaths", "FilePaths", "qc_violin"]
__version__ = version("myanalysis")
