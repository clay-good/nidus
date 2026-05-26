"""COMBINE archive (.omex) emitter.

Bundles the nidus mechanistic-modeling exports into a single COMBINE
archive (`.omex`) — a ZIP file with a `manifest.xml` describing the
contents. This is the canonical way to ship a multi-format
systems-biology model bundle to colleagues and journals.

Spec: https://identifiers.org/combine.specifications/omex

The archive contains:
- `sbml/<submodel>.xml` for each registry submodel
- `sbml/nidus_pregnancy_composed.xml` (top-level composed model)
- `sedml/<submodel>.sedml` for each time-trajectory submodel - a
  canonical UniformTimeCourse simulation experiment (0-40 weeks,
  400 points) pointing at the matching SBML
- `cellml/<submodel>.cellml` for each registry submodel
- `physicell/nidus-parameters.xml`
- `manifest.xml`
- `metadata.rdf` — top-level provenance (dataset version, generation
  timestamp, citation pointer back to the nidus repo)
"""

from __future__ import annotations

import datetime as _dt
import zipfile
from pathlib import Path

from nidus.export.cellml import write_cellml
from nidus.export.composed import write_composed_sbml
from nidus.export.physiocell import write_physiocell
from nidus.export.registry import SUBMODELS
from nidus.export.sbml import write_sbml
from nidus.export.sedml import write_sedml
from nidus.load import Dataset

MANIFEST_NS = "http://identifiers.org/combine.specifications/omex-manifest"


def _format_entries(entries: list[tuple[str, str, bool]]) -> str:
    lines = ['<?xml version="1.0" encoding="UTF-8"?>', f'<omexManifest xmlns="{MANIFEST_NS}">']
    lines.append(f'  <content location="." format="{MANIFEST_NS}"/>')
    for location, fmt, is_master in entries:
        master = ' master="true"' if is_master else ""
        lines.append(f'  <content location="{location}" format="{fmt}"{master}/>')
    lines.append("</omexManifest>")
    return "\n".join(lines) + "\n"


def _build_metadata_rdf(dataset_version: str) -> str:
    now = _dt.datetime.now(_dt.timezone.utc).isoformat()
    return (
        '<?xml version="1.0" encoding="UTF-8"?>\n'
        '<rdf:RDF xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#"\n'
        '         xmlns:dcterms="http://purl.org/dc/terms/"\n'
        '         xmlns:nidus="https://github.com/clay-good/nidus/ontology#">\n'
        '  <rdf:Description rdf:about=".">\n'
        f"    <dcterms:created>{now}</dcterms:created>\n"
        f"    <nidus:datasetVersion>{dataset_version}</nidus:datasetVersion>\n"
        "    <nidus:source>https://github.com/clay-good/nidus</nidus:source>\n"
        "    <dcterms:description>COMBINE archive of all nidus "
        "mechanistic-modeling exports (SBML L3v2, CellML 2.0, "
        "PhysioCell parameters). See the nidus repository for parameter "
        "provenance and confidence-tier annotations.</dcterms:description>\n"
        "  </rdf:Description>\n"
        "</rdf:RDF>\n"
    )


def write_combine_archive(
    ds: Dataset,
    output_path: str | Path,
    *,
    dataset_version: str = "0.4.0.dev0",
    include_cellml_1_1: bool = False,
) -> Path:
    """Build all exports under a temp staging dir, then ZIP into ``.omex``.

    The master content (the entry point a tool should open first) is the
    composed SBML model.
    """
    out_path = Path(output_path)
    if out_path.suffix == "":
        out_path = out_path.with_suffix(".omex")
    out_path.parent.mkdir(parents=True, exist_ok=True)

    # Build everything in memory by writing to a staging directory.
    import tempfile

    with tempfile.TemporaryDirectory() as tmp:
        staging = Path(tmp)
        sbml_paths = write_sbml(ds, staging / "sbml")
        composed_path = write_composed_sbml(ds, staging / "sbml")
        sedml_paths = write_sedml(ds, staging / "sedml")
        cellml_paths = write_cellml(ds, staging / "cellml", version="2.0")
        cellml_1_1_paths: list[Path] = []
        if include_cellml_1_1:
            cellml_1_1_paths = write_cellml(ds, staging / "cellml_1_1", version="1.1")
        physicell_path = write_physiocell(ds, staging / "physicell")

        sbml_fmt = "http://identifiers.org/combine.specifications/sbml"
        sedml_fmt = "http://identifiers.org/combine.specifications/sed-ml"
        cellml2_fmt = "http://identifiers.org/combine.specifications/cellml.2.0"
        cellml1_fmt = "http://identifiers.org/combine.specifications/cellml.1.1"
        physicell_fmt = "http://purl.org/NET/mediatypes/application/xml"
        metadata_fmt = "http://identifiers.org/combine.specifications/omex-metadata"

        entries: list[tuple[str, str, bool]] = []
        for p in sbml_paths:
            entries.append((f"sbml/{p.name}", sbml_fmt, False))
        entries.append((f"sbml/{composed_path.name}", sbml_fmt, True))
        for p in sedml_paths:
            entries.append((f"sedml/{p.name}", sedml_fmt, False))
        for p in cellml_paths:
            entries.append((f"cellml/{p.name}", cellml2_fmt, False))
        for p in cellml_1_1_paths:
            entries.append((f"cellml_1_1/{p.name}", cellml1_fmt, False))
        entries.append((f"physicell/{physicell_path.name}", physicell_fmt, False))
        entries.append(("metadata.rdf", metadata_fmt, False))

        manifest_xml = _format_entries(entries)
        metadata_rdf = _build_metadata_rdf(dataset_version)

        with zipfile.ZipFile(out_path, "w", zipfile.ZIP_DEFLATED) as zf:
            zf.writestr("manifest.xml", manifest_xml)
            zf.writestr("metadata.rdf", metadata_rdf)
            for p in sbml_paths:
                zf.write(p, f"sbml/{p.name}")
            zf.write(composed_path, f"sbml/{composed_path.name}")
            for p in sedml_paths:
                zf.write(p, f"sedml/{p.name}")
            for p in cellml_paths:
                zf.write(p, f"cellml/{p.name}")
            for p in cellml_1_1_paths:
                zf.write(p, f"cellml_1_1/{p.name}")
            zf.write(physicell_path, f"physicell/{physicell_path.name}")

    # Sanity-check: the archive opens and contains expected files.
    with zipfile.ZipFile(out_path) as zf:
        names = set(zf.namelist())
    assert "manifest.xml" in names
    assert any(n.endswith("nidus_pregnancy_composed.xml") for n in names)
    assert len([n for n in names if n.startswith("sbml/")]) == len(SUBMODELS) + 1

    return out_path
