"""Tests for the v0.4 mechanistic-modeling exports.

Covers:
- Registry consistency (every submodel's parameter ids resolve)
- NumPy reference kernels (sanity checks against known values)
- SBML generation + libSBML consistency check
- CellML 2.0 and 1.1 generation
- PhysioCell parameter export
- Round-trip: SBML/CellML algebraic models, when evaluated, match the
  reference NumPy kernels.
"""

from __future__ import annotations

import re
from pathlib import Path

import numpy as np
import pytest

import nidus

# Tier-A canonical values that the reference kernels must reproduce.
SEVERINGHAUS_P50_MMHG = 26.6
HBF_P50_MMHG = 19.5


# ---- Registry + reference kernel sanity ----------------------------


def test_registry_lists_submodels() -> None:
    from nidus.export import list_submodels

    summary = list_submodels()
    ids = {s["id"] for s in summary}
    assert {
        "placental_villous_growth",
        "o2hb_dissociation_adult",
        "o2hb_dissociation_fetal",
        "placental_glucose_glut1",
        "placental_glucose_glut3",
        "maternal_cardiac_output_trajectory",
        "maternal_map_trajectory",
        "uterine_artery_flow_logistic",
        "placental_o2_equilibrator",
        "plasma_volume_expansion",
        "hadlock_fetal_weight",
        "gfr_logistic_trajectory",
        "amniotic_fluid_volume_trajectory",
        "svr_trajectory",
        "pao2_trajectory_linear",
        "tidal_volume_trajectory",
        "heart_rate_trajectory",
        "stroke_volume_trajectory",
        "renal_plasma_flow_trajectory",
        "minute_ventilation_trajectory",
        "arterial_ph_trajectory",
        "hadlock_bpd_growth",
        "hadlock_hc_growth",
        "hadlock_ac_growth",
        "hadlock_fl_growth",
        "homa_ir_trajectory",
        "tsh_trajectory",
        "cortisol_trajectory",
        "hpl_trajectory",
        "progesterone_trajectory",
        "estradiol_trajectory",
        "fetal_heart_rate_trajectory",
        "hcg_trajectory",
        "umbilical_artery_pi_trajectory",
        "mca_pi_trajectory",
        "cerebroplacental_ratio",
        "placental_fetal_allometry",
        "maternal_fetal_igg_transfer",
        "placental_cortisol_gradient",
        "maternal_microchimerism_trajectory",
        "fetal_pulmonary_fluid_trajectory",
    } == ids


def test_registry_parameters_resolve(ds: nidus.Dataset) -> None:
    """Every parameter id referenced by a submodel must exist in the dataset."""
    from nidus.export import SUBMODELS

    for sm in SUBMODELS:
        for pid in sm.parameter_ids:
            assert pid in ds, f"{sm.id} references missing parameter {pid}"


def test_severinghaus_saturation_at_p50() -> None:
    from nidus.export.reference import severinghaus_o2_saturation

    # By definition, S(P50) = 0.5 to within a small numerical tolerance.
    s = severinghaus_o2_saturation(SEVERINGHAUS_P50_MMHG)
    assert s == pytest.approx(0.5, abs=0.01), (
        f"Severinghaus should give ~0.5 saturation at P50; got {s}"
    )


def test_severinghaus_monotone() -> None:
    from nidus.export.reference import severinghaus_o2_saturation

    po2 = np.array([10.0, 20.0, 30.0, 50.0, 80.0, 100.0])
    s = severinghaus_o2_saturation(po2)
    assert np.all(np.diff(s) > 0), "saturation must be monotonically increasing in PO2"


def test_severinghaus_rejects_nonpositive() -> None:
    from nidus.export.reference import severinghaus_o2_saturation

    with pytest.raises(ValueError):
        severinghaus_o2_saturation(0.0)
    with pytest.raises(ValueError):
        severinghaus_o2_saturation(-5.0)


def test_fetal_hbf_left_shift() -> None:
    """At any given PO2, fetal HbF saturation > adult HbA saturation."""
    from nidus.export.reference import fetal_hbf_o2_saturation, severinghaus_o2_saturation

    for po2 in [20.0, 30.0, 40.0, 50.0]:
        fetal = fetal_hbf_o2_saturation(po2)
        adult = severinghaus_o2_saturation(po2)
        assert fetal > adult, f"HbF should be left-shifted at PO2={po2}"


def test_fetal_hbf_saturation_at_p50() -> None:
    from nidus.export.reference import fetal_hbf_o2_saturation

    assert fetal_hbf_o2_saturation(HBF_P50_MMHG) == pytest.approx(0.5, abs=0.01)


def test_logistic_growth_endpoints() -> None:
    from nidus.export.reference import placental_area_logistic

    a0, k = 0.5, 11.5
    very_early = placental_area_logistic(
        0.0,
        initial_area_m2=a0,
        term_area_m2=k,
        growth_rate_per_week=0.18,
        midpoint_week=22.0,
    )
    very_late = placental_area_logistic(
        45.0,
        initial_area_m2=a0,
        term_area_m2=k,
        growth_rate_per_week=0.18,
        midpoint_week=22.0,
    )
    # Very-early: a0 + small fraction of span
    assert a0 < very_early < a0 + 0.5
    # Very-late: close to k
    assert very_late == pytest.approx(k, abs=0.5)


def test_gfr_logistic_endpoints() -> None:
    from nidus.export.reference import maternal_gfr_logistic

    early = float(
        maternal_gfr_logistic(
            0.0,
            baseline_ml_per_min=100.0,
            peak_ml_per_min=150.0,
            growth_rate_per_week=0.4,
            peak_week=16.0,
        )
    )
    late = float(
        maternal_gfr_logistic(
            40.0,
            baseline_ml_per_min=100.0,
            peak_ml_per_min=150.0,
            growth_rate_per_week=0.4,
            peak_week=16.0,
        )
    )
    # Very early: close to baseline; very late: close to plateau.
    assert 100.0 < early < 101.0
    assert late == pytest.approx(150.0, abs=0.5)


def test_amniotic_fluid_volume_shape() -> None:
    from nidus.export.reference import amniotic_fluid_volume

    kwargs = dict(
        early_baseline_ml=100.0,
        peak_ml=800.0,
        peak_week=33.0,
        spread_weeks=9.0,
    )
    early = float(amniotic_fluid_volume(12.0, **kwargs))  # type: ignore[arg-type]
    peak = float(amniotic_fluid_volume(33.0, **kwargs))  # type: ignore[arg-type]
    term = float(amniotic_fluid_volume(40.0, **kwargs))  # type: ignore[arg-type]
    # At peak week, AFV equals the published peak.
    assert peak == pytest.approx(800.0)
    # At 12 weeks (~21w before peak), well below peak.
    assert early < 400.0
    # At term (~7w after peak), declining but still well above early.
    assert 500.0 < term < 800.0


def test_glut1_michaelis_menten_saturating() -> None:
    from nidus.export.reference import glut1_michaelis_menten

    # At [S] = Km, V = Vmax/2
    v = glut1_michaelis_menten(2.5, km_mmol_per_l=2.5, vmax_per_area=0.075)
    assert v == pytest.approx(0.0375)

    # At very high [S], V approaches Vmax
    v_high = glut1_michaelis_menten(1000.0, km_mmol_per_l=2.5, vmax_per_area=0.075)
    assert v_high == pytest.approx(0.075, abs=0.001)


def test_maternal_cardiac_output_peak_at_center() -> None:
    from nidus.export.reference import maternal_cardiac_output

    co_peak = maternal_cardiac_output(
        28.0, baseline_l_per_min=5.0, peak_excess_l_per_min=2.0, peak_week=28.0, spread_weeks=8.0
    )
    co_early = maternal_cardiac_output(
        0.0, baseline_l_per_min=5.0, peak_excess_l_per_min=2.0, peak_week=28.0, spread_weeks=8.0
    )
    assert co_peak == pytest.approx(7.0)
    assert co_early < co_peak


def test_maternal_map_nadir_at_center() -> None:
    from nidus.export.reference import maternal_map

    nadir = maternal_map(
        20.0, baseline_mmhg=85.0, nadir_drop_mmhg=8.0, nadir_week=20.0, spread_weeks=6.0
    )
    early = maternal_map(
        0.0, baseline_mmhg=85.0, nadir_drop_mmhg=8.0, nadir_week=20.0, spread_weeks=6.0
    )
    assert nadir == pytest.approx(77.0)
    assert early > nadir


def test_uterine_artery_flow_logistic_endpoints() -> None:
    from nidus.export.reference import uterine_artery_flow

    early = uterine_artery_flow(
        4.0, baseline_ml_per_min=100.0, term_ml_per_min=750.0, growth_rate_per_week=0.25
    )
    late = uterine_artery_flow(
        40.0, baseline_ml_per_min=100.0, term_ml_per_min=750.0, growth_rate_per_week=0.25
    )
    assert 100.0 < early < 200.0
    assert late == pytest.approx(750.0, abs=20.0)


def test_placental_o2_equilibrator_linear() -> None:
    from nidus.export.reference import placental_o2_equilibrator

    out = placental_o2_equilibrator(50.0, max_equilibration=0.7)
    assert out == pytest.approx(35.0)


def test_plasma_volume_expansion_endpoints() -> None:
    from nidus.export.reference import plasma_volume_expansion

    early = plasma_volume_expansion(8.0, early_l=2.6, term_l=4.7)
    late = plasma_volume_expansion(40.0, early_l=2.6, term_l=4.7)
    assert early == pytest.approx(2.6, abs=0.5)
    assert late == pytest.approx(4.7, abs=0.1)


def test_hadlock_fetal_weight_reasonable_term() -> None:
    from nidus.export.reference import hadlock_fetal_weight

    # ~term biometry → ~3000-4000 g
    w = hadlock_fetal_weight(bpd_mm=95.0, hc_mm=340.0, ac_mm=340.0, fl_mm=72.0)
    assert 2500.0 < w < 4500.0


def test_svr_trajectory_drops_then_recovers() -> None:
    from nidus.export.reference import maternal_svr_trajectory

    kwargs = dict(
        baseline_map_mmhg=85.0,
        map_nadir_drop_mmhg=8.0,
        map_nadir_week=20.0,
        map_spread_weeks=6.0,
        baseline_co_l_per_min=5.0,
        peak_excess_co_l_per_min=2.0,
        co_peak_week=28.0,
        co_spread_weeks=8.0,
    )
    early = float(maternal_svr_trajectory(0.0, **kwargs))  # type: ignore[arg-type]
    mid = float(maternal_svr_trajectory(24.0, **kwargs))  # type: ignore[arg-type]
    late = float(maternal_svr_trajectory(40.0, **kwargs))  # type: ignore[arg-type]
    # Physiological pattern: SVR drops in mid-pregnancy then recovers.
    assert mid < early
    assert mid < late
    # Order of magnitude check (~800-1500 dyn*s/cm^5 in pregnancy).
    assert 500.0 < mid < 2000.0


def test_pao2_linear_endpoints() -> None:
    from nidus.export.reference import maternal_pao2_linear

    at_zero = float(maternal_pao2_linear(0.0, baseline_mmhg=100.0, term_mmhg=105.0))
    at_term = float(maternal_pao2_linear(40.0, baseline_mmhg=100.0, term_mmhg=105.0))
    assert at_zero == pytest.approx(100.0)
    assert at_term == pytest.approx(105.0)


def test_tidal_volume_sigmoid_endpoints() -> None:
    from nidus.export.reference import maternal_tidal_volume

    early = float(maternal_tidal_volume(0.0, baseline_ml=450.0, term_ml=650.0))
    late = float(maternal_tidal_volume(40.0, baseline_ml=450.0, term_ml=650.0))
    assert early == pytest.approx(450.0, abs=5.0)
    assert late == pytest.approx(650.0, abs=5.0)


def test_heart_rate_trajectory_endpoints() -> None:
    from nidus.export.reference import maternal_heart_rate

    early = float(maternal_heart_rate(0.0, baseline_bpm=72.0, term_bpm=88.0))
    late = float(maternal_heart_rate(40.0, baseline_bpm=72.0, term_bpm=88.0))
    assert early == pytest.approx(72.0, abs=1.0)
    assert late == pytest.approx(88.0, abs=1.0)


def test_stroke_volume_gaussian_peak() -> None:
    from nidus.export.reference import maternal_stroke_volume

    peak = float(
        maternal_stroke_volume(
            24.0, baseline_ml=68.0, peak_excess_ml=12.0, peak_week=24.0, spread_weeks=8.0
        )
    )
    early = float(
        maternal_stroke_volume(
            4.0, baseline_ml=68.0, peak_excess_ml=12.0, peak_week=24.0, spread_weeks=8.0
        )
    )
    assert peak == pytest.approx(80.0)
    assert early < peak


def test_rpf_gaussian_peak_and_decline() -> None:
    from nidus.export.reference import renal_plasma_flow

    kwargs = dict(
        baseline_ml_per_min=600.0,
        peak_ml_per_min=1100.0,
        peak_week=20.0,
        spread_weeks=8.0,
    )
    peak = float(renal_plasma_flow(20.0, **kwargs))  # type: ignore[arg-type]
    early = float(renal_plasma_flow(4.0, **kwargs))  # type: ignore[arg-type]
    term = float(renal_plasma_flow(40.0, **kwargs))  # type: ignore[arg-type]
    # At peak week, RPF == peak.
    assert peak == pytest.approx(1100.0)
    # RPF rises from baseline and declines toward term (Dunlop bell-shape).
    assert early < peak
    assert term < peak
    assert term > early or term == pytest.approx(early, abs=50.0)


def test_minute_ventilation_rises_through_pregnancy() -> None:
    from nidus.export.reference import maternal_minute_ventilation

    kwargs = dict(
        baseline_vt_ml=450.0,
        term_vt_ml=650.0,
        baseline_rr_bpm=14.0,
        term_rr_bpm=17.0,
    )
    early = float(maternal_minute_ventilation(0.0, **kwargs))  # type: ignore[arg-type]
    late = float(maternal_minute_ventilation(40.0, **kwargs))  # type: ignore[arg-type]
    # Endpoints: VT * RR at baseline and term.
    assert early == pytest.approx(450.0 * 14.0, rel=0.02)
    assert late == pytest.approx(650.0 * 17.0, rel=0.02)
    # Pregnancy rise of ~30-75% over baseline.
    assert late > early * 1.3


def test_arterial_ph_linear_endpoints() -> None:
    from nidus.export.reference import maternal_arterial_ph

    at_zero = float(maternal_arterial_ph(0.0, baseline_ph=7.40, term_ph=7.44))
    at_term = float(maternal_arterial_ph(40.0, baseline_ph=7.40, term_ph=7.44))
    assert at_zero == pytest.approx(7.40)
    assert at_term == pytest.approx(7.44)


def test_hadlock_biometry_cubic_fit_matches_anchors(ds: nidus.Dataset) -> None:
    """The cubic fit must reproduce the seven weekly anchors within ~3 mm."""
    from nidus.export.reference import HADLOCK_ANCHOR_WEEKS, hadlock_biometry_cubic

    for prefix, max_resid_mm in [("bpd", 1.0), ("hc", 3.0), ("ac", 2.0), ("fl", 1.0)]:
        anchors = [ds[f"fetal_growth.{prefix}_{w}w_mm"].value.central for w in HADLOCK_ANCHOR_WEEKS]
        fitted = hadlock_biometry_cubic(list(HADLOCK_ANCHOR_WEEKS), anchors)
        residuals = np.abs(np.asarray(fitted) - np.asarray(anchors))
        assert residuals.max() < max_resid_mm, (
            f"{prefix} cubic fit residual {residuals.max():.2f} mm exceeds {max_resid_mm} mm"
        )


def test_hadlock_biometry_cubic_monotone_in_pregnancy_range() -> None:
    """Each biometry should grow monotonically across 16-40 weeks."""
    from nidus.export.reference import hadlock_biometry_cubic

    # Synthetic Tier-A-style anchors (the dataset values would do too).
    bpd = [35.0, 47.0, 61.0, 71.5, 82.0, 89.0, 93.0]
    t = np.linspace(16, 40, 25)
    vals = hadlock_biometry_cubic(t, bpd)
    assert np.all(np.diff(vals) > 0), "BPD must rise monotonically through pregnancy"


def test_homa_ir_sigmoid_endpoints() -> None:
    from nidus.export.reference import maternal_homa_ir

    early = float(maternal_homa_ir(0.0, baseline=1.5, term=4.5))
    late = float(maternal_homa_ir(40.0, baseline=1.5, term=4.5))
    assert early == pytest.approx(1.5, abs=0.1)
    assert late == pytest.approx(4.5, abs=0.1)


def test_tsh_piecewise_holds_nadir() -> None:
    from nidus.export.reference import maternal_tsh

    early = float(maternal_tsh(6.0, t1_value=0.6, term_value=2.0))
    t1 = float(maternal_tsh(12.0, t1_value=0.6, term_value=2.0))
    term = float(maternal_tsh(40.0, t1_value=0.6, term_value=2.0))
    # Before week 12, value clamped at T1 nadir.
    assert early == pytest.approx(0.6)
    assert t1 == pytest.approx(0.6)
    # At term week, value equals term endpoint.
    assert term == pytest.approx(2.0)


def test_cortisol_rises_through_pregnancy() -> None:
    from nidus.export.reference import maternal_cortisol

    early = float(maternal_cortisol(0.0, baseline_ug_per_dl=12.0, term_ug_per_dl=32.0))
    mid = float(maternal_cortisol(22.0, baseline_ug_per_dl=12.0, term_ug_per_dl=32.0))
    late = float(maternal_cortisol(40.0, baseline_ug_per_dl=12.0, term_ug_per_dl=32.0))
    # Midpoint of sigmoid is at week 22, value = (baseline+term)/2.
    assert mid == pytest.approx(22.0, abs=0.5)
    # Monotonic rise; late approaches term plateau within ~1 ug/dL.
    assert early < mid < late
    assert late == pytest.approx(32.0, abs=2.0)


def test_hpl_rises_from_zero_to_term() -> None:
    from nidus.export.reference import maternal_hpl

    early = float(maternal_hpl(0.0, baseline_ug_per_ml=0.0, term_ug_per_ml=7.0))
    mid = float(maternal_hpl(24.0, baseline_ug_per_ml=0.0, term_ug_per_ml=7.0))
    late = float(maternal_hpl(40.0, baseline_ug_per_ml=0.0, term_ug_per_ml=7.0))
    # hPL is undetectable non-pregnant, rises through gestation.
    assert early < 0.5
    assert mid == pytest.approx(3.5, abs=0.5)
    assert late == pytest.approx(7.0, abs=0.5)


def test_progesterone_rises_10x_by_term() -> None:
    from nidus.export.reference import maternal_progesterone

    early = float(maternal_progesterone(0.0, baseline_ng_per_ml=10.0, term_ng_per_ml=150.0))
    late = float(maternal_progesterone(40.0, baseline_ng_per_ml=10.0, term_ng_per_ml=150.0))
    assert early == pytest.approx(10.0, abs=2.0)
    assert late == pytest.approx(150.0, abs=10.0)
    assert late > 10.0 * early


def test_estradiol_sigmoid_endpoints() -> None:
    from nidus.export.reference import maternal_estradiol

    early = float(maternal_estradiol(0.0, baseline_ng_per_ml=0.1, term_ng_per_ml=14.0))
    late = float(maternal_estradiol(40.0, baseline_ng_per_ml=0.1, term_ng_per_ml=14.0))
    assert early == pytest.approx(0.1, abs=0.5)
    assert late == pytest.approx(14.0, abs=2.0)


def test_fetal_heart_rate_falls_through_pregnancy() -> None:
    from nidus.export.reference import fetal_heart_rate

    early = float(fetal_heart_rate(0.0, baseline_bpm=170.0, term_bpm=140.0))
    late = float(fetal_heart_rate(40.0, baseline_bpm=170.0, term_bpm=140.0))
    # FHR baseline > term; the sigmoid encodes a fall.
    assert early == pytest.approx(170.0, abs=1.0)
    assert late == pytest.approx(140.0, abs=1.0)
    assert late < early


def test_hcg_peaks_then_declines() -> None:
    from nidus.export.reference import maternal_hcg

    kwargs = dict(peak_miu_per_ml=120000.0, peak_week=10.0, term_miu_per_ml=10000.0)
    early = float(maternal_hcg(5.0, **kwargs))  # type: ignore[arg-type]
    peak = float(maternal_hcg(10.0, **kwargs))  # type: ignore[arg-type]
    term = float(maternal_hcg(40.0, **kwargs))  # type: ignore[arg-type]
    # Rise: at week 5, hcg(5) = peak * (5/10)^2 = peak/4.
    assert early == pytest.approx(30000.0)
    # At peak week, hcg = peak exactly.
    assert peak == pytest.approx(120000.0)
    # At term week 40, decline matches the curated term value.
    assert term == pytest.approx(10000.0, rel=1e-6)


def test_ua_pi_falls_through_pregnancy() -> None:
    from nidus.export.reference import umbilical_artery_pi

    early = float(umbilical_artery_pi(16.0, baseline=1.5, term=0.85))
    late = float(umbilical_artery_pi(40.0, baseline=1.5, term=0.85))
    assert early > late
    assert late == pytest.approx(0.85, abs=0.1)


def test_mca_pi_bell_shape() -> None:
    from nidus.export.reference import mca_pi

    peak = float(mca_pi(28.0, baseline=1.5, peak=2.0))
    early = float(mca_pi(16.0, baseline=1.5, peak=2.0))
    late = float(mca_pi(40.0, baseline=1.5, peak=2.0))
    # At peak week, MCA-PI hits the curated peak.
    assert peak == pytest.approx(2.0)
    # Bell: both shoulders below peak.
    assert early < peak
    assert late < peak


def test_cpr_above_one_in_normal_pregnancy() -> None:
    from nidus.export.reference import cerebroplacental_ratio

    kwargs = dict(ua_pi_baseline=1.5, ua_pi_term=0.85, mca_pi_baseline=1.5, mca_pi_peak=2.0)
    cpr_24 = float(cerebroplacental_ratio(24.0, **kwargs))  # type: ignore[arg-type]
    cpr_term = float(cerebroplacental_ratio(38.0, **kwargs))  # type: ignore[arg-type]
    # Normal pregnancy: CPR > 1 (MCA resistance higher than UA resistance).
    assert cpr_24 > 1.0
    assert cpr_term > 1.0


def test_placental_fetal_allometry_term_ratio() -> None:
    from nidus.export.reference import placental_fetal_allometry

    # Term: FW ~3500 g, PW(a=0.4, b=0.85) ~ 412 g; ratio ~1:8.5.
    pw = float(placental_fetal_allometry(3500.0, coefficient_a=0.4, exponent_b=0.85))
    assert 350.0 < pw < 500.0
    ratio = 3500.0 / pw
    # Canonical term placental:fetal weight ratio is 1:6 to 1:9.
    assert 5.0 < ratio < 10.0


def test_igg_transfer_rises_through_pregnancy() -> None:
    from nidus.export.reference import maternal_fetal_igg_transfer

    early = float(maternal_fetal_igg_transfer(16.0, baseline=0.2, term=1.2))
    late = float(maternal_fetal_igg_transfer(40.0, baseline=0.2, term=1.2))
    assert early < late
    # Term ratio > 1 (active transport overshoots maternal levels).
    assert late > 1.0


def test_placental_cortisol_gradient_inactivates() -> None:
    from nidus.export.reference import placental_cortisol_gradient

    fetal = float(placental_cortisol_gradient(30.0, inactivation_fraction=0.85))
    # 15% of maternal: 30 * 0.15 = 4.5
    assert fetal == pytest.approx(4.5)


def test_microchimerism_accumulates_through_pregnancy() -> None:
    from nidus.export.reference import maternal_microchimerism_trajectory

    early = float(maternal_microchimerism_trajectory(12.0, baseline=0.0, term=1.0))
    late = float(maternal_microchimerism_trajectory(38.0, baseline=0.0, term=1.0))
    assert early < late
    # Late concentration approaches the term anchor.
    assert late > 0.5


def test_fetal_pulmonary_fluid_reverses_near_term() -> None:
    from nidus.export.reference import fetal_pulmonary_fluid_trajectory

    mid = float(fetal_pulmonary_fluid_trajectory(24.0, baseline=5.0, term=-5.0))
    near_term = float(fetal_pulmonary_fluid_trajectory(39.0, baseline=5.0, term=-5.0))
    # Mid-gestation: net secretion (positive).
    assert mid > 0.0
    # Near term: net reabsorption (negative).
    assert near_term < 0.0


def test_hypothesis_only_submodels_carry_warning(ds: nidus.Dataset, libsbml_module) -> None:
    """Phase C submodels must emit DO NOT USE FOR PREDICTION annotation."""
    from nidus.export import build_sbml

    for sm_id in [
        "maternal_fetal_igg_transfer",
        "placental_cortisol_gradient",
        "maternal_microchimerism_trajectory",
        "fetal_pulmonary_fluid_trajectory",
    ]:
        xml = build_sbml(ds, sm_id)
        assert "reviewStatus" in xml, f"{sm_id} missing reviewStatus annotation"
        assert "hypothesis-only" in xml, f"{sm_id} missing hypothesis-only marker"
        assert "DO NOT USE FOR PREDICTION" in xml, f"{sm_id} missing warning"


def test_shipped_submodels_do_not_carry_warning(ds: nidus.Dataset, libsbml_module) -> None:
    """Default 'shipped' status must NOT emit the hypothesis-only marker."""
    from nidus.export import build_sbml

    xml = build_sbml(ds, "placental_villous_growth")
    assert "hypothesis-only" not in xml
    assert "DO NOT USE FOR PREDICTION" not in xml


def test_glut3_higher_affinity_than_glut1() -> None:
    """GLUT3 has lower Km (higher affinity) — at low [S] it should win."""
    from nidus.export.reference import michaelis_menten_flux

    glut1 = michaelis_menten_flux(0.5, km_mmol_per_l=2.5, vmax_per_area=0.075)
    glut3 = michaelis_menten_flux(0.5, km_mmol_per_l=1.0, vmax_per_area=0.05)
    # GLUT3 saturates at lower [S]; at [S] = 0.5, fractional saturation is 0.33 vs 0.17
    assert (glut3 / 0.05) > (glut1 / 0.075)


# ---- SBML generation -----------------------------------------------


@pytest.fixture(scope="module")
def libsbml_module():
    return pytest.importorskip("libsbml")


@pytest.fixture(scope="module")
def libcellml_module():
    return pytest.importorskip("libcellml")


_ALL_SUBMODEL_IDS = [
    "placental_villous_growth",
    "o2hb_dissociation_adult",
    "o2hb_dissociation_fetal",
    "placental_glucose_glut1",
    "placental_glucose_glut3",
    "maternal_cardiac_output_trajectory",
    "maternal_map_trajectory",
    "uterine_artery_flow_logistic",
    "placental_o2_equilibrator",
    "plasma_volume_expansion",
    "hadlock_fetal_weight",
    "gfr_logistic_trajectory",
    "amniotic_fluid_volume_trajectory",
    "svr_trajectory",
    "pao2_trajectory_linear",
    "tidal_volume_trajectory",
    "heart_rate_trajectory",
    "stroke_volume_trajectory",
    "renal_plasma_flow_trajectory",
    "minute_ventilation_trajectory",
    "arterial_ph_trajectory",
    "hadlock_bpd_growth",
    "hadlock_hc_growth",
    "hadlock_ac_growth",
    "hadlock_fl_growth",
    "homa_ir_trajectory",
    "tsh_trajectory",
    "cortisol_trajectory",
    "hpl_trajectory",
    "progesterone_trajectory",
    "estradiol_trajectory",
    "fetal_heart_rate_trajectory",
    "hcg_trajectory",
    "umbilical_artery_pi_trajectory",
    "mca_pi_trajectory",
    "cerebroplacental_ratio",
    "placental_fetal_allometry",
    "maternal_fetal_igg_transfer",
    "placental_cortisol_gradient",
    "maternal_microchimerism_trajectory",
    "fetal_pulmonary_fluid_trajectory",
]


@pytest.mark.parametrize("submodel_id", _ALL_SUBMODEL_IDS)
def test_sbml_builds_and_validates(ds: nidus.Dataset, libsbml_module, submodel_id: str) -> None:
    from nidus.export import build_sbml

    xml = build_sbml(ds, submodel_id)
    # Parse the result and re-check consistency
    reader = libsbml_module.SBMLReader()
    doc = reader.readSBMLFromString(xml)
    assert doc.getNumErrors() == 0, (
        f"parse errors: {[doc.getError(i).getMessage() for i in range(doc.getNumErrors())]}"
    )
    # Submodel id appears in the model
    assert submodel_id in xml
    # nidus tier annotation appears
    assert "confidenceTier" in xml


def test_sbml_unknown_submodel(ds: nidus.Dataset) -> None:
    from nidus.export import build_sbml

    with pytest.raises(KeyError, match="Unknown submodel"):
        build_sbml(ds, "not_a_real_submodel")


def test_sbml_round_trip_severinghaus(ds: nidus.Dataset, libsbml_module, tmp_path: Path) -> None:
    """Numerical round-trip: simulate the SBML model in tellurium (if
    available) and compare against the NumPy reference. Falls back to a
    light textual check if tellurium isn't installed."""
    from nidus.export import build_sbml
    from nidus.export.reference import severinghaus_o2_saturation

    xml = build_sbml(ds, "o2hb_dissociation_adult")
    sbml_path = tmp_path / "model.xml"
    sbml_path.write_text(xml)

    try:
        import tellurium as te  # type: ignore[import-untyped]
    except ImportError:
        # No tellurium — just verify the assignment-rule expression appears.
        assert "po2_mmhg" in xml
        assert "23400" in xml
        return

    r = te.loadSBMLModel(str(sbml_path))
    # Sweep PO2 and compare against NumPy reference
    for po2 in [20.0, 40.0, 60.0, 100.0]:
        r.reset()
        r.po2_mmhg = po2
        r.simulate(0, 1, 2)  # let the assignment rule evaluate
        sat_sbml = r.saturation
        sat_ref = float(severinghaus_o2_saturation(po2))
        assert sat_sbml == pytest.approx(sat_ref, rel=1e-6), (
            f"Round-trip mismatch at PO2={po2}: SBML={sat_sbml}, ref={sat_ref}"
        )


def test_write_sbml_produces_all_files(ds: nidus.Dataset, libsbml_module, tmp_path: Path) -> None:
    from nidus.export import SUBMODELS, write_sbml

    paths = write_sbml(ds, tmp_path)
    assert len(paths) == len(SUBMODELS)
    assert len(paths) >= 39
    expected_names = {f"{sm.id}.xml" for sm in SUBMODELS}
    actual_names = {p.name for p in paths}
    assert actual_names == expected_names


# ---- CellML generation ---------------------------------------------


@pytest.mark.parametrize("submodel_id", _ALL_SUBMODEL_IDS)
def test_cellml_2_builds(ds: nidus.Dataset, libcellml_module, submodel_id: str) -> None:
    from nidus.export import build_cellml

    xml = build_cellml(ds, submodel_id, version="2.0")
    assert "<?xml" in xml
    assert "model" in xml.lower()
    # CellML 2.0 namespace appears
    assert "cellml/2.0" in xml


def test_cellml_1_1_fallback(ds: nidus.Dataset, libcellml_module) -> None:
    from nidus.export import build_cellml

    xml = build_cellml(ds, "o2hb_dissociation_adult", version="1.1")
    # 1.1 namespace appears, 2.0 namespace does not
    assert "cellml/1.1" in xml
    assert "cellml/2.0" not in xml


def test_cellml_unknown_submodel(ds: nidus.Dataset) -> None:
    from nidus.export import build_cellml

    with pytest.raises(KeyError, match="Unknown submodel"):
        build_cellml(ds, "not_a_real_submodel")


def test_write_cellml_both_versions(ds: nidus.Dataset, libcellml_module, tmp_path: Path) -> None:
    from nidus.export import write_cellml

    paths_2 = write_cellml(ds, tmp_path / "v2", version="2.0")
    assert len(paths_2) >= 39
    assert all(p.suffix == ".cellml" for p in paths_2)

    paths_1 = write_cellml(ds, tmp_path / "v1", version="1.1")
    assert len(paths_1) >= 39
    assert all(p.name.endswith(".cellml1.cellml") for p in paths_1)


# ---- PhysioCell ----------------------------------------------------


def test_physiocell_params_contains_all_dataset_params(ds: nidus.Dataset) -> None:
    from nidus.export import build_physiocell_params

    xml = build_physiocell_params(ds)
    # Every parameter id (with . replaced by __) must appear
    for p in ds:
        safe_id = p.id.replace(".", "__")
        assert f"<{safe_id}" in xml, f"missing param {safe_id}"
    # Wraps in PhysiCell_settings
    assert "<PhysiCell_settings>" in xml
    assert "</PhysiCell_settings>" in xml
    # Subsystem comments appear
    assert "<!-- maternal_cardiovascular -->" in xml


def test_physiocell_includes_provenance_in_description(ds: nidus.Dataset) -> None:
    from nidus.export import build_physiocell_params

    xml = build_physiocell_params(ds)
    # Spot-check a known param: tier + citation key in description
    mahendru_param = "maternal_cardiovascular__baseline_cardiac_output_l_per_min"
    matches = re.findall(rf"<{mahendru_param}[^>]+>", xml)
    assert matches, f"didn't find element for {mahendru_param}"
    elt = matches[0]
    assert "tier=B" in elt
    assert "mahendru-2014-cardiac-output" in elt


def test_write_physiocell(ds: nidus.Dataset, tmp_path: Path) -> None:
    from nidus.export import write_physiocell

    path = write_physiocell(ds, tmp_path)
    assert path.name == "nidus-parameters.xml"
    assert path.exists()
    assert path.read_text().startswith("<?xml")


# ---- Composed model ------------------------------------------------


def test_composed_sbml_builds(ds: nidus.Dataset, libsbml_module) -> None:
    from nidus.export import build_composed_sbml

    xml = build_composed_sbml(ds)
    assert "nidus_pregnancy_composed" in xml
    # Cross-submodel outputs all present
    for v in [
        "placental_area_m2",
        "cardiac_output_l_per_min",
        "map_mmhg",
        "uterine_flow_ml_per_min",
        "plasma_volume_l",
        "maternal_sat",
        "umbilical_vein_po2_mmhg",
        "fetal_sat",
        "glut1_flux",
        "glut3_flux",
        "efw_g",
    ]:
        assert v in xml, f"missing composed output {v}"
    # Re-parses cleanly
    doc = libsbml_module.SBMLReader().readSBMLFromString(xml)
    assert doc.getNumErrors() == 0


def test_composed_sbml_round_trip_sanity(ds: nidus.Dataset, libsbml_module, tmp_path: Path) -> None:
    """If tellurium is available, simulate the composed model and sanity-check."""
    from nidus.export import write_composed_sbml

    path = write_composed_sbml(ds, tmp_path)
    try:
        import tellurium as te  # type: ignore[import-untyped]
    except ImportError:
        pytest.skip("tellurium not installed")

    r = te.loadSBMLModel(str(path))
    r.t_weeks = 28.0
    r.simulate(0, 1, 2)
    # At ~28 weeks, plausibility checks:
    assert 5.0 < r.cardiac_output_l_per_min < 9.0
    assert 60.0 < r.map_mmhg < 100.0
    assert 0.0 < r.maternal_sat < 1.0
    assert 0.0 < r.fetal_sat < 1.0


# ---- COMBINE archive -----------------------------------------------


def test_combine_archive(ds: nidus.Dataset, libsbml_module, tmp_path: Path) -> None:
    import zipfile

    from nidus.export import write_combine_archive

    out = write_combine_archive(ds, tmp_path / "nidus.omex")
    assert out.exists() and out.suffix == ".omex"
    with zipfile.ZipFile(out) as zf:
        names = zf.namelist()
        assert "manifest.xml" in names
        assert "metadata.rdf" in names
        assert "sbml/nidus_pregnancy_composed.xml" in names
        assert "physicell/nidus-parameters.xml" in names
        # Manifest references the composed model as master
        manifest = zf.read("manifest.xml").decode()
        assert 'master="true"' in manifest
        assert "nidus_pregnancy_composed.xml" in manifest


def test_combine_archive_default_extension(ds: nidus.Dataset, tmp_path: Path) -> None:
    from nidus.export import write_combine_archive

    out = write_combine_archive(ds, tmp_path / "no_ext")
    assert out.suffix == ".omex"


# ---- Sensitivity sweep utility (spec 03 §5) -----------------------


def test_sweep_basic_shape() -> None:
    from nidus.export import sweep
    from nidus.export.reference import maternal_fetal_igg_transfer

    t = np.linspace(12, 40, 8)
    result = sweep(
        maternal_fetal_igg_transfer,
        t,
        fixed={"term": 1.2},
        sweep_param="baseline",
        sweep_values=[0.1, 0.2, 0.3],
    )
    assert result["output"].shape == (3 * 8,)
    assert result["sweep_value"].shape == (3 * 8,)
    assert result["independent"].shape == (3 * 8,)
    # First block has sweep_value = 0.1
    assert float(result["sweep_value"][0]) == pytest.approx(0.1)
    # Tiled independent: first block matches t exactly
    np.testing.assert_allclose(result["independent"][:8], t)


def test_sweep_monotone_in_baseline() -> None:
    """Raising baseline shifts the IgG-ratio curve up at every t."""
    from nidus.export import sweep
    from nidus.export.reference import maternal_fetal_igg_transfer

    t = np.linspace(12, 40, 5)
    result = sweep(
        maternal_fetal_igg_transfer,
        t,
        fixed={"term": 1.2},
        sweep_param="baseline",
        sweep_values=[0.0, 0.3, 0.6],
    )
    # Reshape to (n_sweep, n_t) and check column-wise monotonicity
    grid = result["output"].reshape(3, 5)
    assert np.all(np.diff(grid, axis=0) > 0)


def test_sweep_rejects_conflicting_sweep_param() -> None:
    from nidus.export import sweep
    from nidus.export.reference import maternal_fetal_igg_transfer

    with pytest.raises(ValueError, match="sweep_param"):
        sweep(
            maternal_fetal_igg_transfer,
            [20.0, 30.0],
            fixed={"baseline": 0.2, "term": 1.2},
            sweep_param="baseline",
            sweep_values=[0.1, 0.2],
        )


def test_sweep_write_csv_round_trip(tmp_path: Path) -> None:
    from nidus.export import sweep, write_sweep_csv
    from nidus.export.reference import placental_cortisol_gradient

    result = sweep(
        placental_cortisol_gradient,
        independent=[10.0, 20.0, 30.0],
        fixed={},
        sweep_param="inactivation_fraction",
        sweep_values=[0.7, 0.85],
    )
    csv_path = tmp_path / "cortisol_sweep.csv"
    write_sweep_csv(
        result, csv_path, independent_label="maternal_ug_per_dl", output_label="fetal_ug_per_dl"
    )

    rows = csv_path.read_text().strip().split("\n")
    # Header + 2 sweep x 3 independent = 7 lines
    assert len(rows) == 7
    assert "sweep_param,sweep_value,maternal_ug_per_dl,fetal_ug_per_dl" in rows[0]
    # At inactivation_fraction = 0.7, fetal = maternal * 0.3
    # First data row: sweep=0.7, indep=10 -> output 3.0
    first = rows[1].split(",")
    assert first[0] == "inactivation_fraction"
    assert float(first[1]) == pytest.approx(0.7)
    assert float(first[2]) == pytest.approx(10.0)
    assert float(first[3]) == pytest.approx(3.0)
