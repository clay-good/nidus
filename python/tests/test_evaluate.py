"""Tests for ``nidus.export.evaluate``."""

from __future__ import annotations

import numpy as np
import pytest

import nidus
from nidus.export import (
    SUBMODELS,
    UNSUPPORTED_REASON,
    Domain,
    evaluate_submodel,
    submodel_domain,
    supported_submodels,
)


@pytest.fixture(scope="module")
def ds() -> nidus.Dataset:
    return nidus.load()


def test_supported_submodels_nonempty() -> None:
    ids = supported_submodels()
    assert len(ids) >= 30
    # Every id is a real registered submodel
    known = {s.id for s in SUBMODELS}
    for sid in ids:
        assert sid in known


def test_supported_and_unsupported_partition_the_registry() -> None:
    supported = set(supported_submodels())
    unsupported = set(UNSUPPORTED_REASON)
    all_ids = {s.id for s in SUBMODELS}
    # No overlap
    assert supported.isdisjoint(unsupported)
    # Every submodel is in one bucket or the other
    assert (supported | unsupported) == all_ids


@pytest.mark.parametrize("submodel_id", supported_submodels())
def test_evaluate_each_supported_submodel(submodel_id: str, ds: nidus.Dataset) -> None:
    domain = submodel_domain(submodel_id)
    x = np.linspace(domain.default_range[0], domain.default_range[1], 10)
    y = evaluate_submodel(ds, submodel_id, x)
    assert y.shape == (10,)
    assert np.all(np.isfinite(y))


@pytest.mark.parametrize("submodel_id", supported_submodels())
def test_submodel_domain_well_formed(submodel_id: str) -> None:
    d = submodel_domain(submodel_id)
    assert isinstance(d, Domain)
    assert d.default_range[0] < d.default_range[1]
    assert d.name and d.label and d.units


def test_evaluate_unknown_submodel_raises(ds: nidus.Dataset) -> None:
    with pytest.raises(KeyError, match="unknown submodel id"):
        evaluate_submodel(ds, "no_such_submodel", [10, 20])


def test_evaluate_unsupported_submodel_raises(ds: nidus.Dataset) -> None:
    # hadlock_fetal_weight: multivariate (BPD, HC, AC, FL), not a 1-D trajectory
    with pytest.raises(ValueError, match="not supported"):
        evaluate_submodel(ds, "hadlock_fetal_weight", [10, 20])


def test_hadlock_biometry_cubic_fit_tracks_anchors_within_tolerance(
    ds: nidus.Dataset,
) -> None:
    """The cubic fit through 7 anchors stays close to each anchor value."""
    for sm_id, prefix in [
        ("hadlock_bpd_growth", "bpd"),
        ("hadlock_hc_growth", "hc"),
        ("hadlock_ac_growth", "ac"),
        ("hadlock_fl_growth", "fl"),
    ]:
        weeks = np.array([16.0, 20.0, 24.0, 28.0, 32.0, 36.0, 40.0])
        fitted = evaluate_submodel(ds, sm_id, weeks)
        anchors = np.array(
            [
                ds[f"fetal_growth.{prefix}_{w}w_mm"].value.central
                for w in (16, 20, 24, 28, 32, 36, 40)
            ]
        )
        # Cubic least-squares fit through 7 points — within ~3% of each anchor
        rel_err = np.abs(fitted - anchors) / anchors
        assert np.all(rel_err < 0.05), (
            f"{sm_id}: max rel err {rel_err.max():.3%} exceeds 5% tolerance"
        )


def test_hadlock_biometry_overrides_a_single_anchor(ds: nidus.Dataset) -> None:
    """Sensitivity sweep on a single anchor lifts the fit near that week."""
    weeks = np.array([28.0])
    baseline = evaluate_submodel(ds, "hadlock_bpd_growth", weeks)[0]
    bumped = evaluate_submodel(
        ds,
        "hadlock_bpd_growth",
        weeks,
        overrides={"a28": baseline + 20.0},
    )[0]
    assert bumped > baseline


def test_evaluate_overrides_replace_a_single_kwarg(ds: nidus.Dataset) -> None:
    t = np.array([20.0, 40.0])
    baseline = evaluate_submodel(ds, "maternal_cardiac_output_trajectory", t)
    bumped = evaluate_submodel(
        ds,
        "maternal_cardiac_output_trajectory",
        t,
        overrides={"peak_excess_l_per_min": 4.0},
    )
    assert bumped[0] > baseline[0]
    assert bumped[1] > baseline[1]


def test_algebraic_submodel_o2hb_evaluates_over_po2(ds: nidus.Dataset) -> None:
    """The adult O2-Hb saturation curve: monotonic in PO2, saturates near 1."""
    po2 = np.array([10.0, 40.0, 100.0])
    sat = evaluate_submodel(ds, "o2hb_dissociation_adult", po2)
    assert sat[0] < sat[1] < sat[2]
    assert sat[2] > 0.95
    assert sat[0] < 0.5


def test_algebraic_submodel_glut1_evaluates_over_substrate(ds: nidus.Dataset) -> None:
    """GLUT1 flux: zero at zero substrate, approaches Vmax for large substrate."""
    substrate = np.array([0.0, 5.0, 1000.0])
    flux = evaluate_submodel(ds, "placental_glucose_glut1", substrate)
    vmax = ds["placental_glucose.glucose_glut1_vmax_per_area_mmol_per_min_per_m2"].value.central
    assert flux[0] == pytest.approx(0.0)
    assert flux[1] > flux[0]
    assert flux[2] == pytest.approx(vmax, rel=0.01)
