from importlib.metadata import version

from . import pl, pp, tl, ul
from ._constants import FilePaths

__all__ = ["pl", "pp", "tl", "ul", "FilePaths"]
__version__ = version("fancypackage")
