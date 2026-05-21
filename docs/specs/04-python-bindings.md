# Spec 04 — Python Bindings & Notebooks

## Context

[`crates/nidus-py/Cargo.toml`](../crates/nidus-py/Cargo.toml)
self-describes as a placeholder: *"Python bindings for Nidus
(placeholder; PyO3 wiring lands in a later prompt)."* The crate's
[`src/lib.rs`](../crates/nidus-py/src/lib.rs) is a comment file.
There is no `pyo3` dependency. There are no notebooks. The
[`examples/`](../examples/) directory at repo root is empty.

A working biological researcher will reach for Python before Rust. If
Nidus is not importable from a Jupyter notebook, it is effectively
invisible to its target audience.

## Deliverables

- A functioning `nidus` PyPI package built with maturin.
- A `Tiered<T>` Python class that round-trips tier and citations.
- `pandas.DataFrame` outputs for telemetry.
- Three executed Jupyter notebooks under `examples/`.
- A Python API reference doc.
- CI builds wheels for the supported matrix.

## Dependencies

Requires Spec 01 (database) and Spec 02 (subsystems) so the Python
API surfaces real, citation-backed values rather than scaffold ones.

## Numbered prompts

### Prompt 04.1 — PyO3 + maturin project setup

Files:
- [`crates/nidus-py/Cargo.toml`](../crates/nidus-py/Cargo.toml)
- new [`crates/nidus-py/pyproject.toml`](../crates/nidus-py/pyproject.toml)
- new [`crates/nidus-py/python/nidus/__init__.py`](../crates/nidus-py/python/nidus/__init__.py)

Changes:
1. Add `pyo3 = { version = "0.22", features = ["extension-module", "abi3-py39"] }`
   as a dependency.
2. Add `[lib] crate-type = ["cdylib", "rlib"]`.
3. Create `pyproject.toml` declaring maturin as the build backend,
   `requires-python = ">=3.9"`, project name `nidus`, version pulled
   from workspace, description, license.
4. Remove the placeholder language from the crate description.
5. Create a thin Python package layer at
   `python/nidus/__init__.py` that re-exports from the compiled
   `_nidus` module and exposes a clean public API.

Verification: `maturin develop -m crates/nidus-py/Cargo.toml` in a
fresh venv produces an importable `nidus` package; `python -c
"import nidus; print(nidus.__version__)"` matches `Cargo.toml`.

### Prompt 04.2 — `Tiered`, `Citation`, `ConfidenceTier` types

File: [`crates/nidus-py/src/lib.rs`](../crates/nidus-py/src/lib.rs).

Expose:
- `class ConfidenceTier(str enum)` with values `A`, `B`, `C`, `D`.
- `class Citation` carrying `id`, `authors`, `title`, `venue`,
  `year`, `doi`, `pmid`.
- `class Tiered` carrying `.value: float`, `.tier: ConfidenceTier`,
  `.citations: list[Citation]`.

`Tiered`'s `__repr__` shows tier and citation count;
arithmetic operators (`+ - * /`) propagate tier and union citations.

Tests in `crates/nidus-py/tests/test_tiered.py` (pytest discoverable
via maturin), cover construction, propagation, equality.

### Prompt 04.3 — Scenario & RunResult API

File: [`crates/nidus-py/src/scenario.rs`](../crates/nidus-py/src/scenario.rs) (new).

Expose:
- `nidus.Scenario.load_builtin(name: str) -> Scenario` (wraps
  `nidus_scenarios::builtin`).
- `nidus.Scenario.from_toml(path) -> Scenario`.
- `nidus.Scenario.with_override(path: str, value) -> Scenario`.
- `nidus.Scenario.run(seed: int | None = None) -> RunResult`.
- `RunResult.telemetry() -> pandas.DataFrame` (one row per
  telemetry event, columns: tick, age_weeks, quantity, value, unit,
  tier, citations).
- `RunResult.to_ndjson(path)`.
- `RunResult.manifest() -> dict` (after Spec 06).

`pandas` is a soft dependency: import lazily inside `telemetry()`
and surface a clear error if missing.

Verification: `python -c "import nidus; df =
nidus.Scenario.load_builtin('normal_term').run().telemetry();
print(df.head())"` prints a non-empty dataframe with all six columns.

### Prompt 04.4 — Parameter database API

File: [`crates/nidus-py/src/database.rs`](../crates/nidus-py/src/database.rs) (new).

Expose:
- `nidus.ParameterDatabase.load(path: str | None = None)` — loads the
  bundled database when `path` is `None`.
- `.list(tier: str | None = None, search: str | None = None) -> list[ParameterEntry]`.
- `.get(id: str) -> ParameterEntry`.
- `.sha256() -> str`.

`ParameterEntry` exposes id, name, unit, age_range, tier, value
spec (uniform / normal / lognormal / point), citation ids.

Verification: `nidus.ParameterDatabase.load().list(tier='A')`
returns ≥ 25 entries.

### Prompt 04.5 — Hypothesis & sensitivity API

File: [`crates/nidus-py/src/hypothesis.rs`](../crates/nidus-py/src/hypothesis.rs) (new).

Expose:
- `nidus.hypothesis.sensitivity(scenario, parameters, n=1024) -> pandas.DataFrame`
  — Sobol indices on the scenario's outputs.
- `nidus.hypothesis.ensemble(scenario, n=512) -> EnsembleResult`.
- `nidus.hypothesis.experiment_design(scenario, model='placental_gas_exchange', top_k=5)` —
  matches Spec 11's generalisation.

Verification: outputs from the Python API match the Rust example
([`crates/nidus-hypothesis/examples/sensitivity_placental_gas_exchange.rs`](../crates/nidus-hypothesis/examples/sensitivity_placental_gas_exchange.rs))
within Monte Carlo error.

### Prompt 04.6 — Validation API

File: [`crates/nidus-py/src/validation.rs`](../crates/nidus-py/src/validation.rs) (new).

Expose `nidus.validation.run() -> ValidationReport` and
`ValidationReport.to_markdown()`, `.to_dataframe()`.

Verification: `nidus.validation.run().to_dataframe()` returns a
dataframe with one row per case.

### Prompt 04.7 — Quickstart notebook

File: new [`examples/quickstart.ipynb`](../examples/quickstart.ipynb)
(paired with `examples/quickstart.py` via jupytext for diff-ability).

Steps:
1. Install (a one-line `pip install` in the first cell, with a fall-
   back `maturin develop` for source installs).
2. Load `normal_term` scenario, run, show first telemetry rows.
3. Plot maternal cardiac output vs age with tier-coloured ribbon for
   the per-individual SD.
4. Plot fetal weight vs NICHD reference percentiles (from Spec 03).
5. Apply a parameter override (e.g. drop term placental surface by
   40 %), re-run, plot the difference.

Use matplotlib only (no seaborn, plotly). The notebook executes
top-to-bottom via `jupyter nbconvert --execute`; outputs are
committed.

### Prompt 04.8 — Hypothesis notebook

File: new [`examples/hypothesis.ipynb`](../examples/hypothesis.ipynb).

Walks Sobol sensitivity on placental gas exchange, ranks parameters
by total-effect, and emits an experiment-design ranking with
explanatory prose.

### Prompt 04.9 — Validation notebook

File: new [`examples/validation.ipynb`](../examples/validation.ipynb).

Runs the validation suite, shows the pass/fail table, plots the
NICHD comparison overlay, and demonstrates how to add a custom case
from Python (via callback into the Rust suite).

### Prompt 04.10 — Python API reference doc

File: new [`docs/python/README.md`](../docs/python/README.md)
plus a generated reference under `docs/python/reference/`.

Use `pdoc` or `sphinx-autodoc` to render the API. Wire generation
into CI; commit the generated HTML to a `gh-pages`-style branch only
(do not commit it to main).

### Prompt 04.11 — Wheel build matrix

File: new [`.github/workflows/wheels.yml`](../.github/workflows/wheels.yml).

Matrix: { linux-x86_64, linux-aarch64, macos-arm64, macos-x86_64,
windows-x86_64 } × { abi3-py39 }. Uses `PyO3/maturin-action`.

Wheels are uploaded as workflow artefacts. On a tag push, also
publish to PyPI via trusted-publishing (no API tokens). Releases
also upload sdists.

Verification: a tag push to a fork produces wheels for the full
matrix; `pip install --pre nidus` succeeds against test.pypi.org.

## Acceptance for Spec 04

- [ ] `pip install nidus` in a clean venv works (after Spec 08 ships
  to PyPI; before then, `maturin develop` works).
- [ ] All three notebooks execute end-to-end and have committed
  outputs.
- [ ] `Tiered` propagates tier and citations through arithmetic.
- [ ] `examples/quickstart.py` (jupytext export) runs as a plain
  script too.
- [ ] CI builds wheels for the full matrix on every PR.
- [ ] `docs/python/README.md` exists and is linked from the main
  README.
