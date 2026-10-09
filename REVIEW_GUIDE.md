# Review Guide

PR review playbook for **review agents running on GitHub**. Imperative voice.

**Scope: review only.** Comment and suggest. Do not push commits or apply fixes.

> Everything above "This repo" comes from the analysis template, which takes it from the analysis-workflow
> plugin; change it there and pull it with `cruft update`. Reviewers cannot load the plugin, which is why this
> copy exists.

The code has usually already run. That is not a reason to lower the bar: requiring a rerun in better shape is a
normal outcome. Say what to redo, not just what was wrong.

## Data governance

Every write to a shared object (a working object under `data/*/processed/`, a SpatialData store, anything other
code loads):

- **Accumulate by addition.** Adding keys to freshly re-read state is commutative, so concurrent sessions can't
  lose each other's work. Removal isn't: that means a new dated copy.
- **Writing back to a shared object needs sign-off on that specific diff.**

## Priorities

### 1. Writes that lose data, or silently do nothing

A write to a working object goes through `commit_adata`, gated behind a dry run. Flag:

- an in-memory AnnData written back over a working object (`write_zarr`/`write_h5ad` onto its path): it erases
  whatever other sessions added since it was read;
- a recomputed key committed under an existing name: `commit_adata` writes only keys not yet on disk, so it is a
  no-op and the PR reports a result the object doesn't hold. Use a new key or a new dated copy;
- a replaced SpatialData image, labels, points or shapes element, where a new element name would do.

### 2. Promotions, which leave no diff

`data/` is gitignored, so an object written into `data/<dataset>/processed/` appears nowhere in the diff; the task
README's `Write-back` section is the only trace. The right subdirectory is not guessable. Check that the PR *says*
where it went and that it was agreed, while moving it is still cheap.

### 3. The task contract

Agent work belongs in a task directory `analysis/<topic>/.../<name>_vN/` with a `README.md` naming real inputs,
outputs and write-back keys. Outputs go through `task_paths(__file__)` to the task's own `results/`, `reports/`,
`figures/`, `outputs/`. Writes to `data/<dataset>/results/` or the central `figures/` are the human lane and are a
finding.

Every key committed to a shared object carries the task's version suffix **and** appears in that README: an
unrecorded key can't be traced back, an unsuffixed one collides with the next version.

### 4. Scientific correctness

The point of the repo. Check that the claim in the PR body follows from what the code computes: the right cells,
the right grouping, a control where one is needed, and a comparison not confounded by condition, time point,
sample or batch. A number that reaches a figure is worth more scrutiny than anything below.

### 5. Reinvention

New code needs a reason to exist. Look outward before accepting it: scverse and the Python ecosystem, then the
repo's sibling code packages, then earlier task directories; a near-match found by grep counts. Name the
candidate and what's wrong with it rather than concluding nothing fits.

The acute case is a helper defined twice in one task or copied between tasks: copies drift, and when they compute
a quantity compared *across* tasks, the result is a wrong conclusion. Copying figure code between versions of one
task is fine.

### 6. Conciseness

Prose is reviewed like code. READMEs, docstrings, comments and the PR body: no restating the diff, no filler
preamble, no exhaustive caveats. Padding rots the same way dead code does, and these docs are load-bearing for
the next agent.

## Do not report

- Anything the CI linters already gate: formatting, imports, line length.
- Lock files, and anything under `data/`.
- Committed notebook outputs: review changed cells' code, never the output blobs.
- Absolute paths built from `main_checkout()`: task outputs are anchored there deliberately.
- Worktree, temp-dir and cwd-relative `data/`/`figures/` path literals in `analysis/` code: a hook blocks them
  before the file is written.

## Drift older than the diff

Parts of a repo may predate these rules. When a PR touches such a file, report the drift once at the lowest
severity and don't block; it gets fixed when a task next touches it. Search the open issues before filing one.

## This repo

<!-- Repo-specific rules go here: its shared stores and their write helpers, its companion packages, its
confounders. -->
