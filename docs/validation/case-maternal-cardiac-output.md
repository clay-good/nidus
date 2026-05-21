# Case — Maternal cardiac output vs. Mahendru 2014

- **Case id:** `case:maternal-cardio:cardiac-output`
- **Subsystem:** `nidus-maternal:cardio`
- **Component level:** Component
- **Tier:** B
- **Tolerance:** ±1.0 L/min around the reference mean at each
  gestational-age point.
- **Citation:**
  [`mahendru-2014-cardiac-output`](../../data/citations/index.toml) —
  Mahendru AA et al., *J Hypertens* 32(4):849–856 (2014), a
  longitudinal cohort of cardiac output across pregnancy.

## What the case tests

The maternal cardio subscriber
([`crates/nidus-maternal/src/cardio.rs`](../../crates/nidus-maternal/src/cardio.rs))
computes population-mean cardiac output as a smooth function of
gestational age. The validation case asks: at 12 / 20 / 28 / 32 / 36 /
40 weeks, does the simulator's mean fall within ±1 L/min of the
published trajectory?

## Why the tolerance

±1 L/min is the published cohort SD; it is the smallest band that
encloses physiologically plausible inter-individual variability without
flagging the simulator on noise the model does not claim to reproduce.
A tighter band would require simulating an explicit population, which
is Stream A's responsibility (Spec 10).

## Current status

Passes against the v0.2.0 maternal cardio model with default
database-derived parameters. The case is rerun on every CI build via
`cargo test -p nidus-validation` and is the single end-to-end case
exercised by `nidus validate`.

## See also

- Reference dataset: [`data/validation/maternal_hemodynamics.toml`](../../data/validation/maternal_hemodynamics.toml)
  (loaded by the
  [`maternal_hemodynamics`](../../crates/nidus-validation/src/datasets/maternal_hemodynamics.rs)
  adapter).
- Source citation:
  [`data/citations/index.toml`](../../data/citations/index.toml) — search
  for `mahendru-2014-cardiac-output`.
