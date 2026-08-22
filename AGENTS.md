# AGENTS.md — working conventions

This file owns the working conventions and is the canonical guidance for any coding agent.
`README.md` is the user-facing overview; anything documented there is referenced from here,
never restated.

## Layout

- **Notebooks**: `analysis/[INITIALS]-[YYYY]-[MM]-[DD]_description.ipynb`
- **Data**: `data/<dataset>/{raw,processed,resources,results}/`, gitignored
- **Package**: `src/<package>/`, installed editable from the checkout

## Paths

Never hardcode a path into `data/` or `figures/` — every path hangs off `FilePaths`:

```python
from myanalysis import FilePaths

FilePaths.DATA           # data/
FilePaths.FIGURES        # figures/ — curated output: talk and paper figures
FilePaths.EXAMPLE_DATASET / "processed" / "adata.h5ad"
```

`FilePaths.ROOT` is resolved from git, so it names the *main* checkout even when called from a
worktree and shared data does not follow your branch. Add a dataset as a constant in
`_constants.py`; each one keeps the `{raw,processed,resources,results}` layout by convention.

## Environments

Dependencies live in `pixi.toml`, not `pyproject.toml` — the latter carries package metadata and
the test config. Run `pixi install` after pulling a change to `pixi.toml`, in the main checkout.

| Task | Command |
| --- | --- |
| Run Python | `pixi run python script.py` |
| Run tests | `pixi run test` |
| Add conda package | `pixi add <package>` |
| Add PyPI package | `pixi add --pypi <package>` |
