"""Trajectory Viewer — pick a submodel, plot its trajectory over its natural domain.

Spec v0.3 §8 item #4. Time-trajectory submodels plot over 8–40 weeks;
algebraic submodels (O2-Hb, glucose Michaelis–Menten, etc.) plot over
their natural domain (PO2, substrate concentration, …) via
``submodel_domain``. The five Hadlock biometry / EFW submodels are
listed but not plotted — their kernels take a list of weekly anchors
rather than scalar kwargs.
"""

from __future__ import annotations

import numpy as np
import streamlit as st

from nidus.export import (
    SUBMODELS,
    UNSUPPORTED_REASON,
    evaluate_submodel,
    submodel_domain,
    supported_submodels,
)
from utils import REPO_URL, get_dataset, tier_badge

st.set_page_config(page_title="Trajectory Viewer · Nidus", layout="wide")
st.title("Trajectory Viewer")
st.markdown(
    "Pick a mechanistic submodel; see its trajectory plotted over its "
    "natural independent variable (gestational age in weeks for time "
    "trajectories, PO2 / substrate / cortisol / fetal weight for "
    "algebraic ones). Trajectories are evaluated by the same NumPy "
    "reference kernels the SBML/CellML round-trip tests use — so what "
    "you see here is exactly what an external simulator would compute "
    "from the exported model."
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
    help="📈 plottable submodels; 📐 multi-anchor biometry fits (not yet wired).",
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
    domain = submodel_domain(chosen_id)
    x = np.linspace(domain.default_range[0], domain.default_range[1], 200)
    y = evaluate_submodel(ds, chosen_id, x)
    chart_data = {domain.label: x, chosen_sm.output_units or "value": y}
    st.line_chart(chart_data, x=domain.label)
else:
    reason = UNSUPPORTED_REASON.get(chosen_id, "no kernel binding")
    st.info(
        f"**Plot not available for this submodel.** {reason}. The dataset "
        "parameters and citations are still listed below, and the SBML / "
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
    f"Plottable submodels: {len(_SUPPORTED)} / {len(SUBMODELS)}. The remaining "
    f"submodel (`hadlock_fetal_weight`) is multivariate in BPD/HC/AC/FL "
    f"and not a 1-D trajectory. Source kernels live in "
    f"`nidus.export.reference`; see the "
    f"[interop spec]({REPO_URL}/blob/main/docs/specs/v0.4/01-mechanistic-modeling-interop.md)."
)
