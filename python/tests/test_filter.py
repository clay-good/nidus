"""Tests for Dataset.filter."""

from __future__ import annotations

import nidus


def test_filter_by_single_subsystem(ds: nidus.Dataset) -> None:
    m = ds.filter(subsystem="maternal_cardiovascular")
    assert len(m) >= 17
    assert all(p.subsystem == "maternal_cardiovascular" for p in m)


def test_filter_by_multiple_subsystems(ds: nidus.Dataset) -> None:
    mcv = ds.filter(subsystem="maternal_cardiovascular")
    mb = ds.filter(subsystem="maternal_blood")
    m = ds.filter(subsystem=["maternal_cardiovascular", "maternal_blood"])
    assert len(m) == len(mcv) + len(mb)
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
    """The four review states partition the dataset. Most parameters remain
    unverified; a citation+source audit promoted some to verified, and the
    machine pre-verification pass promoted source-confirmed values to
    pending_human_review (sourced but not yet human-signed-off)."""
    unverified = ds.filter(review_status="unverified")
    pending = ds.filter(review_status="pending_human_review")
    verified = ds.filter(review_status="verified")
    contested = ds.filter(review_status="contested")
    assert len(unverified) + len(pending) + len(verified) + len(contested) == len(ds)
    # Most parameters still need human re-verification against original PDFs.
    # This assertion is a guardrail against accidental mass-promotion, not
    # a fixed target — the count evolves as parameters are individually
    # verified or contested. The lower bound is loose enough that ongoing
    # verification work doesn't break it but tight enough to catch a bug
    # that flips every parameter to verified by accident.
    assert len(unverified) >= 30
    # pending_human_review must never be confused with verified: a parameter
    # in that state has machine provenance but no human sign-off.
    for p in pending:
        assert p.extraction.source_check is not None
        assert p.extraction.reviewer is None


def test_filter_no_constraints_returns_all(ds: nidus.Dataset) -> None:
    f = ds.filter()
    assert len(f) == len(ds)
