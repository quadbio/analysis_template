# Conventions

How analysis is organized in this repo, written for the humans working in it: everything here applies to a human's
work. Coding agents follow the same rules and add their own on top (a worktree, a session and a PR per task, a
human's sign-off on every write-back), from the [analysis-workflow](https://github.com/quadbio/analysis-workflow)
plugin. Agents are mentioned here only where a human needs to know what they do.

> Everything here comes from the analysis template; change it there and pull it with `cruft update`.

## Start a task

A human starts a task with

```bash
pixi run analysis-workflow new analysis/<dataset>/<topic>/human_<name>_v1 --notebook 01_<step>
```

which creates the task directory with its `README.md` and a starter notebook in `notebooks/`, then opens the
notebook, fills in the README's question, and works. The README's author line takes the git user name;
`--author <name>` sets another.

A task that ports older work, from another repo or a folder older than these conventions, is started with
`--ported-from <repo>:<path>@<commit>`. The README records where it came from, and the task keeps the old version
number. Lane and author follow who originated the work, not who ported it.

## Tasks

All analysis lives in task directories, `analysis/<dataset>/<topic>/<lane>_<name>_vN/`:

- `<dataset>` is there even when the repo has one dataset. Topics, such as `preprocessing/`, `annotation/` or
  `spatial/`, can mostly be worked on in any order.
- `<lane>` is `human` or `agent`; the README's author line says who: a name, or the model.
- `vN` counts the answers to one question across both lanes: `human_markers_v1` may be followed by
  `agent_markers_v2`. `analysis-workflow new` refuses any other version than the next, but for a port.
- A task is edited freely until its first write-back to a shared object or until other tasks read its outputs (for
  an agent's task: its merge). After that it is frozen, and a change is the next version, whose README names the
  one it follows.

| in a task | tracked | holds |
| --- | --- | --- |
| `README.md` | yes | the task's id, the question, deliverables, write-back; kept current |
| `inputs.yaml` | yes | what the task's code consumed, written by an agent (What an artifact rests on) |
| `notebooks/` | yes | `NN_<step>.ipynb`, numbered in run order; outputs committed, so keep them small |
| `scripts/` | yes | `NN_<step>.py`, numbered in run order; `_common.py` holds the task's paths |
| `workflow/` | yes | a workflow engine's files: Snakefile, rules, configs, profiles |
| `results/` | yes | small evidence tables; past ~1 MB they belong in `outputs/` |
| `reports/` | yes | a report |
| `figures/` | no | figures |
| `outputs/` | no | data artifacts |
| `logs/` | no | batch-job logs |

`analysis-workflow new` lays a task out this way, and the names are reserved for what the table says. At a task's
end, `analysis-workflow tidy <task>` removes every directory it left empty. Every finished task has its `README.md`
and its `inputs.yaml`.

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

A task writes into its own directory, and so do the external tools, shell scripts and batch jobs it runs. A
workflow engine runs with its working directory in `PATHS.outputs`, where its results and its own state land. An
object other tasks will load goes to `processed/` inside a `writes` block (below), which records the task in it; an
agent does so only after a human's sign-off. The task README records its path.

Every write into `processed/` sits in a `writes` block: a notebook cell that starts `%%writes <path>`, or
`with writes(<path>):` in a script, where `<path>` is the store. It records in the store which task wrote what
(`adata.uns["provenance"]`, `sdata.attrs["provenance"]`). That goes for a write-back, a new object, a new
SpatialData element and a copy out of a task's `outputs/`. A store a batch job built there is moved, once
reviewed: nothing half-written reaches shared storage, and a rerun of the job cannot touch it. Stores only grow:
nothing in one is replaced or removed in place.

**Limitation.** Only AnnData and SpatialData stores hold such a record. Any other file under `data/` has none: a
trace stops at it, and the only link to the task that made it is that task's README.

## Working objects

A working object is an AnnData zarr store, `processed/working/<name>_<YYYY-MM-DD>.zarr`, in which results from many
tasks accumulate.

- Read only what is needed: `ad.io.read_elem(zarr.open_group(path)["obs"])`, or `ad.experimental.read_lazy`.
- Write back only through `commit_adata`, naming the keys to add. It refuses a key that is already there, so
  nobody's results get overwritten:

  ```python
  from analysis_workflow import commit_adata

  commit_adata(adata, path, keys={"obs": ["leiden_fine"]})            # dry run: shows what it would write
  ```

  ```python
  %%writes path
  commit_adata(adata, path, keys={"obs": ["leiden_fine"]}, yes=True)  # writes
  ```

- Never write an in-memory object over a working object: it erases what others added since it was read. Changing
  or removing a key means a new dated copy. In it a key may be dropped; one whose values change gets a new name,
  so a name stands for the same values in every copy.
- Create one with `adata.write_zarr(path, consolidate_metadata=False)` in a `writes` block, at a path that doesn't
  exist yet. Readers of a consolidated store never see keys added later, so `commit_adata` refuses one.
- Give keys descriptive names, and say what each holds in the task README's Write-back section.
- Labels: one categorical `obs` column, colours in `uns["<key>_colors"]`.
- A result that would grow the object materially (`analyze_anndata_size`) becomes a standalone AnnData on the same
  `obs_names`, never a bare `.npy`.

## Figure conventions

Conventions shared by the repo's figures, whatever draws them, live in `resources/figure_conventions.yaml`. Like
everything in the root `resources/`, it is tracked, unlike `data/<dataset>/resources/`.

- A convention that fits in a store goes there: the colours of a label in `uns["<key>_colors"]`. The file holds the
  rest, such as method colours and marker shapes, and the colours of a label several datasets share (e.g. a
  genotype), which each store's `uns` copies from it.
- One section per kind (`colors`, `markers`, ...), keys naming what they hold precisely: `sample_embedding_methods`,
  not `methods`.
- The top level holds what all datasets share; `datasets: <dataset>:` adds a dataset's own, in the same sections.
  No key is set at both levels; `tests/test_figure_conventions.py` checks it.
- A script reads the file from its own checkout, not the main one, so a branch that changes it sees the change.

## What an artifact rests on

Two records answer it. A store records which task wrote each of its keys (Data, above). A task's `inputs.yaml`
lists what its code consumed: stores with the keys used, other tasks' files, data files. The
[analysis-workflow](https://github.com/quadbio/analysis-workflow) plugin's `declare-inputs` skill writes that list
from the task's scripts and notebooks. For a human's task, the human asks an agent in this repo to declare its
inputs once the task is finished.

```bash
pixi run analysis-workflow trace <store> <key>      # or: trace <file>
pixi run analysis-workflow trace <store> <key> --format pdf --output <file>.pdf
```

then shows the tasks and artifacts a key or a file rests on, back to the raw data, and fails on a task whose
inputs are not declared. The second form draws the tasks as a graph. The plugin's `trace-lineage` skill writes
both up, as a graph and a summary.

## Exceptions

A rule here, or one of the plugin's, is broken only on purpose and with a human's approval. The pull request notes
it as a row of its "Method and decisions" table:

| decision | value | by | why |
| --- | --- | --- | --- |
| exception: `<the rule>` | `<what was done>` | `<who approved, YYYY-MM-DD>` | `<why the rule could not hold>` |

When the exception belongs to one task, that task's README names it too, in that pull request's entry under
"PRs and issues".

## Git

Humans work in the main checkout. For a human's task a pull request is optional, and encouraged for anything
others build on:

```bash
git switch -c <branch>
git add analysis/<dataset>/<topic>/<task> && git commit -m "<what>"
git push -u origin <branch>
gh pr create                   # its body starts from the PR template
```

It is reviewed against `REVIEW_GUIDE.md`. Switching branches changes the main checkout that agents' sessions read,
`pixi.toml` included, so a human switches back to `main` when done.
