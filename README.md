# 🧬 analysis_template

A [cruft](https://cruft.github.io/cruft/) template for notebook-first single-cell and spatial analysis
repos, managed with [pixi](https://pixi.sh). Humans work in notebooks; coding agents follow the
[analysis-workflow](https://github.com/quadbio/analysis-workflow) plugin, which every generated repo enables.

> Building a reusable Python library? Use the [scverse cookiecutter](https://github.com/scverse/cookiecutter-scverse) instead.

## Create a project

```bash
uvx cruft create https://github.com/quadbio/analysis_template
cd my-analysis
git init -b main               # before pixi install: the package takes its version from git
pixi install
pixi run install-hooks
pixi run test
git add -A && git commit -m "Create from analysis_template"
```

You're prompted for the repository name, the package name (derived from it), a description, and your
name and e-mail. Then push it, e.g. `gh repo create <owner>/my-analysis --private --source . --push`. The
generated `README.md` takes it from there.

## Update a project

```bash
uvx cruft check                # is this project behind the template?
uvx cruft update               # apply the template's changes since the last update
```

Resolve conflicts and any `*.rej` files by hand; pre-commit refuses to commit either. `README.md`,
`analysis/`, `data/`, `src/` and `tests/` belong to the project once created, and updates leave them alone
(`[tool.cruft] skip` in its `pyproject.toml`).

A repo created before this template used cruft starts receiving updates with
`uvx cruft link https://github.com/quadbio/analysis_template`.

## Develop the template

Everything a project gets lives under `{{cookiecutter.project_name}}/`; `cookiecutter.json` holds the prompts.
`uvx cookiecutter . --no-input -o <dir>` renders your working tree (`cruft create` renders the last commit).
CI creates a project on every pull request and runs its tests and pre-commit.

## License

[BSD 3-Clause](LICENSE).
