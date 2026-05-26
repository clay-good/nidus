"""Tests for ``nidus.export.evaluate``."""

from __future__ import annotations

import numpy as np
import pytest

import nidus
from nidus.export import (
    SUBMODELS,
    UNSUPPORTED_REASON,
    evaluate_submodel,
    supported_submodels,
)


@pytest.fixture(scope="module")
def ds() -> nidus.Dataset:
    return nidus.load()


def test_supported_submodels_nonempty() -> None:
    ids = supported_submodels()
    assert len(ids) >= 15
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
    t = np.linspace(8, 40, 10)
    y = evaluate_submodel(ds, submodel_id, t)
    assert y.shape == (10,)
    assert np.all(np.isfinite(y))


def test_evaluate_unknown_submodel_raises(ds: nidus.Dataset) -> None:
    with pytest.raises(KeyError, match="unknown submodel id"):
        evaluate_submodel(ds, "no_such_submodel", [10, 20])


def test_evaluate_unsupported_submodel_raises(ds: nidus.Dataset) -> None:
    # Algebraic submodel — registered but no time-trajectory binding
    with pytest.raises(ValueError, match="not supported"):
        evaluate_submodel(ds, "o2hb_dissociation_adult", [10, 20])


def test_evaluate_overrides_replace_a_single_kwarg(ds: nidus.Dataset) -> None:
    t = np.array([20.0, 40.0])
    baseline = evaluate_submodel(ds, "maternal_cardiac_output_trajectory", t)
    # Bump the peak excess; output at the peak should rise
    bumped = evaluate_submodel(
        ds,
        "maternal_cardiac_output_trajectory",
        t,
        overrides={"peak_excess_l_per_min": 4.0},
    )
    assert bumped[0] > baseline[0]
    assert bumped[1] > baseline[1]
