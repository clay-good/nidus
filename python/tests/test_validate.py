"""Tests for nidus.validate."""

from __future__ import annotations

import json
import shutil
from pathlib import Path

import pytest

import nidus


def test_bundled_dataset_validates() -> None:
    """The shipped dataset must pass its own schemas. If this fails on
    main, the dataset and the schema have drifted apart."""
    nidus.validate()


def test_validate_with_explicit_path() -> None:
    from nidus.load import _default_dataset_dir

    nidus.validate(path=_default_dataset_dir())


def _copy_dataset(tmp_path: Path) -> Path:
    from nidus.load import _default_dataset_dir

    dst = tmp_path / "dataset"
    shutil.copytree(_default_dataset_dir(), dst)
    return dst


def test_bad_tier_value_raises(tmp_path: Path) -> None:
    dst = _copy_dataset(tmp_path)
    paramfile = next((dst / "parameters").glob("*.json"))
    records = json.loads(paramfile.read_text())
    records[0]["tier"] = "Z"  # not in A/B/C/D
    paramfile.write_text(json.dumps(records))
    with pytest.raises(nidus.ValidationError):
        nidus.validate(path=dst)


def test_unknown_citation_reference_raises(tmp_path: Path) -> None:
    dst = _copy_dataset(tmp_path)
    paramfile = next((dst / "parameters").glob("*.json"))
    records = json.loads(paramfile.read_text())
    records[0]["citations"] = ["this-citation-does-not-exist-2099"]
    paramfile.write_text(json.dumps(records))
    with pytest.raises(nidus.ValidationError, match="unknown citation"):
        nidus.validate(path=dst)


def test_citation_key_field_mismatch_raises(tmp_path: Path) -> None:
    dst = _copy_dataset(tmp_path)
    citepath = dst / "citations" / "citations.json"
    cites = json.loads(citepath.read_text())
    first_key = next(iter(cites))
    cites[first_key]["key"] = "wrong-key-on-purpose"
    citepath.write_text(json.dumps(cites))
    with pytest.raises(nidus.ValidationError, match="does not match"):
        nidus.validate(path=dst)


def test_validation_message_caps_errors(tmp_path: Path) -> None:
    """A massively broken dataset should produce a readable, capped error
    summary rather than thousands of lines."""
    dst = _copy_dataset(tmp_path)
    paramfile = next((dst / "parameters").glob("*.json"))
    records = json.loads(paramfile.read_text())
    for r in records:
        r["tier"] = "Z"
    paramfile.write_text(json.dumps(records))
    with pytest.raises(nidus.ValidationError) as exc_info:
        nidus.validate(path=dst)
    # Error message should not blow up on very many errors.
    assert len(str(exc_info.value)) < 50_000
