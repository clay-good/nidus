"""Dataset loader.

Public entry point: :func:`load`. The bundled dataset is resolved from
either the installed wheel (``nidus/_dataset/``) or, for development,
from the repository's ``dataset/`` directory next to the source tree.

The loader does no JSON Schema validation — use :func:`nidus.validate`
for that. The loader does, however, enforce structural invariants that
the schema does not cover: every parameter's ``citations`` resolve to a
known citation key, and parameter ids are globally unique across files.
"""

from __future__ import annotations

import json
from collections.abc import Iterator
from pathlib import Path
from typing import Any

from nidus.models import (
    Applicability,
    Citation,
    Extraction,
    Parameter,
    TierDef,
    Trajectory,
    Value,
)


def _default_dataset_dir() -> Path:
    """Locate the bundled dataset.

    Looks first for an installed-wheel layout (``nidus/_dataset/``),
    then for a development-source layout (``<repo>/dataset/``).
    """
    here = Path(__file__).parent
    candidates = [
        here / "_dataset",  # installed wheel
        here.parent.parent / "dataset",  # dev: python/nidus/.. = python/, then /../dataset
    ]
    for c in candidates:
        if (c / "tiers" / "tiers.json").exists():
            return c
    tried = "\n  ".join(str(c) for c in candidates)
    raise FileNotFoundError(
        f"Could not locate the nidus dataset. Tried:\n  {tried}\n"
        "Pass nidus.load(path=...) explicitly, or install the package."
    )


def _str_or_none(v: Any) -> str | None:
    return None if v is None else str(v)


def _build_citation(c: dict[str, Any]) -> Citation:
    return Citation(
        key=c["key"],
        type=c["type"],
        title=c["title"],
        authors=tuple(c["authors"]),
        year=int(c["year"]),
        journal=c.get("journal"),
        volume=_str_or_none(c.get("volume")),
        issue=_str_or_none(c.get("issue")),
        pages=c.get("pages"),
        publisher=c.get("publisher"),
        doi=c.get("doi"),
        pmid=_str_or_none(c.get("pmid")),
        url=c.get("url"),
        open_access=c.get("open_access"),
        isbn=c.get("isbn"),
        notes=c.get("notes"),
    )


def _build_value(v: dict[str, Any]) -> Value:
    return Value(
        central=float(v["central"]),
        units=v["units"],
        low=None if v.get("low") is None else float(v["low"]),
        high=None if v.get("high") is None else float(v["high"]),
        distribution=v.get("distribution"),
        ci=None if v.get("ci") is None else float(v["ci"]),
    )


def _build_trajectory(t: dict[str, Any]) -> Trajectory:
    rng = t.get("valid_range_weeks")
    return Trajectory(
        type=t["type"],
        params=dict(t["params"]),
        valid_range_weeks=None if rng is None else (float(rng[0]), float(rng[1])),
    )


def _build_extraction(e: dict[str, Any]) -> Extraction:
    return Extraction(
        review_status=e["review_status"],
        method=e.get("method"),
        by=e.get("by"),
        date=e.get("date"),
        reviewer=e.get("reviewer"),
    )


def _build_applicability(a: dict[str, Any]) -> Applicability:
    return Applicability(
        population=a.get("population"),
        excludes=tuple(a.get("excludes", [])),
    )


def _build_parameter(p: dict[str, Any], citations: dict[str, Citation]) -> Parameter:
    cited = []
    for key in p["citations"]:
        if key not in citations:
            raise ValueError(f"Parameter {p['id']!r} references unknown citation {key!r}")
        cited.append(citations[key])
    primary_key = p.get("primary_citation")
    if primary_key is not None and primary_key not in citations:
        raise ValueError(f"Parameter {p['id']!r} primary_citation={primary_key!r} unknown")
    return Parameter(
        id=p["id"],
        name=p["name"],
        subsystem=p["subsystem"],
        value=_build_value(p["value"]),
        tier=p["tier"],
        tier_rationale=p["tier_rationale"],
        citations=tuple(cited),
        extraction=_build_extraction(p["extraction"]),
        category=p.get("category"),
        trajectory=_build_trajectory(p["trajectory"]) if p.get("trajectory") else None,
        primary_citation=citations.get(primary_key) if primary_key else None,
        applicability=_build_applicability(p["applicability"]) if p.get("applicability") else None,
        notes=p.get("notes"),
    )


class Dataset:
    """A loaded nidus dataset.

    Provides dict-like access by parameter id, iteration over parameters,
    and a :meth:`filter` method for subsetting.
    """

    def __init__(
        self,
        parameters: dict[str, Parameter],
        citations: dict[str, Citation],
        tiers: dict[str, TierDef],
    ) -> None:
        self._parameters: dict[str, Parameter] = parameters
        self.citations: dict[str, Citation] = citations
        self.tiers: dict[str, TierDef] = tiers

    def __getitem__(self, id: str) -> Parameter:
        try:
            return self._parameters[id]
        except KeyError:
            raise KeyError(f"Unknown parameter id: {id!r}") from None

    def __contains__(self, id: object) -> bool:
        return isinstance(id, str) and id in self._parameters

    def __iter__(self) -> Iterator[Parameter]:
        return iter(self._parameters.values())

    def __len__(self) -> int:
        return len(self._parameters)

    def __repr__(self) -> str:
        n = len(self._parameters)
        c = len(self.citations)
        return (
            f"<nidus.Dataset: {n} parameter{'s' if n != 1 else ''}, "
            f"{c} citation{'s' if c != 1 else ''}>"
        )

    @property
    def parameters(self) -> tuple[Parameter, ...]:
        """All parameters in insertion order."""
        return tuple(self._parameters.values())

    def ids(self) -> tuple[str, ...]:
        """All parameter ids."""
        return tuple(self._parameters.keys())

    def subsystems(self) -> tuple[str, ...]:
        """Sorted list of distinct subsystems present in the dataset."""
        return tuple(sorted({p.subsystem for p in self._parameters.values()}))

    def filter(
        self,
        subsystem: str | list[str] | tuple[str, ...] | None = None,
        tier: str | list[str] | tuple[str, ...] | None = None,
        review_status: str | list[str] | tuple[str, ...] | None = None,
    ) -> Dataset:
        """Return a new ``Dataset`` containing only matching parameters.

        Any ``None`` argument is treated as "no constraint on this axis".
        String arguments are equivalent to a single-element list. Citations
        and tier definitions are carried through unchanged so back-references
        still resolve.
        """

        def _norm(v: str | list[str] | tuple[str, ...] | None) -> set[str] | None:
            if v is None:
                return None
            if isinstance(v, str):
                return {v}
            return set(v)

        sub_set = _norm(subsystem)
        tier_set = _norm(tier)
        rs_set = _norm(review_status)

        out: dict[str, Parameter] = {}
        for pid, p in self._parameters.items():
            if sub_set is not None and p.subsystem not in sub_set:
                continue
            if tier_set is not None and p.tier not in tier_set:
                continue
            if rs_set is not None and p.extraction.review_status not in rs_set:
                continue
            out[pid] = p
        return Dataset(out, self.citations, self.tiers)

    def citations_for(self, citation_key: str) -> tuple[Parameter, ...]:
        """Return all parameters that cite the given citation key."""
        return tuple(
            p for p in self._parameters.values() if any(c.key == citation_key for c in p.citations)
        )


def load(
    version: str | None = None,
    path: str | Path | None = None,
) -> Dataset:
    """Load the nidus dataset.

    Parameters
    ----------
    version:
        Reserved for future use. Pass-through versions of the dataset
        will be supported once a version-pinning mechanism is in place.
        Raises ``NotImplementedError`` if set.
    path:
        Optional directory containing a ``parameters/``, ``citations/``,
        ``tiers/``, and ``schema/`` layout. If unset, the bundled
        dataset is used.

    Returns
    -------
    Dataset
        Loaded dataset, ready for indexed access and filtering.
    """
    if version is not None:
        raise NotImplementedError(
            "Version-pinned loading is not yet supported. Install a specific "
            "package version with `pip install nidus==<version>` instead."
        )
    root = Path(path) if path is not None else _default_dataset_dir()

    # Tiers
    with (root / "tiers" / "tiers.json").open(encoding="utf-8") as f:
        tiers_raw = json.load(f)
    tiers_raw.pop("$schema", None)
    tiers: dict[str, TierDef] = {
        k: TierDef(
            label=v["label"],
            criteria=tuple(v["criteria"]),
            examples=tuple(v.get("examples", [])),
        )
        for k, v in tiers_raw.items()
    }

    # Citations
    with (root / "citations" / "citations.json").open(encoding="utf-8") as f:
        citations_raw = json.load(f)
    citations: dict[str, Citation] = {key: _build_citation(c) for key, c in citations_raw.items()}

    # Parameters
    parameters: dict[str, Parameter] = {}
    for jsonfile in sorted((root / "parameters").glob("*.json")):
        with jsonfile.open(encoding="utf-8") as f:
            records = json.load(f)
        for r in records:
            param = _build_parameter(r, citations)
            if param.id in parameters:
                raise ValueError(
                    f"Duplicate parameter id {param.id!r} (found again in {jsonfile.name})"
                )
            parameters[param.id] = param

    return Dataset(parameters, citations, tiers)
