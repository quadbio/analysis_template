from importlib.metadata import version

from ._constants import FilePaths
from .plotting import embedding_density, qc_violin, styled_umap

__all__ = ["FilePaths", "embedding_density", "qc_violin", "styled_umap"]
__version__ = version("myanalysis")
