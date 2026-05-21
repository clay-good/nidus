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
    for status in ("verified", "unverified", "contested"):
        if review_counts.get(status):
            print(f"  {status:<12s}: {review_counts[status]}")
    print()
    if args.subsystem:
        return 0
    print("Parameters per subsystem:")
    for sub in ds.subsystems():
        sub_ds = ds.filter(subsystem=sub)
        print(f"  {sub:<28s} {len(sub_ds):>3}")
    return 0


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

    return p


def main(argv: list[str] | None = None) -> int:
    """Entry point referenced by the ``nidus`` console script."""
    parser = make_parser()
    args = parser.parse_args(argv)
    return int(args.func(args) or 0)


if __name__ == "__main__":
    sys.exit(main())
