# Analysis template (pixi, notebook-first)

Template for single-cell/spatial **analysis** repos. If you are building a Python library, use the [scverse cookiecutter](https://github.com/scverse/cookiecutter-scverse) instead.

After you set this up, **replace this README with project-specific docs** so collaborators know what the project does. A good replacement includes: a one-line goal, data locations, key notebooks to run, and who to ping.

## What is pixi?

[Pixi](https://pixi.sh) is a modern package manager that handles both **conda** and **PyPI** packages in one tool. Think of it as a replacement for conda/mamba + pip that:

- Creates isolated environments per project (like conda environments)
- Installs packages from conda-forge AND PyPI together
- Locks exact versions for reproducibility (`pixi.lock`)
- Works cross-platform (macOS, Linux, Windows)

**You don't need conda or pip installed** — pixi handles everything.

### Installing pixi

```bash
# macOS / Linux
curl -fsSL https://pixi.sh/install.sh | bash

# Or with Homebrew
brew install pixi
```

See [pixi installation docs](https://pixi.sh/latest/#installation) for other options.

## Quick start

```bash
pixi install                   # create environment (reads pixi.toml)
pixi shell                     # activate the environment
pre-commit install             # set up git hooks (run once)
pixi run jupyter lab           # start notebooks
pixi run pytest                # run tests
pixi run install-kernel        # add Jupyter kernel (run once)
```

### Daily workflow

Once set up, your typical workflow is:

```bash
cd your-project
pixi shell                     # activate environment
jupyter lab                    # work in notebooks
# ... do your analysis ...
exit                           # leave pixi shell when done
```

Or run commands without entering the shell:

```bash
pixi run jupyter lab           # runs jupyter in pixi environment
pixi run python my_script.py   # runs script in pixi environment
```

## Adding packages

All dependencies live in `pixi.toml`. To add a new package:

### Option 1: Command line (recommended)

```bash
# Add from conda-forge (preferred for scientific packages)
pixi add numpy
pixi add "scanpy>=1.10"

# Add from PyPI (when not available on conda-forge)
pixi add --pypi some-pypi-only-package
```

### Option 2: Edit pixi.toml directly

```toml
# In pixi.toml:

[dependencies]
# Conda packages go here
numpy = ">=2.0"

[pypi-dependencies]
# PyPI packages go here
some-package = "*"
```

Then run `pixi install` to update the environment.

**Tip**: Prefer conda-forge packages when available — they're pre-compiled and faster to install. Use PyPI for packages only available there.

See [pixi documentation](https://pixi.sh/latest/) for more details.

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

- **Pixi**: package manager and environment ([docs](https://pixi.sh))
- **Ruff**: lint/format Python + notebooks ([docs](https://docs.astral.sh/ruff/))
- **Biome**: format JSON/YAML ([docs](https://biomejs.dev/))
- **Pre-commit**: git hooks for code quality — install with `pre-commit install` after `pixi shell`

## GPU notes

- **macOS**: PyTorch uses MPS (Apple Silicon GPU); JAX is CPU-only.
- **Linux**: `rapids-singlecell` + `jax[cuda12]` enable NVIDIA GPU acceleration.

The template automatically configures the right packages per platform.

## Clusters

For cluster usage (e.g., ETH Euler):
- General docs: https://docs.hpc.ethz.ch/
- Start notebooks via JupyterHub: https://jupyter.euler.hpc.ethz.ch/hub/
