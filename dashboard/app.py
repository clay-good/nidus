"""Nidus dashboard — Streamlit entry point.

Placeholder. The dashboard layout is specified in
docs/specs/v0.3/01-dataset-and-dashboard.md §8.
"""

import streamlit as st

st.set_page_config(
    page_title="Nidus",
    page_icon="🧬",
    layout="wide",
)

st.title("Nidus")
st.caption("Curated dataset of human gestational physiology parameters")

st.info(
    "This dashboard is a v0.3.0.dev0 scaffold. The interactive pages "
    "(Parameter Explorer, Trajectory Viewer, Sensitivity Sandbox, etc.) "
    "land incrementally. See the project README and "
    "`docs/specs/v0.3/01-dataset-and-dashboard.md` for the plan."
)

st.markdown(
    """
    ### Coming soon
    - **Parameter Explorer** — searchable, filterable parameter table.
    - **Trajectory Viewer** — week-by-week central + uncertainty bands.
    - **Sensitivity Sandbox** — vary a parameter, observe downstream.
    - **Citation Provenance** — citation graph, BibTeX export.
    - **Unknowns Registry** — Tier D entries as research questions.
    """
)
