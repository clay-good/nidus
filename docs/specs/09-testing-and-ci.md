# Spec 09 — Testing and CI

## Context

The repo's test discipline is solid where it exists — every crate has
inline `#[cfg(test)]` tests, and `cargo test --workspace` covers 114
tests across v0.1. But the audit identifies real gaps:

- No `tests/` integration directories in: `nidus-cli`, `nidus-maternal`,
  `nidus-placenta`, `nidus-fetal`, `nidus-scenarios`, `nidus-hypothesis`,
  `nidus-observability` (audit items 83–89).
- No end-to-end scenario test (audit item 90).
- No reproducibility test (audit item 92).
- No GitHub Actions CI file at present beyond Spec 03/04/05/08
  additions.
- Test coverage is not measured.
- No fuzz targets.
- No benchmarks.
- No determinism regression test crossing OS boundaries.
- No issue templates (`.github/ISSUE_TEMPLATE/`).

This spec is cross-cutting: it overlays on every other spec to make
sure the system stays correct as it grows.

## Deliverables

- Integration test crates for every workspace crate that lacks one.
- A GitHub Actions matrix covering build, clippy, fmt, test, doc,
  Python test, validation, reproducibility, MSRV, coverage.
- Three issue templates.
- Fuzz targets for the parameter loader and numeric layer.
- Criterion benchmarks for the engine inner loop.
- Coverage reporting via `cargo-llvm-cov` uploaded to a public host
  (Codecov or equivalent).

## Dependencies

Cross-cuts everything. Can be worked in parallel with Specs 01–08.

## Numbered prompts

### Prompt 09.1 — Integration test crates

For each of `nidus-cli`, `nidus-maternal`, `nidus-placenta`,
`nidus-fetal`, `nidus-scenarios`, `nidus-hypothesis`,
`nidus-observability`, add a `tests/` directory containing at least
one integration test exercising the public API as a downstream user
would.

Minimum coverage per crate:
- `nidus-cli`: `tests/cli_run.rs` invokes the binary via `assert_cmd`
  and walks `run`, `validate`, `doctor`, `reproduce`, `cite`.
- `nidus-maternal`: scenario harness running each module for a full
  pregnancy and asserting trajectory bounds.
- `nidus-placenta`: end-to-end gas + glucose + AA flux integration.
- `nidus-fetal`: growth trajectory landing inside NICHD percentile
  band given a normal-term scenario.
- `nidus-scenarios`: override stack semantics (already partially
  covered).
- `nidus-hypothesis`: Sobol ranking reproducible at fixed seed.
- `nidus-observability`: NDJSON + CSV round-trip.

Verification: `cargo test --workspace` count rises by ≥ 25.

### Prompt 09.2 — End-to-end determinism test

File: new
[`crates/nidus-cli/tests/determinism.rs`](../crates/nidus-cli/tests/determinism.rs).

Runs the same scenario twice with the same seed via the CLI in two
fresh temp dirs, asserts byte-identical NDJSON outputs. Also asserts
different seeds diverge.

### Prompt 09.3 — Cross-platform determinism in CI

File: [`.github/workflows/ci.yml`](../.github/workflows/ci.yml).

Add a job that runs the determinism test on the full OS matrix
(linux-x86_64, linux-aarch64, macos-arm64, macos-x86_64,
windows-x86_64) and uploads the NDJSON output as a workflow
artefact. A follow-up job downloads all artefacts and diffs them;
any mismatch fails the build.

This is the canonical check that the Q32.32 fixed-point machinery
in [`crates/nidus-core/src/numerics/fixed.rs`](../crates/nidus-core/src/numerics/fixed.rs)
holds across architectures.

### Prompt 09.4 — Reproduce-from-manifest test

File: new
[`crates/nidus-cli/tests/reproduce.rs`](../crates/nidus-cli/tests/reproduce.rs).

Runs `nidus run`, then `nidus reproduce <manifest> --verify
<original>`, asserts exit 0.

### Prompt 09.5 — Python-binding tests

File: new
[`crates/nidus-py/tests/test_scenario.py`](../crates/nidus-py/tests/test_scenario.py)
plus a `pytest.ini` and CI step.

Covers `Tiered` arithmetic, telemetry dataframe shape, manifest
round-trip, parameter listing, ensemble + sensitivity returning
expected columns.

### Prompt 09.6 — Validation regression gate

(Cross-references Spec 03 Prompt 03.13.)

The CI job already lands in Spec 03; ensure it runs on every PR and
on the main branch nightly with the prebuilt artefacts to detect
upstream toolchain regressions.

### Prompt 09.7 — Coverage reporting

File: new [`.github/workflows/coverage.yml`](../.github/workflows/coverage.yml).

Uses `cargo-llvm-cov` for Rust + `coverage.py` for Python. Uploads
combined LCOV to Codecov. PRs comment with delta vs main.

Set a soft floor of 75 % line coverage; below that, CI emits a
warning, not a failure.

### Prompt 09.8 — MSRV job

CI job pinned to the `rust-version` field declared in
[`Cargo.toml`](../Cargo.toml). Build + test only; clippy not gated
on MSRV.

### Prompt 09.9 — Doc build job

CI job runs `cargo doc --workspace --no-deps -D warnings` and uploads
the HTML as a workflow artefact. On the main branch, deploys to
GitHub Pages at `/api/`.

### Prompt 09.10 — Fuzz targets

File: new [`fuzz/`](../fuzz/) directory (`cargo-fuzz` layout).

Targets:
- `fuzz_targets/parameter_loader.rs` — random TOML bytes through
  `ParameterDatabase::load_str`. No panic, no UB.
- `fuzz_targets/scenario_spec.rs` — random TOML bytes through
  `ScenarioSpec::from_str`.
- `fuzz_targets/fixed_arith.rs` — random `Fixed` operations; checked
  semantics never panic or overflow silently.

Add a weekly CI job running each target for ten minutes.

### Prompt 09.11 — Benchmarks

File: new
[`crates/nidus-core/benches/engine.rs`](../crates/nidus-core/benches/engine.rs)
and per-subsystem benches.

`criterion`-based. Benchmarks: full-pregnancy run at minute
resolution; ensemble of 100 individuals; Sobol indices at N=1024.

CI uploads benchmark artefacts; a follow-up issue (not blocking)
can wire `bencher.dev` regression detection.

### Prompt 09.12 — Issue templates

Files: new
- [`.github/ISSUE_TEMPLATE/bug-report.yml`](../.github/ISSUE_TEMPLATE/bug-report.yml)
- [`.github/ISSUE_TEMPLATE/parameter-request.yml`](../.github/ISSUE_TEMPLATE/parameter-request.yml)
- [`.github/ISSUE_TEMPLATE/hypothesis-proposal.yml`](../.github/ISSUE_TEMPLATE/hypothesis-proposal.yml)
- [`.github/ISSUE_TEMPLATE/config.yml`](../.github/ISSUE_TEMPLATE/config.yml)

Bug template asks for: Nidus version, OS, exact command, full output,
manifest if available.

Parameter template asks for: parameter id, proposed value spec,
candidate citations, tier rationale, downstream consumers.

Hypothesis template asks for: hypothesis statement, currently active
unknown channel(s), proposed experiment design, expected effect size.

### Prompt 09.13 — CI matrix consolidation

File: [`.github/workflows/ci.yml`](../.github/workflows/ci.yml).

Single PR workflow with jobs:
- `fmt`: `cargo fmt --check`.
- `clippy`: `cargo clippy --workspace --all-targets -- -D warnings`.
- `build-test`: matrix over OS; `cargo build --workspace`, `cargo
  test --workspace`.
- `doc`: `cargo doc -D warnings`.
- `python`: `maturin build`, `pytest`.
- `validate`: `nidus validate --format json`.
- `determinism`: cross-OS determinism (Prompt 09.3).
- `msrv`: MSRV check.

Cache `~/.cargo` and `target/`. Average PR build under ten minutes.

### Prompt 09.14 — Pre-commit hooks

File: new [`.pre-commit-config.yaml`](../.pre-commit-config.yaml).

Hooks: `cargo fmt`, `cargo clippy --no-deps` (warnings only), `ruff`
for Python, `prettier` for dashboard TypeScript. Document in
`CONTRIBUTING.md`.

## Acceptance for Spec 09

- [ ] Every crate has a `tests/` directory with at least one
  integration test.
- [ ] Cross-OS determinism job green.
- [ ] `nidus reproduce --verify` covered by CI.
- [ ] Coverage reporting active; main-branch baseline established.
- [ ] Three issue templates render on GitHub.
- [ ] Fuzz targets build; weekly fuzz job scheduled.
- [ ] Benchmarks compile (`cargo bench --no-run`).
- [ ] Pre-commit config documented.
- [ ] Average PR build < 10 min.
