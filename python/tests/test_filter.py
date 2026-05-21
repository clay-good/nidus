"""Tests for Dataset.filter."""

from __future__ import annotations

import nidus


def test_filter_by_single_subsystem(ds: nidus.Dataset) -> None:
    m = ds.filter(subsystem="maternal_cardiovascular")
    assert len(m) == 14
    assert all(p.subsystem == "maternal_cardiovascular" for p in m)


def test_filter_by_multiple_subsystems(ds: nidus.Dataset) -> None:
    m = ds.filter(subsystem=["maternal_cardiovascular", "maternal_blood"])
    assert len(m) == 14 + 9
    assert {p.subsystem for p in m} == {"maternal_cardiovascular", "maternal_blood"}


def test_filter_by_tier(ds: nidus.Dataset) -> None:
    b = ds.filter(tier="B")
    assert len(b) > 0
    assert all(p.tier == "B" for p in b)


def test_filter_by_multiple_tiers(ds: nidus.Dataset) -> None:
    bc = ds.filter(tier=["B", "C"])
    assert all(p.tier in {"B", "C"} for p in bc)
    # Multi-tier filter is the union, so it must be at least as large as
    # either single-tier filter.
    just_b = ds.filter(tier="B")
    just_c = ds.filter(tier="C")
    assert len(bc) == len(just_b) + len(just_c)


def test_filter_combined(ds: nidus.Dataset) -> None:
    f = ds.filter(subsystem="maternal_cardiovascular", tier="B")
    assert all(p.subsystem == "maternal_cardiovascular" and p.tier == "B" for p in f)


def test_filter_returns_dataset(ds: nidus.Dataset) -> None:
    f = ds.filter(tier="B")
    assert isinstance(f, nidus.Dataset)
    # Citations and tiers carried through unchanged so back-refs still resolve.
    assert f.citations is ds.citations
    assert f.tiers is ds.tiers


def test_filter_empty_when_unknown_tier(ds: nidus.Dataset) -> None:
    f = ds.filter(tier="Z")
    assert len(f) == 0


def test_filter_by_review_status(ds: nidus.Dataset) -> None:
    f = ds.filter(review_status="unverified")
    # The migration marks everything unverified; expect all 54.
    assert len(f) == 54


def test_filter_no_constraints_returns_all(ds: nidus.Dataset) -> None:
    f = ds.filter()
    assert len(f) == len(ds)
