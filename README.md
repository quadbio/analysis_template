# Analysis template (pixi, notebook-first)

Template for single-cell/spatial **analysis** repos. If you are building a Python library, use the scverse cookiecutter instead: https://github.com/scverse/cookiecutter-scverse.

After you set this up, **replace this README with project-specific docs** so collaborators know what the project does. A good replacement includes: a one-line goal, data locations, key notebooks to run, and who to ping.

## Quick start (pixi)

```bash
pixi install                   # create environment
pixi shell                     # activate it
pre-commit install             # set up git hooks (run once)
pixi run jupyter lab           # start notebooks
pixi run pytest                # run tests
pixi run install-kernel        # add Jupyter kernel (run once)
```

Environment is defined in `pixi.toml` (GPU-ready: torch, jax, rapids-singlecell on Linux; MPS on macOS). `pyproject.toml` is kept for metadata and tool configs (ruff, pytest, hatch-vcs) only.

## What to customize

1. Update `pixi.toml` metadata: project name, description, authors, and kernel display name.
2. Rename the package directory `src/myanalysis/` to your project slug, and update the `name` in `pyproject.toml` to match.
3. Adjust paths in `src/<your-package>/_constants.py` to match your datasets.
4. Update `.github/copilot-instructions.md` with your project name, goal, and dataset locations. This helps AI coding assistants (GitHub Copilot, Claude, etc.) understand your project when you ask them for help.
5. **Replace this README** with project-specific docs: what the project does, how to run key notebooks, and who to contact.

## Data and notebooks

- Notebook naming: `[INITIALS]-[YYYY]-[MM]-[DD]_description.ipynb`.
- Data layout (one folder per dataset):
    - `data/<dataset>/raw/`
    - `data/<dataset>/processed/`
    - `data/<dataset>/resources/`
    - `data/<dataset>/results/`
- Figures: `figures/` or `data/<dataset>/results/`.
- Import paths via the local package:

```python
from myanalysis import FilePaths
```

## Tooling

- **Pixi**: single source of dependency truth (see `pixi.toml`).
- **Ruff**: lint/format Python + notebooks (config in `pyproject.toml`).
- **Biome**: format JSON/YAML (pre-commit hook).
- **Pre-commit**: install with `pre-commit install` (after `pixi shell`).

## GPU notes

- macOS: torch uses MPS; JAX is CPU-only.
- Linux: `rapids-singlecell` + `jax[cuda12]` enable GPU acceleration.

## Clusters

For cluster usage (e.g., ETH Euler):
- General docs: https://docs.hpc.ethz.ch/
- Start notebooks via JupyterHub: https://jupyter.euler.hpc.ethz.ch/hub/
