"""Refuse answers that would render into a broken project."""

import keyword
import sys

PACKAGE_NAME = "{{ cookiecutter.package_name }}"
# Rendered into TOML strings, which these characters would break.
TOML_VALUES = {
    "project_description": r"""{{ cookiecutter.project_description }}""",
    "author_full_name": r"""{{ cookiecutter.author_full_name }}""",
    "author_email": r"""{{ cookiecutter.author_email }}""",
}

if not PACKAGE_NAME.isidentifier() or keyword.iskeyword(PACKAGE_NAME):
    sys.exit(f"ERROR: package_name {PACKAGE_NAME!r} is not a valid Python identifier.")
for key, value in TOML_VALUES.items():
    if '"' in value or "\\" in value:
        sys.exit(f"ERROR: {key} may not contain double quotes or backslashes.")
