"""Sensitivity Sandbox — vary a submodel parameter, see the trajectory shift.

Spec v0.3 §8 item #5. Works against the 36 bound submodels in
``nidus.export.evaluate``; the independent variable's natural domain
is read off ``submodel_domain``.
"""

from __future__ import annotations

import numpy as np
import streamlit as st

from nidus.export import (
    SUBMODELS,
    evaluate_submodel,
    kernel_parameter_mapping,
    submodel_domain,
    supported_submodels,
)
from utils import REPO_URL, get_dataset, tier_badge

st.set_page_config(page_title="Sensitivity Sandbox · Nidus", layout="wide")
st.title("Sensitivity Sandbox")
st.markdown(
    "Pick a submodel, pick an input parameter, pick a relative range. "
    "The page plots how the submodel's trajectory changes as the chosen "
    "parameter is varied around its central value. Useful for one-at-a-"
    "time sensitivity probing and for IUGR-style what-ifs."
)

ds = get_dataset()

# ---- Submodel + parameter pickers ----------------------------------

supported = supported_submodels()
sm_options = {next(s.name for s in SUBMODELS if s.id == sid): sid for sid in supported}
chosen_label = st.selectbox("Submodel", options=sorted(sm_options.keys()))
chosen_id = sm_options[chosen_label]

kw_to_pid = kernel_parameter_mapping(chosen_id)

if not kw_to_pid:
    st.info(
        "This submodel has no swept parameters — its kernel uses hard-coded "
        "constants (e.g. Severinghaus O2-Hb). Use the **Trajectory Viewer** "
        "to see its baseline curve instead."
    )
    st.stop()

chosen_kw = st.selectbox(
    "Parameter to sweep",
    options=list(kw_to_pid.keys()),
    format_func=lambda kw: f"{kw}  ({kw_to_pid[kw]})",
)
chosen_pid = kw_to_pid[chosen_kw]
chosen_param = ds[chosen_pid]
central = float(chosen_param.value.central)

# ---- Range slider --------------------------------------------------

col1, col2 = st.columns(2)
with col1:
    rel_range_pct = st.slider(
        "Relative range (±%)",
        min_value=5,
        max_value=80,
        value=30,
        step=5,
        help="Percent of the central value to sweep above and below.",
    )
with col2:
    n_lines = st.slider(
        "Number of sweep values",
        min_value=3,
        max_value=11,
        value=5,
        step=2,
        help="How many curves to plot. Always includes the central value.",
    )

half = central * rel_range_pct / 100.0
sweep_values = np.linspace(central - half, central + half, n_lines)

# ---- Plot ----------------------------------------------------------

domain = submodel_domain(chosen_id)
x = np.linspace(domain.default_range[0], domain.default_range[1], 200)
chart_rows: dict[str, np.ndarray] = {domain.label: x}
for v in sweep_values:
    y = evaluate_submodel(ds, chosen_id, x, overrides={chosen_kw: float(v)})
    chart_rows[f"{chosen_kw} = {v:.3g}"] = y

st.line_chart(chart_rows, x=domain.label)

# ---- Parameter detail ----------------------------------------------

st.subheader("Swept parameter")
c1, c2, c3 = st.columns([3, 1, 2])
with c1:
    st.markdown(f"**{chosen_param.name}**  \n`{chosen_param.id}`")
with c2:
    st.markdown(tier_badge(chosen_param.tier))
with c3:
    cite = chosen_param.primary_citation
    if cite:
        href = (
            f"https://doi.org/{cite.doi}"
            if cite.doi
            else (f"https://pubmed.ncbi.nlm.nih.gov/{cite.pmid}" if cite.pmid else None)
        )
        label = f"{cite.key} ({cite.year})"
        st.markdown(f"[{label}]({href})" if href else label)
st.caption(
    f"Central: **{central} {chosen_param.value.units or ''}**. "
    f"Sweep range: {sweep_values[0]:.3g} → {sweep_values[-1]:.3g} "
    f"({rel_range_pct}% around central)."
)

# ---- Footer --------------------------------------------------------

st.divider()
st.caption(
    "The sweep uses `nidus.export.evaluate_submodel(..., overrides=...)` — "
    "the same reference kernels exercised by SBML/CellML round-trip tests. "
    f"For multi-parameter sweeps or CSV output, see `nidus.export.sweep` in "
    f"the [API reference]({REPO_URL}/blob/main/docs/exports/index.md)."
)
