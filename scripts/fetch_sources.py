#!/usr/bin/env python3
"""Fetch source evidence for every citation, for machine pre-verification.

For each record in ``dataset/citations/citations.json`` this queries
Europe PMC (which serves abstracts for nearly everything and open-access
full text for the OA subset) and caches what it finds under
``data/validation/sources/<key>.json``.

The cache is the input to the machine pre-verification pass: a reviewer
(human or machine) compares each parameter's stored value against the
abstract / full text of its primary citation.

The raw source cache is **gitignored** — it contains publishers' abstract
and full-text content. Only our own analysis (short verbatim quotes inside
``data/validation/machine_checks.json``) is committed.

Run from the repo root:

    python scripts/fetch_sources.py            # fetch all, skip cached
    python scripts/fetch_sources.py --force    # re-fetch everything
    python scripts/fetch_sources.py --keys brace-1989-amniotic-fluid ...
"""

from __future__ import annotations

import argparse
import json
import re
import time
from pathlib import Path
from typing import Any

import requests

REPO = Path(__file__).parent.parent
CITATIONS = REPO / "dataset" / "citations" / "citations.json"
CACHE_DIR = REPO / "data" / "validation" / "sources"

EPMC = "https://www.ebi.ac.uk/europepmc/webservices/rest"
USER_AGENT = "nidus-source-fetch/0.3 (+https://github.com/clay-good/nidus; mailto:hi@claygood.com)"
TIMEOUT = 25
SLEEP = 0.34

_WS = re.compile(r"\s+")
_TAG = re.compile(r"<[^>]+>")


def _get(url: str, params: dict[str, Any] | None = None) -> requests.Response | None:
    try:
        r = requests.get(
            url, params=params, headers={"User-Agent": USER_AGENT}, timeout=TIMEOUT
        )
    except requests.RequestException:
        return None
    return r if r.status_code == 200 else None


def epmc_search(query: str) -> dict[str, Any] | None:
    """Return the top Europe PMC 'core' record for a query, or None."""
    r = _get(
        f"{EPMC}/search",
        {"query": query, "resultType": "core", "format": "json", "pageSize": 1},
    )
    if r is None:
        return None
    try:
        results = r.json().get("resultList", {}).get("result", [])
    except ValueError:
        return None
    return results[0] if results else None


def find_record(c: dict[str, Any]) -> dict[str, Any] | None:
    """Resolve a citation to a Europe PMC record by DOI, then PMID, then title."""
    if c.get("doi"):
        rec = epmc_search(f'DOI:"{c["doi"]}"')
        time.sleep(SLEEP)
        if rec:
            return rec
    if c.get("pmid"):
        rec = epmc_search(f"EXT_ID:{c['pmid']} AND SRC:MED")
        time.sleep(SLEEP)
        if rec:
            return rec
    if c.get("title"):
        # Title search is a fallback; confirm the year roughly matches so we
        # do not latch onto an unrelated same-title record.
        rec = epmc_search(f'TITLE:"{c["title"]}"')
        time.sleep(SLEEP)
        if rec:
            try:
                if (
                    not c.get("year")
                    or abs(int(rec.get("pubYear", 0)) - int(c["year"])) <= 1
                ):
                    return rec
            except (ValueError, TypeError):
                return rec
    return None


def fetch_fulltext(rec: dict[str, Any]) -> str | None:
    """If the record is in Europe PMC full text, fetch and flatten it to text."""
    if rec.get("inEPMC") != "Y":
        return None
    pmcid = rec.get("pmcid")
    if not pmcid:
        return None
    r = _get(f"{EPMC}/{pmcid}/fullTextXML")
    if r is None:
        return None
    text = _TAG.sub(" ", r.text)
    text = _WS.sub(" ", text).strip()
    return text or None


def main() -> int:
    p = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    p.add_argument("--force", action="store_true", help="Re-fetch even if cached")
    p.add_argument(
        "--keys", nargs="*", default=None, help="Restrict to these citation keys"
    )
    args = p.parse_args()

    citations: dict[str, dict] = json.loads(CITATIONS.read_text(encoding="utf-8"))
    CACHE_DIR.mkdir(parents=True, exist_ok=True)
    keys = sorted(args.keys) if args.keys else sorted(citations)

    n_oa = n_abstract = n_none = n_cached = 0
    for key in keys:
        if key not in citations:
            print(f"WARN unknown key: {key}")
            continue
        out = CACHE_DIR / f"{key}.json"
        if out.exists() and not args.force:
            n_cached += 1
            continue
        c = citations[key]
        rec = find_record(c)
        record: dict[str, Any] = {
            "key": key,
            "doi": c.get("doi"),
            "pmid": c.get("pmid"),
            "title_local": c.get("title"),
            "found": rec is not None,
        }
        if rec is None:
            record["evidence"] = "none"
            n_none += 1
            print(
                f"  NONE     {key}  (no Europe PMC record; book / pre-index / paywalled)"
            )
        else:
            fulltext = fetch_fulltext(rec)
            record.update(
                {
                    "epmc_id": rec.get("id"),
                    "epmc_source": rec.get("source"),
                    "title_epmc": rec.get("title"),
                    "year_epmc": rec.get("pubYear"),
                    "is_open_access": rec.get("isOpenAccess") == "Y",
                    "abstract": rec.get("abstractText"),
                    "fulltext": fulltext,
                }
            )
            if fulltext:
                record["evidence"] = "fulltext"
                n_oa += 1
                print(f"  FULLTEXT {key}  ({len(fulltext)} chars)")
            elif rec.get("abstractText"):
                record["evidence"] = "abstract"
                n_abstract += 1
                print(f"  ABSTRACT {key}  ({len(rec.get('abstractText', ''))} chars)")
            else:
                record["evidence"] = "none"
                n_none += 1
                print(f"  NONE     {key}  (record found but no abstract/full text)")
        out.write_text(
            json.dumps(record, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
        )

    print()
    print(f"Citations:        {len(keys)}")
    print(f"  already cached: {n_cached}")
    print(f"  full text:      {n_oa}")
    print(f"  abstract only:  {n_abstract}")
    print(f"  no evidence:    {n_none}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
