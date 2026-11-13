"""Project-wide paths for notebooks and scripts; a task's own outputs come from ``analysis_workflow.task_paths``."""

from analysis_workflow import main_checkout


class FilePaths:
    """Project-wide paths. Add a dataset as a constant here; never hardcode one.

    ``ROOT`` is the *main* checkout even from a git worktree, so shared data does not follow your branch.
    """

    ROOT = main_checkout(__file__)

    DATA = ROOT / "data"

    EXAMPLE_DATASET = DATA / "example_dataset"
