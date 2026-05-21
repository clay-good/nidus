# Extending the Validation Suite

A new validation case has four moving parts. All four must land in the
same PR, or the case is incomplete:

1. **A reference dataset** — TOML under
   [`data/validation/`](../../data/validation/), with every numeric
   value traceable to a published source. The TOML must reference a
   citation that already resolves in
   [`data/citations/index.toml`](../../data/citations/index.toml);
   if the source is new, add the citation entry first
   (see [the citation README](../../data/citations/README.md)).
2. **A Rust adapter** under
   [`crates/nidus-validation/src/datasets/`](../../crates/nidus-validation/src/datasets/),
   following the
   [`maternal_hemodynamics`](../../crates/nidus-validation/src/datasets/maternal_hemodynamics.rs)
   shape: `include_str!` the TOML, deserialize behind a `OnceLock`
   cache, expose a `&'static Dataset` accessor.
3. **A `ValidationCase` constructor** in
   [`crates/nidus-validation/src/builtin.rs`](../../crates/nidus-validation/src/builtin.rs),
   plumbed into `built_in_cases()`.
4. **A case doc** in this directory (`case-<id>.md`) linked from
   [`overview.md`](overview.md).

## Tolerance choice

Pick the smallest band that the cohort's reported variability can
defend. ±SD around the published mean is the default; widen only if the
case is integration-level (multiple subsystems compose) or the cohort
SD is unrepresentative of the population the case targets. Tier C/D
cases should not invent a tolerance — they land in the `Unvalidatable`
bucket by design.

## Probe wiring

`nidus validate` routes each case's `component` string to a probe
function
([`crates/nidus-cli/src/main.rs`](../../crates/nidus-cli/src/main.rs)).
Add a match arm for the new component, returning the simulator output
sampled at the case's gestational-age points. Cases whose component is
not wired emit NaN and are recorded as `Unvalidatable`; CI treats this
as an authoring error.

## Verification checklist

A reviewer should be able to:

- Open the cited PDF and find every numeric value in the TOML.
- Run `cargo test -p nidus-validation` and see the new case pass.
- Run `cargo run -p nidus-cli -- validate --format markdown` and see
  the new case appear in the per-subsystem rollup.
- Confirm the tolerance choice is defended in the case doc.

## See also

- [`overview.md`](overview.md) — what the suite covers.
- [`report-schema.md`](report-schema.md) — the JSON output schema.
- [`docs/contributing/parameter-pull-requests.md`](../contributing/parameter-pull-requests.md)
  — the same review discipline applies to dataset PRs.
