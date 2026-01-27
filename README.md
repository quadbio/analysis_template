# 🧬 Analysis Template

A notebook-first template for single-cell/spatial analysis projects. Uses [pixi](https://pixi.sh) for environment management.

> If you're building a reusable Python library, use the [scverse cookiecutter](https://github.com/scverse/cookiecutter-scverse) instead.

---

## 🚀 Getting Started

**You've initialized a new repo from this template—great!** Follow these steps to set up your project.

### Step 1: Install pixi

*Skip this if you already have pixi installed.*

```bash
# macOS / Linux
curl -fsSL https://pixi.sh/install.sh | bash

# Or with Homebrew (macOS)
brew install pixi
```

Restart your terminal after installation. See [pixi installation docs](https://pixi.sh/latest/#installation) for Windows and other options.

### Step 1b: Install GitHub CLI (optional)

*Recommended if you're working on a remote server and need to authenticate with GitHub.*

```bash
# macOS
brew install gh

# Linux (no sudo required)
curl -sS https://webi.sh/gh | sh
```

Then authenticate: `gh auth login`. See [GitHub CLI installation docs](https://github.com/cli/cli#installation) for more options.

### Step 2: Clone your repo locally

```bash
git clone <your-repo-url>
cd <your-project-name>
```

The URL depends on your authentication method:
- **HTTPS**: `https://github.com/owner/repo.git`
- **SSH**: `git@github.com:owner/repo.git`
- **GitHub CLI**: `gh repo clone owner/repo`

### Step 3: Customize the template

Before installing the environment, update these files with your project details:

| File | What to change |
|------|----------------|
| `src/myanalysis/` | **Rename this folder** to your project slug (e.g., `src/myproject/`) |
| `pyproject.toml` | Update `name` to match your renamed folder |
| `pixi.toml` | Update `name`, `description`, `authors`, kernel `display-name`, and `myanalysis` → your package name in `[pypi-dependencies]` |

### Step 4: Set up the environment

```bash
pixi install                   # create environment from pixi.toml
pixi run pre-commit install    # set up code quality hooks
pixi run install-kernel        # register Jupyter kernel
```

💡 **Tip**: Use `pixi shell` to enter the environment interactively—then you can run commands directly without the `pixi run` prefix.

### Step 5: Verify your setup

```bash
pixi run test                  # should pass (tests your package imports correctly)
pixi run lab                   # opens Jupyter Lab
```

In Jupyter Lab, check that your kernel appears (look for the name you set in `pixi.toml`).

### Step 6: Make your first commit

```bash
git add -A
git commit -m "Initial project setup"
git push
```

💡 Pre-commit hooks will run and may reformat some files. If so, just `git add -A && git commit -m "Initial project setup"` again.

🎉 **You're ready to start analyzing!**

---

## 📊 Start Your Analysis

- **Demo notebook**: Check out `analysis/demo_scRNA_workflow.ipynb` for a complete scRNA-seq workflow example using scanpy's PBMC 3k dataset.
- **New notebooks**: Copy `analysis/XX-2026-01-27_sample_notebook.ipynb` as a starting point. Follow the naming convention: `[INITIALS]-[YYYY]-[MM]-[DD]_description.ipynb`.
- **Add your data**: Create folders under `data/` and register paths in `src/<your-package>/_constants.py`.
- **Replace this README** with your project documentation once you're set up.

---

## ☕ Daily Workflow

```bash
cd your-project
pixi shell                     # activate environment
jupyter lab                    # work in notebooks, or start via jupyter-hub
# ... do your analysis ...
exit                           # leave pixi shell when done
```

Or run commands directly without entering the shell:

```bash
pixi run lab                   # start Jupyter Lab
pixi run python script.py      # run a script
```

---

## 📚 Reference

<details>
<summary><strong>📦 What is pixi?</strong></summary>

[Pixi](https://pixi.sh) is a modern package manager that handles both **conda** and **PyPI** packages in one tool:

- 🔒 Creates **isolated environments** per project
- 🔀 Installs from **conda-forge AND PyPI** together
- 📌 Locks exact versions for **reproducibility** (`pixi.lock`)
- 💻 Works **cross-platform** (macOS, Linux, Windows)

**You don't need conda or pip installed** — pixi handles everything!

</details>

<details>
<summary><strong>➕ Adding packages</strong></summary>

All dependencies live in `pixi.toml`. To add a new package:

```bash
# From conda-forge (preferred for scientific packages)
pixi add numpy
pixi add "scanpy>=1.10"

# From PyPI (when not on conda-forge)
pixi add --pypi some-package
```

Or edit `pixi.toml` directly and run `pixi install`.

💡 **Tip**: Prefer PyPI packages when available — mixing conda and pip can cause dependency conflicts.

👉 See [pixi documentation](https://pixi.sh/latest/) for more details.

</details>

<details>
<summary><strong>📓 Data and notebook conventions</strong></summary>

- **Notebook naming**: `[INITIALS]-[YYYY]-[MM]-[DD]_description.ipynb`
- **Data layout** (one folder per dataset):
    - `data/<dataset>/raw/` — original data files
    - `data/<dataset>/processed/` — preprocessed data
    - `data/<dataset>/resources/` — reference data, annotations
    - `data/<dataset>/results/` — analysis outputs
- **Figures**: `figures/` or `data/<dataset>/results/`
- **Import paths** via the local package:

```python
from yourpackage import FilePaths
```

</details>

<details>
<summary><strong>🔧 Pre-commit & code quality</strong></summary>

This template uses **pre-commit hooks** to automatically check your code before each commit:

| Tool | What it does |
|------|--------------|
| [Ruff](https://docs.astral.sh/ruff/) | Lints and formats Python code + notebooks |
| [Biome](https://biomejs.dev/) | Formats JSON/JSONC files |
| [pyproject-fmt](https://github.com/tox-dev/pyproject-fmt) | Formats `pyproject.toml` |

Hooks run automatically on `git commit`. To run manually:

```bash
pre-commit run --all-files
```

💡 If a check reformats your code, just `git add` the changes and commit again.

</details>

<details>
<summary><strong>🖥️ GPU notes</strong></summary>

| Platform | PyTorch | JAX |
|----------|---------|-----|
| **macOS** (Apple Silicon) | ✅ MPS acceleration | ❌ CPU only |
| **Linux** (NVIDIA GPU) | ✅ CUDA | ✅ CUDA 12 |

The template auto-configures packages per platform. Linux also gets [rapids-singlecell](https://rapids-singlecell.readthedocs.io/) for GPU-accelerated analysis.

</details>

<details>
<summary><strong>🖧 Cluster usage</strong></summary>

For cluster usage (e.g., ETH Euler):

- 📚 General docs: https://docs.hpc.ethz.ch/
- 🚀 Notebooks via JupyterHub: https://jupyter.euler.hpc.ethz.ch/hub/

</details>
