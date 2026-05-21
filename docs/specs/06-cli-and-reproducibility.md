# Spec 06 — CLI, Manifest, Reproducibility

## Context

The CLI today (see
[`crates/nidus-cli/src/main.rs`](../crates/nidus-cli/src/main.rs))
ships: `validate`, `hypothesis-report`, `list parameters`, plus the
implicit `run` path consumed by tests. There are gaps:

- No `nidus run <scenario>` high-level command writing structured
  outputs.
- No `nidus doctor` for environment introspection.
- No reproducibility manifest — outputs lack version, seed,
  database hash, scenario hash.
- No `nidus reproduce <manifest>` re-runner.
- No `nidus cite` for software citation (lives in Spec 08).
- No progress indicators on long-running ensembles (audit item 132).
- No CSV export (audit item 107).
- `panic!` paths remain in
  [`telemetry.rs:39`](../crates/nidus-observability/src/telemetry.rs)
  and [`database.rs`](../crates/nidus-data/src/database.rs) (Spec 12
  cleans the rest; this spec fixes the ones the CLI touches).

This spec turns the CLI into something a researcher can drive end-to-
end without writing any code.

## Deliverables

- `nidus run <scenario>`: bundled outputs (NDJSON, CSV, Markdown
  summary, manifest).
- `nidus doctor`: prints toolchain + database + tier coverage.
- `nidus reproduce <manifest>`: byte-identical re-run.
- A documented manifest schema (versioned).
- Progress indicators on long runs.
- `docs/reproducibility.md`.

## Dependencies

Requires Spec 01 (database hash) and Spec 02 (modules) for the
manifest to capture a complete state. Spec 08 (release) consumes
this spec's manifest to produce stable artefacts.

## Numbered prompts

### Prompt 06.1 — `nidus run` subcommand

File: [`crates/nidus-cli/src/main.rs`](../crates/nidus-cli/src/main.rs)
plus new module
[`crates/nidus-cli/src/run.rs`](../crates/nidus-cli/src/run.rs).

Behaviour:
- Args: `nidus run <scenario> [--seed N] [--age-range a-b]
  [--out <dir>] [--emit ndjson|csv|both] [--strict-tier A|B|C]
  [--n-individuals N]`.
- `--out <dir>` (default: `./nidus-run-<timestamp>/`) writes:
  `telemetry.ndjson`, `telemetry.csv`, `summary.md`,
  `manifest.json`, and `report.html` (a static rendering of the
  Markdown summary plus inlined plots produced from the CSV via a
  bundled Python helper or via a Rust plotter — pick the lightest
  path).
- Emits structured progress to stderr (`indicatif`-style bar);
  `--quiet` silences it.

Verification: `nidus run normal_term --out /tmp/x` produces all
four files; `head -1 /tmp/x/telemetry.ndjson` is valid JSON.

### Prompt 06.2 — Manifest schema

File: new [`crates/nidus-cli/src/manifest.rs`](../crates/nidus-cli/src/manifest.rs).
Schema doc: new [`docs/reproducibility.md`](../docs/reproducibility.md).

`Manifest` struct (serde, `deny_unknown_fields`):

```rust
struct Manifest {
    schema_version: u32,         // bump on breaking change
    nidus_version: String,
    git_sha: String,             // from compile-time env
    rust_version: String,
    host_os: String,             // e.g. "linux-x86_64"
    scenario_name: String,
    scenario_sha256: String,     // hash of resolved scenario TOML
    parameter_db_sha256: String, // from Spec 01.9
    rng_seed: u64,
    age_range: (f64, f64),
    n_individuals: u32,
    tick_count: u64,
    started_at_utc: String,      // ISO-8601
    finished_at_utc: String,
    enabled_modules: Vec<String>,
    strict_tier: Option<String>,
}
```

`docs/reproducibility.md` documents every field, the schema-version
bump policy, and what bytes are covered by each hash.

Verification: round-trip test (struct → JSON → struct → equal); a
fresh `nidus run` writes a valid `manifest.json`.

### Prompt 06.3 — Build-time embedding

File: [`crates/nidus-cli/build.rs`](../crates/nidus-cli/build.rs)
(may already exist for Spec 05; extend, don't replace).

Emits `NIDUS_GIT_SHA`, `NIDUS_BUILD_TIMESTAMP`, `NIDUS_RUSTC_VERSION`
as compile-time env vars consumed by `manifest.rs`.

Verification: `nidus doctor` prints a non-empty git SHA matching
`git rev-parse HEAD` on a fresh build.

### Prompt 06.4 — `nidus doctor`

File: [`crates/nidus-cli/src/doctor.rs`](../crates/nidus-cli/src/doctor.rs)
(new).

Prints, all human-readable + `--json` machine-readable:
- Binary version, git SHA, rustc version, OS.
- Parameter database path, hash, parameter count per tier per
  subsystem.
- Loaded scenarios available (`builtin` and discovered TOML).
- Required Python environment for notebooks (best-effort).
- Disk and memory sanity check.

Verification: `nidus doctor --json | jq .parameter_db_sha256`
matches what `ParameterDatabase::sha256()` produces.

### Prompt 06.5 — `nidus reproduce`

File: new [`crates/nidus-cli/src/reproduce.rs`](../crates/nidus-cli/src/reproduce.rs).

Behaviour:
- Args: `nidus reproduce <manifest.json> [--verify <existing-out-dir>]`.
- Loads the manifest, re-resolves scenario by name, asserts every
  hash matches the current build, re-runs with the same seed,
  writes the same output set to a new dir.
- If `--verify` is supplied, diffs the new NDJSON against the
  reference one byte-for-byte and exits non-zero on mismatch.

Verification: `nidus run normal_term --out /tmp/a; nidus reproduce
/tmp/a/manifest.json --verify /tmp/a` exits 0; mutating a
parameter TOML between the two calls causes a clear hash-mismatch
error.

### Prompt 06.6 — CSV exporter

File: new
[`crates/nidus-observability/src/csv.rs`](../crates/nidus-observability/src/csv.rs).

Wide-format CSV: one row per tick, one column per
`(source, quantity)` pair. Headers carry units in parentheses.
Citations and tiers go to a sibling `metadata.csv` indexed by column
name.

Verification: round-trips a small synthetic dataset; `nidus run
... --emit csv` produces parseable output (`csv.DictReader` round-
trip in a Python test).

### Prompt 06.7 — Progress indicators

File: [`crates/nidus-hypothesis/src/ensemble.rs`](../crates/nidus-hypothesis/src/ensemble.rs)
and the relevant CLI sites.

Wrap ensemble + sensitivity loops in `indicatif::ProgressBar`. The
progress bar respects `--quiet` and renders nothing under
`isatty == false` (CI).

Verification: `nidus hypothesis-report --n 1024` shows a live bar
in a terminal; pipe to a file and the bar is suppressed.

### Prompt 06.8 — Convert remaining CLI panics to typed errors

Files: [`crates/nidus-observability/src/telemetry.rs:39`](../crates/nidus-observability/src/telemetry.rs),
[`crates/nidus-data/src/database.rs`](../crates/nidus-data/src/database.rs)
(any `panic!`).

Convert `panic!` to `Result`/`anyhow::Error` with messages that
include the path and the offending value. CLI exits non-zero with a
clear message.

Verification: `cargo clippy --workspace --all-targets -- -D
warnings -D clippy::panic` clean (selectively allowed only in test
modules).

### Prompt 06.9 — `--age-range` sweep helper

File: [`crates/nidus-cli/src/run.rs`](../crates/nidus-cli/src/run.rs).

`--age-range 14-20` restricts the simulator's start/end ages. Adds
a `--sweep <param>=<start>:<end>:<step>` form that runs the same
scenario N times and writes per-sweep telemetry under
`out/sweep/<value>/`.

Verification: `nidus run normal_term --sweep
maternal.cardio.baseline_map_mmhg=80:100:5 --out /tmp/sweep`
produces five subdirectories with manifests.

### Prompt 06.10 — Friendly errors

File: [`crates/nidus-cli/src/main.rs`](../crates/nidus-cli/src/main.rs).

Wrap all subcommands in an `anyhow::Result<()>` entry point;
top-level `eprintln!`s render the error chain + a hint
(`run --strict-tier B` if strict-A fails, etc.). Document
exit-code semantics in `docs/cli-reference.md` (Prompt 07.x).

## Acceptance for Spec 06

- [ ] `nidus run normal_term --out /tmp/x` produces a complete output
  set including manifest.
- [ ] `nidus doctor` prints zero errors on a clean build.
- [ ] `nidus reproduce ... --verify` exits 0 on a same-machine round
  trip.
- [ ] No `panic!` in non-test code paths reached by any CLI
  subcommand.
- [ ] Progress bars visible in terminals, silent in pipes.
- [ ] `docs/reproducibility.md` exists and documents the manifest
  schema.
