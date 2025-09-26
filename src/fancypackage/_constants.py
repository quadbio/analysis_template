from pathlib import Path


class FilePaths:
    """Paths to the data and figures directories."""

    ROOT = Path(__file__).parents[3].resolve()

    DATA = ROOT / "data"
    FIGURES = ROOT / "figures"
    EXAMPLE_DATASET = DATA / "example_dataset"
