# human_scrna_workflow_v1

**Date:** 2026-01-27
**Author:** ML

<!-- Every heading below stays, in this order, and no others are added; a section with nothing to say reads "None."
The guidance comments stay too. -->

A demo of a complete scRNA-seq workflow on scanpy's PBMC 3k data, from QC to a working object, marking which
steps to run locally and which on a GPU cluster.

## Deliverables

<!-- What the task delivers. An agent agrees them with the human at the start, from the default unless they chose
otherwise; a later change is recorded here too. -->

| deliverable | where |
| --- | --- |
| UMAP overviews | `figures/` (gitignored) |
| a new working object | Write-back, below |

## Inputs

<!-- The actual files, not concepts: this is what makes the task re-runnable. -->

- scanpy's PBMC 3k dataset, downloaded to `data/example_dataset/raw/`
- CellTypist's `Immune_All_High.pkl` model

## Write-back

<!-- What went into a shared object, under which keys, and anything placed in `data/<dataset>/processed/` with its
final path. -->

- `data/example_dataset/processed/working/pbmc3k_2026-01-27.zarr`, a new working object, holding:
  - `obsm["X_scVI"]`, `obsm["X_umap"]`: scVI latent space and its UMAP
  - `obs["leiden"]`: Leiden clusters at resolution 0.5
  - `obs["cell_type"]`: CellTypist labels, majority-voted

## Running

<!-- The notebooks in `notebooks/` and scripts in `scripts/`, in run order, on the main checkout's environment. Batch
jobs get `MAIN=<main checkout>` at submit and log to `PATHS.logs`. -->

`notebooks/01_scrna_workflow.ipynb`, top to bottom; its scVI section is faster on a GPU.

## Jobs

<!-- Batch jobs this task launched, counted at the end. -->

None.

## PRs and issues

<!-- Every PR and issue this task opened, in any repo, added when opened, with a short summary of each; the details
are in the PR. -->

None.
