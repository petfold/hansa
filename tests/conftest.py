"""Put the src layout on the path so the tests run without an install, and
prefer the sibling checkouts of loopmarket and factbond when they are beside
this repository: hansa codes against their current record shapes (the v6
statement, the counterparty gate), which a release may not carry yet."""
import pathlib
import sys

HERE = pathlib.Path(__file__).resolve().parents[1]
for sibling in ("factbond", "loopmarket"):
    src = HERE.parent / sibling / "src"
    if src.exists():
        sys.path.insert(0, str(src))
sys.path.insert(0, str(HERE / "src"))
