# Tutorial: Contributing a Parameter Update

A worked example of the pull-request workflow for parameter
contributions. Read alongside
[CONTRIBUTING.md](../../CONTRIBUTING.md) and the extended notes in
[`docs/contributing/parameter-pull-requests.md`](../contributing/parameter-pull-requests.md).

## The setup

Suppose you have run the hypothesis-generation workflow on a scenario
([`docs/tutorials/hypothesis_workflow.md`](hypothesis_workflow.md))
and the experiment-design suggester named the placental maximum
equilibration coefficient as the highest-yield measurement. You have
designed and executed an experiment that estimates this coefficient
at 0.31 ± 0.04 (95% CI half-width) under standard conditions, and
the result is published in a peer-reviewed venue. You want to merge
this measurement into the parameter database so that future
simulations see a better-constrained value.

## 1. Add the citation

Open `data/citations/index.toml` and add a new `[[citation]]` block:

```toml
[[citation]]
id = "lastname-2026-placental-equilibration"
authors = "Lastname F, Lastname G, Lastname H"
title = "Quantitative measurement of placental gas-exchange equilibration in normal term pregnancy"
venue = "Placenta"
year = 2026
doi = "10.1000/placenta.example"
pmid = "00000000"
notes = "Cohort of N pregnancies at term, gas-exchange equilibration measured by..."
```

The `id` is kebab-case, stable, and conventionally `firstauthor-year-shortdescription`.

## 2. Add or update the parameter

If no parameter for this quantity exists yet, open the most
applicable file under `data/parameters/placenta/` (or create one) and
add a new `[[parameter]]` block:

```toml
[[parameter]]
id = "placenta-gas-exchange-max-equilibration"
name = "Placental gas-exchange maximum equilibration coefficient"
description = "Asymptotic equilibration coefficient between maternal arterial PO₂ and fetal umbilical-vein PO₂ at large placental surface area, used by the venous-equilibrator gas-exchange model."
tier = "B"
unit = "dimensionless"
value = { kind = "point", value = 0.31, uncertainty = 0.04 }
citation = "lastname-2026-placental-equilibration"
population = "Term singleton pregnancies, GA 37–40 wk, ethnically diverse"
age_range = { min_weeks = 37, max_weeks = 40 }
technique = "..."
caveats = "Measurement assumes maternal arterial PO₂ in physiological range; behaviour outside the studied range is extrapolated."
```

The tier sits at B rather than A because, while the form of the
equilibration equation is now settled, a single cohort is not yet
multiple independent confirmations. Tier inflation is more serious
than tier deflation; choose B unless you have grounds to call the
measurement Tier A.

## 3. Update CHANGELOG.md

Under the current `[Unreleased]` section, in the `Parameters`
subheading, add a line:

```
- placenta-gas-exchange-max-equilibration [Tier B, cite:lastname-2026-placental-equilibration] (added)
```

Tier promotions (C → B, B → A) are even more important to record —
they are the visible trace of empirical work advancing the simulator.

## 4. Confirm validation still passes

```sh
cargo test --workspace
cargo clippy --workspace --all-targets -- -D warnings
```

A new parameter must not regress any case in `nidus-validation`. If a
case did regress, that is a signal worth raising in the PR
description: either the new value is at odds with a reference
dataset and the discrepancy needs investigation, or the validation
case is itself out of date and needs updating.

## 5. Open the pull request

Use the parameter-contribution section of the PR template
([`.github/PULL_REQUEST_TEMPLATE.md`](../../.github/PULL_REQUEST_TEMPLATE.md)).
Fill in the structured fields — the reviewer uses them to verify the
citation against its original source. The single most important box
to tick is **"I have personally consulted this source: yes"**;
citations that have not been verified by the contributor are not
merged.

## What happens on merge

1. The next ensemble run of any scenario that depends on this
   parameter sees the new value and the tighter uncertainty.
2. The next sensitivity-analysis run sees the parameter as
   better-constrained and ranks a different parameter as the next
   most valuable measurement.
3. The simulator's overall uncertainty about gestational physiology
   decreases in exactly the region your experiment characterised.

This is the closing-the-loop property described in SPEC.md §10. The
loop does not close inside the software; it closes in the lab and
the clinic. Your contribution is what reaches the software.
