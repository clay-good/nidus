#!/usr/bin/env python3
"""Probe every citation's DOI / PMID / URL for reachability.

Run from the repo root:

    python scripts/check_citation_reachability.py

Exit codes:
    0 — all checkable citations resolved (HTTP 2xx/3xx)
    1 — one or more failed to resolve

The script is run weekly by .github/workflows/citations.yml; failures
there open a tracking issue. Citations of type "book" or any record
without a DOI/PMID/URL are skipped (counted but not failed).
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

import requests

REPO = Path(__file__).parent.parent
CITATIONS = REPO / "dataset" / "citations" / "citations.json"

TIMEOUT_SECONDS = 15
USER_AGENT = "nidus-citation-reachability/0.3 (+https://github.com/claygood/nidus)"


def resolve_url(c: dict) -> str | None:
    if c.get("doi"):
        return f"https://doi.org/{c['doi']}"
    if c.get("pmid"):
        return f"https://pubmed.ncbi.nlm.nih.gov/{c['pmid']}/"
    if c.get("url"):
        return c["url"]
    return None


def probe(url: str) -> int:
    """Return HTTP status code, or -1 on network failure.

    Tries HEAD first; some hosts reject HEAD with 405, in which case we
    fall back to GET with a streaming response (closed immediately).
    """
    headers = {"User-Agent": USER_AGENT}
    try:
        r = requests.head(
            url, allow_redirects=True, timeout=TIMEOUT_SECONDS, headers=headers
        )
        if r.status_code == 405:
            r = requests.get(
                url,
                allow_redirects=True,
                timeout=TIMEOUT_SECONDS,
                headers=headers,
                stream=True,
            )
            r.close()
        return r.status_code
    except requests.RequestException:
        return -1


def main() -> int:
    if not CITATIONS.exists():
        print(f"error: {CITATIONS} not found", file=sys.stderr)
        return 2

    citations: dict[str, dict] = json.loads(CITATIONS.read_text(encoding="utf-8"))

    n_total = len(citations)
    n_checked = 0
    n_skipped = 0
    failures: list[tuple[str, str]] = []

    for key, c in sorted(citations.items()):
        url = resolve_url(c)
        if url is None:
            ctype = c.get("type", "?")
            print(f"  SKIP {key}  (type={ctype}, no DOI/PMID/URL)")
            n_skipped += 1
            continue
        n_checked += 1
        status = probe(url)
        if status == -1:
            print(f"  FAIL {key}  network error -> {url}")
            failures.append((key, f"network error: {url}"))
        elif 200 <= status < 400:
            print(f"  OK   {key}  [{status}] {url}")
        else:
            print(f"  FAIL {key}  HTTP {status} -> {url}")
            failures.append((key, f"HTTP {status}: {url}"))

    print()
    print(f"Total citations:    {n_total}")
    print(f"  checked:          {n_checked}")
    print(f"  skipped (no id):  {n_skipped}")
    print(f"  unreachable:      {len(failures)}")

    if failures:
        print("\nUnreachable:")
        for key, why in failures:
            print(f"  - {key}: {why}")
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
