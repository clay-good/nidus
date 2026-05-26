"""Submodel evaluation: dataset → numeric trajectory in one call.

The SBML / CellML builders carry submodel-specific knowledge about
which dataset parameter feeds which kernel argument. ``evaluate.py``
exposes that mapping as a small public registry so the dashboard
(Trajectory Viewer, Sensitivity Sandbox) and downstream notebooks can
evaluate a submodel on a numeric grid without re-implementing the
binding.

Coverage is deliberately scoped to **time-trajectory submodels with a
direct reference-kernel mapping** — ~20 of the 41 registered
submodels. Submodels whose independent variable is a domain quantity
(PO2, substrate concentration, fetal weight, biometry) or whose kernel
needs the dataset-specific Hadlock cubic fit are flagged in
``UNSUPPORTED_REASON`` so callers can degrade gracefully.
"""

from __future__ import annotations

from collections.abc import Callable, Sequence

import numpy as np
from numpy.typing import NDArray

from nidus.load import Dataset

from . import reference as _ref
from .registry import SUBMODELS

_Kernel = Callable[..., NDArray[np.float64]]

# (submodel_id) -> (kernel, {kernel_kwarg: dataset_parameter_id}). The
# kernel's first positional argument is always the independent
# variable (t_weeks for time-trajectory submodels).


def _bind(**mapping: str) -> dict[str, str]:
    return mapping


_TIME_TRAJECTORY_BINDINGS: dict[str, tuple[_Kernel, dict[str, str]]] = {
    "placental_villous_growth": (
        _ref.placental_area_logistic,
        _bind(
            initial_area_m2="placental_structure.initial_area_m2",
            term_area_m2="placental_structure.term_area_m2",
            growth_rate_per_week="placental_structure.growth_rate_per_week",
            midpoint_week="placental_structure.midpoint_week",
        ),
    ),
    "maternal_cardiac_output_trajectory": (
        _ref.maternal_cardiac_output,
        _bind(
            baseline_l_per_min="maternal_cardiovascular.baseline_cardiac_output_l_per_min",
            peak_excess_l_per_min="maternal_cardiovascular.peak_excess_cardiac_output_l_per_min",
            peak_week="maternal_cardiovascular.cardiac_output_peak_week",
            spread_weeks="maternal_cardiovascular.cardiac_output_spread_weeks",
        ),
    ),
    "maternal_map_trajectory": (
        _ref.maternal_map,
        _bind(
            baseline_mmhg="maternal_cardiovascular.baseline_map_mmhg",
            nadir_drop_mmhg="maternal_cardiovascular.map_nadir_drop_mmhg",
            nadir_week="maternal_cardiovascular.map_nadir_week",
            spread_weeks="maternal_cardiovascular.map_spread_weeks",
        ),
    ),
    "uterine_artery_flow_logistic": (
        _ref.uterine_artery_flow,
        _bind(
            baseline_ml_per_min="maternal_cardiovascular.baseline_uterine_flow_ml_per_min",
            term_ml_per_min="maternal_cardiovascular.term_uterine_flow_ml_per_min",
            growth_rate_per_week="maternal_cardiovascular.uterine_flow_growth_rate_per_week",
        ),
    ),
    "plasma_volume_expansion": (
        _ref.plasma_volume_expansion,
        _bind(
            early_l="maternal_blood.plasma_volume_early_l",
            term_l="maternal_blood.plasma_volume_l",
        ),
    ),
    "gfr_logistic_trajectory": (
        _ref.maternal_gfr_logistic,
        _bind(
            baseline_ml_per_min="maternal_renal.baseline_gfr_ml_per_min",
            peak_ml_per_min="maternal_renal.gfr_ml_per_min",
            growth_rate_per_week="maternal_renal.gfr_logistic_rate_per_week",
            peak_week="maternal_renal.gfr_peak_week",
        ),
    ),
    "heart_rate_trajectory": (
        _ref.maternal_heart_rate,
        _bind(
            baseline_bpm="maternal_cardiovascular.baseline_heart_rate_bpm",
            term_bpm="maternal_cardiovascular.peak_excess_heart_rate_bpm",
        ),
    ),
    "tidal_volume_trajectory": (
        _ref.maternal_tidal_volume,
        _bind(
            baseline_ml="maternal_respiratory.baseline_tidal_volume_ml",
            term_ml="maternal_respiratory.tidal_volume_ml_term",
        ),
    ),
    "fetal_heart_rate_trajectory": (
        _ref.fetal_heart_rate,
        _bind(
            baseline_bpm="fetal_circulation.fhr_baseline_bpm",
            term_bpm="fetal_circulation.fhr_term_bpm",
        ),
    ),
    "homa_ir_trajectory": (
        _ref.maternal_homa_ir,
        _bind(
            baseline="maternal_endocrine.homa_ir_baseline",
            term="maternal_endocrine.homa_ir_term",
        ),
    ),
    "cortisol_trajectory": (
        _ref.maternal_cortisol,
        _bind(
            baseline_ug_per_dl="maternal_endocrine.cortisol_baseline_ug_per_dl",
            term_ug_per_dl="maternal_endocrine.cortisol_term_ug_per_dl",
        ),
    ),
    "hpl_trajectory": (
        _ref.maternal_hpl,
        _bind(
            baseline_ug_per_ml="placental_endocrine.hpl_baseline_ug_per_ml",
            term_ug_per_ml="placental_endocrine.hpl_term_ug_per_ml",
        ),
    ),
    "progesterone_trajectory": (
        _ref.maternal_progesterone,
        _bind(
            baseline_ng_per_ml="placental_endocrine.progesterone_baseline_ng_per_ml",
            term_ng_per_ml="placental_endocrine.progesterone_term_ng_per_ml",
        ),
    ),
    "estradiol_trajectory": (
        _ref.maternal_estradiol,
        _bind(
            baseline_ng_per_ml="placental_endocrine.estradiol_baseline_ng_per_ml",
            term_ng_per_ml="placental_endocrine.estradiol_term_ng_per_ml",
        ),
    ),
    "hcg_trajectory": (
        _ref.maternal_hcg,
        _bind(
            peak_miu_per_ml="placental_endocrine.hcg_peak_miu_per_ml",
            peak_week="placental_endocrine.hcg_peak_week",
            term_miu_per_ml="placental_endocrine.hcg_term_miu_per_ml",
        ),
    ),
    "umbilical_artery_pi_trajectory": (
        _ref.umbilical_artery_pi,
        _bind(
            baseline="fetal_circulation.ua_pi_baseline",
            term="fetal_circulation.ua_pi_term",
        ),
    ),
    "arterial_ph_trajectory": (
        _ref.maternal_arterial_ph,
        _bind(
            baseline_ph="maternal_respiratory.baseline_arterial_ph",
            term_ph="maternal_respiratory.term_arterial_ph",
        ),
    ),
    "pao2_trajectory_linear": (
        _ref.maternal_pao2_linear,
        _bind(
            baseline_mmhg="maternal_respiratory.baseline_pao2_mmhg",
            term_mmhg="maternal_respiratory.pao2_mmhg_term",
        ),
    ),
    "maternal_fetal_igg_transfer": (
        _ref.maternal_fetal_igg_transfer,
        _bind(
            baseline="placental_structure.igg_transfer_ratio_baseline",
            term="placental_structure.igg_transfer_ratio_term",
        ),
    ),
    "maternal_microchimerism_trajectory": (
        _ref.maternal_microchimerism_trajectory,
        _bind(
            baseline="maternal_blood.fetal_microchimerism_baseline_cells_per_ml",
            term="maternal_blood.fetal_microchimerism_term_cells_per_ml",
        ),
    ),
    "fetal_pulmonary_fluid_trajectory": (
        _ref.fetal_pulmonary_fluid_trajectory,
        _bind(
            baseline="fetal_metabolism.pulmonary_fluid_net_rate_baseline_ml_per_kg_h",
            term="fetal_metabolism.pulmonary_fluid_net_rate_term_ml_per_kg_h",
        ),
    ),
}


UNSUPPORTED_REASON: dict[str, str] = {
    "o2hb_dissociation_adult": "Algebraic in PO2 (mmHg), not in time",
    "o2hb_dissociation_fetal": "Algebraic in PO2 (mmHg), not in time",
    "placental_glucose_glut1": "Algebraic in substrate (mmol/L), not in time",
    "placental_glucose_glut3": "Algebraic in substrate (mmol/L), not in time",
    "placental_o2_equilibrator": "Algebraic in maternal intervillous PO2",
    "placental_cortisol_gradient": "Algebraic in maternal cortisol",
    "placental_fetal_allometry": "Algebraic in fetal weight",
    "hadlock_fetal_weight": "Multivariate (BPD, HC, AC, FL) — not a 1-D trajectory",
    "stroke_volume_trajectory": "Kernel needs a peak_week / spread_weeks pair not yet curated",
    "renal_plasma_flow_trajectory": "Kernel needs a peak_week / spread_weeks pair not yet curated",
    "minute_ventilation_trajectory": "Kernel needs baseline + term RR/VT all four; partial mapping",
    "svr_trajectory": "Derived from CO + MAP; requires both submodels' params",
    "amniotic_fluid_volume_trajectory": "Piecewise kernel needs the spread-weeks anchor",
    "tsh_trajectory": "Piecewise-linear kernel needs the T1 anchor",
    "mca_pi_trajectory": "Bell-shaped kernel requires the peak_week anchor",
    "cerebroplacental_ratio": "Combinator of two submodels (UA-PI + MCA-PI)",
    "hadlock_bpd_growth": "Cubic-fit kernel needs 7 weekly anchors",
    "hadlock_hc_growth": "Cubic-fit kernel needs 7 weekly anchors",
    "hadlock_ac_growth": "Cubic-fit kernel needs 7 weekly anchors",
    "hadlock_fl_growth": "Cubic-fit kernel needs 7 weekly anchors",
}


def supported_submodels() -> list[str]:
    """Submodel ids that ``evaluate_submodel`` can handle today."""
    return list(_TIME_TRAJECTORY_BINDINGS.keys())


def evaluate_submodel(
    ds: Dataset,
    submodel_id: str,
    t_weeks: Sequence[float] | NDArray[np.floating],
    *,
    overrides: dict[str, float] | None = None,
) -> NDArray[np.float64]:
    """Evaluate a time-trajectory submodel on a numeric grid.

    Args:
        ds: the loaded nidus dataset.
        submodel_id: a registered submodel id (see ``nidus.export.SUBMODELS``).
        t_weeks: gestational ages to evaluate (weeks).
        overrides: optional ``{kernel_kwarg: value}`` overrides. Use to
            run sensitivity sweeps — replaces a single kernel argument
            for the duration of the call.

    Returns:
        1-D NumPy array of the submodel's primary observable, same
        length as ``t_weeks``.

    Raises:
        KeyError: if ``submodel_id`` is unknown to the registry.
        ValueError: if the submodel is registered but has no kernel
            binding (see ``UNSUPPORTED_REASON``).
    """
    if not any(s.id == submodel_id for s in SUBMODELS):
        raise KeyError(f"unknown submodel id: {submodel_id!r}")
    binding = _TIME_TRAJECTORY_BINDINGS.get(submodel_id)
    if binding is None:
        reason = UNSUPPORTED_REASON.get(submodel_id, "not yet bound to a kernel")
        raise ValueError(f"submodel {submodel_id!r} not supported: {reason}")
    kernel, mapping = binding
    kwargs: dict[str, float] = {kw: ds[pid].value.central for kw, pid in mapping.items()}
    if overrides:
        kwargs.update(overrides)
    return kernel(np.asarray(t_weeks, dtype=float), **kwargs)


def kernel_parameter_mapping(submodel_id: str) -> dict[str, str]:
    """Return ``{kernel_kwarg: dataset_parameter_id}`` for a supported submodel.

    Use this when you need to introspect which kernel argument
    corresponds to which dataset parameter — e.g. to surface the
    parameter that's about to be swept in a sensitivity analysis. For
    unsupported submodels, raises the same ``ValueError`` as
    :func:`evaluate_submodel`.
    """
    if not any(s.id == submodel_id for s in SUBMODELS):
        raise KeyError(f"unknown submodel id: {submodel_id!r}")
    binding = _TIME_TRAJECTORY_BINDINGS.get(submodel_id)
    if binding is None:
        reason = UNSUPPORTED_REASON.get(submodel_id, "not yet bound to a kernel")
        raise ValueError(f"submodel {submodel_id!r} not supported: {reason}")
    _, mapping = binding
    return dict(mapping)
