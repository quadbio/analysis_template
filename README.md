# 🧬 Analysis Template (pixi, notebook-first)

Template for single-cell/spatial **analysis** repos. If you're building a Python library, use the [scverse cookiecutter](https://github.com/scverse/cookiecutter-scverse) instead.

> 📝 **After setup, replace this README** with project-specific docs so collaborators know what the project does. Include: a one-line goal, data locations, key notebooks to run, and who to ping.

---

## 📦 What is pixi?

[Pixi](https://pixi.sh) is a modern package manager that handles both **conda** and **PyPI** packages in one tool. Think of it as a replacement for conda/mamba + pip that:

- 🔒 Creates **isolated environments** per project (like conda environments)
- 🔀 Installs packages from **conda-forge AND PyPI** together
- 📌 Locks exact versions for **reproducibility** (`pixi.lock`)
- 💻 Works **cross-platform** (macOS, Linux, Windows)

**You don't need conda or pip installed** — pixi handles everything!

### 🛠️ Installing pixi

```bash
# macOS / Linux
curl -fsSL https://pixi.sh/install.sh | bash

# Or with Homebrew (macOS)
brew install pixi
```

👉 See [pixi installation docs](https://pixi.sh/latest/#installation) for Windows and other options.

---

## 🚀 Quick start

```bash
pixi install                   # create environment (reads pixi.toml)
pixi shell                     # activate the environment
pre-commit install             # set up code quality hooks (run once)
pixi run lab                   # start Jupyter Lab
pixi run test                  # run tests
pixi run install-kernel        # add Jupyter kernel (run once)
```

### ☕ Daily workflow

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
pixi run lab                   # runs Jupyter in pixi environment
pixi run python my_script.py   # runs script in pixi environment
```

---

## ➕ Adding packages

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

💡 **Tip**: Prefer **conda-forge** packages when available — they're pre-compiled and faster to install. Use PyPI for packages only available there.

👉 See [pixi documentation](https://pixi.sh/latest/) for more details.

---

## ✏️ What to customize

1. Update `pixi.toml` metadata: project name, description, authors, and kernel display name.
2. Rename the package directory `src/myanalysis/` to your project slug, and update the `name` in `pyproject.toml` to match.
3. Adjust paths in `src/<your-package>/_constants.py` to match your datasets.
4. Update `.github/copilot-instructions.md` with your project name, goal, and dataset locations. This helps AI coding assistants (GitHub Copilot, Claude, etc.) understand your project.
5. 📝 **Replace this README** with project-specific docs: what the project does, how to run key notebooks, and who to contact.

---

## 📓 Data and notebooks

- **Notebook naming**: `[INITIALS]-[YYYY]-[MM]-[DD]_description.ipynb`
- **Data layout** (one folder per dataset):
    - `data/<dataset>/raw/` — original data files
    - `data/<dataset>/processed/` — preprocessed data
    - `data/<dataset>/resources/` — reference data, annotations
    - `data/<dataset>/results/` — analysis outputs
- **Figures**: `figures/` or `data/<dataset>/results/`
- **Import paths** via the local package:

```python
from myanalysis import FilePaths
```

---

## 🔧 Tooling & code quality

This template uses **pre-commit hooks** to automatically check your code before each commit. This catches common issues early and keeps code consistent across the team.

### What are pre-commit hooks?

[Pre-commit](https://pre-commit.com/) is a tool that runs checks on your code **every time you run `git commit`**. If any check fails, the commit is blocked until you fix the issue. This ensures:

- ✅ Code is consistently formatted
- ✅ Common bugs are caught early
- ✅ Everyone's code looks the same

### Tools we use

| Tool | What it does | Docs |
|------|--------------|------|
| 🦀 **[Ruff](https://docs.astral.sh/ruff/)** | Lints (finds bugs/style issues) and formats Python code + Jupyter notebooks. Super fast! | [Rules](https://docs.astral.sh/ruff/rules/) |
| 🌿 **[Biome](https://biomejs.dev/)** | Formats JSON and JSONC files for consistency | [Guide](https://biomejs.dev/guides/getting-started/) |
| 📋 **[pyproject-fmt](https://github.com/tox-dev/pyproject-fmt)** | Keeps `pyproject.toml` nicely formatted | — |

### Setting up pre-commit

Run this once after cloning the repo:

```bash
pixi shell
pre-commit install
```

Now hooks run automatically on `git commit`. To run all checks manually:

```bash
pre-commit run --all-files
```

💡 **Tip**: If a check reformats your code, just `git add` the changes and commit again!

---

## 🖥️ GPU notes

| Platform | PyTorch | JAX |
|----------|---------|-----|
| **macOS** (Apple Silicon) | ✅ MPS acceleration | ❌ CPU only |
| **Linux** (NVIDIA GPU) | ✅ CUDA | ✅ CUDA 12 via `jax[cuda12]` |

The template automatically configures the right packages per platform. Linux also gets [rapids-singlecell](https://rapids-singlecell.readthedocs.io/) for GPU-accelerated single-cell analysis.

---

## 🖧 Cluster usage

For cluster usage (e.g., ETH Euler):

- 📚 General docs: https://docs.hpc.ethz.ch/
- 🚀 Start notebooks via JupyterHub: https://jupyter.euler.hpc.ethz.ch/hub/
