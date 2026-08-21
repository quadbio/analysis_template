from importlib.metadata import version

from ._constants import DatasetPaths, FilePaths, TaskPaths, main_checkout, task_paths
from .plotting import qc_violin

__all__ = ["DatasetPaths", "FilePaths", "TaskPaths", "main_checkout", "qc_violin", "task_paths"]
__version__ = version("myanalysis")
