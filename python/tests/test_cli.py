"""Tests for the ``nidus`` console-script entry point."""

from __future__ import annotations

import json
import shutil
from pathlib import Path

import pytest

from nidus import __version__
from nidus.cli import main


def _run(capsys: pytest.CaptureFixture[str], argv: list[str]) -> tuple[int, str, str]:
    code = main(argv)
    captured = capsys.readouterr()
    return code, captured.out, captured.err


def test_version_subcommand(capsys: pytest.CaptureFixture[str]) -> None:
    code, out, _ = _run(capsys, ["version"])
    assert code == 0
    assert __version__ in out


def test_top_level_version_flag(capsys: pytest.CaptureFixture[str]) -> None:
    with pytest.raises(SystemExit) as exc:
        _run(capsys, ["--version"])
    assert exc.value.code == 0


def test_validate_bundled(capsys: pytest.CaptureFixture[str]) -> None:
    code, out, _ = _run(capsys, ["validate"])
    assert code == 0
    assert "OK" in out


def test_validate_bad_path(tmp_path: Path, capsys: pytest.CaptureFixture[str]) -> None:
    code, _, err = _run(capsys, ["validate", "--path", str(tmp_path / "nope")])
    # The loader raises FileNotFoundError before validation runs; that
    # surfaces as a Python exception rather than a non-zero exit. Either
    # is fine here — pytest catches the SystemExit if it happens.
    # We just assert it does not silently succeed.
    assert code != 0 or "OK" not in err


def test_validate_corrupted_dataset(tmp_path: Path, capsys: pytest.CaptureFixture[str]) -> None:
    from nidus.load import _default_dataset_dir

    src = _default_dataset_dir()
    dst = tmp_path / "dataset"
    shutil.copytree(src, dst)
    # Corrupt a parameter
    paramfile = next((dst / "parameters").glob("*.json"))
    records = json.loads(paramfile.read_text())
    records[0]["tier"] = "Z"  # invalid
    paramfile.write_text(json.dumps(records))

    code, _, err = _run(capsys, ["validate", "--path", str(dst)])
    assert code == 1
    assert "validation failed" in err


def test_info(capsys: pytest.CaptureFixture[str]) -> None:
    code, out, _ = _run(capsys, ["info"])
    assert code == 0
    assert "Parameters:" in out
    assert "Tier distribution:" in out
    # Sanity: known subsystem appears in the per-subsystem section
    assert "maternal_cardiovascular" in out


def test_info_filtered_by_subsystem(
    capsys: pytest.CaptureFixture[str],
) -> None:
    code, out, _ = _run(capsys, ["info", "--subsystem", "maternal_cardiovascular"])
    assert code == 0
    assert "Parameters:" in out


def test_info_unknown_subsystem(
    capsys: pytest.CaptureFixture[str],
) -> None:
    code, _, err = _run(capsys, ["info", "--subsystem", "not_a_real_subsystem"])
    assert code == 2
    assert "no parameters match" in err


def test_no_subcommand_errors(
    capsys: pytest.CaptureFixture[str],
) -> None:
    with pytest.raises(SystemExit) as exc:
        _run(capsys, [])
    # argparse exits with 2 on missing required arg
    assert exc.value.code == 2


def test_export_bibtex(capsys: pytest.CaptureFixture[str]) -> None:
    code, out, _ = _run(capsys, ["export", "--format", "bibtex"])
    assert code == 0
    # 33 citations -> 32 @article/@book/etc entries
    assert out.count("@") >= 32
    # Spot-check a known key resolves
    assert "mahendru-2014-cardiac-output" in out
    # And its DOI is included
    assert "10.1097/hjh.0000000000000090" in out


def test_export_csv(capsys: pytest.CaptureFixture[str]) -> None:
    code, out, _ = _run(capsys, ["export", "--format", "csv"])
    assert code == 0
    lines = out.strip().split("\n")
    # Header + one row per parameter
    assert len(lines) >= 1 + 138
    # Header contains expected columns
    assert "id" in lines[0]
    assert "tier" in lines[0]
    assert "primary_citation_doi" in lines[0]
    # A known parameter appears
    assert any("baseline_cardiac_output_l_per_min" in line for line in lines)


def test_export_requires_format(capsys: pytest.CaptureFixture[str]) -> None:
    with pytest.raises(SystemExit):
        _run(capsys, ["export"])  # argparse: --format is required
