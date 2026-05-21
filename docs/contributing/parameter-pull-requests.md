# Parameter Pull Requests

This is the extended version of the parameter-contribution section of
[CONTRIBUTING.md](../../CONTRIBUTING.md). Read CONTRIBUTING.md first
for the project's overall stance on contributions; this page covers
the mechanics of a parameter pull request specifically.

## What counts as a parameter pull request

A pull request that adds, modifies, or retires an entry in
`data/parameters/` or `data/citations/`. The PR template
([.github/PULL_REQUEST_TEMPLATE.md](../../.github/PULL_REQUEST_TEMPLATE.md))
has a section dedicated to parameter contributions; please fill it in
rather than leaving the boilerplate.

## Required fields

Every parameter entry must include:

- `id` — kebab-case, stable across releases.
- `name` — human-readable.
- `description` — one or two sentences.
- `tier` — `A`, `B`, `C`, or `D`.
- `unit` — free-form (the units schema is still informal in v0.1.0).
- `value` — one of `point { value, uncertainty? }`, `uniform { low,
  high }`, `normal { mean, sd }`, or `lognormal { mu, sigma }`.
- `citation` — the id of a corresponding entry in `data/citations/`.
- `population` — enough detail that a reader can assess applicability.
- `age_range { min_weeks, max_weeks }` — gestational coverage.
- `technique` (optional) — measurement modality with known limits.
- `caveats` (optional) — extrapolation hazards.

The TOML schema rejects unknown fields, so typos fail loudly at load
time.

## Review checklist

The reviewer verifies, in this order:

1. **Citation verification.** Open the source. Confirm the parameter
   value matches what the source reports (or that the inferred value
   is a reasonable derivation, documented in `caveats`). Citations
   that cannot be verified are not merged.
2. **Tier assignment.** A Tier A claim requires the parameter to be
   *mechanistic and precisely measured across multiple independent
   studies*. A Tier B claim allows the constants to vary but requires
   the form of the governing equation to be settled. Tier inflation
   is a more serious error than tier deflation.
3. **Population description.** The reader must be able to assess
   applicability. "Adults" is not specific enough; "Adult Norwegian
   women, primigravid, 24–32 weeks gestation" is.
4. **Age range alignment.** The `age_range` covers the gestational
   span the source reports; extrapolation outside that span is noted
   in `caveats`.
5. **Validation suite still passes.** New or modified parameters do
   not break any case in `nidus-validation`.

## Tier promotions and demotions

When a new measurement promotes a parameter from Tier D to Tier C, or
Tier C to Tier B, two things happen:

1. The parameter entry is updated and the citation list is appended
   (the old citations remain, so the history of the parameter is
   visible).
2. The change is recorded in [CHANGELOG.md](../../CHANGELOG.md) under
   that release's `Parameters` subheading, naming the parameter id,
   the old and new tier, and the new citation that motivated the
   promotion.

Tier demotions are also recorded, and reviewed with the same care: a
demotion typically reflects new evidence questioning a prior result,
and the questioning citation is added to the affected parameter's
record.

## Closing the loop

A parameter pull request closes one cycle of the hypothesis-generation
loop described in SPEC.md §10. The simulator generated a hypothesis
(via [`nidus-hypothesis::experiment_design`](../../crates/nidus-hypothesis/src/experiment_design.rs)),
a researcher designed an experiment, the experiment produced a
measurement, and the measurement now updates the simulator's
parameter database. The next sensitivity analysis run will see this
parameter as better-constrained and will recommend a different
parameter as the next most valuable measurement.
