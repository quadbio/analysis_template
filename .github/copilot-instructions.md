# Copilot Instructions for Analysis Template

## Project context (fill these before working)
- **Project name:** <fill>
- **One-liner goal:** <fill>
- **Primary datasets / locations:** <fill>

## Important notes
- This is an analysis repository using **pixi** for environment management
- Use `pixi run <command>` or `pixi shell` to work in the environment
- Analysis notebooks follow template: `analysis/[INITIALS]-[YYYY]-[MM]-[DD]_description.ipynb`
- Avoid drafting summary documents, e.g. endless markdown files. Just summarize in chat what you did, why, and any open questions.
- Don't update my jupyter notebooks - I manage them myself.

## Environment Management (pixi)

```bash
# Install environment
pixi install

# Activate shell
pixi shell

# Run commands directly
pixi run jupyter lab
pixi run pytest

# Install Jupyter kernel (already done)
pixi run install-kernel
```

### Platform-specific behavior
- **macOS ARM64**: CPU-only JAX, PyTorch with MPS support
- **Linux (Euler)**: JAX with CUDA 12, PyTorch with CUDA support. Start notebooks via JupyterHub: https://jupyter.euler.hpc.ethz.ch/hub/

## Analysis Workflow

### Notebook naming convention
`analysis/[INITIALS]-[YYYY]-[MM]-[DD]_description.ipynb`

### Data organization
```
data/
  <dataset_name>/
    raw/          # Original data files
    processed/    # Preprocessed AnnData objects
    resources/    # Reference data, annotations
    results/      # Analysis outputs
```

### Using local package
```python
from myanalysis import FilePaths
```
Paths resolve relative to repo root; adjust `_constants.py` for your datasets.

## Development Notes

- Python 3.12 for maximum package compatibility
- Uses pixi.toml as single source of truth (not pyproject.toml for analysis deps)
- pyproject.toml exists mainly for package metadata and testing
- Run `pixi install` after pulling changes that update `pixi.toml`
