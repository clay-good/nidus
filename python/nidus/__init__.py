"""Nidus — curated dataset of human gestational physiology parameters.

Public API:
    nidus.load()       -> Dataset
    nidus.validate()   -> None  (raises ValidationError on any issue)

See README.md and docs/specs/v0.3-pivot/01-dataset-and-dashboard.md for
the public API design.
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
