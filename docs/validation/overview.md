# Validation Suite — Overview

The validation suite is how Nidus earns trust: every simulator output
that claims to reproduce a published measurement is checked against the
publication, every tick, every run. A case that diverges by more than
its declared tolerance is a regression; the CLI exits non-zero and CI
fails.

The framework lives in
[`crates/nidus-validation`](../../crates/nidus-validation/). The
single-source list of cases that ship with the binary is
[`nidus_validation::builtin::built_in_cases`](../../crates/nidus-validation/src/builtin.rs),
which is what `nidus validate` runs.

## What the suite covers (v0.2.0)

Each shipped case targets one of three component levels described in
SPEC.md §10 — *component*, *integration*, *outcome* — and carries the
confidence tier of the parameters it tests:

| Case id | Subsystem | Level | Tier | Dataset |
| --- | --- | --- | --- | --- |
| `case:maternal-cardio:cardiac-output` | Maternal | Component | B | [Mahendru 2014](case-maternal-cardiac-output.md) |

The case docs (linked above) record the tolerance choice, the citation,
and the current pass/fail status.

## Tier-aware tolerances

The suite does not score Tier C/D cases on the same axis as Tier A/B:
under-determined parameters can produce outputs that drift far from any
single published cohort without that being a bug. The
[`Agreement`](../../crates/nidus-validation/src/report.rs) classifier
reflects this — Tier C/D cases land in the `Unvalidatable` bucket
unless every point falls strictly inside the reference band. Tier A/B
cases use the four-bucket scale (`Excellent` / `Adequate` / `Divergent`
/ `Unvalidatable`) keyed off RMS residual and in-range counts.

## Running the suite

```sh
cargo run -p nidus-cli -- validate --format markdown
cargo run -p nidus-cli -- validate --format json | jq '.summary'
```

The Markdown form is meant to be readable in a PR description. The JSON
form is schema-stable; see
[`report-schema.md`](report-schema.md).

## What is intentionally not here yet

SPEC_V0.2.md Prompts B1/B2 call for the NICHD growth, placental
Doppler, and fetal cardiac datasets to be wired in as live validation
cases. The Rust adapters
([`crates/nidus-validation/src/datasets/`](../../crates/nidus-validation/src/datasets/))
have a working maternal-hemodynamics implementation; the other three
adapters are waiting on per-dataset TOMLs authored by a contributor
with access to the published source PDFs. The verification workflow is
described in [`extending.md`](extending.md) and follows the same review
checklist as
[`docs/contributing/parameter-pull-requests.md`](../contributing/parameter-pull-requests.md).
