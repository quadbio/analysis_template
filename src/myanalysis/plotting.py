"""Plotting utilities for single-cell analysis.

This module provides custom plotting functions that wrap scanpy/matplotlib
with project-specific defaults and styling.
"""

from collections.abc import Sequence

import matplotlib.pyplot as plt
import numpy as np
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


def styled_umap(
    adata: AnnData,
    color: str | Sequence[str],
    *,
    title: str | None = None,
    palette: str | Sequence[str] | None = None,
    figsize: tuple[float, float] = (6, 5),
    save: str | None = None,
    **kwargs,
) -> plt.Figure:
    """Plot UMAP with clean styling suitable for presentations.

    Parameters
    ----------
    adata
        Annotated data matrix with UMAP coordinates in `.obsm['X_umap']`.
    color
        Key(s) in `adata.obs` or gene names to color by.
    title
        Plot title. If None, uses the color key.
    palette
        Color palette name or list of colors.
    figsize
        Figure size as (width, height).
    save
        Path to save figure. If None, figure is not saved.
    **kwargs
        Additional arguments passed to `sc.pl.umap`.

    Returns
    -------
    matplotlib Figure object.
    """
    if "X_umap" not in adata.obsm:
        msg = "UMAP not found. Run sc.tl.umap first."
        raise ValueError(msg)

    fig, ax = plt.subplots(figsize=figsize)

    sc.pl.umap(
        adata,
        color=color,
        ax=ax,
        show=False,
        frameon=False,
        palette=palette,
        **kwargs,
    )

    if title is not None:
        ax.set_title(title, fontsize=14, fontweight="bold")

    # Clean up axes
    ax.set_xlabel("UMAP1", fontsize=10)
    ax.set_ylabel("UMAP2", fontsize=10)

    plt.tight_layout()

    if save is not None:
        fig.savefig(save, dpi=150, bbox_inches="tight")

    return fig


def embedding_density(
    adata: AnnData,
    basis: str = "umap",
    *,
    groupby: str | None = None,
    figsize: tuple[float, float] = (6, 5),
    save: str | None = None,
) -> plt.Figure:
    """Plot cell density on embedding, optionally split by group.

    Useful for visualizing batch effects or condition-specific distributions.

    Parameters
    ----------
    adata
        Annotated data matrix with embedding coordinates.
    basis
        Embedding to use (e.g., 'umap', 'pca').
    groupby
        Key in `adata.obs` to split density by.
    figsize
        Figure size as (width, height).
    save
        Path to save figure. If None, figure is not saved.

    Returns
    -------
    matplotlib Figure object.
    """
    key = f"X_{basis}"
    if key not in adata.obsm:
        msg = f"Embedding '{key}' not found in adata.obsm."
        raise ValueError(msg)

    coords = adata.obsm[key][:, :2]

    if groupby is None:
        fig, ax = plt.subplots(figsize=figsize)
        ax.hexbin(coords[:, 0], coords[:, 1], gridsize=50, cmap="viridis", mincnt=1)
        ax.set_xlabel(f"{basis.upper()}1")
        ax.set_ylabel(f"{basis.upper()}2")
        ax.set_title("Cell density")
        ax.set_aspect("equal")
    else:
        groups = adata.obs[groupby].unique()
        n_groups = len(groups)
        ncols = min(3, n_groups)
        nrows = int(np.ceil(n_groups / ncols))
        fig, axes = plt.subplots(nrows, ncols, figsize=(figsize[0] * ncols, figsize[1] * nrows))
        axes = np.atleast_2d(axes).flatten()

        for ax, group in zip(axes[:n_groups], groups, strict=False):
            mask = adata.obs[groupby] == group
            ax.hexbin(coords[mask, 0], coords[mask, 1], gridsize=50, cmap="viridis", mincnt=1)
            ax.set_title(f"{groupby}: {group}")
            ax.set_xlabel(f"{basis.upper()}1")
            ax.set_ylabel(f"{basis.upper()}2")
            ax.set_aspect("equal")

        # Hide unused axes
        for ax in axes[n_groups:]:
            ax.set_visible(False)

    plt.tight_layout()

    if save is not None:
        fig.savefig(save, dpi=150, bbox_inches="tight")

    return fig
