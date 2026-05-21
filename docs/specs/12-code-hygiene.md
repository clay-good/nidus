# Spec 12 — Code Hygiene, Error Handling, and Final Polish

## Context

After Specs 01–11 land, the code base will be feature-complete for
v0.2. This spec is the final pass that catches the residue identified
in the audit:

- `panic!` paths in non-test code (audit items 114, 115).
- "scaffolding" docstrings on Params structs that survived only
  because their default constructors were not removed (audit items
  142–146).
- `README.md` listing crates as "(planned)" that are now shipped
  (audit item 156).
- Stale tutorial language, "TBD" labels.
- `CONTRIBUTING.md` sparse for code contributions (audit item 157).
- Error messages without actionable context (audit item 133).
- No `BUILD.md` for setting up a dev environment from scratch.
- `PROGRESS.md` needs a v0.2 section and a v0.3 roadmap.
- `CHANGELOG.md` needs a `## [0.2.0]` entry.

## Deliverables

- Zero `panic!`/`unwrap!`/`expect!` in non-test code (modulo a small
  documented allowlist).
- Every scaffolding docstring removed and replaced by a citation
  pointer.
- All error types documented; user-facing errors carry actionable
  hints.
- README, CONTRIBUTING, PROGRESS, CHANGELOG all reflect v0.2 state.
- A `BUILD.md` covering the developer environment.
- A `ROADMAP.md` covering v0.3+.

## Dependencies

Last spec. Runs after 01–11 to clean up everything else's residue.

## Numbered prompts

### Prompt 12.1 — Eliminate `panic!`/`unwrap!`/`expect!` outside tests

Cross-cutting. Use:

```sh
rg --type rust 'panic!\(|\.unwrap\(\)|\.expect\(' \
   crates/ --glob '!**/tests/**' --glob '!**/benches/**' \
   --glob '!**/examples/**'
```

For each hit outside `#[cfg(test)]`:
- If the path is genuinely unreachable, replace with `unreachable!()`
  and a `// SAFETY:` comment naming the invariant.
- Otherwise, return a typed error.

Specific known sites:
- [`crates/nidus-observability/src/telemetry.rs:39`](../crates/nidus-observability/src/telemetry.rs).
- [`crates/nidus-data/src/database.rs`](../crates/nidus-data/src/database.rs).

A clippy lint enforces this in CI:

```toml
# in Cargo.toml [workspace.lints.clippy]
panic = { level = "deny", priority = -1 }
unwrap_used = "deny"
expect_used = "deny"
```

with module-level `#[allow]`s in test files.

Verification: `cargo clippy --workspace --all-targets -- -D
warnings` clean.

### Prompt 12.2 — Remove scaffolding docstrings

Files: any remaining sites flagged in the audit:
- [`crates/nidus-maternal/src/cardio.rs:71-73`](../crates/nidus-maternal/src/cardio.rs)
- [`crates/nidus-maternal/src/lib.rs:12-14`](../crates/nidus-maternal/src/lib.rs)
- [`crates/nidus-placenta/src/structure.rs:8-9`](../crates/nidus-placenta/src/structure.rs)
- [`crates/nidus-placenta/src/transport.rs:23-24`](../crates/nidus-placenta/src/transport.rs)
- [`crates/nidus-fetal/src/special_circulation.rs:92-93`](../crates/nidus-fetal/src/special_circulation.rs)

After Spec 01 moves defaults to the database, the "scaffolding"
language is stale. Replace with a one-line docstring referencing the
parameter id range now used (e.g. `"Loaded from
maternal.cardio.* via [`MaternalCardioParams::from_database`]."`).

Verification: `rg 'scaffold|placeholder' crates/ --type rust`
returns no matches outside of explicitly-named test fixtures.

### Prompt 12.3 — Error message overhaul

Files: every `Error` enum in the workspace.

For each variant:
- `Display` impl gives the user the path, value, expected vs. found.
- A `hint(&self) -> Option<&str>` returns a suggested next step
  ("did you mean `--strict-tier B`?", "run `nidus doctor` to verify
  the database path"...).
- CLI top-level handler prints hint after the chain.

Specific places:
- `DatabaseError` (Spec 01.x).
- `ScenarioSpec::Error`.
- `Manifest::Error` (Spec 06).
- `RunError`.

### Prompt 12.4 — `BUILD.md`

File: new [`BUILD.md`](../BUILD.md).

Covers, for a contributor on a fresh machine:
- Rust toolchain (`rustup`, the exact MSRV from `Cargo.toml`).
- Python ≥ 3.9 and how to set up a venv.
- `maturin develop -m crates/nidus-py/Cargo.toml`.
- Pre-commit setup.
- Running the full test suite, the dashboard, the docs site.
- Common pitfalls (`pyo3-build-config` on macOS, MSVC on Windows).

Linked from `CONTRIBUTING.md`.

### Prompt 12.5 — `CONTRIBUTING.md` expansion

File: [`CONTRIBUTING.md`](../CONTRIBUTING.md).

Augment the existing parameter-PR workflow with three new sections:
- "Submitting a code change": branch naming, commit style, PR
  template, review expectations, CI requirements.
- "Adding a validation case": link to
  [`docs/validation/extending.md`](../docs/validation/extending.md)
  (Spec 03 Prompt 03.12).
- "Adding a hypothesis model": link to
  [`docs/tutorials/hypothesis_workflow.md`](../docs/tutorials/hypothesis_workflow.md)
  and the trait definition.

### Prompt 12.6 — `PROGRESS.md` v0.2 section

File: [`PROGRESS.md`](../PROGRESS.md).

Add a `## v0.2.0` section with one checkbox per prompt in this spec
set (cross-referenced to `specs/`). Reformat the existing v0.1
section under an explicit `## v0.1.0` heading. Add a `## v0.3+
roadmap` heading at the bottom containing the items pulled from
docs during Spec 07 Prompt 07.13.

### Prompt 12.7 — `CHANGELOG.md`

File: [`CHANGELOG.md`](../CHANGELOG.md).

Add a `## [0.2.0] — YYYY-MM-DD` section under the per-release
subheading convention (Engine, Parameters, Unknown channels,
Validation cases, Python, Dashboard, CLI, Distribution). One entry
per spec.

### Prompt 12.8 — `ROADMAP.md`

File: new [`ROADMAP.md`](../ROADMAP.md).

Captures the explicitly-deferred items (embryonic period, labour and
delivery, twin/higher-order pregnancies — items 134–136), the
"nice-to-have" items pulled out of docs during 07.13, plus any
emergent v0.3 ideas. Linked from README.

### Prompt 12.9 — `clippy.toml` and lint discipline

File: new [`clippy.toml`](../clippy.toml) plus
[`Cargo.toml`](../Cargo.toml) workspace lints.

Strict lint floor:
- `pedantic` warnings.
- `panic` deny (Prompt 12.1).
- `missing_docs` warn at the crate root for public items.
- `as_conversions` deny outside numerics.

Per-crate exceptions documented inline.

### Prompt 12.10 — Doc coverage

File: workspace-level. Run `cargo doc --workspace --no-deps` and
ensure every public type / function has a docstring. Add module-
level docs for any crate root that lacks one.

CI gates on `-D missing_docs` at the crate-root level (not every
private fn).

### Prompt 12.11 — Final repo-wide grep

A finishing sweep: grep for everything that should not exist in a
released repo.

```sh
rg -i 'todo!|fixme|xxx|hack|scaffold|placeholder|wip\b' \
   --type rust --type markdown crates/ docs/ data/ scenarios/ \
   README.md CONTRIBUTING.md
```

Every hit must be triaged: fixed, moved to ROADMAP, or explicitly
documented as a known limitation in the relevant module page.

### Prompt 12.12 — Release rehearsal

After every other prompt is green: cut a `v0.2.0-rc.1` tag, walk the
release workflow from Spec 08, run `scripts/verify-release.sh`,
fix any leftover issues, then cut `v0.2.0`. Update the README badges
to point at the v0.2.0 release.

## Acceptance for Spec 12

- [ ] Zero `panic!`/`unwrap!`/`expect!` outside `#[cfg(test)]` (CI
  enforces).
- [ ] No "scaffold" / "placeholder" / "TODO" strings outside of
  `ROADMAP.md` and `PROGRESS.md`'s historical sections.
- [ ] `BUILD.md` exists; a fresh contributor can build everything by
  following it.
- [ ] `CONTRIBUTING.md` covers code, validation, and hypothesis
  contributions.
- [ ] `PROGRESS.md` has a v0.2 section with checkbox-per-spec.
- [ ] `CHANGELOG.md` has a `## [0.2.0]` entry.
- [ ] `ROADMAP.md` exists and is linked from README.
- [ ] `cargo clippy --workspace --all-targets -- -D warnings` clean.
- [ ] `cargo doc --workspace --no-deps -D warnings` clean.
- [ ] A v0.2.0 release is published with all artefacts.
