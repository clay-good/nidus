"""Nidus dashboard — home page (Streamlit entry point).

Run locally with::

    streamlit run dashboard/app.py

Or browse the hosted instance on Streamlit Community Cloud (URL in the
repository README once the deploy lands).
"""

from __future__ import annotations

from collections import Counter

import pandas as pd
import streamlit as st

from utils import PYPI_URL, REPO_URL, get_dataset

st.set_page_config(page_title="Nidus", layout="wide")

ds = get_dataset()

st.title("Nidus")
st.markdown(
    "A curated, citation-backed dataset of human gestational physiology "
    "parameters, annotated with explicit confidence tiers."
)

# ---- Stats row ------------------------------------------------------

tier_counts = Counter(p.tier for p in ds)

c1, c2, c3, c4 = st.columns(4)
c1.metric("Parameters", len(ds))
c2.metric("Citations", len(ds.citations))
c3.metric("Subsystems", len(ds.subsystems()))
c4.metric("Tier A entries", tier_counts.get("A", 0))

st.divider()

# ---- What it is / isn't ---------------------------------------------

col_is, col_isnt = st.columns(2)
with col_is:
    st.subheader("Nidus is")
    st.markdown(
        "- A JSON dataset, schema-validated (draft 2020-12), FAIR-compliant\n"
        "- A Python package — `pip install nidus`\n"
        "- This interactive dashboard\n"
        "- Citable via Zenodo DOI on every release\n"
        "- MIT licence on the code, CC-BY-4.0 on the dataset"
    )
with col_isnt:
    st.subheader("Nidus is not")
    st.markdown(
        "- A clinical decision-support tool\n"
        "- A mechanistic simulator (use [CellML](https://www.cellml.org/), "
        "[COPASI](http://copasi.org/), or "
        "[PhysioCell](http://physicell.org/) for that)\n"
        "- Validated for any decision affecting a real patient"
    )

st.divider()

# ---- Tier system ----------------------------------------------------

st.subheader("Confidence tiers")
st.markdown(
    "Every parameter carries one of four tiers describing the strength of "
    "evidence behind it. Tier propagation through derived quantities "
    "inherits the lowest input tier."
)

tier_table = pd.DataFrame(
    [
        {
            "Tier": tier,
            "Label": ds.tiers[tier].label,
            "In dataset": tier_counts.get(tier, 0),
            "Primary criterion": ds.tiers[tier].criteria[0],
        }
        for tier in "ABCD"
    ]
)
st.dataframe(tier_table, width="stretch", hide_index=True)

tier_chart = pd.DataFrame(
    [{"Tier": t, "Count": tier_counts.get(t, 0)} for t in "ABCD"]
).set_index("Tier")
st.bar_chart(tier_chart, height=200)

st.divider()

# ---- Quickstart -----------------------------------------------------

st.subheader("Use it from Python")
st.code(
    """import nidus

ds = nidus.load()

co = ds["maternal_cardiovascular.baseline_cardiac_output_l_per_min"]
print(co.value.central, co.value.units)       # 4.6 L/min
print(co.tier)                                 # B
print(co.primary_citation.doi)                 # 10.1097/hjh.0000000000000090

# Filter to maternal cardiovascular Tier-A entries:
for p in ds.filter(subsystem="maternal_cardiovascular", tier="A"):
    print(p.id)
""",
    language="python",
)

st.divider()

# ---- Pages signpost -------------------------------------------------

st.subheader("Browse the dataset")
st.markdown(
    "- **Parameter Explorer** — filterable table with per-parameter detail\n"
    "- **Subsystem Deep-Dive** — tier mix and key citations per subsystem\n"
    "- **Citation Provenance** — two-way lookup between papers and parameters\n"
    "- **Unknowns Registry** — Tier-D entries as structured research questions\n"
    "- **Download** — full dataset ZIP, per-subsystem JSON, BibTeX"
)

st.info(
    "**Coming with future releases:** a *Trajectory Viewer* (week-by-week "
    "value bands) and a *Sensitivity Sandbox* (vary a parameter, see the "
    "downstream effect). Both depend on trajectory metadata that is not yet "
    "populated for most parameters."
)

st.divider()

# ---- Cite & links ---------------------------------------------------

st.subheader("Cite")
st.markdown(
    "Cite the dataset by its Zenodo concept DOI (minted on the first "
    "release). Machine-readable citation metadata is in "
    f"[`CITATION.cff`]({REPO_URL}/blob/main/CITATION.cff)."
)

st.caption(
    f"Code: MIT · Dataset: CC-BY-4.0 · [Repository]({REPO_URL}) · [PyPI]({PYPI_URL})"
)
