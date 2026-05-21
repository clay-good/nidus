"""Nidus — curated dataset of human gestational physiology parameters.

A pure-Python package distributing a citation-backed, confidence-tier-
annotated dataset of maternal-placental-fetal physiology values
spanning 8-40 weeks gestation. See the
`documentation <https://claygood.github.io/nidus/>`_ for full
details.

The public API is intentionally minimal:

- :func:`load` returns a :class:`Dataset`.
- :func:`validate` checks a dataset against the bundled JSON Schemas.

Quick start:

    >>> import nidus
    >>> ds = nidus.load()
    >>> p = ds["maternal_cardiovascular.baseline_cardiac_output_l_per_min"]
    >>> p.value.central, p.value.units, p.tier
    (4.6, 'L/min', 'B')
"""

from nidus.load import Dataset, load
from nidus.models import (
    Applicability,
    Citation,
    Extraction,
    Parameter,
    TierDef,
    Trajectory,
    Value,
)
from nidus.validate import ValidationError, validate

__version__ = "0.3.0.dev0"

__all__ = [
    "Applicability",
    "Citation",
    "Dataset",
    "Extraction",
    "Parameter",
    "TierDef",
    "Trajectory",
    "ValidationError",
    "Value",
    "__version__",
    "load",
    "validate",
]
