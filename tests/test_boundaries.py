"""Dependency boundaries (CLAUDE.md B1, B2) — must always pass.

B1: importing hansa needs no network and no optional dependency.
B2: hansa may import loopmarket and factbond; neither imports hansa.
The reverse-direction check reads the sibling checkouts when present and is
skipped otherwise.
"""
import importlib
import pathlib
import sys

import pytest


def test_b1_import_is_offline_and_dependency_free():
    before = set(sys.modules)
    importlib.import_module("hansa")
    loaded = set(sys.modules) - before
    for forbidden in ("requests", "swarm_bee", "web3"):
        assert not any(m == forbidden or m.startswith(forbidden + ".") for m in loaded)


@pytest.mark.parametrize("sibling", ["loopmarket", "factbond"])
def test_b2_siblings_never_import_hansa(sibling):
    root = pathlib.Path(__file__).resolve().parents[2] / sibling / "src"
    if not root.exists():
        pytest.skip(f"{sibling} checkout not beside this repository")
    hits = [p for p in root.rglob("*.py") if "import hansa" in p.read_text(errors="ignore")]
    assert hits == [], f"{sibling} imports hansa: {hits}"
