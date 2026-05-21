"""Dataclasses for the nidus dataset.

These mirror the JSON Schemas in ``dataset/schema/`` but are intended for
end-user attribute access rather than validation. Validation against the
schemas happens separately in :mod:`nidus.validate`; the loader in
:mod:`nidus.load` constructs these objects from already-validated input.

All classes are :func:`dataclasses.dataclass` instances with ``frozen=True``
(hashable, immutable) and ``slots=True`` (lower memory overhead than the
default ``__dict__`` form). Loaded datasets are therefore safe to share
across threads and to cache.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Literal

Tier = Literal["A", "B", "C", "D"]
"""Type alias for the four confidence tiers."""

Subsystem = Literal[
    "maternal_cardiovascular",
    "maternal_blood",
    "maternal_respiratory",
    "maternal_renal",
    "placental_structure",
    "placental_gas_exchange",
    "placental_glucose",
    "fetal_circulation",
    "fetal_growth",
    "fetal_metabolism",
]
"""Type alias enumerating the ten subsystems."""


@dataclass(frozen=True, slots=True)
class Value:
    """Numerical value of a parameter with optional uncertainty bounds.

    Most v0.3 records use ``distribution="normal"`` with ``low``/``high``
    at one sigma (``ci=0.683``); a few are point estimates with no bounds.

    Attributes:
        central: Best central estimate.
        units: SI or domain-conventional unit string, e.g. ``"L/min"``,
            ``"mmHg"``, ``"g"``.
        low: Optional lower bound at the level given by ``ci``.
        high: Optional upper bound at the level given by ``ci``.
        distribution: Optional distribution shape — one of ``"normal"``,
            ``"lognormal"``, ``"uniform"``, or ``"empirical"``.
        ci: Optional confidence-interval level for ``low``/``high``,
            e.g. ``0.683`` for one sigma or ``0.95`` for 95% CI.
    """

    central: float
    units: str
    low: float | None = None
    high: float | None = None
    distribution: str | None = None
    ci: float | None = None


@dataclass(frozen=True, slots=True)
class Trajectory:
    """Optional gestational-age-dependent shape of a parameter.

    Most v0.3 records are scalars and omit ``trajectory``. The field is
    reserved for future curation work where parameters vary across the
    gestational window.

    Attributes:
        type: Shape family — one of ``"constant"``, ``"linear"``,
            ``"polynomial"``, ``"gaussian"``, ``"logistic"``,
            ``"exponential"``, or ``"piecewise"``.
        params: Shape-specific parameter dict, e.g. for ``"gaussian"``:
            ``{"peak_week": 30, "fwhm_weeks": 12}``.
        valid_range_weeks: Optional ``(start, end)`` gestational window
            outside which the trajectory should not be evaluated; tier
            degrades on extrapolation outside this range.
    """

    type: str
    params: dict[str, float]
    valid_range_weeks: tuple[float, float] | None = None


@dataclass(frozen=True, slots=True)
class Extraction:
    """Provenance metadata: how, by whom, and when a parameter was extracted.

    Every Tier A/B record is expected to graduate from
    ``review_status="unverified"`` to ``"verified"`` via the human-with-PDF
    workflow documented in ``docs/contributing/verification.md``.

    Attributes:
        review_status: ``"unverified"``, ``"verified"``, or ``"contested"``.
        method: How the value was extracted — e.g. ``"table_2_column_3"``
            or ``"figure_4_digitised"``.
        by: Identifier (handle or name) of the extractor.
        date: ISO-format date of extraction.
        reviewer: Identifier of the human who verified against the paper.
    """

    review_status: str
    method: str | None = None
    by: str | None = None
    date: str | None = None
    reviewer: str | None = None


@dataclass(frozen=True, slots=True)
class Applicability:
    """Population the parameter applies to, and known exclusions.

    Tier degrades by one level when a parameter is applied outside its
    declared ``population``.

    Attributes:
        population: Free-text description of the source cohort.
        excludes: Conditions or populations the parameter is *not* valid
            for (e.g. ``("twins", "chronic_hypertension")``).
    """

    population: str | None = None
    excludes: tuple[str, ...] = field(default_factory=tuple)


@dataclass(frozen=True, slots=True)
class Citation:
    """A single bibliographic record.

    Journal articles, preprints, and conference papers should carry a
    DOI or PMID. Books and pre-DOI references may have neither.

    Attributes:
        key: Citation key, also used as the dict key in
            ``citations.json``.
        type: One of ``"journal-article"``, ``"book"``, ``"book-chapter"``,
            ``"conference-paper"``, ``"preprint"``, ``"report"``,
            ``"dataset"``, ``"thesis"``.
        title: Publication title.
        authors: Tuple of author strings, "Family GI" or "Family, Given"
            style.
        year: Publication year (1800-2100).
        journal: Container title for journal articles.
        publisher: Publisher for books and reports.
        volume: Journal volume.
        issue: Journal issue.
        pages: Pages range (e.g. ``"849-856"``).
        doi: Bare DOI without the ``https://doi.org/`` prefix.
        pmid: PubMed identifier.
        url: Fallback URL if neither DOI nor PMID exists.
        isbn: ISBN for books.
        open_access: Whether the work is open-access.
        notes: Free-text notes.
    """

    key: str
    type: str
    title: str
    authors: tuple[str, ...]
    year: int
    journal: str | None = None
    volume: str | None = None
    issue: str | None = None
    pages: str | None = None
    publisher: str | None = None
    doi: str | None = None
    pmid: str | None = None
    url: str | None = None
    open_access: bool | None = None
    isbn: str | None = None
    notes: str | None = None


@dataclass(frozen=True, slots=True)
class Parameter:
    """A single physiological parameter with resolved citations and metadata.

    Note that :attr:`citations` is a tuple of resolved :class:`Citation`
    objects, not citation keys — the loader resolves them at construction
    time so ``p.citations[0].doi`` works without a separate lookup.

    Attributes:
        id: Dotted, snake_case identifier, e.g.
            ``"maternal_cardiovascular.baseline_cardiac_output_l_per_min"``.
        name: Human-readable name.
        subsystem: One of the ten :data:`Subsystem` enum values.
        value: The :class:`Value` with central and optional bounds.
        tier: Confidence tier — ``"A"``, ``"B"``, ``"C"``, or ``"D"``.
        tier_rationale: Free-text rationale referencing the evidence base.
        citations: Resolved :class:`Citation` objects (not keys).
        extraction: Provenance metadata.
        category: Optional finer-grained category within the subsystem.
        trajectory: Optional gestational-age-dependent shape.
        primary_citation: Optional most-load-bearing :class:`Citation`.
        applicability: Optional population + exclusions.
        notes: Optional free-text caveats.
    """

    id: str
    name: str
    subsystem: str
    value: Value
    tier: str
    tier_rationale: str
    citations: tuple[Citation, ...]
    extraction: Extraction
    category: str | None = None
    trajectory: Trajectory | None = None
    primary_citation: Citation | None = None
    applicability: Applicability | None = None
    notes: str | None = None


@dataclass(frozen=True, slots=True)
class TierDef:
    """Definition of a single confidence tier (A, B, C, or D).

    Loaded into :attr:`Dataset.tiers` keyed by ``"A"`` through ``"D"``.

    Attributes:
        label: Short human-readable label, e.g. ``"Well-established"``.
        criteria: Bullet-list criteria a parameter must satisfy.
        examples: Optional list of example parameter ids at this tier.
    """

    label: str
    criteria: tuple[str, ...]
    examples: tuple[str, ...] = field(default_factory=tuple)
