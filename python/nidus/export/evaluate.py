"""Submodel evaluation: dataset → numeric trajectory in one call.

The SBML / CellML builders carry submodel-specific knowledge about
which dataset parameter feeds which kernel argument. ``evaluate.py``
exposes that mapping as a small public registry so the dashboard
(Trajectory Viewer, Sensitivity Sandbox) and downstream notebooks can
evaluate a submodel on a numeric grid without re-implementing the
binding.

Each binding declares the **domain** the submodel evaluates over —
gestational time in weeks, partial pressure in mmHg, substrate
concentration in mmol/L, etc. — so dashboards and tutorials can pick
a sensible plotting grid automatically.

Coverage as of this iteration: **40 of the 41 registered submodels.**
The only remaining unsupported entry is ``hadlock_fetal_weight``,
which takes four biometry inputs (BPD, HC, AC, FL) simultaneously
and is therefore not a 1-D trajectory — see ``UNSUPPORTED_REASON``.
"""

from __future__ import annotations

from collections.abc import Callable, Sequence
from dataclasses import dataclass

import numpy as np
from numpy.typing import NDArray

from nidus.load import Dataset

from . import reference as _ref
from .registry import SUBMODELS

_Kernel = Callable[..., NDArray[np.float64]]


@dataclass(frozen=True)
class Domain:
    """The independent variable a submodel evaluates over."""

    name: str
    label: str
    units: str
    default_range: tuple[float, float]


TIME_WEEKS = Domain("t_weeks", "gestational age (weeks)", "weeks", (8.0, 40.0))
PO2_MMHG = Domain("po2_mmhg", "PO2 (mmHg)", "mmHg", (5.0, 120.0))
SUBSTRATE_MMOL = Domain(
    "substrate_mmol_per_l", "substrate concentration (mmol/L)", "mmol/L", (0.1, 20.0)
)
INTERVILLOUS_PO2 = Domain(
    "maternal_intervillous_po2_mmhg", "intervillous PO2 (mmHg)", "mmHg", (10.0, 100.0)
)
MATERNAL_CORTISOL = Domain(
    "maternal_cortisol_ug_per_dl", "maternal cortisol (μg/dL)", "μg/dL", (5.0, 50.0)
)
FETAL_WEIGHT = Domain("fetal_weight_g", "fetal weight (g)", "g", (100.0, 4500.0))


@dataclass(frozen=True)
class _Binding:
    kernel: _Kernel
    params: dict[str, str]  # kernel_kwarg -> dataset_parameter_id
    domain: Domain


def _b(kernel: _Kernel, domain: Domain, **mapping: str) -> _Binding:
    return _Binding(kernel=kernel, params=mapping, domain=domain)


_HADLOCK_ANCHOR_WEEKS: tuple[int, ...] = (16, 20, 24, 28, 32, 36, 40)


def _hadlock_biometry_kernel(
    t_weeks: NDArray[np.floating],
    *,
    a16: float,
    a20: float,
    a24: float,
    a32: float,
    a36: float,
    a40: float,
    a28: float,
) -> NDArray[np.float64]:
    """Scalar-kwarg adapter over ``hadlock_biometry_cubic``.

    The underlying kernel takes a list of 7 weekly anchors. This
    adapter exposes them as named keyword arguments so the standard
    ``_BINDINGS`` shape (and sensitivity-sweep overrides) work.
    """
    return _ref.hadlock_biometry_cubic(
        t_weeks,
        [a16, a20, a24, a28, a32, a36, a40],
        anchor_weeks=_HADLOCK_ANCHOR_WEEKS,
    )


_BINDINGS: dict[str, _Binding] = {
    # ---- Time-trajectory submodels ----------------------------------
    "placental_villous_growth": _b(
        _ref.placental_area_logistic,
        TIME_WEEKS,
        initial_area_m2="placental_structure.initial_area_m2",
        term_area_m2="placental_structure.term_area_m2",
        growth_rate_per_week="placental_structure.growth_rate_per_week",
        midpoint_week="placental_structure.midpoint_week",
    ),
    "maternal_cardiac_output_trajectory": _b(
        _ref.maternal_cardiac_output,
        TIME_WEEKS,
        baseline_l_per_min="maternal_cardiovascular.baseline_cardiac_output_l_per_min",
        peak_excess_l_per_min="maternal_cardiovascular.peak_excess_cardiac_output_l_per_min",
        peak_week="maternal_cardiovascular.cardiac_output_peak_week",
        spread_weeks="maternal_cardiovascular.cardiac_output_spread_weeks",
    ),
    "maternal_map_trajectory": _b(
        _ref.maternal_map,
        TIME_WEEKS,
        baseline_mmhg="maternal_cardiovascular.baseline_map_mmhg",
        nadir_drop_mmhg="maternal_cardiovascular.map_nadir_drop_mmhg",
        nadir_week="maternal_cardiovascular.map_nadir_week",
        spread_weeks="maternal_cardiovascular.map_spread_weeks",
    ),
    "uterine_artery_flow_logistic": _b(
        _ref.uterine_artery_flow,
        TIME_WEEKS,
        baseline_ml_per_min="maternal_cardiovascular.baseline_uterine_flow_ml_per_min",
        term_ml_per_min="maternal_cardiovascular.term_uterine_flow_ml_per_min",
        growth_rate_per_week="maternal_cardiovascular.uterine_flow_growth_rate_per_week",
    ),
    "plasma_volume_expansion": _b(
        _ref.plasma_volume_expansion,
        TIME_WEEKS,
        early_l="maternal_blood.plasma_volume_early_l",
        term_l="maternal_blood.plasma_volume_l",
    ),
    "gfr_logistic_trajectory": _b(
        _ref.maternal_gfr_logistic,
        TIME_WEEKS,
        baseline_ml_per_min="maternal_renal.baseline_gfr_ml_per_min",
        peak_ml_per_min="maternal_renal.gfr_ml_per_min",
        growth_rate_per_week="maternal_renal.gfr_logistic_rate_per_week",
        peak_week="maternal_renal.gfr_peak_week",
    ),
    "heart_rate_trajectory": _b(
        _ref.maternal_heart_rate,
        TIME_WEEKS,
        baseline_bpm="maternal_cardiovascular.baseline_heart_rate_bpm",
        term_bpm="maternal_cardiovascular.peak_excess_heart_rate_bpm",
    ),
    "tidal_volume_trajectory": _b(
        _ref.maternal_tidal_volume,
        TIME_WEEKS,
        baseline_ml="maternal_respiratory.baseline_tidal_volume_ml",
        term_ml="maternal_respiratory.tidal_volume_ml_term",
    ),
    "fetal_heart_rate_trajectory": _b(
        _ref.fetal_heart_rate,
        TIME_WEEKS,
        baseline_bpm="fetal_circulation.fhr_baseline_bpm",
        term_bpm="fetal_circulation.fhr_term_bpm",
    ),
    "homa_ir_trajectory": _b(
        _ref.maternal_homa_ir,
        TIME_WEEKS,
        baseline="maternal_endocrine.homa_ir_baseline",
        term="maternal_endocrine.homa_ir_term",
    ),
    "cortisol_trajectory": _b(
        _ref.maternal_cortisol,
        TIME_WEEKS,
        baseline_ug_per_dl="maternal_endocrine.cortisol_baseline_ug_per_dl",
        term_ug_per_dl="maternal_endocrine.cortisol_term_ug_per_dl",
    ),
    "hpl_trajectory": _b(
        _ref.maternal_hpl,
        TIME_WEEKS,
        baseline_ug_per_ml="placental_endocrine.hpl_baseline_ug_per_ml",
        term_ug_per_ml="placental_endocrine.hpl_term_ug_per_ml",
    ),
    "progesterone_trajectory": _b(
        _ref.maternal_progesterone,
        TIME_WEEKS,
        baseline_ng_per_ml="placental_endocrine.progesterone_baseline_ng_per_ml",
        term_ng_per_ml="placental_endocrine.progesterone_term_ng_per_ml",
    ),
    "estradiol_trajectory": _b(
        _ref.maternal_estradiol,
        TIME_WEEKS,
        baseline_ng_per_ml="placental_endocrine.estradiol_baseline_ng_per_ml",
        term_ng_per_ml="placental_endocrine.estradiol_term_ng_per_ml",
    ),
    "hcg_trajectory": _b(
        _ref.maternal_hcg,
        TIME_WEEKS,
        peak_miu_per_ml="placental_endocrine.hcg_peak_miu_per_ml",
        peak_week="placental_endocrine.hcg_peak_week",
        term_miu_per_ml="placental_endocrine.hcg_term_miu_per_ml",
    ),
    "umbilical_artery_pi_trajectory": _b(
        _ref.umbilical_artery_pi,
        TIME_WEEKS,
        baseline="fetal_circulation.ua_pi_baseline",
        term="fetal_circulation.ua_pi_term",
    ),
    "arterial_ph_trajectory": _b(
        _ref.maternal_arterial_ph,
        TIME_WEEKS,
        baseline_ph="maternal_respiratory.baseline_arterial_ph",
        term_ph="maternal_respiratory.term_arterial_ph",
    ),
    "pao2_trajectory_linear": _b(
        _ref.maternal_pao2_linear,
        TIME_WEEKS,
        baseline_mmhg="maternal_respiratory.baseline_pao2_mmhg",
        term_mmhg="maternal_respiratory.pao2_mmhg_term",
    ),
    "maternal_fetal_igg_transfer": _b(
        _ref.maternal_fetal_igg_transfer,
        TIME_WEEKS,
        baseline="placental_structure.igg_transfer_ratio_baseline",
        term="placental_structure.igg_transfer_ratio_term",
    ),
    "maternal_microchimerism_trajectory": _b(
        _ref.maternal_microchimerism_trajectory,
        TIME_WEEKS,
        baseline="maternal_blood.fetal_microchimerism_baseline_cells_per_ml",
        term="maternal_blood.fetal_microchimerism_term_cells_per_ml",
    ),
    "fetal_pulmonary_fluid_trajectory": _b(
        _ref.fetal_pulmonary_fluid_trajectory,
        TIME_WEEKS,
        baseline="fetal_metabolism.pulmonary_fluid_net_rate_baseline_ml_per_kg_h",
        term="fetal_metabolism.pulmonary_fluid_net_rate_term_ml_per_kg_h",
    ),
    "stroke_volume_trajectory": _b(
        _ref.maternal_stroke_volume,
        TIME_WEEKS,
        baseline_ml="maternal_cardiovascular.baseline_stroke_volume_ml",
        peak_excess_ml="maternal_cardiovascular.peak_excess_stroke_volume_ml",
        peak_week="maternal_cardiovascular.cardiac_output_peak_week",
        spread_weeks="maternal_cardiovascular.cardiac_output_spread_weeks",
    ),
    "renal_plasma_flow_trajectory": _b(
        _ref.renal_plasma_flow,
        TIME_WEEKS,
        baseline_ml_per_min="maternal_renal.renal_plasma_flow_baseline_ml_per_min",
        peak_ml_per_min="maternal_renal.renal_plasma_flow_peak_ml_per_min",
        peak_week="maternal_renal.rpf_peak_week",
    ),
    "minute_ventilation_trajectory": _b(
        _ref.maternal_minute_ventilation,
        TIME_WEEKS,
        baseline_vt_ml="maternal_respiratory.baseline_tidal_volume_ml",
        term_vt_ml="maternal_respiratory.tidal_volume_ml_term",
        baseline_rr_bpm="maternal_respiratory.baseline_respiratory_rate_bpm",
        term_rr_bpm="maternal_respiratory.term_respiratory_rate_bpm",
    ),
    "amniotic_fluid_volume_trajectory": _b(
        _ref.amniotic_fluid_volume,
        TIME_WEEKS,
        early_baseline_ml="amniotic_fluid.afv_early_baseline_ml",
        peak_ml="amniotic_fluid.afv_peak_ml",
        peak_week="amniotic_fluid.afv_peak_week",
        spread_weeks="amniotic_fluid.afv_spread_weeks",
    ),
    "svr_trajectory": _b(
        _ref.maternal_svr_trajectory,
        TIME_WEEKS,
        baseline_map_mmhg="maternal_cardiovascular.baseline_map_mmhg",
        map_nadir_drop_mmhg="maternal_cardiovascular.map_nadir_drop_mmhg",
        map_nadir_week="maternal_cardiovascular.map_nadir_week",
        map_spread_weeks="maternal_cardiovascular.map_spread_weeks",
        baseline_co_l_per_min="maternal_cardiovascular.baseline_cardiac_output_l_per_min",
        peak_excess_co_l_per_min="maternal_cardiovascular.peak_excess_cardiac_output_l_per_min",
        co_peak_week="maternal_cardiovascular.cardiac_output_peak_week",
        co_spread_weeks="maternal_cardiovascular.cardiac_output_spread_weeks",
    ),
    "tsh_trajectory": _b(
        _ref.maternal_tsh,
        TIME_WEEKS,
        t1_value="maternal_endocrine.tsh_t1_miu_per_l",
        term_value="maternal_endocrine.tsh_term_miu_per_l",
    ),
    "mca_pi_trajectory": _b(
        _ref.mca_pi,
        TIME_WEEKS,
        baseline="fetal_circulation.mca_pi_baseline",
        peak="fetal_circulation.mca_pi_peak",
    ),
    "cerebroplacental_ratio": _b(
        _ref.cerebroplacental_ratio,
        TIME_WEEKS,
        ua_pi_baseline="fetal_circulation.ua_pi_baseline",
        ua_pi_term="fetal_circulation.ua_pi_term",
        mca_pi_baseline="fetal_circulation.mca_pi_baseline",
        mca_pi_peak="fetal_circulation.mca_pi_peak",
    ),
    # ---- Algebraic submodels (non-time domain) ----------------------
    "o2hb_dissociation_adult": _b(
        # Severinghaus kernel takes only PO2 — its P50 / Hill n are
        # baked-in constants, but the dataset still carries the matched
        # values for provenance.
        _ref.severinghaus_o2_saturation,
        PO2_MMHG,
    ),
    "o2hb_dissociation_fetal": _b(
        _ref.fetal_hbf_o2_saturation,
        PO2_MMHG,
        p50_mmhg="fetal_metabolism.fetal_p50_mmhg",
    ),
    "placental_glucose_glut1": _b(
        _ref.michaelis_menten_flux,
        SUBSTRATE_MMOL,
        km_mmol_per_l="placental_glucose.glucose_glut1_km_mmol_per_l",
        vmax_per_area="placental_glucose.glucose_glut1_vmax_per_area_mmol_per_min_per_m2",
    ),
    "placental_glucose_glut3": _b(
        _ref.michaelis_menten_flux,
        SUBSTRATE_MMOL,
        km_mmol_per_l="placental_glucose.glucose_glut3_km_mmol_per_l",
        vmax_per_area="placental_glucose.glucose_glut3_vmax_per_area_mmol_per_min_per_m2",
    ),
    "placental_o2_equilibrator": _b(
        _ref.placental_o2_equilibrator,
        INTERVILLOUS_PO2,
        max_equilibration="placental_gas_exchange.gas_max_equilibration",
    ),
    "placental_cortisol_gradient": _b(
        _ref.placental_cortisol_gradient,
        MATERNAL_CORTISOL,
        inactivation_fraction="placental_structure.hsd2_cortisol_inactivation_fraction",
    ),
    "placental_fetal_allometry": _b(
        _ref.placental_fetal_allometry,
        FETAL_WEIGHT,
        coefficient_a="placental_structure.allometric_coefficient_a",
        exponent_b="placental_structure.allometric_exponent_b",
    ),
    # ---- Hadlock biometry (cubic fit through 7 weekly anchors) ------
    "hadlock_bpd_growth": _b(
        _hadlock_biometry_kernel,
        TIME_WEEKS,
        a16="fetal_growth.bpd_16w_mm",
        a20="fetal_growth.bpd_20w_mm",
        a24="fetal_growth.bpd_24w_mm",
        a28="fetal_growth.bpd_28w_mm",
        a32="fetal_growth.bpd_32w_mm",
        a36="fetal_growth.bpd_36w_mm",
        a40="fetal_growth.bpd_40w_mm",
    ),
    "hadlock_hc_growth": _b(
        _hadlock_biometry_kernel,
        TIME_WEEKS,
        a16="fetal_growth.hc_16w_mm",
        a20="fetal_growth.hc_20w_mm",
        a24="fetal_growth.hc_24w_mm",
        a28="fetal_growth.hc_28w_mm",
        a32="fetal_growth.hc_32w_mm",
        a36="fetal_growth.hc_36w_mm",
        a40="fetal_growth.hc_40w_mm",
    ),
    "hadlock_ac_growth": _b(
        _hadlock_biometry_kernel,
        TIME_WEEKS,
        a16="fetal_growth.ac_16w_mm",
        a20="fetal_growth.ac_20w_mm",
        a24="fetal_growth.ac_24w_mm",
        a28="fetal_growth.ac_28w_mm",
        a32="fetal_growth.ac_32w_mm",
        a36="fetal_growth.ac_36w_mm",
        a40="fetal_growth.ac_40w_mm",
    ),
    "hadlock_fl_growth": _b(
        _hadlock_biometry_kernel,
        TIME_WEEKS,
        a16="fetal_growth.fl_16w_mm",
        a20="fetal_growth.fl_20w_mm",
        a24="fetal_growth.fl_24w_mm",
        a28="fetal_growth.fl_28w_mm",
        a32="fetal_growth.fl_32w_mm",
        a36="fetal_growth.fl_36w_mm",
        a40="fetal_growth.fl_40w_mm",
    ),
}


UNSUPPORTED_REASON: dict[str, str] = {
    "hadlock_fetal_weight": "Multivariate (BPD, HC, AC, FL) — not a 1-D trajectory",
}


def supported_submodels() -> list[str]:
    """Submodel ids that ``evaluate_submodel`` can handle today."""
    return list(_BINDINGS.keys())


def submodel_domain(submodel_id: str) -> Domain:
    """Return the :class:`Domain` (independent variable) for a supported submodel."""
    _, binding = _resolve(submodel_id)
    return binding.domain


def evaluate_submodel(
    ds: Dataset,
    submodel_id: str,
    x_values: Sequence[float] | NDArray[np.floating],
    *,
    overrides: dict[str, float] | None = None,
) -> NDArray[np.float64]:
    """Evaluate a submodel on a numeric grid.

    Args:
        ds: the loaded nidus dataset.
        submodel_id: a registered submodel id (see ``nidus.export.SUBMODELS``).
        x_values: values of the submodel's independent variable. Check
            :func:`submodel_domain` for the expected units (gestational
            age in weeks, PO2 in mmHg, substrate concentration in
            mmol/L, etc.).
        overrides: optional ``{kernel_kwarg: value}`` overrides. Use to
            run sensitivity sweeps — replaces a single kernel argument
            for the duration of the call.

    Returns:
        1-D NumPy array of the submodel's primary observable, same
        length as ``x_values``.

    Raises:
        KeyError: if ``submodel_id`` is unknown to the registry.
        ValueError: if the submodel is registered but has no kernel
            binding (see :data:`UNSUPPORTED_REASON`).
    """
    _, binding = _resolve(submodel_id)
    kwargs: dict[str, float] = {kw: ds[pid].value.central for kw, pid in binding.params.items()}
    if overrides:
        kwargs.update(overrides)
    return binding.kernel(np.asarray(x_values, dtype=float), **kwargs)


def kernel_parameter_mapping(submodel_id: str) -> dict[str, str]:
    """Return ``{kernel_kwarg: dataset_parameter_id}`` for a supported submodel.

    Use this when you need to introspect which kernel argument
    corresponds to which dataset parameter — e.g. to surface the
    parameter that's about to be swept in a sensitivity analysis. For
    unsupported submodels, raises the same ``ValueError`` as
    :func:`evaluate_submodel`.
    """
    _, binding = _resolve(submodel_id)
    return dict(binding.params)


def _resolve(submodel_id: str) -> tuple[str, _Binding]:
    if not any(s.id == submodel_id for s in SUBMODELS):
        raise KeyError(f"unknown submodel id: {submodel_id!r}")
    binding = _BINDINGS.get(submodel_id)
    if binding is None:
        reason = UNSUPPORTED_REASON.get(submodel_id, "not yet bound to a kernel")
        raise ValueError(f"submodel {submodel_id!r} not supported: {reason}")
    return submodel_id, binding
