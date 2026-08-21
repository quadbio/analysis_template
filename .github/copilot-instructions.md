# Copilot Instructions for Analysis Template

## Project context

See the project README for details about the project goal, datasets, and structure.

## Quick reference

| Task | Command |
|------|---------|
| Run Python | `pixi run python script.py` |
| Run tests | `pixi run test` |
| Add conda package | `pixi add <package>` |
| Add PyPI package | `pixi add --pypi <package>` |

## Project structure

Canonical guidance lives in `AGENTS.md` — analysis tasks, where outputs go, the data rules and
environments. If this file conflicts with it, `AGENTS.md` wins.

- **Notebooks**: `analysis/[INITIALS]-[YYYY]-[MM]-[DD]_description.ipynb`
- **Agent tasks**: one directory each, `analysis/<topic>/.../<name_vN>/` — copy
  `analysis/_task_template/`. Output paths come from `task_paths(__file__)`, never a bare
  relative path.
- **Data**: `data/<dataset>/{raw,processed,resources,results}/`
- **Paths**: Use `from <package> import FilePaths` (edit `_constants.py` for datasets)
- **Deps**: All in `pixi.toml` (not pyproject.toml)
- Run `pixi install` after pulling changes that update `pixi.toml` — in the main checkout
