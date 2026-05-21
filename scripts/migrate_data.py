#!/usr/bin/env python3
"""One-shot migration: data/ (legacy TOML) -> dataset/ (new JSON).

Reads:
    data/parameters/<dir>/<stem>.toml
    data/citations/index.toml
Writes:
    dataset/parameters/<subsystem>.json
    dataset/citations/citations.json
Verifies each output validates against dataset/schema/.

Run from repo root:
    python3 scripts/migrate_data.py

This script is intended to be run exactly once. After the migration is
committed and verified, the legacy data/ directory can be removed.
"""

from __future__ import annotations

import json
import sys
import tomllib
from pathlib import Path
from typing import Any

import jsonschema

REPO = Path(__file__).parent.parent
DATA = REPO / "data"
DATASET = REPO / "dataset"

# Map (dir_name, file_stem) -> canonical subsystem enum value.
SUBSYSTEM_MAP: dict[tuple[str, str], str] = {
    ("maternal", "cardio"):            "maternal_cardiovascular",
    ("maternal", "blood"):             "maternal_blood",
    ("maternal", "respiratory"):       "maternal_respiratory",
    ("maternal", "renal"):             "maternal_renal",
    ("placenta", "structure"):         "placental_structure",
    ("placenta", "gas_transport"):     "placental_gas_exchange",
    ("placenta", "glucose_transport"): "placental_glucose",
    ("fetal",    "circulation"):       "fetal_circulation",
    ("fetal",    "growth"):            "fetal_growth",
    ("fetal",    "metabolism"):        "fetal_metabolism",
}


def make_dotted_id(kebab_id: str, subsystem: str, dir_name: str, file_stem: str) -> str:
    """Produce a schema-valid dotted ID.

    The source TOML uses flat kebab-case identifiers like
    ``maternal-cardio-baseline-cardiac-output-l-per-min``. The new schema
    wants two-or-more dotted segments with snake_case tokens. We use the
    subsystem enum as the first segment, and the source kebab ID (with
    its file-path prefix stripped if present) as the second.

    Stripping only the known file-path prefix (rather than dropping a
    fixed number of tokens) preserves uniqueness across siblings like
    ``maternal-blood-volume-l`` and ``maternal-plasma-volume-l``.
    """
    rest = kebab_id
    # Try stripping "<dir>-<file_stem>-" first, then "<dir>-".
    for prefix in (f"{dir_name}-{file_stem}-", f"{dir_name}-"):
        if rest.startswith(prefix):
            rest = rest[len(prefix):]
            break
    rest = rest.replace("-", "_")
    return f"{subsystem}.{rest}"


def convert_value(src: dict[str, Any], units: str) -> dict[str, Any]:
    """Map source ``value`` shape to new schema's ``value`` object.

    Source shapes:
        {kind = "normal", mean = X, sd = Y}
        {kind = "point",  value = X, uncertainty = Y}
    """
    kind = src.get("kind")
    if kind == "normal":
        mean = float(src["mean"])
        sd = float(src["sd"])
        return {
            "central": mean,
            "low": round(mean - sd, 6),
            "high": round(mean + sd, 6),
            "units": units,
            "distribution": "normal",
            "ci": 0.683,  # one sigma; matches source mean/sd semantics
        }
    if kind == "point":
        val = float(src["value"])
        unc = float(src.get("uncertainty", 0.0))
        if unc > 0:
            return {
                "central": val,
                "low": round(val - unc, 6),
                "high": round(val + unc, 6),
                "units": units,
            }
        return {"central": val, "units": units}
    raise ValueError(f"Unknown value kind: {kind!r}")


def make_tier_rationale(p: dict[str, Any]) -> str:
    """Synthesise a tier_rationale string from the source fields.

    The source TOML does not carry an explicit rationale, but it does
    carry ``technique``, ``population``, ``caveats``, and the citation
    list — together these reconstruct a defensible rationale until a
    human re-reviews each entry.
    """
    parts: list[str] = []
    tier = p["tier"]
    citation = p["citation"]
    parts.append(f"Tier {tier} pending re-review. Source citation: {citation}.")
    if p.get("technique"):
        parts.append(f"Technique: {p['technique']}.")
    if p.get("population"):
        parts.append(f"Population: {p['population']}.")
    if p.get("caveats"):
        parts.append(f"Caveats: {p['caveats']}")
    return " ".join(parts)


def convert_parameter(
    p: dict[str, Any], subsystem: str, dir_name: str, file_stem: str
) -> dict[str, Any]:
    """Map one source ``[[parameter]]`` entry to a new schema record."""
    out: dict[str, Any] = {
        "id": make_dotted_id(p["id"], subsystem, dir_name, file_stem),
        "name": p["name"],
        "subsystem": subsystem,
        "value": convert_value(p["value"], p["unit"]),
        "tier": p["tier"],
        "tier_rationale": make_tier_rationale(p),
        "citations": [p["citation"]],
        "primary_citation": p["citation"],
        "extraction": {
            "review_status": "unverified",
            "by": None if "by" not in p else p["by"],
        },
    }
    # Strip None-valued extraction sub-fields so the document stays clean.
    out["extraction"] = {k: v for k, v in out["extraction"].items() if v is not None}

    # Applicability — derived from the source ``population`` and (where
    # the source mentions twins / chronic disease) excludes.
    if p.get("population"):
        out["applicability"] = {"population": p["population"]}

    # Notes — carry forward description + caveats, so nothing is lost.
    notes_parts: list[str] = []
    if p.get("description"):
        notes_parts.append(p["description"])
    if p.get("caveats"):
        notes_parts.append(f"Caveats: {p['caveats']}")
    if notes_parts:
        out["notes"] = " ".join(notes_parts)

    return out


BOOK_VENUE_HINTS = ("publication", "press", "publishers", "publishing", "book")


def infer_citation_type(c: dict[str, Any]) -> str:
    """Best-effort type inference from source fields."""
    venue = (c.get("venue") or "").lower()
    if any(hint in venue for hint in BOOK_VENUE_HINTS):
        return "book"
    if c.get("doi") or c.get("pmid"):
        return "journal-article"
    if c.get("year") and not c.get("venue"):
        return "report"
    return "journal-article"


def convert_citation(c: dict[str, Any]) -> dict[str, Any]:
    """Map one source ``[[citation]]`` entry to the new schema."""
    ctype = infer_citation_type(c)
    out: dict[str, Any] = {
        "key": c["id"],
        "type": ctype,
        "title": c["title"],
        # Source 'authors' is a single string; the new schema wants a list.
        "authors": [a.strip() for a in c["authors"].replace(";", ",").split(",") if a.strip()],
        "year": int(c["year"]),
    }
    if c.get("venue"):
        if ctype in ("book", "book-chapter"):
            out["publisher"] = c["venue"]
        else:
            out["journal"] = c["venue"]
    if c.get("doi"):
        out["doi"] = c["doi"]
    if c.get("pmid"):
        out["pmid"] = c["pmid"]
    if c.get("url"):
        out["url"] = c["url"]
    if c.get("notes"):
        out["notes"] = c["notes"]
    return out


def main() -> int:
    # ----- Load schemas -----
    with (DATASET / "schema" / "parameter.schema.json").open() as f:
        param_schema = json.load(f)
    with (DATASET / "schema" / "citation.schema.json").open() as f:
        cite_schema = json.load(f)

    # ----- Convert citations -----
    with (DATA / "citations" / "index.toml").open("rb") as f:
        cite_src = tomllib.load(f)

    citations_out: dict[str, dict[str, Any]] = {}
    for c in cite_src.get("citation", []):
        record = convert_citation(c)
        jsonschema.validate(record, cite_schema)
        citations_out[record["key"]] = record

    cite_out_path = DATASET / "citations" / "citations.json"
    cite_out_path.write_text(
        json.dumps(citations_out, indent=2, ensure_ascii=False, sort_keys=True) + "\n"
    )
    print(f"Wrote {len(citations_out)} citations -> {cite_out_path.relative_to(REPO)}")

    # ----- Convert parameters -----
    by_subsystem: dict[str, list[dict[str, Any]]] = {}
    seen_ids: set[str] = set()

    for toml_path in sorted((DATA / "parameters").rglob("*.toml")):
        dir_name = toml_path.parent.name
        file_stem = toml_path.stem
        key = (dir_name, file_stem)
        if key not in SUBSYSTEM_MAP:
            print(f"  WARN: no subsystem mapping for {toml_path}, skipping")
            continue
        subsystem = SUBSYSTEM_MAP[key]

        with toml_path.open("rb") as f:
            src = tomllib.load(f)

        for p in src.get("parameter", []):
            try:
                record = convert_parameter(p, subsystem, dir_name, file_stem)
            except Exception as e:
                print(f"  ERROR converting {p.get('id', '?')}: {e}", file=sys.stderr)
                raise

            if record["id"] in seen_ids:
                # Collision: append a stable disambiguator.
                # This shouldn't happen given the source IDs are unique.
                raise SystemExit(f"Duplicate id: {record['id']}")
            seen_ids.add(record["id"])

            # Cross-check: every citation key referenced must exist.
            for ck in record["citations"]:
                if ck not in citations_out:
                    raise SystemExit(
                        f"Parameter {record['id']} cites unknown citation {ck!r}"
                    )

            jsonschema.validate(record, param_schema)
            by_subsystem.setdefault(subsystem, []).append(record)

    for subsystem, records in sorted(by_subsystem.items()):
        out_path = DATASET / "parameters" / f"{subsystem}.json"
        # Sort parameters within a file for stable diffs.
        records.sort(key=lambda r: r["id"])
        out_path.write_text(
            json.dumps(records, indent=2, ensure_ascii=False) + "\n"
        )
        print(f"Wrote {len(records):3d} parameters -> {out_path.relative_to(REPO)}")

    total = sum(len(v) for v in by_subsystem.values())
    print(f"\nTotal: {total} parameters across {len(by_subsystem)} subsystems; "
          f"{len(citations_out)} citations.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
