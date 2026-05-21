"""Shared pytest fixtures."""

from __future__ import annotations

import pytest

import nidus


@pytest.fixture(scope="session")
def ds() -> nidus.Dataset:
    """The bundled dataset, loaded once per test session."""
    return nidus.load()
