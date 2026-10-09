# 🧬 {{ cookiecutter.project_name }}

{{ cookiecutter.project_description }}

<!-- Describe the project here. The sections below come from quadbio/analysis_template and update with `cruft update`. -->

---

## 🚀 Getting Started

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

### Step 2: Clone the repo

```bash
git clone <repo-url>
cd {{ cookiecutter.project_name }}
```

The URL depends on your authentication method:
- **HTTPS**: `https://github.com/owner/repo.git`
- **SSH**: `git@github.com:owner/repo.git`
- **GitHub CLI**: `gh repo clone owner/repo`

### Step 3: Set up the environment

```bash
pixi install                   # create environment from pixi.toml
pixi run install-hooks         # pre-commit hooks
pixi run install-kernel        # register Jupyter kernel
```

> **Notebook outputs are committed.** They are the record of what a notebook actually
> produced, and GitHub renders them. Keep them small: clear a notebook by hand before
> committing if it carries a huge embedded image or an accidental dump.

💡 **Tip**: Use `pixi shell` to enter the environment interactively—then you can run commands directly without the `pixi run` prefix.

### Step 4: Verify your setup

```bash
pixi run test                  # should pass (tests your package imports correctly)
pixi run lab                   # opens Jupyter Lab
```

In Jupyter Lab, check that your kernel appears (look for `{{ cookiecutter.project_name }} (pixi)`).

🎉 **You're ready to start analyzing!**

---

## 📊 Start Your Analysis

- **Demo notebook**: Check out `analysis/ML-2026-01-27_demo_scRNA_workflow.ipynb` for a complete scRNA-seq workflow example using scanpy's PBMC 3k dataset.
- **New notebooks**: Copy `analysis/XX-2026-01-27_sample_notebook.ipynb` as a starting point. Follow the naming convention: `[INITIALS]-[YYYY]-[MM]-[DD]_description.ipynb`.
- **Add your data**: Create folders under `data/` and register paths in `src/{{ cookiecutter.package_name }}/_constants.py`.

---

## 🤖 Working with coding agents

Agents follow [`AGENTS.md`](AGENTS.md) and the
[analysis-workflow](https://github.com/quadbio/analysis-workflow) Claude Code plugin (a skill plus
guard hooks) that this repo enables. Install the plugin once per machine:

```bash
claude plugin marketplace add quadbio/claude-plugins
claude plugin install analysis-workflow@quadbio
```

---

## ☕ Daily Workflow

```bash
cd {{ cookiecutter.project_name }}
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
- **Data layout** (one folder per dataset, gitignored):
    - `data/<dataset>/raw/` — bytes as they arrived; never written by analysis
    - `data/<dataset>/resources/` — curated inputs that are not data: gene lists, marker tables
    - `data/<dataset>/processed/` — objects code loads to do new work, as AnnData `.zarr`
    - `data/<dataset>/results/` — a notebook's own outputs, file names prefixed with the notebook's stem
- **Figures**: `figures/<topic>/`
- **Import paths** via the local package:

```python
from {{ cookiecutter.package_name }} import FilePaths
```

</details>

<details>
<summary><strong>🔧 Pre-commit & code quality</strong></summary>

This repo uses **pre-commit hooks** to automatically check your code before each commit:

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

The **default** environment is CPU-only on every platform (on macOS, PyTorch
still uses MPS automatically). This is what `pixi install` and CI use.

GPU acceleration lives in a separate **`gpu`** environment that you opt into
explicitly on a Linux/CUDA machine (e.g. ETH Euler):

```bash
pixi install -e gpu            # CUDA 12 build of JAX + rapids-singlecell
pixi run -e gpu install-kernel # register a kernel for the gpu env
pixi shell -e gpu              # or activate it interactively
```

| Environment | PyTorch | JAX | rapids-singlecell |
|-------------|---------|-----|-------------------|
| `default` (all platforms) | ✅ (MPS on macOS) | CPU | ❌ |
| `gpu` (Linux + NVIDIA only) | ✅ CUDA | ✅ CUDA 12 | ✅ |

> Keeping the GPU stack out of the default environment means CI and CPU-only
> machines don't try to resolve unusable CUDA wheels. See
> [rapids-singlecell](https://rapids-singlecell.readthedocs.io/).

</details>

<details>
<summary><strong>🔑 Secrets & environment variables</strong></summary>

Store API keys and other secrets in a `.env` file at the repo root. It is
**gitignored** and must never be committed.

```bash
cp .env.example .env   # then fill in your real values
```

`.env.example` (tracked, placeholder values only) documents which variables the
project expects. Load them in a notebook or script with, e.g.,
[python-dotenv](https://github.com/theskumar/python-dotenv):

```python
from dotenv import load_dotenv
load_dotenv()
```

If you ever paste a real key into a tracked file, rotate it immediately in the
provider's dashboard — git history is hard to scrub.

</details>

<details>
<summary><strong>🖧 Cluster usage</strong></summary>

For cluster usage (e.g., ETH Euler):

- 📚 General docs: https://docs.hpc.ethz.ch/
- 🚀 Notebooks via JupyterHub: https://jupyter.euler.hpc.ethz.ch/hub/

</details>
