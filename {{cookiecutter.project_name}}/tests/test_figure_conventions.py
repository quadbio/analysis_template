from pathlib import Path

import yaml

CONVENTIONS = Path(__file__).parents[1] / "resources" / "figure_conventions.yaml"


def _set_twice(shared: dict, own: dict, keys: tuple = ()):
    """Keys of ``own`` that ``shared`` already sets; a section both extend is fine."""
    for key, value in own.items():
        if key in shared:
            if isinstance(value, dict) and isinstance(shared[key], dict):
                yield from _set_twice(shared[key], value, (*keys, key))
            else:
                yield ".".join(map(str, (*keys, key)))


def test_set_twice_finds_duplicates():
    shared = {"colors": {"methods": {"A": "#000000"}}}
    assert not list(_set_twice(shared, {"colors": {"methods": {"B": "#111111"}, "week": {2: "#222222"}}}))
    assert list(_set_twice(shared, {"colors": {"methods": {"A": "#333333"}}})) == ["colors.methods.A"]


def test_no_figure_convention_set_twice():
    """A dataset's section only adds to the shared one (CONVENTIONS.md, Figure conventions)."""
    shared = yaml.safe_load(CONVENTIONS.read_text())
    for name, own in (shared.pop("datasets", None) or {}).items():
        twice = list(_set_twice(shared, own or {}))
        assert not twice, f"set both repo-wide and for {name}: {twice}"
