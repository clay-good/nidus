"""Smoke test for the Streamlit dashboard.

Each page is loaded with Streamlit's AppTest harness and asserted to
render with zero exceptions or errors. This catches regressions where a
dashboard page calls a removed nidus.* API or references a moved
dataset file.

Skipped automatically if Streamlit is not installed (e.g. a minimal
install of just the package without ``[dev]`` extras).
"""

from __future__ import annotations

import sys
from pathlib import Path

import pytest

streamlit_testing = pytest.importorskip(
    "streamlit.testing.v1",
    reason="streamlit not installed; install with `pip install -e .[dev]`",
)
AppTest = streamlit_testing.AppTest

_REPO = Path(__file__).resolve().parent.parent.parent
_DASHBOARD = _REPO / "dashboard"

PAGES = [
    _DASHBOARD / "app.py",
    _DASHBOARD / "pages" / "01_Parameter_Explorer.py",
    _DASHBOARD / "pages" / "02_Subsystem_Deep_Dive.py",
    _DASHBOARD / "pages" / "03_Citation_Provenance.py",
    _DASHBOARD / "pages" / "04_Unknowns_Registry.py",
    _DASHBOARD / "pages" / "05_Download.py",
]


@pytest.fixture(autouse=True)
def _dashboard_on_path() -> None:
    """Make ``from utils import ...`` resolvable for the dashboard pages."""
    p = str(_DASHBOARD)
    if p not in sys.path:
        sys.path.insert(0, p)


@pytest.mark.parametrize("page", PAGES, ids=lambda p: p.name)
def test_page_renders_without_exception(page: Path) -> None:
    if not page.exists():
        pytest.skip(f"{page} not present")
    at = AppTest.from_file(str(page), default_timeout=20).run()
    issues = list(at.exception) + list(at.error)
    assert not issues, f"{page.name} raised during render:\n" + "\n".join(
        f"  - {e.value}" for e in issues
    )
