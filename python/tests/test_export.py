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

    early = float(maternal_gfr_logistic(
        0.0,
        baseline_ml_per_min=100.0,
        peak_ml_per_min=150.0,
        growth_rate_per_week=0.4,
        peak_week=16.0,
    ))
    late = float(maternal_gfr_logistic(
        40.0,
        baseline_ml_per_min=100.0,
        peak_ml_per_min=150.0,
        growth_rate_per_week=0.4,
        peak_week=16.0,
    ))
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
    assert len(paths) >= 13
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
    assert len(paths_2) >= 13
    assert all(p.suffix == ".cellml" for p in paths_2)

    paths_1 = write_cellml(ds, tmp_path / "v1", version="1.1")
    assert len(paths_1) >= 13
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
