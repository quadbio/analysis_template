import anndata as ad
import numpy as np
import pytest

import myanalysis
from myanalysis import FilePaths, qc_violin


def test_package_has_version():
    assert myanalysis.__version__ is not None


def test_filepaths_root_exists():
    """Verify the project root is correctly resolved."""
    assert FilePaths.ROOT.exists()
    assert (FilePaths.ROOT / "pixi.toml").exists()


def test_filepaths_directories():
    """Verify standard directories are defined and accessible."""
    assert FilePaths.DATA.parent == FilePaths.ROOT
    assert FilePaths.FIGURES.parent == FilePaths.ROOT


def test_qc_violin_missing_metrics():
    """Verify qc_violin raises informative error when QC metrics are missing."""
    # Create minimal AnnData without QC metrics
    adata = ad.AnnData(np.random.rand(10, 5))

    with pytest.raises(ValueError, match="No QC metrics found"):
        qc_violin(adata)
