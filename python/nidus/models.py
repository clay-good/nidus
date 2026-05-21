"""Dataclasses for the nidus dataset.

These mirror the JSON Schemas in ``dataset/schema/`` but are intended for
end-user attribute access rather than validation. Validation against the
schemas happens separately in :mod:`nidus.validate`; the loader in
:mod:`nidus.load` constructs these objects from already-validated input.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Literal, Optional

Tier = Literal["A", "B", "C", "D"]
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


@dataclass(frozen=True, slots=True)
class Value:
    """Numerical value of a parameter, with optional uncertainty bounds."""

    central: float
    units: str
    low: Optional[float] = None
    high: Optional[float] = None
    distribution: Optional[str] = None
    ci: Optional[float] = None


@dataclass(frozen=True, slots=True)
class Trajectory:
    """Optional gestational-age-dependent trajectory shape."""

    type: str
    params: dict[str, float]
    valid_range_weeks: Optional[tuple[float, float]] = None


@dataclass(frozen=True, slots=True)
class Extraction:
    """Provenance metadata: how, by whom, and when the parameter was extracted."""

    review_status: str
    method: Optional[str] = None
    by: Optional[str] = None
    date: Optional[str] = None
    reviewer: Optional[str] = None


@dataclass(frozen=True, slots=True)
class Applicability:
    """Population the parameter applies to, and known exclusions."""

    population: Optional[str] = None
    excludes: tuple[str, ...] = field(default_factory=tuple)


@dataclass(frozen=True, slots=True)
class Citation:
    """A single bibliographic record."""

    key: str
    type: str
    title: str
    authors: tuple[str, ...]
    year: int
    journal: Optional[str] = None
    volume: Optional[str] = None
    issue: Optional[str] = None
    pages: Optional[str] = None
    publisher: Optional[str] = None
    doi: Optional[str] = None
    pmid: Optional[str] = None
    url: Optional[str] = None
    open_access: Optional[bool] = None
    isbn: Optional[str] = None
    notes: Optional[str] = None


@dataclass(frozen=True, slots=True)
class Parameter:
    """A single physiological parameter with resolved citations and metadata.

    Note that ``citations`` is a tuple of resolved :class:`Citation` objects,
    not citation keys; the loader resolves them at construction time.
    """

    id: str
    name: str
    subsystem: str
    value: Value
    tier: str
    tier_rationale: str
    citations: tuple[Citation, ...]
    extraction: Extraction
    category: Optional[str] = None
    trajectory: Optional[Trajectory] = None
    primary_citation: Optional[Citation] = None
    applicability: Optional[Applicability] = None
    notes: Optional[str] = None


@dataclass(frozen=True, slots=True)
class TierDef:
    """Definition of a single confidence tier (A, B, C, or D)."""

    label: str
    criteria: tuple[str, ...]
    examples: tuple[str, ...] = field(default_factory=tuple)
