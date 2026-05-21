"""JSON Schema validation for a nidus dataset.

Runs every parameter, citation, and tier definition against its schema
(draft 2020-12). Additionally checks cross-file invariants the schemas
cannot express: citation keys are unique, parameter ids are unique
across files, and every parameter's ``citations`` resolve to a real
citation.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import jsonschema


class ValidationError(Exception):
    """Raised when a dataset fails schema or cross-reference validation.

    The message contains a multi-line summary of all errors found, up to
    a sensible cap.
    """


def _load_json(path: Path) -> Any:
    with path.open(encoding="utf-8") as f:
        return json.load(f)


def validate(path: str | Path | None = None) -> None:
    """Validate a nidus dataset against the bundled JSON Schemas.

    Runs every parameter, citation, and tier definition against its
    schema (draft 2020-12). Also enforces cross-file invariants the
    schema cannot express: parameter ids are globally unique, every
    citation key referenced by a parameter exists, and the dict key in
    ``citations.json`` matches the embedded ``"key"`` field.

    Args:
        path: Directory containing the dataset layout. Defaults to the
            bundled dataset (same resolution as :func:`nidus.load`).

    Raises:
        ValidationError: On any schema violation or cross-file
            inconsistency. The message aggregates all errors found
            (capped at 50 lines).

    Example:

        >>> import nidus
        >>> nidus.validate()  # bundled dataset; raises on any issue
    """
    if path is None:
        from nidus.load import _default_dataset_dir

        root = _default_dataset_dir()
    else:
        root = Path(path)

    param_schema = _load_json(root / "schema" / "parameter.schema.json")
    cite_schema = _load_json(root / "schema" / "citation.schema.json")
    tier_schema = _load_json(root / "schema" / "tier.schema.json")

    errors: list[str] = []

    # ---- Tiers --------------------------------------------------------
    tiers_raw = _load_json(root / "tiers" / "tiers.json")
    try:
        jsonschema.validate(tiers_raw, tier_schema)
    except jsonschema.ValidationError as e:
        errors.append(f"tiers.json: {e.message}")

    # ---- Citations ----------------------------------------------------
    citations_raw = _load_json(root / "citations" / "citations.json")
    citation_keys: set[str] = set()
    if not isinstance(citations_raw, dict):
        errors.append("citations.json must be a JSON object keyed by citation key")
    else:
        for key, c in citations_raw.items():
            try:
                jsonschema.validate(c, cite_schema)
            except jsonschema.ValidationError as e:
                errors.append(f"citations[{key}]: {e.message}")
                continue
            if c.get("key") != key:
                errors.append(
                    f"citations[{key}]: 'key' field ({c.get('key')!r}) does not "
                    f"match dict key ({key!r})"
                )
            citation_keys.add(key)

    # ---- Parameters ---------------------------------------------------
    param_ids: set[str] = set()
    for jsonfile in sorted((root / "parameters").glob("*.json")):
        records = _load_json(jsonfile)
        if not isinstance(records, list):
            errors.append(f"{jsonfile.name}: must be a JSON array")
            continue
        for i, r in enumerate(records):
            label = f"{jsonfile.name}[{i}]"
            if isinstance(r, dict) and "id" in r:
                label = f"{jsonfile.name}[{i}] (id={r['id']})"
            try:
                jsonschema.validate(r, param_schema)
            except jsonschema.ValidationError as e:
                errors.append(f"{label}: {e.message}")
                continue
            pid = r["id"]
            if pid in param_ids:
                errors.append(f"{label}: duplicate parameter id {pid!r}")
            param_ids.add(pid)
            for ck in r.get("citations", []):
                if ck not in citation_keys:
                    errors.append(f"{label}: cites unknown citation {ck!r}")
            primary = r.get("primary_citation")
            if primary is not None and primary not in citation_keys:
                errors.append(f"{label}: primary_citation={primary!r} not in citations.json")

    if errors:
        cap = 50
        head = "\n".join(f"  - {e}" for e in errors[:cap])
        if len(errors) > cap:
            head += f"\n  ... and {len(errors) - cap} more"
        plural = "" if len(errors) == 1 else "s"
        raise ValidationError(f"Dataset validation failed ({len(errors)} error{plural}):\n{head}")
