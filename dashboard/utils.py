"""Shared helpers for the nidus dashboard.

Lives at the dashboard root (sibling of ``app.py``); the leading
underscore convention would also work but Streamlit only treats files
inside ``pages/`` as routable pages, so a plain module here is enough.
"""

from __future__ import annotations

import sys
from pathlib import Path

# Ensure ``import nidus`` resolves when the dashboard is run from any
# working directory (Streamlit Cloud, local dev, CI smoke test).
_REPO_ROOT = Path(__file__).resolve().parent.parent
_PYTHON_DIR = _REPO_ROOT / "python"
if _PYTHON_DIR.exists() and str(_PYTHON_DIR) not in sys.path:
    sys.path.insert(0, str(_PYTHON_DIR))

import streamlit as st  # noqa: E402

import nidus  # noqa: E402

# ---- Tier rendering -------------------------------------------------

TIER_COLOR = {
    "A": "green",
    "B": "blue",
    "C": "orange",
    "D": "red",
}


def tier_badge(tier: str) -> str:
    """Return a Streamlit-flavoured Markdown badge for a tier."""
    colour = TIER_COLOR.get(tier, "gray")
    return f":{colour}[**Tier {tier}**]"


# ---- Dataset cache --------------------------------------------------


@st.cache_resource
def get_dataset() -> nidus.Dataset:
    """Load the nidus dataset once per dashboard process."""
    return nidus.load()


# ---- Citation rendering --------------------------------------------


def citation_url(c: nidus.Citation) -> str | None:
    if c.doi:
        return f"https://doi.org/{c.doi}"
    if c.pmid:
        return f"https://pubmed.ncbi.nlm.nih.gov/{c.pmid}"
    if c.url:
        return c.url
    return None


def short_authors(c: nidus.Citation, n: int = 2) -> str:
    if len(c.authors) <= n:
        return ", ".join(c.authors)
    return ", ".join(c.authors[:n]) + " et al."


def citation_line(c: nidus.Citation) -> str:
    """A single Markdown line summarising a citation."""
    url = citation_url(c)
    venue = c.journal or c.publisher or ""
    body = f"{short_authors(c)} ({c.year}). *{c.title}*."
    if venue:
        body += f" {venue}."
    if url:
        return f"[{body}]({url})"
    return body


# ---- Repo links ----------------------------------------------------

REPO_URL = "https://github.com/claygood/nidus"
PYPI_URL = "https://pypi.org/project/nidus/"
ISSUE_TEMPLATE_RESEARCH_QUESTION = (
    f"{REPO_URL}/issues/new?template=hypothesis-proposal.yml"
)
ISSUE_TEMPLATE_PARAMETER = f"{REPO_URL}/issues/new?template=parameter-request.yml"
