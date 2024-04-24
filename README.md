# Analysis template repository

This contains the raw structure I usually use when doing single-cell/spatial data analysis. This template is based on ideas from Philipp Weiler, I took heavy inspiration and copied parts from [his template repository](https://github.com/WeilerP/sc_analysis_template).

## Set up

1. Rename `src/fancypackage/`.
2. Update `pyproject.toml` to include the correct information
    - Project name
    - Project description
    - Project-specific Python requirements
    - Project author
    - Project maintainers
    - Project URLs
3. Update `src/fancypackage/core/_constants.py` to include any paths relevant to your analysis and that should be accessible from any script or Jupyter notebook
4. Update this README to include the relevant information about your project.

## Installation

```bash
pip install -e ".[dev]"
pre-commit install
```

## Things to keep in mind

Whenever you use a new single-cell tool, add it to `known_bio` in `pyproject.toml` s.t. `isort` can work correctly.
