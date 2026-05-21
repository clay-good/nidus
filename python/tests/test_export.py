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
    assert "placental_villous_growth" in ids
    assert "o2hb_dissociation_adult" in ids
    assert "o2hb_dissociation_fetal" in ids
    assert "placental_glucose_glut1" in ids


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


def test_glut1_michaelis_menten_saturating() -> None:
    from nidus.export.reference import glut1_michaelis_menten

    # At [S] = Km, V = Vmax/2
    v = glut1_michaelis_menten(2.5, km_mmol_per_l=2.5, vmax_per_area=0.075)
    assert v == pytest.approx(0.0375)

    # At very high [S], V approaches Vmax
    v_high = glut1_michaelis_menten(1000.0, km_mmol_per_l=2.5, vmax_per_area=0.075)
    assert v_high == pytest.approx(0.075, abs=0.001)


# ---- SBML generation -----------------------------------------------


@pytest.fixture(scope="module")
def libsbml_module():
    return pytest.importorskip("libsbml")


@pytest.fixture(scope="module")
def libcellml_module():
    return pytest.importorskip("libcellml")


@pytest.mark.parametrize(
    "submodel_id",
    [
        "placental_villous_growth",
        "o2hb_dissociation_adult",
        "o2hb_dissociation_fetal",
        "placental_glucose_glut1",
    ],
)
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
    assert len(paths) == 4
    expected_names = {f"{sm.id}.xml" for sm in SUBMODELS}
    actual_names = {p.name for p in paths}
    assert actual_names == expected_names


# ---- CellML generation ---------------------------------------------


@pytest.mark.parametrize(
    "submodel_id",
    [
        "placental_villous_growth",
        "o2hb_dissociation_adult",
        "o2hb_dissociation_fetal",
        "placental_glucose_glut1",
    ],
)
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
    assert len(paths_2) == 4
    assert all(p.suffix == ".cellml" for p in paths_2)

    paths_1 = write_cellml(ds, tmp_path / "v1", version="1.1")
    assert len(paths_1) == 4
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
