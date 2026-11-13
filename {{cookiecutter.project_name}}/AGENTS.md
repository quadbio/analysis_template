# AGENTS.md — working conventions

This file is the canonical guidance for any coding agent. `README.md` is the user-facing overview;
anything documented there is referenced from here, never restated.

## Workflow

Task directories, output paths, the `data/` layout and working objects follow
[`CONVENTIONS.md`](CONVENTIONS.md), for humans and agents alike. What only agents do (a worktree, a session and a
PR per task, sign-off on every write-back) comes from the
[analysis-workflow](https://github.com/quadbio/analysis-workflow) plugin, enabled in `.claude/settings.json`: load
its skill before writing analysis code, outputs or data. Pull requests are reviewed against
[`REVIEW_GUIDE.md`](REVIEW_GUIDE.md).

## This repo

<!-- Replace with this project's facts: its datasets and where each working object lives,
environment specifics, companion code packages. Rules the plugin owns are not restated here. -->

- **Package**: `src/<package>/`, installed editable from the main checkout
- **Paths**: every dataset path hangs off `FilePaths` in `src/<package>/_constants.py`:

```python
from {{ cookiecutter.package_name }} import FilePaths

FilePaths.EXAMPLE_DATASET / "processed" / "adata.zarr"
```

## Environments

Dependencies live in `pixi.toml`, not `pyproject.toml`, which carries package metadata and the
test config.

| Task | Command |
| --- | --- |
| Run Python | `pixi run python script.py` |
| Run tests | `pixi run test` |
| Add a conda / PyPI package | `pixi add <package>` / `pixi add --pypi <package>` |

The `gpu` environment (Linux with NVIDIA) adds rapids-singlecell: use it over scanpy for neighbors, UMAP and
clustering on more than about 100k cells, in a GPU job.
