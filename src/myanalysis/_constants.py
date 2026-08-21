"""Project-wide path constants for notebooks and scripts."""

from __future__ import annotations

import subprocess
from dataclasses import dataclass
from functools import lru_cache
from pathlib import Path

# Files that mark the repository root, searched for upward from this module.
_ROOT_MARKERS = ("pixi.toml", ".git")


def _find_root(start: Path) -> Path:
    """Locate the repo root by walking upward until a marker file is found.

    Falls back to the fixed ``src/<package>/`` layout (three levels up) when no
    marker is present, e.g. for a non-editable installed copy.
    """
    for parent in (start, *start.parents):
        if any((parent / marker).exists() for marker in _ROOT_MARKERS):
            return parent
    return start.parents[2]


@dataclass(frozen=True)
class DatasetPaths:
    """Standard subfolders for a single dataset (``data/<name>/``)."""

    root: Path

    @property
    def raw(self) -> Path:
        """Original, unmodified input data."""
        return self.root / "raw"

    @property
    def processed(self) -> Path:
        """Preprocessed / intermediate data."""
        return self.root / "processed"

    @property
    def resources(self) -> Path:
        """Reference data, gene sets, annotations."""
        return self.root / "resources"

    @property
    def results(self) -> Path:
        """Analysis outputs (tables, exported objects)."""
        return self.root / "results"

    def create(self) -> DatasetPaths:
        """Create all standard subfolders (idempotent). Returns ``self``."""
        for path in (self.raw, self.processed, self.resources, self.results):
            path.mkdir(parents=True, exist_ok=True)
        return self


class FilePaths:
    """Project-wide paths for notebooks and scripts."""

    ROOT = _find_root(Path(__file__).resolve())

    DATA = ROOT / "data"
    FIGURES = ROOT / "figures"

    # The bundled example dataset; customize / add your own via `dataset()`.
    EXAMPLE_DATASET = DATA / "example_dataset"

    @classmethod
    def dataset(cls, name: str) -> DatasetPaths:
        """Return the standard raw/processed/resources/results paths for a dataset.

        Examples
        --------
        >>> paths = FilePaths.dataset("pbmc3k").create()
        >>> paths.processed / "adata.h5ad"  # doctest: +SKIP
        """
        return DatasetPaths(cls.DATA / name)


# --------------------------------------------------------------------------- #
# Analysis tasks                                                              #
# --------------------------------------------------------------------------- #

#: Task subdirectories that git tracks: small, reviewable, they ride the PR.
TRACKED_TASK_DIRS = ("results", "reports")

#: Task subdirectories git ignores: heavy or noisy, anchored to the main checkout.
UNTRACKED_TASK_DIRS = ("figures", "outputs", "logs")

#: Directory names that are *inside* a task rather than a task themselves.
_RESERVED_TASK_SUBDIRS = frozenset({*TRACKED_TASK_DIRS, *UNTRACKED_TASK_DIRS, "scripts", "slurm", "notebooks", "docs"})


@lru_cache(maxsize=1)
def main_checkout() -> Path:
    """Absolute path of the *main* checkout, even when called from a git worktree.

    Resolved from git rather than from where this package happens to be installed.
    ``--git-common-dir`` points at the main checkout's ``.git`` from any worktree,
    whereas :data:`FilePaths.ROOT` walks up for a marker and so stops at the worktree
    (a worktree's ``.git`` is a file, but it still exists).
    """
    try:
        out = subprocess.run(
            ["git", "rev-parse", "--path-format=absolute", "--git-common-dir"],
            cwd=Path(__file__).resolve().parent,
            capture_output=True,
            text=True,
            check=True,
        ).stdout.strip()
    except (subprocess.CalledProcessError, OSError):
        return FilePaths.ROOT
    return Path(out).parent


@dataclass(frozen=True)
class TaskPaths:
    """Where one analysis task's outputs go, split by durability rather than by kind.

    ``results`` and ``reports`` stay in the checkout the calling file lives in, so they
    ride the pull request. ``figures``, ``outputs`` and ``logs`` are anchored to the main
    checkout, so they survive a worktree being removed — a bare relative path written from
    a worktree is lost silently, because worktrees are gitignored and git will not warn you.
    """

    task: Path
    results: Path
    reports: Path
    figures: Path
    outputs: Path
    logs: Path

    def ensure(self) -> TaskPaths:
        """Create the directories. Call this from the writer, never at import time."""
        for name in (*TRACKED_TASK_DIRS, *UNTRACKED_TASK_DIRS):
            getattr(self, name).mkdir(parents=True, exist_ok=True)
        return self


def task_paths(file: str | Path) -> TaskPaths:
    """Resolve the output directories for the task that ``file`` belongs to.

    Pass ``__file__``. The task directory is the nearest ancestor under ``analysis/``
    whose name is not a known task subdirectory, so both ``<task>/_common.py`` and
    ``<task>/scripts/step.py`` resolve to ``<task>``.

    Examples
    --------
    >>> paths = task_paths(__file__).ensure()  # doctest: +SKIP
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
        results=task / "results",
        reports=task / "reports",
        figures=main_task / "figures",
        outputs=main_task / "outputs",
        logs=main_task / "logs",
    )
