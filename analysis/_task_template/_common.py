"""Shared paths and constants for this task. Copy with the template; edit in place.

Every output path in the task comes from here, so nothing is a bare relative path. That
matters because a relative write from inside a git worktree lands in the worktree and
disappears when it is removed — and since worktrees are gitignored, git will not warn you.

``task_paths`` splits the task's directories by durability, not by kind:

    results/  reports/    tracked -> stay in this checkout, ride the pull request
    figures/  outputs/  logs/    ignored -> anchored to the MAIN checkout, survive teardown

Nothing is created at import time. Call ``PATHS.ensure()`` in the writer, so a dry run
stays dry.
"""

from myanalysis import task_paths

PATHS = task_paths(__file__)

#: Small, reviewable evidence tables (csv/json) and the task's HTML report.
RESULTS = PATHS.results
REPORTS = PATHS.reports

#: Heavy or noisy: figures, data artifacts, Slurm logs. Gitignored, anchored to MAIN.
FIGURES = PATHS.figures
OUTPUTS = PATHS.outputs
LOGS = PATHS.logs

#: The object this task reads. Supplied by the human at session start and recorded in
#: README.md — never hardcoded here, because which object is current changes over time.
#: Set it from an environment variable, a CLI argument, or edit this line for the task.
WORKING_OBJECT = None
