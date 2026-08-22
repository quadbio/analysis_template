"""Project-wide paths for notebooks and scripts."""

from __future__ import annotations

import subprocess
from functools import lru_cache
from pathlib import Path


@lru_cache(maxsize=1)
def _repo_root() -> Path:
    """The repository root, from git so a worktree still names the main checkout.

    Falls back to walking up for ``pixi.toml``/``.git`` outside a repository.
    """
    try:
        git_dir = subprocess.run(
            ["git", "rev-parse", "--path-format=absolute", "--git-common-dir"],
            cwd=Path(__file__).resolve().parent,
            capture_output=True,
            text=True,
            check=True,
        ).stdout.strip()
        return Path(git_dir).parent
    except (subprocess.CalledProcessError, OSError):
        here = Path(__file__).resolve()
        for parent in (here, *here.parents):
            if (parent / "pixi.toml").exists() or (parent / ".git").exists():
                return parent
        return here.parents[2]


class FilePaths:
    """Project-wide paths. Add a dataset as a constant here; never hardcode one."""

    ROOT = _repo_root()

    DATA = ROOT / "data"
    FIGURES = ROOT / "figures"

    EXAMPLE_DATASET = DATA / "example_dataset"
