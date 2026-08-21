#!/usr/bin/env bash
# Submit with ./slurm/submit.sh slurm/job.sbatch — it supplies --output/--error as
# absolute paths in the MAIN checkout. Do not add --output here; a relative one would
# write into the worktree and be lost at teardown.
#SBATCH --job-name=task-step
#SBATCH --time=04:00:00
#SBATCH --cpus-per-task=8
#SBATCH --mem-per-cpu=8G
set -euo pipefail

TASK_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
MAIN="$(dirname "$(git -C "$TASK_DIR" rev-parse --path-format=absolute --git-common-dir)")"

# Record what this ran against, so the log identifies the code even after a merge.
echo "task:   $TASK_DIR"
echo "commit: $(git -C "$TASK_DIR" rev-parse --short HEAD)"

# Resolve the interpreter once: concurrent `pixi run` calls serialize on the env prefix.
PY="$MAIN/.pixi/envs/default/bin/python"

"$PY" "$TASK_DIR/scripts/step.py" "$@"
