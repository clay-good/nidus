#!/usr/bin/env python3
"""Copy ``dataset/`` into ``python/nidus/_dataset/`` for packaging.

Hatchling cannot reliably include files from outside the project root
(``python/``) in both the wheel and the sdist. This script copies the
repository's top-level ``dataset/`` directory into the package source
tree under ``python/nidus/_dataset/`` so that the standard packaging
flow picks it up automatically.

The destination is gitignored. Run this before ``python -m build``:

    python scripts/sync_dataset_into_package.py
    cd python && python -m build

Idempotent: removes any existing copy and re-creates it from source.
"""

from __future__ import annotations

import shutil
import sys
from pathlib import Path

REPO = Path(__file__).parent.parent
SRC = REPO / "dataset"
DST = REPO / "python" / "nidus" / "_dataset"


def main() -> int:
    if not SRC.exists():
        print(f"error: source dataset not found at {SRC}", file=sys.stderr)
        return 1
    if DST.exists():
        shutil.rmtree(DST)
    shutil.copytree(SRC, DST, ignore=shutil.ignore_patterns(".DS_Store", "__pycache__"))
    n_files = sum(1 for _ in DST.rglob("*") if _.is_file())
    print(f"Copied {n_files} files: {SRC.relative_to(REPO)} -> {DST.relative_to(REPO)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
