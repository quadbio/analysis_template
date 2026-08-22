import anndata as ad
import matplotlib
import numpy as np
import pytest
from matplotlib.figure import Figure

import myanalysis
from myanalysis import FilePaths, qc_violin

# Headless backend so plotting works in CI.
matplotlib.use("Agg")


def test_package_has_version():
    assert myanalysis.__version__ is not None


def test_filepaths():
    """The root resolves to the checkout, and dataset constants hang off it."""
    assert (FilePaths.ROOT / "pixi.toml").exists()
    assert FilePaths.DATA == FilePaths.ROOT / "data"
    assert FilePaths.EXAMPLE_DATASET == FilePaths.DATA / "example_dataset"


def test_qc_violin():
    """qc_violin returns a matplotlib Figure for an AnnData with QC metrics."""
    rng = np.random.default_rng(0)
    adata = ad.AnnData(rng.random((20, 5)))
    for metric in ("n_genes_by_counts", "total_counts", "pct_counts_mt"):
        adata.obs[metric] = rng.random(20)

    assert isinstance(qc_violin(adata), Figure)


def test_qc_violin_missing_metrics():
    """qc_violin raises an informative error when QC metrics are missing."""
    adata = ad.AnnData(np.random.default_rng(0).random((10, 5)))
    with pytest.raises(ValueError, match="No QC metrics found"):
        qc_violin(adata)
