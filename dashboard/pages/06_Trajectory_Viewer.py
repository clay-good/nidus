"""Trajectory Viewer — pick a submodel, plot its trajectory across 8–40 weeks.

Spec v0.3 §8 item #4. The plotting subset is the ~21 time-trajectory
submodels with a kernel binding in ``nidus.export.evaluate``;
algebraic and multivariate submodels are still listed (mathematical
form + input parameters with tier badges + citations) but plotted only
where the binding exists.
"""

from __future__ import annotations

import numpy as np
import streamlit as st

from nidus.export import (
    SUBMODELS,
    UNSUPPORTED_REASON,
    evaluate_submodel,
    supported_submodels,
)
from utils import REPO_URL, get_dataset, tier_badge

st.set_page_config(page_title="Trajectory Viewer · Nidus", layout="wide")
st.title("Trajectory Viewer")
st.markdown(
    "Pick a mechanistic submodel; see its trajectory across 8–40 weeks "
    "alongside the dataset parameters that feed it. Trajectories are "
    "evaluated by the same NumPy reference kernels the SBML/CellML "
    "round-trip tests use — so what you see here is exactly what an "
    "external simulator would compute from the exported model."
)

ds = get_dataset()

# ---- Submodel picker -----------------------------------------------

_SUPPORTED = set(supported_submodels())
sm_options: dict[str, str] = {}
for sm in SUBMODELS:
    tag = "📈 " if sm.id in _SUPPORTED else "📐 "
    sm_options[f"{tag}{sm.name}"] = sm.id

chosen_label = st.selectbox(
    "Submodel",
    options=sorted(sm_options.keys()),
    help="📈 plottable time-trajectory submodels; 📐 algebraic or multivariate.",
)
chosen_id = sm_options[chosen_label]
chosen_sm = next(s for s in SUBMODELS if s.id == chosen_id)

# ---- Submodel header -----------------------------------------------

st.subheader(chosen_sm.name)
worst_tier_letter = max(
    (ds[pid].tier for pid in chosen_sm.parameter_ids),
    key=lambda t: "ABCD".index(t),
)
st.markdown(
    f"{tier_badge(worst_tier_letter)} &nbsp; "
    f"`{chosen_sm.id}` &nbsp; "
    f"output units: `{chosen_sm.output_units or 'unspecified'}` &nbsp; "
    f"independent variable: `{chosen_sm.independent_variable or 'algebraic'}` &nbsp; "
    f"SBO: `{chosen_sm.sbo_term or 'n/a'}`"
)
st.caption(chosen_sm.description)

# ---- Plot ----------------------------------------------------------

if chosen_id in _SUPPORTED:
    t = np.linspace(8.0, 40.0, 200)
    y = evaluate_submodel(ds, chosen_id, t)
    chart_data = {"gestational age (weeks)": t, chosen_sm.output_units or "value": y}
    st.line_chart(chart_data, x="gestational age (weeks)")
else:
    reason = UNSUPPORTED_REASON.get(chosen_id, "no kernel binding")
    st.info(
        f"**Plot not available for this submodel.** {reason}. The dataset "
        "parameters + mathematical form remain available below; the SBML / "
        "CellML / SED-ML files on the Download page evaluate against the "
        "same kernels."
    )

# ---- Inputs panel --------------------------------------------------

st.subheader("Inputs")
for pid in chosen_sm.parameter_ids:
    p = ds[pid]
    cols = st.columns([3, 1, 1, 4])
    with cols[0]:
        st.markdown(f"**{p.name}**  \n`{p.id}`")
    with cols[1]:
        st.markdown(f"{p.value.central} {p.value.units or ''}")
    with cols[2]:
        st.markdown(tier_badge(p.tier))
    with cols[3]:
        if p.primary_citation:
            cite = p.primary_citation
            href = (
                f"https://doi.org/{cite.doi}"
                if cite.doi
                else (
                    f"https://pubmed.ncbi.nlm.nih.gov/{cite.pmid}"
                    if cite.pmid
                    else None
                )
            )
            label = f"{cite.key} ({cite.year})"
            st.markdown(f"[{label}]({href})" if href else label)
        st.caption(p.extraction.review_status)

# ---- Footer --------------------------------------------------------

st.divider()
st.caption(
    f"Plottable submodels: {len(_SUPPORTED)} / {len(SUBMODELS)}. The rest are "
    "algebraic (PO2-, substrate-, fetal-weight-domain) or use a multivariate "
    f"fit (Hadlock EFW). Source kernels live in `nidus.export.reference`. "
    f"See the [interop spec]({REPO_URL}/blob/main/docs/specs/v0.4/01-mechanistic-modeling-interop.md)."
)
