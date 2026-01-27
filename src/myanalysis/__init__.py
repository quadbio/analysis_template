from importlib.metadata import version

from ._constants import FilePaths
from .plotting import qc_violin

__all__ = ["FilePaths", "qc_violin"]
__version__ = version("myanalysis")
