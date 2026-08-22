"""Shared paths for this task. Copy with the template; edit in place.

Every output path in the task comes from here, so nothing is a bare relative path.
Nothing is created at import: call ``PATHS.create()`` in the writer, so a dry run stays dry.
"""

from myanalysis import task_paths

PATHS = task_paths(__file__)

#: Tracked: small evidence tables and the report. Ride the pull request.
RESULTS = PATHS.results
REPORTS = PATHS.reports

#: Gitignored, anchored to the main checkout so they survive worktree teardown.
FIGURES = PATHS.figures
OUTPUTS = PATHS.outputs
LOGS = PATHS.logs

#: The object this task reads. Supplied per session and recorded in README.md — never
#: hardcoded, because which object is current changes over time.
WORKING_OBJECT = None
