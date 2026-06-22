#!/usr/bin/env python3
"""One-shot renamer for instantiating this template.

Replaces the placeholder package name ``myanalysis`` and the placeholder
project/kernel name ``analysis-template`` everywhere they appear, and renames
the ``src/myanalysis`` directory. Run it once, right after cloning your new repo from the template and *before*
``pixi install`` (it uses only the standard library, so plain ``python`` works):

    python scripts/rename_package.py myproject
    # or, with an explicit Jupyter display name:
    python scripts/rename_package.py myproject --display-name "My Project"

(Also available as ``pixi run rename`` once the environment is installed.)

``PACKAGE`` must be a valid Python identifier (letters, digits, underscores;
not starting with a digit), e.g. ``myproject`` or ``pbmc_atlas``. The project
slug used for the pixi workspace and the Jupyter kernel is derived from it by
turning underscores into hyphens (``pbmc_atlas`` -> ``pbmc-atlas``).

The script is intentionally dependency-free (stdlib only) so it runs before the
environment is installed. It does NOT touch README.md (you're meant to replace
that with your own project docs) or .env.example.
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

OLD_PACKAGE = "myanalysis"
OLD_PROJECT = "analysis-template"
OLD_DISPLAY = "Analysis Template (Pixi)"

REPO_ROOT = Path(__file__).resolve().parents[1]

# Files in which to replace the package name (whole-word) and project slug.
TARGET_FILES = [
    "pyproject.toml",
    "pixi.toml",
    "tests/test_basic.py",
]
# Notebooks are scanned dynamically so new ones are picked up too.
NOTEBOOK_GLOB = "analysis/*.ipynb"


def _fail(msg: str) -> None:
    sys.exit(f"error: {msg}")


def replace_in_file(path: Path, replacements: list[tuple[str, str]]) -> bool:
    """Apply (pattern, repl) regex substitutions to a file. Returns True if changed."""
    if not path.exists():
        return False
    original = path.read_text()
    text = original
    for pattern, repl in replacements:
        text = re.sub(pattern, repl, text)
    if text != original:
        path.write_text(text)
        return True
    return False


def main() -> None:
    parser = argparse.ArgumentParser(description="Rename the template package/project in place.")
    parser.add_argument("package", help="New package import name (valid Python identifier, e.g. 'myproject').")
    parser.add_argument(
        "--display-name",
        default=None,
        help="Jupyter kernel display name (default: derived from the package name).",
    )
    args = parser.parse_args()

    new_package = args.package
    if not new_package.isidentifier():
        _fail(f"{new_package!r} is not a valid Python identifier (use letters, digits, underscores).")
    if new_package == OLD_PACKAGE:
        _fail(f"the new name equals the placeholder {OLD_PACKAGE!r}; nothing to do.")

    new_project = new_package.replace("_", "-")
    new_display = args.display_name or f"{new_package.replace('_', ' ').title()} (Pixi)"

    src_old = REPO_ROOT / "src" / OLD_PACKAGE
    src_new = REPO_ROOT / "src" / new_package
    if not src_old.is_dir():
        _fail(
            f"{src_old.relative_to(REPO_ROOT)} not found. The template may already be renamed "
            "(this script is meant to run once on a fresh clone)."
        )
    if src_new.exists():
        _fail(f"{src_new.relative_to(REPO_ROOT)} already exists; refusing to overwrite.")

    # Whole-word replacements so we never touch substrings of other identifiers.
    replacements = [
        (rf"\b{re.escape(OLD_PACKAGE)}\b", new_package),
        (re.escape(OLD_PROJECT), new_project),
        (re.escape(OLD_DISPLAY), new_display),
    ]

    changed: list[str] = []
    for rel in TARGET_FILES:
        if replace_in_file(REPO_ROOT / rel, replacements):
            changed.append(rel)
    # The package's own sources (e.g. `version("myanalysis")` in __init__.py) —
    # process these before renaming the directory, while the old path is valid.
    for py in sorted(src_old.rglob("*.py")):
        if replace_in_file(py, replacements):
            changed.append(str(py.relative_to(REPO_ROOT)))
    for nb in sorted(REPO_ROOT.glob(NOTEBOOK_GLOB)):
        if replace_in_file(nb, replacements):
            changed.append(str(nb.relative_to(REPO_ROOT)))

    # Rename the package directory last, after its references are updated.
    src_old.rename(src_new)
    changed.append(f"src/{OLD_PACKAGE}/ -> src/{new_package}/")

    print(f"Renamed package '{OLD_PACKAGE}' -> '{new_package}'")
    print(f"Project/kernel slug '{OLD_PROJECT}' -> '{new_project}'")
    print(f"Kernel display name -> '{new_display}'")
    print("\nChanged:")
    for c in changed:
        print(f"  - {c}")
    print(
        "\nNext steps:\n"
        "  1. Review the diff (git diff / git status).\n"
        "  2. Update the [workspace] description and authors in pixi.toml.\n"
        "  3. Replace README.md with your own project docs.\n"
        "  4. pixi install && pixi run install-hooks && pixi run install-kernel\n"
        "  5. pixi run test"
    )


if __name__ == "__main__":
    main()
