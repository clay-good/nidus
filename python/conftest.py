"""Pytest path bootstrap.

Ensures ``import nidus`` works when pytest is invoked from anywhere
(repo root, ``python/``, or ``python/tests``) without requiring an
editable install. Once ``pip install -e python/`` becomes standard
this file can be removed.
"""

from __future__ import annotations

import sys
from pathlib import Path

_HERE = Path(__file__).parent
if str(_HERE) not in sys.path:
    sys.path.insert(0, str(_HERE))
