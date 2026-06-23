#!/usr/bin/env python3
"""Print the machine-pre-verification context for one or more parameters.

For each parameter id, prints the stored value + metadata and the cached
source evidence (abstract always; a pointer to the full-text cache file when
present, since full text can be tens of thousands of characters and should be
grepped, not dumped).

This is the clean interface the comparison pass (human or subagent) uses, so
nobody has to hunt across dataset/parameters/*.json and
data/validation/sources/*.json by hand.

    python scripts/preverify_context.py <param_id> [<param_id> ...]
    python scripts/preverify_context.py --subsystem maternal_respiratory
    python scripts/preverify_context.py --list-subsystem placental_endocrine
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

REPO = Path(__file__).parent.parent
PARAM_DIR = REPO / "dataset" / "parameters"
SOURCE_DIR = REPO / "data" / "validation" / "sources"
ABSTRACT_CAP = 4000


def load_params() -> dict[str, dict[str, Any]]:
    out: dict[str, dict[str, Any]] = {}
    for f in sorted(PARAM_DIR.glob("*.json")):
        for p in json.loads(f.read_text(encoding="utf-8")):
            out[p["id"]] = p
    return out


def print_one(pid: str, params: dict[str, dict[str, Any]]) -> None:
    p = params.get(pid)
    print("=" * 78)
    if p is None:
        print(f"UNKNOWN PARAMETER: {pid}")
        return
    v = p.get("value", {})
    print(f"PARAMETER : {pid}")
    print(f"name      : {p.get('name')}")
    print(f"tier      : {p.get('tier')}   subsystem: {p.get('subsystem')}")
    print(
        f"value     : central={v.get('central')} low={v.get('low')} "
        f"high={v.get('high')} units={v.get('units')}"
    )
    if p.get("trajectory"):
        print(f"trajectory: {json.dumps(p['trajectory'])}")
    print(f"primary   : {p.get('primary_citation')}")
    print(f"rationale : {p.get('tier_rationale')}")
    if p.get("notes"):
        print(f"notes     : {p.get('notes')}")

    pc = p.get("primary_citation")
    src_file = SOURCE_DIR / f"{pc}.json"
    print("-" * 40)
    if not src_file.exists():
        print(f"SOURCE    : (no cache for {pc}; run scripts/fetch_sources.py)")
        return
    s = json.loads(src_file.read_text(encoding="utf-8"))
    print(f"SOURCE    : evidence={s.get('evidence')}  title={s.get('title_epmc')}")
    if s.get("evidence") == "fulltext":
        print(
            f"full text : grep it -> {src_file.relative_to(REPO)}  ('fulltext' field)"
        )
        abs = s.get("abstract") or ""
        if abs:
            print(f"abstract  : {abs[:ABSTRACT_CAP]}")
    elif s.get("evidence") == "abstract":
        print(f"abstract  : {(s.get('abstract') or '')[:ABSTRACT_CAP]}")
    else:
        print("evidence  : none (book / pre-index / no abstract) -> source_unavailable")


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("ids", nargs="*", help="Parameter ids")
    ap.add_argument("--subsystem", help="Print all params in a subsystem")
    ap.add_argument(
        "--list-subsystem", help="List param ids in a subsystem (one per line)"
    )
    args = ap.parse_args()

    params = load_params()

    if args.list_subsystem:
        for pid, p in params.items():
            if p.get("subsystem") == args.list_subsystem:
                print(pid)
        return 0

    ids = list(args.ids)
    if args.subsystem:
        ids += [
            pid for pid, p in params.items() if p.get("subsystem") == args.subsystem
        ]
    for pid in ids:
        print_one(pid, params)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
