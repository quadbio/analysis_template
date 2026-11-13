# Review Guide

PR review playbook for **review agents running on GitHub**. Imperative voice.

**Scope: review only.** Comment and suggest. Do not push commits or apply fixes.

> Everything above "This repo" comes from the analysis template; change it there and pull it with `cruft update`.
> It tells reviewers, who cannot load the analysis-workflow plugin, what to check of `CONVENTIONS.md` and the
> plugin's rules. A PR's task directory says its lane: `human_…` or `agent_…`.

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
- a replaced SpatialData image, labels, points or shapes element, where a new element name would do.

### 2. Promotions, which leave no diff

`data/` is gitignored, so an object written into `data/<dataset>/processed/` appears nowhere in the diff; the task
README's `Write-back` section is the only trace. The right subdirectory is not guessable. Check that the README
*says* where it went and, for an agent's PR, that the PR body flags it for sign-off and that it was agreed, while
moving it is still cheap.

### 3. The task contract

Work belongs in a task directory `analysis/<dataset>/<topic>/.../<lane>_<name>_vN/`. Check that its README's
content is real: the actual input files, the deliverables, a short summary of each PR. An edit to a frozen task's
directory (one written back from, or merged) is a finding: analysis moves forward, and a new version names the one
it follows. A task is one branch merged through one or more PRs, so a directory whose earlier PRs (its README lists
them) came from this PR's branch is this task's own, not an earlier one. Outputs written outside the task directory,
other than to a shared object, are a finding.

Every key committed to a shared object appears in that README: an unrecorded key can't be traced back.

### 4. Scientific correctness

The point of the repo. Check that each finding in the PR body follows from what the code computes: the right cells,
the right grouping, a control where one is needed, and a comparison not confounded by condition, time point, sample
or batch. A number that reaches a deliverable is worth more scrutiny than anything below.

### 5. Reinvention

New code needs a reason to exist. Look outward before accepting it: scverse and the Python ecosystem, then the
repo's sibling code packages, then earlier task directories; a near-match found by grep counts. Name the
candidate and what's wrong with it rather than concluding nothing fits.

The acute case is a helper defined twice in one task or copied between tasks: copies drift, and when they compute a
quantity compared *across* tasks, the result is a wrong conclusion. Copying code from the version a task follows is
fine.

### 6. Conciseness

Prose is reviewed like code. READMEs, docstrings, comments and the PR body: no restating the diff, no filler
preamble, no exhaustive caveats. Padding rots the same way dead code does, and these docs are load-bearing for
the next agent. Among the files that keep changing, each fact is written once: findings in the deliverables, the
overview in the task README, which gives each PR a short summary. A PR's body, laid out by
`.github/pull_request_template.md`, is its record as of the merge and may state what the deliverables showed then. A
living file that restates another instead of linking to it is a finding, because the copies drift.

## Do not report

- Anything the CI linters already gate: formatting, imports, line length.
- Lock files, and anything under `data/`.
- Committed notebook outputs: review changed cells' code, never the output blobs.
- Absolute paths built from `main_checkout()`: task outputs are anchored there deliberately.
- In an `agent_` task: its layout and its README's headings, which a hook holds to the task template; and
  worktree, temp-dir and cwd-relative `data/`/`figures/` path literals, which a hook blocks before the file is
  written. A `human_` task has no such hook: report these there.

## Drift older than the diff

Parts of a repo may predate these rules. When a PR touches such a file, report the drift once at the lowest
severity and don't block; it gets fixed when a task next touches it. Earlier task directories are not drift: they
stay as they are. Search the open issues before filing one.

## This repo

<!-- Repo-specific rules go here: its shared stores and their write helpers, its companion packages, its
confounders. -->
