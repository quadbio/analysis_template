"""Plotting utilities for single-cell analysis.

This module provides custom plotting functions that wrap scanpy/matplotlib
with project-specific defaults and styling.
"""

import matplotlib.pyplot as plt
import scanpy as sc
from anndata import AnnData


def qc_violin(
    adata: AnnData,
    *,
    groupby: str | None = None,
    figsize: tuple[float, float] = (10, 3),
    save: str | None = None,
) -> plt.Figure:
    """Plot QC metrics as violin plots with consistent styling.

    Parameters
    ----------
    adata
        Annotated data matrix with QC metrics in `.var` and `.obs`.
    groupby
        Key in `adata.obs` to group violins by (e.g., 'sample').
    figsize
        Figure size as (width, height).
    save
        Path to save figure. If None, figure is not saved.

    Returns
    -------
    matplotlib Figure object.
    """
    qc_vars = ["n_genes_by_counts", "total_counts", "pct_counts_mt"]
    available = [v for v in qc_vars if v in adata.obs.columns]

    if not available:
        msg = f"No QC metrics found in adata.obs. Expected: {qc_vars}"
        raise ValueError(msg)

    fig, axes = plt.subplots(1, len(available), figsize=figsize)
    if len(available) == 1:
        axes = [axes]

    for ax, var in zip(axes, available, strict=False):
        sc.pl.violin(adata, var, groupby=groupby, ax=ax, show=False)
        ax.set_title(var.replace("_", " ").title())

    plt.tight_layout()

    if save is not None:
        fig.savefig(save, dpi=150, bbox_inches="tight")

    return fig
