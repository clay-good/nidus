#!/usr/bin/env python3
"""Aggregate per-parameter machine pre-verification checks into a review queue.

Reads the individual check records written under ``data/validation/checks/``
(one ``<parameter_id>.json`` per parameter, produced by the comparison pass)
and emits two committed artifacts:

* ``data/validation/machine_checks.json`` — the structured aggregate.
* ``data/validation/REVIEW_QUEUE.md`` — a human worklist, grouped so a
  researcher can pick the highest-value items first (mismatches and
  Tier A/B first), each with the verbatim supporting quote to confirm.

IMPORTANT: this is a *machine pre-verification* layer. It never changes any
parameter's ``extraction.review_status`` — that promotion stays human-only.
The queue tells a reviewer where to look and what the machine found; the
human reads the source and makes the call.

Run from the repo root:

    python scripts/build_review_queue.py
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

REPO = Path(__file__).parent.parent
PARAM_DIR = REPO / "dataset" / "parameters"
CHECK_DIR = REPO / "data" / "validation" / "checks"
OUT_JSON = REPO / "data" / "validation" / "machine_checks.json"
OUT_MD = REPO / "data" / "validation" / "REVIEW_QUEUE.md"

VERDICTS = ["mismatch", "close", "match", "not_found", "source_unavailable"]
VERDICT_LABEL = {
    "match": "✅ match — source value agrees with stored value",
    "close": "🟡 close — same ballpark, confirm exact figure / statistic",
    "mismatch": "❌ mismatch — source appears to report a different value",
    "not_found": "🔍 not found — value not in fetched text (check table/figure in full PDF)",
    "source_unavailable": "⬜ no source — book / paywalled / no abstract retrieved",
}
TIER_ORDER = {"A": 0, "B": 1, "C": 2, "D": 3}


def load_params() -> dict[str, dict[str, Any]]:
    params: dict[str, dict[str, Any]] = {}
    for f in sorted(PARAM_DIR.glob("*.json")):
        for p in json.loads(f.read_text(encoding="utf-8")):
            params[p["id"]] = p
    return params


def main() -> int:
    params = load_params()
    checks: list[dict[str, Any]] = []
    if CHECK_DIR.exists():
        for f in sorted(CHECK_DIR.glob("*.json")):
            checks.append(json.loads(f.read_text(encoding="utf-8")))

    by_id = {c["parameter_id"]: c for c in checks}
    # Parameters with no check record yet are reported as not-yet-checked.
    for pid in params:
        by_id.setdefault(
            pid,
            {
                "parameter_id": pid,
                "tier": params[pid].get("tier"),
                "subsystem": params[pid].get("subsystem"),
                "primary_citation": params[pid].get("primary_citation"),
                "verdict": "not_checked",
                "evidence_level": "none",
            },
        )
    records = list(by_id.values())

    def sort_key(c: dict[str, Any]) -> tuple:
        return (
            VERDICTS.index(c["verdict"]) if c["verdict"] in VERDICTS else 99,
            TIER_ORDER.get(c.get("tier"), 9),
            c["parameter_id"],
        )

    records.sort(key=sort_key)

    counts: dict[str, int] = {}
    for c in records:
        counts[c["verdict"]] = counts.get(c["verdict"], 0) + 1

    aggregate = {
        "generated_note": (
            "MACHINE PRE-VERIFICATION — NOT human verification. For each parameter, "
            "the primary citation's source text (open-access full text where available, "
            "otherwise the abstract) was fetched via Europe PMC and compared to the "
            "stored value. Every match/close/mismatch verdict carries a verbatim quote "
            "from the source so a human can confirm in seconds. This layer never sets "
            "extraction.review_status; promoting a parameter to 'verified' remains a "
            "human action after reading the source."
        ),
        "counts": counts,
        "total_parameters": len(params),
        "checks": records,
    }
    OUT_JSON.write_text(
        json.dumps(aggregate, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
    )

    # ---- Markdown worklist ---------------------------------------------------
    lines: list[str] = []
    lines.append("# Machine pre-verification review queue")
    lines.append("")
    lines.append(
        "**This is not verification.** A machine fetched each parameter's primary "
        "source (open-access full text where available, otherwise the abstract) and "
        "compared it to the stored value. Your job: read the quote (and, where needed, "
        "the full paper), confirm or correct the value, then set "
        "`extraction.review_status` to `verified` (or `contested`) in the dataset. "
        "The machine never does that promotion."
    )
    lines.append("")
    lines.append("## Summary")
    lines.append("")
    lines.append("| Verdict | Count |")
    lines.append("| ------- | ----- |")
    for v in [*VERDICTS, "not_checked"]:
        if counts.get(v):
            lines.append(f"| {VERDICT_LABEL.get(v, v)} | {counts[v]} |")
    lines.append(f"| **Total parameters** | **{len(params)}** |")
    lines.append("")
    lines.append(
        "Work top-down: mismatches first (a wrong value is worse than an unverified "
        "one), then Tier A/B, then the rest."
    )
    lines.append("")

    for v in VERDICTS:
        group = [c for c in records if c["verdict"] == v]
        if not group:
            continue
        lines.append(f"## {VERDICT_LABEL.get(v, v)}  ({len(group)})")
        lines.append("")
        for c in group:
            p = params.get(c["parameter_id"], {})
            val = p.get("value", {})
            stored = f"{val.get('central')} {val.get('units', '')}".strip()
            lines.append(
                f"### `{c['parameter_id']}`  ·  Tier {c.get('tier')}  ·  stored: {stored}"
            )
            lines.append("")
            lines.append(
                f"- **Primary citation:** `{c.get('primary_citation')}`  "
                f"(_evidence: {c.get('evidence_level')}_)"
            )
            if c.get("source_reports"):
                lines.append(f"- **Source reports:** {c['source_reports']}")
            if c.get("supporting_quote"):
                lines.append(f"- **Quote:** > {c['supporting_quote']}")
            if c.get("note"):
                lines.append(f"- **Reviewer note:** {c['note']}")
            lines.append("")
    OUT_MD.write_text("\n".join(lines) + "\n", encoding="utf-8")

    print(f"Wrote {OUT_JSON.relative_to(REPO)} and {OUT_MD.relative_to(REPO)}")
    print(f"Counts: {counts}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
