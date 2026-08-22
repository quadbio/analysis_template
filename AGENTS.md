# AGENTS.md — working conventions

This file owns the working conventions and is the canonical guidance for any coding agent.
`README.md` is the user-facing overview; anything documented there is referenced from here,
never restated.

## Layout

- **Notebooks**: `analysis/[INITIALS]-[YYYY]-[MM]-[DD]_description.ipynb`
- **Data**: `data/<dataset>/{raw,processed,resources,results}/`, gitignored
- **Package**: `src/<package>/`, installed editable from the checkout

## Paths

Never hardcode a path into `data/` or `figures/`. Everything resolves from `FilePaths`:

```python
from myanalysis import FilePaths

ds = FilePaths.dataset("pbmc3k")     # .root .raw .processed .resources .results
ds.create()                          # idempotent; call it in the writer, not at import
adata.write_h5ad(ds.processed / "adata.h5ad")
```

`FilePaths.ROOT` is the repository root, resolved from git so it names the *main* checkout
even when called from a worktree; `FilePaths.DATA` and `FilePaths.FIGURES` hang off it. Add a
dataset by calling `FilePaths.dataset("<name>")` — `_constants.py` only needs editing to change
the shared layout itself.

`FilePaths.FIGURES` is for **curated** output: figures chosen for a talk or a paper.

## Environments

Dependencies live in `pixi.toml`, not `pyproject.toml` — the latter carries package metadata and
the test config. Run `pixi install` after pulling a change to `pixi.toml`, in the main checkout.

| Task | Command |
| --- | --- |
| Run Python | `pixi run python script.py` |
| Run tests | `pixi run test` |
| Add conda package | `pixi add <package>` |
| Add PyPI package | `pixi add --pypi <package>` |
