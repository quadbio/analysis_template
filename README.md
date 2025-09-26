# Analysis template repository

This contains the raw structure I usually use when doing single-cell/spatial data analysis. This template is based on ideas from Philipp Weiler's [template repository](https://github.com/WeilerP/sc_analysis_template) as well as the [scverse cookiecutter template](https://github.com/scverse/cookiecutter-scverse).

## Set up

1. Rename `src/fancypackage/`.
2. Update `pyproject.toml` to include the following information:
    - Project name
    - Project description
    - Project-specific Python requirements
    - Project author
    - Project maintainers
    - Project URLs
3. Update `src/fancypackage/ul/constants.py` to include any paths relevant to your analysis and that should be accessible from any script or Jupyter notebook
4. Update this README to include the relevant information about your project.

## Installation

```bash
pip install -e ".[dev,test]"
pre-commit install
```

## Development

This template uses:
- **Biome** for JavaScript/JSON/YAML formatting
- **Ruff** for Python linting and formatting
- **Pre-commit hooks** for code quality

The package provides a minimal structure for analysis projects. Add your analysis-specific dependencies (numpy, pandas, scanpy, etc.) as needed for your project.
