# Conventions

How analysis is organized in this repo. Humans and coding agents follow the same rules; agents add their own on top
(a worktree, a session and a PR per task, sign-off on every write-back), from the
[analysis-workflow](https://github.com/quadbio/analysis-workflow) plugin.

> Everything here comes from the analysis template; change it there and pull it with `cruft update`.

## Start a task

```bash
pixi run analysis-workflow new analysis/<dataset>/<topic>/human_<name>_v1 --author <your initials> --notebook 01_<step>
```

This creates the task directory with its `README.md` and a starter notebook in `notebooks/`. Open the notebook,
fill in the README's question and inputs, and work.

## Tasks

All analysis lives in task directories, `analysis/<dataset>/<topic>/<lane>_<name>_vN/`:

- `<dataset>` is there even when the repo has one dataset. Topics, such as `preprocessing/`, `annotation/` or
  `spatial/`, can mostly be worked on in any order.
- `<lane>` is `human` or `agent`; the README's author line says who: initials, or the model.
- `vN` counts the answers to one question across both lanes: `human_markers_v1` may be followed by
  `agent_markers_v2`. `analysis-workflow new` refuses any other version than the next.
- A task is edited freely until its first write-back to a shared object or until other tasks read its outputs (for
  an agent's task: its merge). After that it is frozen, and a change is the next version, whose README names the
  one it follows.

| in a task | tracked | holds |
| --- | --- | --- |
| `README.md` | yes | the question, inputs, deliverables, write-back; kept current |
| `notebooks/` | yes | `NN_<step>.ipynb`, numbered in run order; outputs committed, so keep them small |
| `scripts/` | yes | `NN_<step>.py`, numbered in run order; `_common.py` holds the task's paths |
| `results/` | yes | small evidence tables; past ~1 MB they belong in `outputs/` |
| `reports/` | yes | a report |
| `figures/` | no | figures |
| `outputs/` | no | data artifacts |
| `logs/` | no | batch-job logs |

Every output path comes from `task_paths`: `PATHS = task_paths()` in a notebook, `task_paths(__file__)` in a script;
`PATHS.ensure()` creates the directories. Dataset paths come from `FilePaths`:

```python
from analysis_workflow import task_paths
from {{ cookiecutter.package_name }} import FilePaths

PATHS = task_paths().ensure()
working = FilePaths.EXAMPLE_DATASET / "processed" / "working" / "pbmc3k_2026-01-27.zarr"
fig.savefig(PATHS.figures / "umap.pdf")
```

## Data

| `data/<dataset>/` | holds |
| --- | --- |
| `raw/` | bytes as they arrived, never changed |
| `resources/` | curated inputs that are not data: gene lists, marker tables |
| `processed/` | objects other tasks load: working objects in `working/`, others in descriptively named subdirectories |

A task writes into its own directory. An object other tasks will load goes to `processed/` (for an agent, after
sign-off), and the task README records its path.

## Working objects

A working object is an AnnData zarr store, `processed/working/<name>_<YYYY-MM-DD>.zarr`, in which results from many
tasks accumulate.

- Read only what you need: `ad.io.read_elem(zarr.open_group(path)["obs"])`, or `ad.experimental.read_lazy`.
- Write back only through `commit_adata`, naming the keys you add. It refuses a key that is already there, so
  nobody's results get overwritten:

  ```python
  from analysis_workflow import commit_adata

  commit_adata(adata, path, keys={"obs": ["leiden_fine"]})            # dry run: shows what it would write
  commit_adata(adata, path, keys={"obs": ["leiden_fine"]}, yes=True)  # writes
  ```

- Never write an in-memory object over a working object: it erases what others added since you read it. Changing
  or removing a key means a new dated copy.
- Give keys descriptive names, and list each in the task README's Write-back section.
- Labels: one categorical `obs` column, colours in `uns["<key>_colors"]`.
- A result that would grow the object materially (`analyze_anndata_size`) becomes a standalone AnnData on the same
  `obs_names`, never a bare `.npy`.

## Git

You work in the main checkout. A pull request is optional and encouraged for anything others build on:

```bash
git switch -c <branch>
git add analysis/<dataset>/<topic>/<task> && git commit -m "<what>"
git push -u origin <branch>
gh pr create                   # its body starts from the PR template
```

It is reviewed against `REVIEW_GUIDE.md`. Switching
branches changes the main checkout that agents' sessions read, `pixi.toml` included: switch back to `main` when you
are done.
