"""Command-line interface for the nidus package.

After ``pip install nidus``::

    nidus --version
    nidus version
    nidus validate
    nidus validate --path my_dataset/
    nidus info
    nidus info --subsystem maternal_cardiovascular

The CLI is intentionally small — it covers the operations a researcher
would otherwise have to write five-line Python snippets for. Everything
else is the Python API or the dashboard.
"""

from __future__ import annotations

import argparse
import sys
from collections import Counter

from nidus import __version__
from nidus.load import _default_dataset_dir, load
from nidus.models import Citation
from nidus.validate import ValidationError, validate


def cmd_version(_args: argparse.Namespace) -> int:
    print(f"nidus {__version__}")
    return 0


def cmd_validate(args: argparse.Namespace) -> int:
    try:
        target = args.path or _default_dataset_dir()
        validate(path=args.path)
    except FileNotFoundError as e:
        print(f"dataset not found: {e}", file=sys.stderr)
        return 1
    except ValidationError as e:
        print(f"validation failed: {e}", file=sys.stderr)
        return 1
    print(f"OK: dataset at {target} validates against bundled schemas")
    return 0


def cmd_info(args: argparse.Namespace) -> int:
    try:
        ds = load(path=args.path)
    except FileNotFoundError as e:
        print(f"dataset not found: {e}", file=sys.stderr)
        return 1

    if args.subsystem:
        ds = ds.filter(subsystem=args.subsystem)
        if len(ds) == 0:
            known = ", ".join(load(path=args.path).subsystems())
            print(
                f"no parameters match subsystem={args.subsystem!r}. Known subsystems: {known}",
                file=sys.stderr,
            )
            return 2

    tier_counts: Counter[str] = Counter(p.tier for p in ds)
    review_counts: Counter[str] = Counter(p.extraction.review_status for p in ds)
    cited_keys = {c.key for p in ds for c in p.citations}

    print(repr(ds))
    print()
    print(f"Parameters:         {len(ds)}")
    print(f"Subsystems:         {len(ds.subsystems())}")
    print(f"Citations referenced: {len(cited_keys)}")
    print()
    print("Tier distribution:")
    for t in "ABCD":
        bar = "#" * tier_counts.get(t, 0)
        print(f"  {t}: {tier_counts.get(t, 0):>3}  {bar}")
    print()
    print("Review status:")
    for status in ("verified", "pending_human_review", "unverified", "contested"):
        if review_counts.get(status):
            print(f"  {status:<20s}: {review_counts[status]}")
    print()
    if args.subsystem:
        return 0
    print("Parameters per subsystem:")
    for sub in ds.subsystems():
        sub_ds = ds.filter(subsystem=sub)
        print(f"  {sub:<28s} {len(sub_ds):>3}")
    return 0


_BIBTEX_TYPE_MAP = {
    "journal-article": "article",
    "book": "book",
    "book-chapter": "incollection",
    "conference-paper": "inproceedings",
    "preprint": "misc",
    "report": "techreport",
    "dataset": "misc",
    "thesis": "phdthesis",
}


def _citation_to_bibtex(c: Citation) -> str:
    entry_type = _BIBTEX_TYPE_MAP.get(c.type, "misc")
    fields: list[str] = []

    def add(name: str, value: object) -> None:
        if value not in (None, "", []):
            fields.append(f"  {name} = {{{value}}}")

    add("title", c.title)
    add("author", " and ".join(c.authors))
    add("year", c.year)
    if entry_type == "article":
        add("journal", c.journal)
    else:
        add("publisher", c.publisher or c.journal)
    add("volume", c.volume)
    add("number", c.issue)
    add("pages", c.pages)
    add("doi", c.doi)
    add("pmid", c.pmid)
    add("url", c.url)
    add("isbn", c.isbn)
    body = ",\n".join(fields)
    return f"@{entry_type}{{{c.key},\n{body}\n}}"


def cmd_export(args: argparse.Namespace) -> int:
    try:
        ds = load(path=args.path)
    except FileNotFoundError as e:
        print(f"dataset not found: {e}", file=sys.stderr)
        return 1
    if args.format in ("sbml", "cellml", "physiocell", "composed", "omex"):
        from pathlib import Path

        out_dir = Path(args.output) if args.output else Path("exports") / args.format
        try:
            if args.format == "sbml":
                from nidus.export import write_sbml

                written = write_sbml(ds, out_dir)
            elif args.format == "cellml":
                from nidus.export import write_cellml

                written = write_cellml(ds, out_dir, version=args.cellml_version)
            elif args.format == "composed":
                from nidus.export import write_composed_sbml

                written = [write_composed_sbml(ds, out_dir)]
            elif args.format == "omex":
                from nidus.export import write_combine_archive

                out_path = Path(args.output) if args.output else Path("exports/nidus.omex")
                written = [write_combine_archive(ds, out_path)]
            else:  # physiocell
                from nidus.export import write_physiocell

                written = [write_physiocell(ds, out_dir)]
        except ImportError as e:
            print(
                f"export dependency missing: {e}. "
                f"Install with `pip install nidus[export]` "
                f"(or `pip install python-libsbml libcellml` directly).",
                file=sys.stderr,
            )
            return 1
        print(f"Wrote {len(written)} file(s) to {out_dir}:", file=sys.stderr)
        for path in written:
            print(f"  {path}")
        return 0
    if args.format == "bibtex":
        print("\n\n".join(_citation_to_bibtex(c) for c in ds.citations.values()))
        return 0
    if args.format == "csv":
        import csv

        writer = csv.writer(sys.stdout)
        writer.writerow(
            [
                "id",
                "name",
                "subsystem",
                "tier",
                "central",
                "low",
                "high",
                "units",
                "distribution",
                "ci",
                "primary_citation",
                "primary_citation_doi",
                "review_status",
                "n_citations",
            ]
        )
        for p in ds:
            writer.writerow(
                [
                    p.id,
                    p.name,
                    p.subsystem,
                    p.tier,
                    p.value.central,
                    p.value.low,
                    p.value.high,
                    p.value.units,
                    p.value.distribution,
                    p.value.ci,
                    p.primary_citation.key if p.primary_citation else "",
                    p.primary_citation.doi if p.primary_citation else "",
                    p.extraction.review_status,
                    len(p.citations),
                ]
            )
        return 0
    # argparse should prevent this; fall-through for type checker.
    print(f"unknown format: {args.format}", file=sys.stderr)
    return 2


def make_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(
        prog="nidus",
        description="Nidus dataset command-line tools.",
    )
    p.add_argument(
        "--version",
        action="version",
        version=f"nidus {__version__}",
    )
    sub = p.add_subparsers(dest="command", required=True, metavar="COMMAND")

    sp_version = sub.add_parser("version", help="Print the nidus package version")
    sp_version.set_defaults(func=cmd_version)

    sp_validate = sub.add_parser(
        "validate",
        help="Validate a nidus dataset against the bundled JSON Schemas",
    )
    sp_validate.add_argument(
        "--path",
        help="Path to a dataset directory (default: bundled dataset)",
    )
    sp_validate.set_defaults(func=cmd_validate)

    sp_info = sub.add_parser("info", help="Print a summary of a nidus dataset")
    sp_info.add_argument("--path", help="Path to a dataset directory (default: bundled dataset)")
    sp_info.add_argument(
        "--subsystem",
        help="Restrict the summary to a single subsystem",
    )
    sp_info.set_defaults(func=cmd_info)

    sp_export = sub.add_parser(
        "export",
        help="Export the dataset to bibtex, csv, sbml, cellml, or physiocell",
    )
    sp_export.add_argument("--path", help="Path to a dataset directory (default: bundled dataset)")
    sp_export.add_argument(
        "--format",
        choices=["bibtex", "csv", "sbml", "cellml", "physiocell", "composed", "omex"],
        required=True,
        help=(
            "Output format. 'bibtex' = all citations; 'csv' = parameter table; "
            "'sbml' = one SBML L3v2 file per submodel; 'cellml' = one CellML 2.0 "
            "file per submodel; 'physiocell' = drop-in <user_parameters>.xml; "
            "'composed' = single SBML L3v2 file wiring all submodels together; "
            "'omex' = COMBINE archive bundling SBML + CellML + PhysioCell."
        ),
    )
    sp_export.add_argument(
        "--output",
        help=(
            "For sbml/cellml/physiocell: output directory (default: ./exports/<format>/). "
            "Ignored for bibtex/csv which write to stdout."
        ),
    )
    sp_export.add_argument(
        "--cellml-version",
        choices=["2.0", "1.1"],
        default="2.0",
        help="CellML version when --format=cellml. Default 2.0; 1.1 fallback for legacy tools.",
    )
    sp_export.set_defaults(func=cmd_export)

    return p


def main(argv: list[str] | None = None) -> int:
    """Entry point referenced by the ``nidus`` console script."""
    parser = make_parser()
    args = parser.parse_args(argv)
    return int(args.func(args) or 0)


if __name__ == "__main__":
    sys.exit(main())
