# Copilot Instructions for Analysis Template

## Project context

See the project README for details about the project goal, datasets, and structure.

## Critical rules
- **Don't update Jupyter notebooks** — I manage them myself
- Use `pixi run <command>` or `pixi shell` for all commands
- Summarize in chat, don't create markdown summary files

## Quick reference

| Task | Command |
|------|---------|
| Run Python | `pixi run python script.py` |
| Run tests | `pixi run test` |
| Add conda package | `pixi add <package>` |
| Add PyPI package | `pixi add --pypi <package>` |

## Project structure
- **Notebooks**: `analysis/[INITIALS]-[YYYY]-[MM]-[DD]_description.ipynb`
- **Data**: `data/<dataset>/{raw,processed,resources,results}/`
- **Paths**: Use `from <package> import FilePaths` (edit `_constants.py` for datasets)
- **Deps**: All in `pixi.toml` (not pyproject.toml)
- pyproject.toml exists mainly for package metadata and testing
- Run `pixi install` after pulling changes that update `pixi.toml`
