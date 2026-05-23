"""Pure-NumPy reference kernels for the exported submodels.

Each kernel evaluates a single mechanistic submodel using only numpy.
The exported SBML/CellML/PhysioCell models must produce numerically
matching output (within tolerance) when simulated. The round-trip
validation in the test suite uses these kernels as the ground truth.

These are NOT a new physiological engine. They are unit-test-grade
evaluators of the same algebraic relationships the exported models
encode.
"""

from __future__ import annotations

from collections.abc import Sequence

import numpy as np
from numpy.typing import NDArray

FloatArrayLike = float | Sequence[float] | NDArray[np.floating]


# ---- 1. Logistic placental villous-surface-area growth -------------


def placental_area_logistic(
    t_weeks: FloatArrayLike,
    *,
    initial_area_m2: float,
    term_area_m2: float,
    growth_rate_per_week: float,
    midpoint_week: float,
) -> NDArray[np.float64]:
    """Logistic villous-surface-area growth.

    `A(t) = A0 + (Aterm - A0) / (1 + exp(-r*(t - t_mid)))`
    """
    t = np.asarray(t_weeks, dtype=np.float64)
    span = term_area_m2 - initial_area_m2
    return initial_area_m2 + span / (1.0 + np.exp(-growth_rate_per_week * (t - midpoint_week)))


# ---- 2. Severinghaus O2-Hb dissociation (adult) --------------------


def severinghaus_o2_saturation(po2_mmhg: FloatArrayLike) -> NDArray[np.float64]:
    """Severinghaus 1979 (PMID 35496) equation 1.

    `S = ((PO2^3 + 150*PO2)^-1 * 23400 + 1)^-1`
    """
    p = np.asarray(po2_mmhg, dtype=np.float64)
    if np.any(p <= 0):
        raise ValueError("PO2 must be strictly positive")
    return 1.0 / ((p**3 + 150.0 * p) ** -1 * 23400.0 + 1.0)


# ---- 3. Fetal HbF dissociation (Bauer 1969 left-shift) -------------


def fetal_hbf_o2_saturation(
    po2_mmhg: FloatArrayLike,
    *,
    p50_mmhg: float = 19.5,
    hill_coefficient: float = 2.85,
) -> NDArray[np.float64]:
    """Hill-form dissociation for fetal HbF.

    `S = (PO2/P50)^n / (1 + (PO2/P50)^n)`
    """
    p = np.asarray(po2_mmhg, dtype=np.float64)
    if np.any(p <= 0):
        raise ValueError("PO2 must be strictly positive")
    ratio = (p / p50_mmhg) ** hill_coefficient
    return ratio / (1.0 + ratio)


# ---- 4. Michaelis-Menten glucose transport (GLUT1, GLUT3) ----------


def michaelis_menten_flux(
    substrate_mmol_per_l: FloatArrayLike,
    *,
    km_mmol_per_l: float,
    vmax_per_area: float,
) -> NDArray[np.float64]:
    """Standard Michaelis-Menten rate law.

    `V = Vmax * [S] / (Km + [S])`

    Same form for GLUT1 (lower-affinity, higher Vmax) and GLUT3
    (higher-affinity, lower Vmax).
    """
    s = np.asarray(substrate_mmol_per_l, dtype=np.float64)
    return vmax_per_area * s / (km_mmol_per_l + s)


# Backward-compatible alias used by earlier tests.
def glut1_michaelis_menten(
    substrate_mmol_per_l: FloatArrayLike,
    *,
    km_mmol_per_l: float,
    vmax_per_area: float,
) -> NDArray[np.float64]:
    return michaelis_menten_flux(
        substrate_mmol_per_l,
        km_mmol_per_l=km_mmol_per_l,
        vmax_per_area=vmax_per_area,
    )


# ---- 5. Maternal cardiac output Gaussian trajectory ----------------


def maternal_cardiac_output(
    t_weeks: FloatArrayLike,
    *,
    baseline_l_per_min: float,
    peak_excess_l_per_min: float,
    peak_week: float,
    spread_weeks: float,
) -> NDArray[np.float64]:
    """Gaussian-bump cardiac-output trajectory.

    `CO(t) = baseline + peak_excess * exp(-((t - peak_week)/spread)^2 / 2)`
    """
    t = np.asarray(t_weeks, dtype=np.float64)
    z = (t - peak_week) / spread_weeks
    return baseline_l_per_min + peak_excess_l_per_min * np.exp(-(z**2) / 2.0)


# ---- 6. Maternal MAP Gaussian-nadir trajectory ---------------------


def maternal_map(
    t_weeks: FloatArrayLike,
    *,
    baseline_mmhg: float,
    nadir_drop_mmhg: float,
    nadir_week: float,
    spread_weeks: float,
) -> NDArray[np.float64]:
    """Gaussian-nadir MAP trajectory.

    `MAP(t) = baseline - nadir_drop * exp(-((t - nadir_week)/spread)^2 / 2)`
    """
    t = np.asarray(t_weeks, dtype=np.float64)
    z = (t - nadir_week) / spread_weeks
    return baseline_mmhg - nadir_drop_mmhg * np.exp(-(z**2) / 2.0)


# ---- 7. Uterine-artery flow logistic growth ------------------------


def uterine_artery_flow(
    t_weeks: FloatArrayLike,
    *,
    baseline_ml_per_min: float,
    term_ml_per_min: float,
    growth_rate_per_week: float,
    midpoint_week: float = 24.0,
) -> NDArray[np.float64]:
    """Logistic growth of uterine-artery flow.

    `Q(t) = baseline + (term - baseline) / (1 + exp(-r*(t - t_mid)))`
    """
    t = np.asarray(t_weeks, dtype=np.float64)
    span = term_ml_per_min - baseline_ml_per_min
    return baseline_ml_per_min + span / (1.0 + np.exp(-growth_rate_per_week * (t - midpoint_week)))


# ---- 8. Placental O2 venous equilibrator ---------------------------


def placental_o2_equilibrator(
    maternal_intervillous_po2_mmhg: FloatArrayLike,
    *,
    max_equilibration: float,
) -> NDArray[np.float64]:
    """Algebraic equilibrium: umbilical vein PO2 = intervillous PO2 * f.

    The `max_equilibration` parameter is the fraction of the maternal-
    side intervillous PO2 that the umbilical vein blood reaches at
    equilibrium (typically ~0.6-0.8 in a healthy term placenta).
    """
    p = np.asarray(maternal_intervillous_po2_mmhg, dtype=np.float64)
    if np.any(p < 0):
        raise ValueError("intervillous PO2 must be non-negative")
    return p * max_equilibration


# ---- 9. Plasma volume sigmoidal expansion --------------------------


def plasma_volume_expansion(
    t_weeks: FloatArrayLike,
    *,
    early_l: float,
    term_l: float,
    growth_rate_per_week: float = 0.2,
    midpoint_week: float = 22.0,
) -> NDArray[np.float64]:
    """Sigmoidal plasma-volume trajectory.

    `PV(t) = early + (term - early) / (1 + exp(-r*(t - t_mid)))`

    Anchored to Bernstein 2001's 12-week value (early_l) and de Haas
    2017's term value (term_l).
    """
    t = np.asarray(t_weeks, dtype=np.float64)
    span = term_l - early_l
    return early_l + span / (1.0 + np.exp(-growth_rate_per_week * (t - midpoint_week)))


# ---- 10. Hadlock IV fetal weight regression ------------------------


def maternal_gfr_logistic(
    t_weeks: FloatArrayLike,
    *,
    baseline_ml_per_min: float,
    peak_ml_per_min: float,
    growth_rate_per_week: float,
    peak_week: float,
) -> NDArray[np.float64]:
    """Logistic GFR trajectory across gestation.

    `GFR(t) = baseline + (peak - baseline) / (1 + exp(-r*(t - t_peak)))`

    Conrad 2001 (PMID 11489744) describes the relaxin-mediated rise to
    ~50% above the non-pregnant baseline by early-mid pregnancy. The
    logistic fit is an approximation; the true curve plateaus then
    declines slightly toward term.
    """
    t = np.asarray(t_weeks, dtype=np.float64)
    span = peak_ml_per_min - baseline_ml_per_min
    return baseline_ml_per_min + span / (1.0 + np.exp(-growth_rate_per_week * (t - peak_week)))


def amniotic_fluid_volume(
    t_weeks: FloatArrayLike,
    *,
    early_baseline_ml: float,
    peak_ml: float,
    peak_week: float,
    spread_weeks: float,
) -> NDArray[np.float64]:
    """Gaussian-bump amniotic-fluid-volume trajectory.

    `AFV(t) = early_baseline + (peak - early_baseline) * exp(-((t - t_peak)/sigma)^2 / 2)`

    Approximation to the Brace & Wolf 1989 (PMID 2782359) curve. The
    published curve is more accurately a piecewise polynomial — see
    `amniotic_fluid.afv_spread_weeks` tier rationale. The Gaussian
    bump matches the peak, declines symmetrically, and uses
    `early_baseline_ml` for the early-pregnancy floor.
    """
    t = np.asarray(t_weeks, dtype=np.float64)
    amplitude = peak_ml - early_baseline_ml
    z = (t - peak_week) / spread_weeks
    return early_baseline_ml + amplitude * np.exp(-(z**2) / 2.0)


# ---- 12. SVR trajectory (derived from MAP + CO) --------------------


def maternal_svr_trajectory(
    t_weeks: FloatArrayLike,
    *,
    baseline_map_mmhg: float,
    map_nadir_drop_mmhg: float,
    map_nadir_week: float,
    map_spread_weeks: float,
    baseline_co_l_per_min: float,
    peak_excess_co_l_per_min: float,
    co_peak_week: float,
    co_spread_weeks: float,
) -> NDArray[np.float64]:
    """Derived SVR across gestation: SVR(t) = MAP(t) * 80 / CO(t).

    Output in dyn*s/cm^5. The 80 multiplier converts mmHg*min/L to the
    CGS resistance unit. Sanghavi 2014 (PMC4172642) is the canonical
    reference for the convention in obstetric haemodynamics.
    """
    map_t = maternal_map(
        t_weeks,
        baseline_mmhg=baseline_map_mmhg,
        nadir_drop_mmhg=map_nadir_drop_mmhg,
        nadir_week=map_nadir_week,
        spread_weeks=map_spread_weeks,
    )
    co_t = maternal_cardiac_output(
        t_weeks,
        baseline_l_per_min=baseline_co_l_per_min,
        peak_excess_l_per_min=peak_excess_co_l_per_min,
        peak_week=co_peak_week,
        spread_weeks=co_spread_weeks,
    )
    return map_t * 80.0 / co_t


# ---- 13. Maternal PaO2 linear trajectory ---------------------------


def maternal_pao2_linear(
    t_weeks: FloatArrayLike,
    *,
    baseline_mmhg: float,
    term_mmhg: float,
    term_week: float = 40.0,
) -> NDArray[np.float64]:
    """Linear PaO2 trajectory.

    `PaO2(t) = baseline + (term - baseline) * (t / term_week)`

    Templeton & Kelman 1976 (PMID 1247088) and Hegewald 2011 document
    the modest rise (typically ~100 -> ~105 mmHg) from
    hyperventilation-induced respiratory alkalosis.
    """
    t = np.asarray(t_weeks, dtype=np.float64)
    return baseline_mmhg + (term_mmhg - baseline_mmhg) * (t / term_week)


# ---- 14. Maternal tidal volume sigmoidal trajectory ----------------


def maternal_tidal_volume(
    t_weeks: FloatArrayLike,
    *,
    baseline_ml: float,
    term_ml: float,
    growth_rate_per_week: float = 0.2,
    midpoint_week: float = 20.0,
) -> NDArray[np.float64]:
    """Sigmoidal tidal-volume trajectory.

    `VT(t) = baseline + (term - baseline) / (1 + exp(-r*(t - t_mid)))`

    LoMauro 2015 (PMID 25624458) reports the ~30-40% rise above
    non-pregnant baseline by term, driven by progesterone-mediated
    increase in respiratory drive.
    """
    t = np.asarray(t_weeks, dtype=np.float64)
    span = term_ml - baseline_ml
    return baseline_ml + span / (1.0 + np.exp(-growth_rate_per_week * (t - midpoint_week)))


# ---- 15. Maternal heart rate sigmoidal trajectory ------------------


def maternal_heart_rate(
    t_weeks: FloatArrayLike,
    *,
    baseline_bpm: float,
    term_bpm: float,
    growth_rate_per_week: float = 0.2,
    midpoint_week: float = 20.0,
) -> NDArray[np.float64]:
    """Sigmoidal heart-rate trajectory.

    `HR(t) = baseline + (term - baseline) / (1 + exp(-r*(t - t_mid)))`
    """
    t = np.asarray(t_weeks, dtype=np.float64)
    span = term_bpm - baseline_bpm
    return baseline_bpm + span / (1.0 + np.exp(-growth_rate_per_week * (t - midpoint_week)))


# ---- 16. Maternal stroke volume Gaussian trajectory ----------------


def maternal_stroke_volume(
    t_weeks: FloatArrayLike,
    *,
    baseline_ml: float,
    peak_excess_ml: float,
    peak_week: float,
    spread_weeks: float,
) -> NDArray[np.float64]:
    """Gaussian-bump stroke-volume trajectory.

    `SV(t) = baseline + peak_excess * exp(-((t - peak_week)/spread)^2 / 2)`

    Peak week and spread are shared with the cardiac-output bump
    (SV is the larger driver of the CO peak per Mahendru 2014).
    """
    t = np.asarray(t_weeks, dtype=np.float64)
    z = (t - peak_week) / spread_weeks
    return baseline_ml + peak_excess_ml * np.exp(-(z**2) / 2.0)


# ---- 17. Renal plasma flow Gaussian trajectory ---------------------


def renal_plasma_flow(
    t_weeks: FloatArrayLike,
    *,
    baseline_ml_per_min: float,
    peak_ml_per_min: float,
    peak_week: float,
    spread_weeks: float = 8.0,
) -> NDArray[np.float64]:
    """Gaussian-bump RPF trajectory (Dunlop 1981).

    `RPF(t) = baseline + (peak - baseline) * exp(-((t - peak_week)/spread)^2 / 2)`
    """
    t = np.asarray(t_weeks, dtype=np.float64)
    amplitude = peak_ml_per_min - baseline_ml_per_min
    z = (t - peak_week) / spread_weeks
    return baseline_ml_per_min + amplitude * np.exp(-(z**2) / 2.0)


# ---- 18. Minute ventilation derived trajectory ---------------------


def maternal_minute_ventilation(
    t_weeks: FloatArrayLike,
    *,
    baseline_vt_ml: float,
    term_vt_ml: float,
    baseline_rr_bpm: float,
    term_rr_bpm: float,
) -> NDArray[np.float64]:
    """Derived minute ventilation: VE(t) = VT(t) * RR(t).

    VT and RR are both sigmoidal with the standard baseline→term form
    used by `maternal_tidal_volume` and the heart-rate trajectory.
    """
    vt = maternal_tidal_volume(t_weeks, baseline_ml=baseline_vt_ml, term_ml=term_vt_ml)
    # RR shares the sigmoidal form (slow rise, ~mid-pregnancy inflection)
    t = np.asarray(t_weeks, dtype=np.float64)
    rr = baseline_rr_bpm + (term_rr_bpm - baseline_rr_bpm) / (1.0 + np.exp(-0.2 * (t - 20.0)))
    return vt * rr


# ---- 19. Maternal arterial pH linear trajectory --------------------


def maternal_arterial_ph(
    t_weeks: FloatArrayLike,
    *,
    baseline_ph: float,
    term_ph: float,
    term_week: float = 40.0,
) -> NDArray[np.float64]:
    """Linear arterial-pH trajectory across gestation.

    `pH(t) = baseline + (term - baseline) * (t / term_week)`
    """
    t = np.asarray(t_weeks, dtype=np.float64)
    return baseline_ph + (term_ph - baseline_ph) * (t / term_week)


# ---- 20. Hadlock biometry cubic-fit growth -------------------------

HADLOCK_ANCHOR_WEEKS: tuple[int, ...] = (16, 20, 24, 28, 32, 36, 40)


def hadlock_biometry_cubic(
    t_weeks: FloatArrayLike,
    weekly_values_mm: Sequence[float],
    *,
    anchor_weeks: Sequence[int] = HADLOCK_ANCHOR_WEEKS,
) -> NDArray[np.float64]:
    """Cubic polynomial fit of biometry vs gestational age.

    Fits `weekly_values_mm` against `anchor_weeks` (default 16, 20, 24,
    28, 32, 36, 40) with `numpy.polyfit(deg=3)` and evaluates the
    polynomial at `t_weeks`. Used for BPD, HC, AC, FL growth submodels
    where the dataset stores discrete weekly anchors from Hadlock 1982.
    """
    coeffs = np.polyfit(np.asarray(anchor_weeks, dtype=np.float64), weekly_values_mm, 3)
    t = np.asarray(t_weeks, dtype=np.float64)
    return np.asarray(np.polyval(coeffs, t), dtype=np.float64)


def hadlock_biometry_cubic_coefficients(
    weekly_values_mm: Sequence[float],
    *,
    anchor_weeks: Sequence[int] = HADLOCK_ANCHOR_WEEKS,
) -> tuple[float, float, float, float]:
    """Return (a3, a2, a1, a0) cubic coefficients for the biometry fit.

    Helper for SBML/CellML builders that need to embed the fit
    coefficients directly in the exported model.
    """
    a3, a2, a1, a0 = np.polyfit(np.asarray(anchor_weeks, dtype=np.float64), weekly_values_mm, 3)
    return float(a3), float(a2), float(a1), float(a0)


# ---- 21. Hadlock IV fetal weight regression ------------------------


def hadlock_fetal_weight(
    *,
    bpd_mm: float,
    hc_mm: float,
    ac_mm: float,
    fl_mm: float,
    intercept: float = 1.3596,
) -> float:
    """Hadlock 1991 four-parameter fetal-weight estimator.

    `log10(EFW) = a + 0.0064*HC + 0.0424*AC + 0.174*FL + 0.00061*BPD*AC - 0.00386*AC*FL`

    Returns weight in grams.
    """
    # Hadlock's coefficients use cm; convert mm → cm
    bpd = bpd_mm / 10.0
    hc = hc_mm / 10.0
    ac = ac_mm / 10.0
    fl = fl_mm / 10.0
    log10_w = (
        intercept + 0.0064 * hc + 0.0424 * ac + 0.174 * fl + 0.00061 * bpd * ac - 0.00386 * ac * fl
    )
    return float(10**log10_w)
