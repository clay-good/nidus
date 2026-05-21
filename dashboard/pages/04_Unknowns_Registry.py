"""Unknowns Registry — Tier-D entries as structured research questions."""

from __future__ import annotations

import streamlit as st

from utils import ISSUE_TEMPLATE_RESEARCH_QUESTION, citation_line, get_dataset

st.set_page_config(page_title="Unknowns Registry · Nidus", layout="wide")
st.title("Unknowns Registry")

st.markdown(
    "Tier-D entries are **structured open questions** — hypothesised "
    "mechanisms or unmeasured quantities, listed so the field knows what is "
    "worth measuring next. Once one or two peer-reviewed studies establish a "
    "value range, an entry is promoted to Tier C and moves into the regular "
    "parameter set."
)

ds = get_dataset()
tier_d = list(ds.filter(tier="D"))

if not tier_d:
    st.info(
        "No Tier-D entries in the dataset yet.\n\n"
        f"If you have a hypothesised mechanism worth measuring next, please "
        f"[open a research-question issue]({ISSUE_TEMPLATE_RESEARCH_QUESTION}).\n\n"
        "Useful candidates have:\n"
        "- a clearly named subsystem (maternal, placental, or fetal)\n"
        "- prior-art references — even if qualitative\n"
        "- a sketch of the measurement that would yield a value range\n"
    )
else:
    st.caption(f"{len(tier_d)} Tier-D entr{'y' if len(tier_d) == 1 else 'ies'}.")
    for p in tier_d:
        with st.expander(f"{p.name}  ·  `{p.id}`"):
            st.markdown(f"**Subsystem:** `{p.subsystem}`")
            if p.notes:
                st.markdown(f"**Why it matters:** {p.notes}")
            st.markdown(f"**Tier-D rationale:** {p.tier_rationale}")
            if p.citations:
                st.markdown("**Prior art:**")
                for c in p.citations:
                    st.markdown(f"- {citation_line(c)}")

st.divider()
st.caption(
    "Tier-D promotion is intentionally conservative: the entry leaves Tier D "
    "only when there is enough quantitative evidence to support at least a "
    "Tier-C value range. See CONTRIBUTING.md."
)
