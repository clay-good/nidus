"""Tests for citation resolution."""

from __future__ import annotations

import nidus


def test_all_32_citations_loaded(ds: nidus.Dataset) -> None:
    assert len(ds.citations) == 32


def test_citation_by_key(ds: nidus.Dataset) -> None:
    c = ds.citations["mahendru-2014-cardiac-output"]
    assert c.year == 2014
    assert any("Mahendru" in a for a in c.authors)
    assert c.doi is not None


def test_parameter_citations_are_resolved_objects(ds: nidus.Dataset) -> None:
    p = ds["maternal_cardiovascular.baseline_cardiac_output_l_per_min"]
    assert len(p.citations) >= 1
    first = p.citations[0]
    assert isinstance(first, nidus.Citation)
    assert first.key == "mahendru-2014-cardiac-output"
    assert first.doi


def test_primary_citation_resolves(ds: nidus.Dataset) -> None:
    p = ds["maternal_cardiovascular.baseline_cardiac_output_l_per_min"]
    assert p.primary_citation is not None
    assert p.primary_citation.key == "mahendru-2014-cardiac-output"


def test_citations_for_returns_parameters(ds: nidus.Dataset) -> None:
    params = ds.citations_for("mahendru-2014-cardiac-output")
    # Mahendru is heavily cited across maternal cardio.
    assert len(params) >= 5
    assert all("mahendru-2014-cardiac-output" in (c.key for c in p.citations) for p in params)


def test_citations_for_unknown_returns_empty(ds: nidus.Dataset) -> None:
    assert ds.citations_for("not-a-real-citation") == ()


def test_every_parameter_has_at_least_one_citation(ds: nidus.Dataset) -> None:
    for p in ds:
        assert len(p.citations) >= 1, f"{p.id} has no citations"


def test_every_cited_key_exists(ds: nidus.Dataset) -> None:
    """Loader should reject any parameter that cites an unknown key, so
    by the time we reach this test the invariant is already maintained.
    This is a belt-and-braces check."""
    known = set(ds.citations.keys())
    for p in ds:
        for c in p.citations:
            assert c.key in known
