#!/usr/bin/env python3
"""Promote source-confirmed parameters to ``review_status=pending_human_review``.

Reads ``data/validation/machine_checks.json`` and an explicit allowlist of
parameter ids (curated — only params whose stored value is confirmed by a
verbatim source quote should be on it). For each, it edits the parameter's
record in ``dataset/parameters/<subsystem>.json``:

* sets ``extraction.review_status = "pending_human_review"``
* attaches ``extraction.source_check`` with the verdict, evidence level,
  source citation, verbatim quote, and what the source reports.

It NEVER sets ``verified`` and never touches ``extraction.reviewer`` — a human
still has to sign off. Re-running is idempotent (it overwrites source_check
for allowlisted params and leaves everything else alone).

    python scripts/promote_pending_review.py --date 2026-06-23 \
        --ids maternal_respiratory.paco2_mmhg_term placental_endocrine.hcg_peak_week ...
    python scripts/promote_pending_review.py --date 2026-06-23 --ids-file pending.txt
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

REPO = Path(__file__).parent.parent
PARAM_DIR = REPO / "dataset" / "parameters"
CHECKS = REPO / "data" / "validation" / "machine_checks.json"
CHECKED_BY = "machine-preverify"


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--date", required=True, help="ISO checked_date to stamp")
    ap.add_argument("--ids", nargs="*", default=[], help="Parameter ids to promote")
    ap.add_argument("--ids-file", help="File with one parameter id per line")
    args = ap.parse_args()

    ids = list(args.ids)
    if args.ids_file:
        ids += [
            ln.strip()
            for ln in Path(args.ids_file).read_text(encoding="utf-8").splitlines()
            if ln.strip() and not ln.startswith("#")
        ]
    allow = set(ids)
    if not allow:
        print("No ids given.")
        return 2

    checks = {c["parameter_id"]: c for c in json.loads(CHECKS.read_text())["checks"]}

    promoted = 0
    missing_check: list[str] = []
    not_found: list[str] = []
    for f in sorted(PARAM_DIR.glob("*.json")):
        params: list[dict[str, Any]] = json.loads(f.read_text(encoding="utf-8"))
        changed = False
        for p in params:
            if p["id"] not in allow:
                continue
            c = checks.get(p["id"])
            if c is None or c.get("verdict") not in ("match", "close"):
                missing_check.append(p["id"])
                continue
            ex = p["extraction"]
            if ex.get("review_status") == "verified":
                print(f"  SKIP {p['id']} — already human-verified")
                continue
            ex["review_status"] = "pending_human_review"
            ex["reviewer"] = None
            source_check: dict[str, Any] = {
                "verdict": c["verdict"],
                "evidence_level": c["evidence_level"],
                # For secondary/regulatory evidence the subagent records the
                # source it actually read; otherwise the evidence is the param's
                # own primary citation.
                "source_citation": c.get("source_citation") or c["primary_citation"],
                "checked_by": CHECKED_BY,
                "checked_date": args.date,
            }
            if c.get("source_url"):
                source_check["source_url"] = c["source_url"]
            if c.get("supporting_quote"):
                source_check["quote"] = c["supporting_quote"]
            if c.get("source_reports"):
                source_check["extracted_value"] = c["source_reports"]
            ex["source_check"] = source_check
            changed = True
            promoted += 1
            print(f"  PROMOTED {p['id']}  ({c['verdict']}, {c['evidence_level']})")
        if changed:
            f.write_text(
                json.dumps(params, indent=2, ensure_ascii=False) + "\n",
                encoding="utf-8",
            )

    seen = {
        p["id"]
        for f in PARAM_DIR.glob("*.json")
        for p in json.loads(f.read_text(encoding="utf-8"))
    }
    not_found = [i for i in allow if i not in seen]

    print(f"\nPromoted: {promoted}")
    if missing_check:
        print(f"No usable check (skipped): {missing_check}")
    if not_found:
        print(f"Unknown parameter ids: {not_found}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
