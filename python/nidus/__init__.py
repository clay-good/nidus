"""Nidus — curated dataset of human gestational physiology parameters.

The public API (load, filter, citations, tiers, trajectories, validate)
is specified in docs/specs/v0.3-pivot/01-dataset-and-dashboard.md §7.
The v0.3.0.dev0 scaffold ships placeholders only; concrete
implementations land incrementally.
"""

from nidus.load import load

__version__ = "0.3.0.dev0"

__all__ = ["load", "__version__"]
