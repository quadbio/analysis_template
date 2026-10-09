"""Refuse a package name Python cannot import."""

import keyword
import sys

PACKAGE_NAME = "{{ cookiecutter.package_name }}"

if not PACKAGE_NAME.isidentifier() or keyword.iskeyword(PACKAGE_NAME):
    sys.exit(f"ERROR: package_name {PACKAGE_NAME!r} is not a valid Python identifier.")
