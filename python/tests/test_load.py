"""Tests for nidus.load and Dataset basics."""

from __future__ import annotations

import pytest

import nidus


def test_load_returns_dataset(ds: nidus.Dataset) -> None:
    assert isinstance(ds, nidus.Dataset)


def test_dataset_has_expected_size(ds: nidus.Dataset) -> None:
    assert len(ds) == 54
    assert len(ds.citations) == 32


def test_repr_mentions_counts(ds: nidus.Dataset) -> None:
    s = repr(ds)
    assert "54" in s
    assert "32" in s


def test_subsystems(ds: nidus.Dataset) -> None:
    expected = {
        "fetal_circulation",
        "fetal_growth",
        "fetal_metabolism",
        "maternal_blood",
        "maternal_cardiovascular",
        "maternal_renal",
        "maternal_respiratory",
        "placental_gas_exchange",
        "placental_glucose",
        "placental_structure",
    }
    assert set(ds.subsystems()) == expected


def test_iter_yields_parameters(ds: nidus.Dataset) -> None:
    items = list(ds)
    assert len(items) == 54
    assert all(isinstance(p, nidus.Parameter) for p in items)


def test_ids_are_unique(ds: nidus.Dataset) -> None:
    ids = ds.ids()
    assert len(ids) == len(set(ids)) == 54


def test_indexed_access(ds: nidus.Dataset) -> None:
    p = ds["maternal_cardiovascular.baseline_cardiac_output_l_per_min"]
    assert p.subsystem == "maternal_cardiovascular"
    assert p.value.units == "L/min"
    assert p.value.central == pytest.approx(4.6)
    assert p.tier == "B"


def test_indexed_access_missing_raises_keyerror(ds: nidus.Dataset) -> None:
    with pytest.raises(KeyError):
        _ = ds["this.does.not.exist"]


def test_contains(ds: nidus.Dataset) -> None:
    assert "maternal_cardiovascular.baseline_cardiac_output_l_per_min" in ds
    assert "does.not.exist" not in ds
    assert 42 not in ds  # type: ignore[operator]


def test_tiers_loaded(ds: nidus.Dataset) -> None:
    assert set(ds.tiers.keys()) == {"A", "B", "C", "D"}
    assert ds.tiers["A"].label == "Well-established"
    assert len(ds.tiers["A"].criteria) >= 1


def test_load_with_explicit_path() -> None:
    """Passing path= should also work."""
    from nidus.load import _default_dataset_dir

    src = _default_dataset_dir()
    ds = nidus.load(path=src)
    assert len(ds) == 54


def test_load_version_not_implemented() -> None:
    with pytest.raises(NotImplementedError):
        nidus.load(version="0.3.0")


def test_load_missing_path_raises(tmp_path) -> None:
    with pytest.raises(FileNotFoundError):
        nidus.load(path=tmp_path / "nope")
