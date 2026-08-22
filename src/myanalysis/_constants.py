"""Project-wide paths for notebooks and scripts."""

from __future__ import annotations

import subprocess
from dataclasses import dataclass, fields
from functools import lru_cache
from pathlib import Path
from typing import Self

#: Standard subfolders of ``data/<dataset>/``.
DATASET_DIRS = ("raw", "processed", "resources", "results")


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


@dataclass(frozen=True)
class _Dirs:
    """A named set of directories."""

    def create(self) -> Self:
        """Create them all, idempotently. Call from the writer, never at import."""
        for field in fields(self):
            getattr(self, field.name).mkdir(parents=True, exist_ok=True)
        return self


@dataclass(frozen=True)
class DatasetPaths(_Dirs):
    """``data/<name>/`` and its standard subfolders."""

    root: Path
    raw: Path
    processed: Path
    resources: Path
    results: Path


class FilePaths:
    """Project-wide paths. Reach datasets through :meth:`dataset`; never hardcode one."""

    ROOT = _repo_root()
    DATA = ROOT / "data"
    FIGURES = ROOT / "figures"

    @classmethod
    def dataset(cls, name: str) -> DatasetPaths:
        """Standard paths for ``data/<name>/``.

        Examples
        --------
        >>> FilePaths.dataset("pbmc3k").create().processed  # doctest: +SKIP
        """
        root = cls.DATA / name
        return DatasetPaths(root=root, **{d: root / d for d in DATASET_DIRS})
