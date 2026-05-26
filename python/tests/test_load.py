"""Tests for nidus.load and Dataset basics."""

from __future__ import annotations

import pytest

import nidus


def test_load_returns_dataset(ds: nidus.Dataset) -> None:
    assert isinstance(ds, nidus.Dataset)


# Lower bounds, kept ~5% below the current shipped totals
# (243 / 68 as of this writing) so the test fires on a substantive
# regression (e.g. accidentally dropping a whole subsystem or wholesale
# citation removal) but doesn't break on a single-row revert. Bump as the
# dataset grows further.
MIN_PARAMETERS = 230
MIN_CITATIONS = 65


def test_dataset_has_expected_size(ds: nidus.Dataset) -> None:
    # Lower bounds; the dataset grows monotonically across releases
    # (see docs/specs/v0.4/02-parameter-expansion-roadmap.md).
    assert len(ds) >= MIN_PARAMETERS
    assert len(ds.citations) >= MIN_CITATIONS


def test_dataset_growth_monotone(ds: nidus.Dataset) -> None:
    """Spec 02 §9 regression guard: subsystem coverage cannot silently shrink.

    Per-subsystem minima are pinned just below the current shipped counts.
    Bump as each subsystem grows; never bump down without an explicit
    deprecation in `dataset/CHANGELOG.md`.
    """
    min_by_subsystem = {
        "amniotic_fluid": 10,
        "fetal_circulation": 17,
        "fetal_growth": 36,
        "fetal_metabolism": 14,
        "maternal_blood": 30,
        "maternal_cardiovascular": 32,
        "maternal_endocrine": 11,
        "maternal_renal": 18,
        "maternal_respiratory": 18,
        "placental_endocrine": 12,
        "placental_gas_exchange": 10,
        "placental_glucose": 6,
        "placental_structure": 17,
    }
    actual: dict[str, int] = {}
    for p in ds:
        actual[p.subsystem] = actual.get(p.subsystem, 0) + 1
    for sub, floor in min_by_subsystem.items():
        got = actual.get(sub, 0)
        assert got >= floor, f"{sub}: {got} parameters; expected >= {floor} (regression)"


def test_repr_mentions_counts(ds: nidus.Dataset) -> None:
    s = repr(ds)
    assert str(len(ds)) in s
    assert str(len(ds.citations)) in s


def test_subsystems(ds: nidus.Dataset) -> None:
    expected = {
        "fetal_circulation",
        "fetal_growth",
        "fetal_metabolism",
        "maternal_blood",
        "maternal_cardiovascular",
        "maternal_renal",
        "maternal_respiratory",
        "maternal_endocrine",
        "placental_gas_exchange",
        "placental_glucose",
        "placental_structure",
        "placental_endocrine",
        "amniotic_fluid",
    }
    assert expected.issubset(set(ds.subsystems()))


def test_iter_yields_parameters(ds: nidus.Dataset) -> None:
    items = list(ds)
    assert len(items) >= MIN_PARAMETERS
    assert all(isinstance(p, nidus.Parameter) for p in items)


def test_ids_are_unique(ds: nidus.Dataset) -> None:
    ids = ds.ids()
    assert len(ids) == len(set(ids))
    assert len(ids) >= MIN_PARAMETERS


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
    assert len(ds) >= MIN_PARAMETERS


def test_load_version_not_implemented() -> None:
    with pytest.raises(NotImplementedError):
        nidus.load(version="0.3.0")


def test_load_missing_path_raises(tmp_path) -> None:
    with pytest.raises(FileNotFoundError):
        nidus.load(path=tmp_path / "nope")
