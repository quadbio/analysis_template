from pathlib import Path


class FilePaths:
    """Paths to the data and figures directories."""

    ROOT = Path(__file__).parents[3].resolve()

    DATA = ROOT / "data"
    FIGURES = ROOT / "figures"
    DATASET_1 = DATA / "dataset_1"
