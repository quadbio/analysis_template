# <task name, matching this directory>

**Date:** <YYYY-MM-DD, when the task started>

One or two sentences on what this task set out to answer.

## Inputs

Name the actual files, not concepts — this is what makes the task re-runnable.

- Working object: `data/<dataset>/processed/<object>.h5ad`
- Other artifacts consumed: `analysis/<other_task>/outputs/<file>`, `data/<dataset>/results/<file>`

## Outputs

| what | where |
| --- | --- |
| evidence tables | `results/` (tracked) |
| report | `reports/` (tracked) |
| figures | `figures/` (gitignored, in the main checkout) |
| data artifacts | `outputs/` (gitignored, in the main checkout) |

## Write-back

What went into the working object, and under which keys. The version identifier in this
directory's name must appear in the key names, so an `obs` column can be traced back here
by grepping `analysis/**/README.md`.

- `obs["<name>_<version>"]` — one line on what it holds
- `obsm["X_<name>_<version>"]` — likewise

Artifacts too large to embed stay in `outputs/` and are listed above instead. Anything
promoted to central storage (`data/<dataset>/...`) at sign-off is recorded here with its
final path.

## Notes

Decisions a reader would otherwise have to reverse-engineer: what was tried and rejected,
which parameters are load-bearing, what is still provisional.
