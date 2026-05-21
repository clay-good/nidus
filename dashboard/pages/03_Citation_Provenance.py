"""Citation Provenance — two-way lookup between citations and parameters."""

from __future__ import annotations

import pandas as pd
import streamlit as st

from utils import citation_url, get_dataset, tier_badge

st.set_page_config(page_title="Citation Provenance · Nidus", layout="wide")
st.title("Citation provenance")

ds = get_dataset()

tab_by_cite, tab_by_param = st.tabs(["By citation", "By parameter"])

# ---- Tab 1: from citation -> parameters ----------------------------

with tab_by_cite:
    st.markdown("Pick a citation to see every parameter in the dataset that cites it.")

    citations_sorted = sorted(ds.citations.values(), key=lambda c: (-c.year, c.key))
    options = {
        f"{c.year} — {c.title[:90]}{'…' if len(c.title) > 90 else ''} ({c.key})": c.key
        for c in citations_sorted
    }
    label = st.selectbox("Citation", list(options.keys()))
    key = options[label]
    c = ds.citations[key]

    st.markdown(f"### {c.title}")
    st.markdown(f"**Authors:** {', '.join(c.authors)}")
    st.markdown(f"**Year:** {c.year}  ·  **Type:** {c.type}")
    if c.journal:
        st.markdown(f"**Venue:** {c.journal}")
    if c.publisher:
        st.markdown(f"**Publisher:** {c.publisher}")
    if c.notes:
        st.caption(c.notes)

    link_parts = []
    if c.doi:
        link_parts.append(f"[DOI](https://doi.org/{c.doi})")
    if c.pmid:
        link_parts.append(f"[PubMed](https://pubmed.ncbi.nlm.nih.gov/{c.pmid})")
    if c.url:
        link_parts.append(f"[URL]({c.url})")
    if link_parts:
        st.markdown("  ·  ".join(link_parts))

    st.divider()

    params = ds.citations_for(key)
    st.subheader(f"Parameters citing this work ({len(params)})")
    if not params:
        st.info("No parameters cite this work.")
    else:
        rows = [
            {
                "ID": p.id,
                "Name": p.name,
                "Subsystem": p.subsystem,
                "Tier": p.tier,
                "Primary?": "yes"
                if p.primary_citation and p.primary_citation.key == key
                else "",
            }
            for p in params
        ]
        st.dataframe(pd.DataFrame(rows), width="stretch", hide_index=True)

# ---- Tab 2: from parameter -> citations ----------------------------

with tab_by_param:
    st.markdown(
        "Pick a parameter to see its full citation chain (primary + supporting)."
    )

    selected = st.selectbox(
        "Parameter", sorted(p.id for p in ds), key="cite_by_param_select"
    )
    p = ds[selected]

    st.markdown(f"### {p.name}")
    st.code(p.id, language="text")
    st.markdown(tier_badge(p.tier))
    st.markdown(
        f"**Value:** {p.value.central} {p.value.units} "
        f"(low {p.value.low}, high {p.value.high})"
        if p.value.low is not None
        else f"**Value:** {p.value.central} {p.value.units}"
    )

    st.subheader(f"Citations ({len(p.citations)})")
    rows = []
    for c in p.citations:
        is_primary = p.primary_citation is not None and c.key == p.primary_citation.key
        url = citation_url(c)
        rows.append(
            {
                "Primary": "yes" if is_primary else "",
                "Key": c.key,
                "Authors": ", ".join(c.authors[:3])
                + (" et al." if len(c.authors) > 3 else ""),
                "Year": c.year,
                "Title": c.title[:90] + ("…" if len(c.title) > 90 else ""),
                "Resolve": url or "",
            }
        )
    df = pd.DataFrame(rows)
    st.dataframe(
        df,
        width="stretch",
        hide_index=True,
        column_config={
            "Resolve": st.column_config.LinkColumn("Resolve", display_text="open"),
        },
    )
