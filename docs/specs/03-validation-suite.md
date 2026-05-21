# Spec 03 — Validation Suite

## Context

The current validation suite has one case
([`crates/nidus-validation/src/builtin.rs:58-74`](../crates/nidus-validation/src/builtin.rs)),
the `maternal_cardio_scaffold_case`, which compares against a
synthetic reference dataset and is explicitly labelled "Tier-C
placeholder" in
[`crates/nidus-validation/tests/maternal_cardio.rs:153`](../crates/nidus-validation/tests/maternal_cardio.rs).

SPEC.md §13 Prompt 13 names three external reference datasets to
validate against — the NICHD Fetal Growth Studies, published
placental Doppler flow ranges, and fetal cardiovascular developmental
data — none of which are bundled today.

[`docs/validation/`](../docs/validation/) is an empty directory.

A research tool earns trust by reproducing measurements it was not
fitted to. This spec builds the suite that does the earning.

## Deliverables

- `crates/nidus-validation/src/datasets/` — Rust adapters for each
  reference dataset.
- `data/validation/` — reviewable TOML for each dataset's raw values.
- ≥ 8 real validation cases (per-subsystem and integration-level)
  wired into `nidus_validation::builtin::suite()`.
- `nidus validate` Markdown report with per-case pass/fail rows,
  per-subsystem rollups, and dataset citations.
- `docs/validation/` populated with overview, per-case docs, and
  extension guide.

## Dependencies

Requires Spec 01 (parameter database) for citation-linked dataset
entries. Requires Spec 02 (subsystem completion) for the modules that
validation cases exercise — though cases can be drafted in parallel
with module work.

## Numbered prompts

### Prompt 03.1 — Dataset adapter scaffold

Files:
- new [`crates/nidus-validation/src/datasets/mod.rs`](../crates/nidus-validation/src/datasets/mod.rs)
- new `crates/nidus-validation/src/datasets/{nichd_growth,doppler_flow,fetal_cardiac,maternal_hemodynamics}.rs`

Define a common type:

```rust
pub struct Dataset {
    pub name: &'static str,
    pub citation_id: CitationId,
    pub quantity: &'static str,
    pub unit: &'static str,
    pub rows: Vec<DatasetRow>,
}
pub struct DatasetRow {
    pub age_weeks: f64,
    pub mean: f64,
    pub sd: f64,
    pub percentile_5: Option<f64>,
    pub percentile_50: Option<f64>,
    pub percentile_95: Option<f64>,
}
```

Each adapter loads its TOML at startup and caches.

Verification: `cargo test -p nidus-validation datasets` covers a
round-trip per adapter; every row references a citation that
resolves.

### Prompt 03.2 — NICHD growth dataset

File: new [`data/validation/nichd_growth.toml`](../data/validation/nichd_growth.toml).

Encode the NICHD Fetal Growth Studies — Singletons (Buck Louis 2015,
Grewal 2018) percentile rows for estimated fetal weight by
gestational week (14–40 wk). Cite the published table.

The dataset is large; record per-week rows with the 3rd, 10th, 50th,
90th, 97th percentiles. Verify against the published source PDF
during review.

Verification: adapter loads it; spot-check three rows match the
publication exactly; citation resolves.

### Prompt 03.3 — Doppler flow dataset

File: new [`data/validation/doppler_flow.toml`](../data/validation/doppler_flow.toml).

Encode reference ranges for uterine artery PI/RI, umbilical artery
PI/RI, and middle cerebral artery PI by gestational age. Cite Acharya
or equivalent reference range publication.

### Prompt 03.4 — Fetal cardiac dataset

File: new [`data/validation/fetal_cardiac.toml`](../data/validation/fetal_cardiac.toml).

Combined ventricular output (Rudolph 1985 / Mielke & Benda 2001),
heart-rate reference ranges, descending aortic PO₂ measurements (von
Kaisenberg 1999 or Hecher).

### Prompt 03.5 — Maternal haemodynamic dataset

File: new [`data/validation/maternal_hemodynamics.toml`](../data/validation/maternal_hemodynamics.toml).

Cardiac output, MAP, uterine artery flow trajectories from Mahendru
2014 (longitudinal cohort).

### Prompt 03.6 — Validation cases: maternal

File: [`crates/nidus-validation/src/builtin.rs`](../crates/nidus-validation/src/builtin.rs).

Replace the scaffold case with two real cases:
- `maternal_cardiac_output_vs_mahendru` — runs normal-term, extracts
  CO at 12/24/36 wk, compares against dataset means within ±SD.
- `maternal_map_vs_mahendru` — same for MAP, expects mid-pregnancy
  nadir within ±SD of dataset.

Each case includes the dataset citation in the result.

### Prompt 03.7 — Validation cases: placental

Cases:
- `uterine_flow_vs_mahendru` — compares simulator's uterine artery
  flow trajectory.
- `umbilical_pi_vs_doppler_reference` — compares against the Doppler
  flow dataset.

### Prompt 03.8 — Validation cases: fetal

Cases:
- `fetal_weight_vs_nichd` — at 20/28/36 wk, simulator population
  median must fall between the 10th and 90th percentile of NICHD;
  per-tick variability of an ensemble of 200 individuals must cover
  the 3rd–97th band.
- `fetal_hr_vs_reference` — heart-rate trajectory falls within
  reference ranges.
- `descending_aortic_po2_vs_published` — value at 30 wk within
  published bounds.

### Prompt 03.9 — Integration-level case

A whole-system case `placental_insufficiency_growth_restriction`:
runs the placental-insufficiency scenario, asserts the resulting
fetal weight at 36 wk falls below the 10th NICHD percentile in
≥ 70 % of an ensemble of 200 individuals. Sensitivity to seed must
be characterised in the case docstring.

### Prompt 03.10 — Report rendering

File: [`crates/nidus-validation/src/report.rs`](../crates/nidus-validation/src/report.rs).

Extend Markdown rendering: per-subsystem rollup table at the top,
then per-case section with quantity, age points sampled, simulator
mean and SD, dataset mean and SD, pass/fail, and citation. JSON
output schema-stable; document the schema in
`docs/validation/report-schema.md` (Prompt 03.12).

Verification: `nidus validate --format markdown` renders all cases;
`nidus validate --format json | jq '.cases | length'` matches the
expected count.

### Prompt 03.11 — Exit-code semantics

File: [`crates/nidus-cli/src/main.rs`](../crates/nidus-cli/src/main.rs).

`nidus validate` exits 0 if every case passes, exits 1 if any
required case fails, exits 2 only on harness errors (missing data,
load failure). Add `--allow-failures <case_id>...` for known
regressions.

Verification: `nidus validate` on a clean v0.2 build exits 0; mutating
a maternal cardio param to silly values causes exit 1.

### Prompt 03.12 — Validation docs

Files: new
- [`docs/validation/overview.md`](../docs/validation/overview.md)
- [`docs/validation/report-schema.md`](../docs/validation/report-schema.md)
- one `case-<name>.md` per case
- [`docs/validation/extending.md`](../docs/validation/extending.md)

Link all from [`docs/README.md`](../docs/README.md). Each case doc
states: which subsystem, which dataset, the tolerance, why the
tolerance was chosen, citation, current pass/fail status.

### Prompt 03.13 — CI gate

File: [`.github/workflows/ci.yml`](../.github/workflows/ci.yml) (or
new file).

Add a CI job that runs `nidus validate --format json` and fails on
exit code 1. Reports are uploaded as workflow artefacts so reviewers
can read the Markdown.

Verification: a PR introducing a regression in any case fails CI.

## Acceptance for Spec 03

- [ ] ≥ 8 cases in `nidus_validation::builtin::suite()`, none with
  "scaffold" or "placeholder" in their name or notes.
- [ ] Every case cites a verified entry in `data/citations/index.toml`.
- [ ] `nidus validate --format markdown` renders cleanly; report
  includes citations and tier annotations.
- [ ] `docs/validation/` indexed from `docs/README.md`; one page per
  case.
- [ ] CI fails on regressions.
