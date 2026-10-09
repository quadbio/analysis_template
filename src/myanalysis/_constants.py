"""Project-wide paths for notebooks and scripts."""

from analysis_workflow import main_checkout


class FilePaths:
    """Project-wide paths. Add a dataset as a constant here; never hardcode one.

    ``ROOT`` is the *main* checkout even from a git worktree, so shared data does not follow your branch.
    """

    ROOT = main_checkout(__file__)

    DATA = ROOT / "data"
    FIGURES = ROOT / "figures"

    EXAMPLE_DATASET = DATA / "example_dataset"
