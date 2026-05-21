"""Mechanistic-modeling exports of the nidus dataset.

This submodule generates SBML, CellML, and PhysioCell representations of
the small set of nidus submodels that are mechanistic enough to express
in those formats. See `docs/specs/v0.4/01-mechanistic-modeling-interop.md`
for the full design.

The public surface is small:

    from nidus.export import (
        list_submodels,          # introspect what's exportable
        build_sbml,              # one submodel -> SBML XML string
        build_cellml,            # one submodel -> CellML XML string
        build_physiocell_params, # full parameters.xml as string
        write_sbml,              # write all SBML files to a directory
        write_cellml,            # write all CellML files to a directory
    )

Each submodel is identified by a stable string id and carries:
- a NumPy reference kernel (in `reference.py`) used for round-trip
  validation,
- a list of source `Parameter` objects from the nidus dataset,
- per-format generators that emit annotated SBML / CellML / etc.

The exports are pure functions of the loaded dataset: re-running the
generators on the same dataset version produces byte-identical output.
"""

from __future__ import annotations

from nidus.export.cellml import build_cellml, write_cellml
from nidus.export.physiocell import build_physiocell_params, write_physiocell
from nidus.export.registry import SUBMODELS, list_submodels
from nidus.export.sbml import build_sbml, write_sbml

__all__ = [
    "SUBMODELS",
    "build_cellml",
    "build_physiocell_params",
    "build_sbml",
    "list_submodels",
    "write_cellml",
    "write_physiocell",
    "write_sbml",
]
