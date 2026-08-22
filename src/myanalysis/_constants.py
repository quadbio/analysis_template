"""Project-wide paths for notebooks, scripts and analysis tasks."""

from __future__ import annotations

import subprocess
from dataclasses import dataclass, fields
from functools import lru_cache
from pathlib import Path
from typing import Self

#: Standard subfolders of ``data/<dataset>/``.
DATASET_DIRS = ("raw", "processed", "resources", "results")

#: Task subdirectories git tracks: small, reviewable, they ride the pull request.
TRACKED_TASK_DIRS = ("results", "reports")

#: Task subdirectories git ignores: heavy or noisy, anchored to the main checkout.
UNTRACKED_TASK_DIRS = ("figures", "outputs", "logs")

#: Directory names that sit *inside* a task rather than being one.
_RESERVED_TASK_SUBDIRS = frozenset({*TRACKED_TASK_DIRS, *UNTRACKED_TASK_DIRS, "scripts", "slurm", "notebooks", "docs"})


@lru_cache(maxsize=1)
def main_checkout() -> Path:
    """The main checkout, resolved from git so a worktree still points at it.

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


@dataclass(frozen=True)
class TaskPaths(_Dirs):
    """One task's directories, split by durability rather than by kind.

    ``results``/``reports`` stay in the calling checkout so they ride the pull request;
    ``figures``/``outputs``/``logs`` are anchored to the main checkout so they survive the
    worktree being removed.
    """

    task: Path
    results: Path
    reports: Path
    figures: Path
    outputs: Path
    logs: Path


class FilePaths:
    """Project-wide paths. Add datasets here; never hardcode one."""

    ROOT = main_checkout()
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


def task_paths(file: str | Path) -> TaskPaths:
    """Output directories for the task ``file`` belongs to. Pass ``__file__``.

    The task is the nearest ancestor under ``analysis/`` that is not a known task
    subdirectory, so ``<task>/_common.py`` and ``<task>/scripts/step.py`` both resolve
    to ``<task>``.

    Examples
    --------
    >>> paths = task_paths(__file__).create()  # doctest: +SKIP
    >>> paths.results / "markers.csv"  # tracked  # doctest: +SKIP
    >>> paths.outputs / "embedding.h5ad"  # gitignored, in the main checkout  # doctest: +SKIP
    """
    path = Path(file).resolve()
    parts = path.parts
    if "analysis" not in parts:
        raise ValueError(f"{path} is not under an 'analysis/' directory")
    checkout = Path(*parts[: parts.index("analysis")])

    task = path.parent
    while task.name in _RESERVED_TASK_SUBDIRS:
        task = task.parent
    if task in (checkout / "analysis", checkout):
        raise ValueError(f"{path} is not inside a task directory under 'analysis/'")

    main_task = main_checkout() / "analysis" / task.relative_to(checkout / "analysis")
    return TaskPaths(
        task=task,
        **{d: task / d for d in TRACKED_TASK_DIRS},
        **{d: main_task / d for d in UNTRACKED_TASK_DIRS},
    )
