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


def test_invalid_tier_definition_raises(tmp_path: Path) -> None:
    """If tiers.json itself violates the schema, validate raises."""
    dst = _copy_dataset(tmp_path)
    tierfile = dst / "tiers" / "tiers.json"
    tiers = json.loads(tierfile.read_text())
    tiers["A"]["criteria"] = []  # empty array violates minItems: 1
    tierfile.write_text(json.dumps(tiers))
    with pytest.raises(nidus.ValidationError, match=r"tiers\.json"):
        nidus.validate(path=dst)


def test_citations_must_be_dict_raises(tmp_path: Path) -> None:
    """citations.json must be a dict, not a list or other type."""
    dst = _copy_dataset(tmp_path)
    citepath = dst / "citations" / "citations.json"
    citepath.write_text(json.dumps(["not", "a", "dict"]))
    with pytest.raises(nidus.ValidationError, match="must be a JSON object"):
        nidus.validate(path=dst)


def test_invalid_citation_raises(tmp_path: Path) -> None:
    """A citation that fails its schema produces a citations[key] error."""
    dst = _copy_dataset(tmp_path)
    citepath = dst / "citations" / "citations.json"
    cites = json.loads(citepath.read_text())
    first_key = next(iter(cites))
    cites[first_key]["year"] = 1500  # below schema minimum (1800)
    citepath.write_text(json.dumps(cites))
    with pytest.raises(nidus.ValidationError, match=f"citations\\[{first_key}\\]"):
        nidus.validate(path=dst)


def test_parameter_file_not_an_array_raises(tmp_path: Path) -> None:
    """A parameters/*.json that is an object instead of an array fails."""
    dst = _copy_dataset(tmp_path)
    paramfile = next((dst / "parameters").glob("*.json"))
    paramfile.write_text(json.dumps({"not": "an array"}))
    with pytest.raises(nidus.ValidationError, match="must be a JSON array"):
        nidus.validate(path=dst)


def test_duplicate_parameter_id_raises(tmp_path: Path) -> None:
    """Two parameter records sharing the same id fail validation."""
    dst = _copy_dataset(tmp_path)
    paramfile = next((dst / "parameters").glob("*.json"))
    records = json.loads(paramfile.read_text())
    if len(records) >= 2:
        records[1]["id"] = records[0]["id"]
    else:
        # Defensive: at least one parameter file must have >= 2 records.
        # Duplicate by hand if not.
        records.append(json.loads(json.dumps(records[0])))
    paramfile.write_text(json.dumps(records))
    with pytest.raises(nidus.ValidationError, match="duplicate parameter id"):
        nidus.validate(path=dst)


def test_unknown_primary_citation_raises(tmp_path: Path) -> None:
    """primary_citation must resolve to a known citation key."""
    dst = _copy_dataset(tmp_path)
    paramfile = next((dst / "parameters").glob("*.json"))
    records = json.loads(paramfile.read_text())
    records[0]["primary_citation"] = "imaginary-paper-2099"
    paramfile.write_text(json.dumps(records))
    with pytest.raises(nidus.ValidationError, match="primary_citation"):
        nidus.validate(path=dst)


def test_validation_summary_word_form(tmp_path: Path) -> None:
    """Single-error message uses singular form (no plural)."""
    dst = _copy_dataset(tmp_path)
    paramfile = next((dst / "parameters").glob("*.json"))
    records = json.loads(paramfile.read_text())
    records[0]["tier"] = "Z"
    paramfile.write_text(json.dumps(records))
    with pytest.raises(nidus.ValidationError) as exc_info:
        nidus.validate(path=dst)
    msg = str(exc_info.value)
    # Single error -> "1 error" without trailing s.
    assert "1 error" in msg and "1 errors" not in msg
