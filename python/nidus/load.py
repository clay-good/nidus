"""Dataset loader. Placeholder — to be implemented.

See docs/specs/v0.3-pivot/01-dataset-and-dashboard.md §7.2 for the
target public API.
"""

from __future__ import annotations

from pathlib import Path
from typing import Any


def load(version: str | None = None, path: str | Path | None = None) -> Any:
    """Load the nidus dataset.

    Parameters
    ----------
    version:
        If set, load a specific dataset version. Defaults to the version
        bundled with the installed package.
    path:
        If set, load the dataset from a local directory rather than the
        bundled one.

    Returns
    -------
    Dataset
        An object exposing per-parameter access, filtering, and citation
        resolution. See the spec for the full surface.

    Raises
    ------
    NotImplementedError
        This loader is a v0.3.0.dev0 placeholder. The concrete
        implementation lands in a subsequent commit.
    """
    raise NotImplementedError(
        "nidus.load() is not yet implemented. The dataset scaffold and "
        "JSON Schemas are in place; the loader will land in a subsequent "
        "commit. See docs/specs/v0.3-pivot/01-dataset-and-dashboard.md."
    )
