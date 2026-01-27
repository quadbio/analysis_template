from pathlib import Path


class FilePaths:
    """Project-wide paths for notebooks and scripts."""

    ROOT = Path(__file__).parents[2].resolve()

    DATA = ROOT / "data"
    FIGURES = ROOT / "figures"

    # Example dataset layout; customize per project
    EXAMPLE_DATASET = DATA / "example_dataset"
