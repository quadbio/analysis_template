#!/usr/bin/env bash
# Submit a job from this task with its log directory resolved absolutely.
#
# `#SBATCH --output=logs/...` is relative to the submit directory, so from a git worktree
# it writes into the worktree and the logs die when the worktree is removed. This resolves
# the task's log directory through `task_paths`, which anchors it to the MAIN checkout, and
# creates it before submitting (sbatch fails silently if the directory is missing).
#
#   ./slurm/submit.sh slurm/job.sbatch [sbatch args...]
set -euo pipefail

TASK_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
MAIN="$(git -C "$TASK_DIR" rev-parse --path-format=absolute --git-common-dir)"
MAIN="$(dirname "$MAIN")"
PY="$MAIN/.pixi/envs/default/bin/python"

LOGS="$("$PY" -c "
from myanalysis import task_paths
p = task_paths('$TASK_DIR/_common.py')
p.ensure()
print(p.logs)
")"

echo "logs -> $LOGS"
sbatch --output="$LOGS/%x-%j.out" --error="$LOGS/%x-%j.err" "$@"
