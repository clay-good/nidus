"""mkdocs hooks for the nidus documentation site.

mkdocs cannot reach files outside ``docs_dir``. This hook copies the
top-level ``notebooks/`` directory into ``docs/notebooks/`` at build
time so that ``mkdocs-jupyter`` can render the notebooks inline.

The destination is gitignored. The hook is wired in via the ``hooks:``
key in ``mkdocs.yml``.
"""

from __future__ import annotations

import shutil
from pathlib import Path
from typing import Any


def on_pre_build(config: Any) -> None:
    docs_dir = Path(config["docs_dir"])
    repo_root = docs_dir.parent
    src = repo_root / "notebooks"
    dst = docs_dir / "notebooks"
    if dst.exists():
        shutil.rmtree(dst)
    if not src.exists():
        return
    shutil.copytree(
        src,
        dst,
        ignore=shutil.ignore_patterns(
            "figures",
            "__pycache__",
            ".ipynb_checkpoints",
            ".DS_Store",
        ),
    )
