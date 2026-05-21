"""Subsystem Deep-Dive — tier mix, parameter list, key citations."""

from __future__ import annotations

from collections import Counter

import pandas as pd
import streamlit as st

from utils import get_dataset, short_authors

st.set_page_config(page_title="Subsystem · Nidus", layout="wide")
st.title("Subsystem deep-dive")

ds = get_dataset()
subsystems = list(ds.subsystems())

selected = st.selectbox("Subsystem", subsystems)
sub_ds = ds.filter(subsystem=selected)

# ---- Stats ----------------------------------------------------------

tier_counts = Counter(p.tier for p in sub_ds)
modal_tier = max(tier_counts, key=lambda k: tier_counts[k]) if tier_counts else "—"
citing_keys = {c.key for p in sub_ds for c in p.citations}

c1, c2, c3 = st.columns(3)
c1.metric("Parameters", len(sub_ds))
c2.metric("Citations referenced", len(citing_keys))
c3.metric("Modal tier", modal_tier)

# ---- Tier distribution ---------------------------------------------

st.subheader("Tier distribution")
tier_df = pd.DataFrame(
    [{"Tier": t, "Count": tier_counts.get(t, 0)} for t in "ABCD"]
).set_index("Tier")
st.bar_chart(tier_df, height=200)

# ---- Parameters table ----------------------------------------------

st.subheader("Parameters in this subsystem")
param_rows = [
    {
        "ID": p.id,
        "Name": p.name,
        "Tier": p.tier,
        "Central": p.value.central,
        "Units": p.value.units,
        "Citations": ", ".join(c.key for c in p.citations[:2])
        + ("…" if len(p.citations) > 2 else ""),
        "Review": p.extraction.review_status,
    }
    for p in sub_ds
]
st.dataframe(pd.DataFrame(param_rows), width="stretch", hide_index=True)

# ---- Key citations -------------------------------------------------

st.subheader("Citations supporting this subsystem")

citation_uses: Counter[str] = Counter()
for p in sub_ds:
    for c in p.citations:
        citation_uses[c.key] += 1

cite_rows = []
for key, uses in citation_uses.most_common():
    c = ds.citations[key]
    cite_rows.append(
        {
            "Citation key": key,
            "Authors": short_authors(c),
            "Year": c.year,
            "Title": c.title,
            "Used by N parameters": uses,
            "DOI": c.doi or "",
            "PMID": c.pmid or "",
        }
    )
st.dataframe(pd.DataFrame(cite_rows), width="stretch", hide_index=True)
