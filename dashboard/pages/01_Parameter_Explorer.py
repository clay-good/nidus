"""Parameter Explorer — filterable table with per-parameter detail."""

from __future__ import annotations

import pandas as pd
import streamlit as st

from utils import citation_line, citation_url, get_dataset, tier_badge

st.set_page_config(page_title="Parameter Explorer · Nidus", layout="wide")
st.title("Parameter Explorer")

ds = get_dataset()

# ---- Filters --------------------------------------------------------

with st.sidebar:
    st.header("Filters")
    subsystems = list(ds.subsystems())
    selected_subs = st.multiselect("Subsystem", subsystems)
    selected_tiers = st.multiselect("Tier", ["A", "B", "C", "D"])
    selected_review = st.multiselect(
        "Review status",
        ["unverified", "pending_human_review", "verified", "contested"],
    )
    search = st.text_input("Search id or name", "")
    st.caption(
        "Filters are AND-combined across columns and OR-combined within a column."
    )

filtered = ds.filter(
    subsystem=selected_subs or None,
    tier=selected_tiers or None,
    review_status=selected_review or None,
)

# ---- Table ----------------------------------------------------------

rows = []
for p in filtered:
    if search:
        needle = search.lower()
        if needle not in p.id.lower() and needle not in p.name.lower():
            continue
    rows.append(
        {
            "ID": p.id,
            "Name": p.name,
            "Subsystem": p.subsystem,
            "Tier": p.tier,
            "Central": p.value.central,
            "Units": p.value.units,
            "Citations": len(p.citations),
            "Review": p.extraction.review_status,
        }
    )

st.caption(f"{len(rows)} parameter{'s' if len(rows) != 1 else ''} matching filters.")

if not rows:
    st.info("No parameters match the current filters.")
    st.stop()

df = pd.DataFrame(rows)
st.dataframe(df, width="stretch", hide_index=True, height=350)

st.divider()

# ---- Detail view ----------------------------------------------------

st.subheader("Detail")

ids = [r["ID"] for r in rows]
selected_id = st.selectbox("Inspect a parameter", ids)
p = ds[selected_id]

head_left, head_right = st.columns([3, 2])
with head_left:
    st.markdown(f"### {p.name}")
    st.code(p.id, language="text")
    st.markdown(tier_badge(p.tier))
    st.markdown(f"*Subsystem:* `{p.subsystem}`")
with head_right:
    delta = None
    if p.value.low is not None and p.value.high is not None:
        delta = f"{p.value.low} – {p.value.high}"
    st.metric(
        label=f"Value ({p.value.units})",
        value=f"{p.value.central:g}",
        delta=delta,
        delta_color="off",
    )
    if p.value.distribution:
        st.caption(
            f"Distribution: {p.value.distribution}"
            + (f" (CI {p.value.ci:.3g})" if p.value.ci is not None else "")
        )

st.markdown("**Tier rationale**")
st.write(p.tier_rationale)

if p.applicability and p.applicability.population:
    st.markdown(f"**Applicability:** {p.applicability.population}")
    if p.applicability.excludes:
        st.caption(f"Excludes: {', '.join(p.applicability.excludes)}")

if p.notes:
    st.markdown("**Notes**")
    st.write(p.notes)

st.markdown("**Citations**")
for c in p.citations:
    primary = (
        " *(primary)*" if p.primary_citation and c.key == p.primary_citation.key else ""
    )
    st.markdown(f"- {citation_line(c)}{primary}")

with st.expander("Extraction provenance"):
    st.json(
        {
            "review_status": p.extraction.review_status,
            "method": p.extraction.method,
            "by": p.extraction.by,
            "date": p.extraction.date,
            "reviewer": p.extraction.reviewer,
        }
    )

# Quick links to citations
links = [(c.key, citation_url(c)) for c in p.citations if citation_url(c)]
if links:
    st.caption(
        "Resolve citations: " + " · ".join(f"[{key}]({url})" for key, url in links)
    )
