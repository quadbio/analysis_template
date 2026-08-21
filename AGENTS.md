# AGENTS.md — analysis conventions

This file owns the working conventions. `README.md` is the user-facing overview; anything
documented elsewhere is referenced from here, never restated.

## Analysis tasks

A **task** is one agent session, one git worktree, one branch, and however many PRs it takes.
It gets one directory, `analysis/<topic>/.../<name_vN>/`, carrying a version suffix. The name is
chosen once and never changed, because the path is what links artifacts back to the analysis
that produced them.

Copy `analysis/_task_template/` to start one.

Humans also work in `analysis/` in notebooks, in the main checkout — the same conventions apply,
and notebooks keep their `[INITIALS]-[YYYY]-[MM]-[DD]_description.ipynb` naming.

### Where outputs go

Placement is decided by *sharing*, on either side: anything another task or a human reads or
writes is central (`data/<dataset>/`); everything else is task-local. That call is made at
end-of-session sign-off rather than at write time — you cannot know at write time whether
something will be reused — so until then artifacts sit in `outputs/`.

Task-local splits by durability, not by kind:

| dir | tracked | lives in | holds |
| --- | --- | --- | --- |
| `results/` | yes | this checkout | small evidence tables — csv, json |
| `reports/` | yes | this checkout | HTML, figures embedded as base64 so they render on GitHub |
| `figures/` | no | the **main** checkout | pdf, png |
| `outputs/` | no | the **main** checkout | data artifacts, checkpoints |
| `logs/` | no | the **main** checkout | batch job output |

The tracked two stay in the worktree so they ride the PR; the untracked three are anchored to
the main checkout so they survive the worktree being removed. Both come from
`task_paths(__file__)` — **never write a bare relative output path.** From a worktree that lands
in the worktree, and since worktrees are gitignored, nothing will warn you.

Batch jobs are the usual way this bites: `--output` resolves against the *submit* directory, so
pass it absolutely (`slurm/submit.sh` does).

The top-level `figures/` is for **curated** output — figures chosen for a talk or a paper — not
for task output.

### The README contract

Every task delivers a report, however small, and a `README.md` naming the date, the inputs it
consumed, the outputs it wrote and where write-back landed. The version suffix appears in the
write-back key names too, so grepping `analysis/**/README.md` gets you from an `obs` column back
to the task that made it. That reverse index is what keeps central storage from being anonymous.

## Data

- Datasets live in `data/<dataset>/{raw,processed,resources,results}/`, gitignored. Note that
  `data/<dataset>/results/` is *central and untracked* — not the same thing as a task's tracked
  `results/`.
- Use `from <package> import FilePaths`; edit `_constants.py` to add a dataset. Never hardcode a
  dataset path.
- **Accumulate by addition.** Adding new keys to a freshly re-read object is commutative, so
  concurrent sessions cannot lose each other's work whatever the write order. Removing something
  is not — that means a new dated copy, keeping the old one so old scripts still run.
- **Never write your in-memory object back over a shared one.** By the time an analysis
  finishes, its copy is stale shared state. Re-read from disk, apply your named additions, write
  a temp file in the same directory and `os.replace` it.
- Which object is current is stated by the human per session and recorded in the task README —
  never hardcoded in a helper or a config, which is how a config ends up pointing at an object
  retired months ago.
- Writing back to a shared object needs explicit sign-off on that specific diff. That gate is
  also what serializes concurrent sessions, which is why no file lock is needed.

## Environments

Dependencies live in `pixi.toml`. **Reusability decides where a package goes, not just whether it
resolves:** one likely to be carried forward is worth making work in the root environment even
when it resists; a stack of packages for a benchmark where at most the winner survives belongs in
an isolated task-local `pixi.toml`, promoted later if it earns it. Only the manifest and lock
persist — the environment is derived, dies with the worktree, and rebuilds with
`pixi install --frozen`.

Run `pixi install` **in the main checkout only**. If the root manifest declares the package as an
editable `path = "."` dependency, installing from a worktree rebases the package — and every
resolved data path with it — into the worktree.

| Task | Command |
| --- | --- |
| Run Python | `pixi run python script.py` |
| Run tests | `pixi run test` |
| Add conda package | `pixi add <package>` |
| Add PyPI package | `pixi add --pypi <package>` |

## Sessions

One task, one session, one worktree. Exit with `/exit` and answer *remove*; push before walking
away, since a worktree with unpushed commits is the only unrecoverable state. Don't exit while
batch jobs are still queued — they reference scripts by path inside the worktree.
