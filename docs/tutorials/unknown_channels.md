# Tutorial: Exploring an Unknown Channel

This tutorial walks through Nidus's three modes for an unknown
channel — `Disabled`, `Fixed`, and `Sample` — and shows the effect of
each on a downstream observable. Read alongside
[`crates/nidus-unknown/src/registry.rs`](../../crates/nidus-unknown/src/registry.rs)
and SPEC.md §3 / §7 for the conceptual background.

## Setup

The v0.1.0 standard registry ships with four channels:

- `maternal-exosomal-mirna-transfer` (Tier D, dimensionless)
- `cellular-microchimerism` (Tier C, illustrative cell-count scale)
- `maternal-cortisol-diurnal-fetal-hpa` (Tier C, fractional)
- `immunoglobulin-transfer-dynamics` (Tier C, fetal:maternal ratio)

All four ship in `Disabled` mode by default — every scenario starts
from the *minimal-model baseline* and the researcher opts in to
specific hypothesised values or to ensemble sampling.

```rust
use nidus_core::rng::{ChildRng, RngService};
use nidus_core::subscriber::SubscriberId;
use nidus_unknown::{ChannelMode, ChannelRegistry};

let mut registry = ChannelRegistry::standard_v0_1();
let mut rng: ChildRng = RngService::from_u64(42)
    .child_for(&SubscriberId::new("tutorial:unknown"), 0);
```

## Three modes side by side

```rust
let id = "maternal-cortisol-diurnal-fetal-hpa";

// Disabled — minimal-model baseline, value resolves to 0.0.
let disabled = registry.current_value(id, &mut rng).unwrap();
assert_eq!(disabled, 0.0);

// Fixed — researcher pins the channel to a single hypothesised value.
registry.set_mode(id, ChannelMode::Fixed(0.40)).unwrap();
let fixed = registry.current_value(id, &mut rng).unwrap();
assert_eq!(fixed, 0.40);

// Sample — each query returns a fresh uniform draw from [low, high].
registry.set_mode(id, ChannelMode::Sample).unwrap();
let samples: Vec<f64> = (0..1000)
    .map(|_| registry.current_value(id, &mut rng).unwrap())
    .collect();
// Stays inside the channel's documented range.
let ch = registry.channel(id).unwrap();
for v in &samples {
    assert!(*v >= ch.parameter_range.low && *v <= ch.parameter_range.high);
}
```

## What the modes are for

- **`Disabled`** is the right default. It gives the minimal-model
  baseline against which the effect of every other mode is measured.
  Differences between a fully-disabled run and a run that enables one
  channel attribute every observed change to that channel alone.
- **`Fixed`** is the right mode when you are testing a specific
  hypothesis: "what would the simulator predict if maternal cortisol
  transfer were 40% of maternal value?" Pin the channel to 0.40 and
  observe.
- **`Sample`** is what an ensemble run consumes. Ensemble draws across
  the documented range produce an outcome distribution that
  *includes* the channel's uncertainty, rather than hiding it. The
  ensemble runner (
  [`nidus-hypothesis::EnsembleRunner`](../../crates/nidus-hypothesis/src/ensemble.rs))
  reads a channel registry the same way it reads parameter specs.

## Tier-promotion path

A channel begins life at Tier D (suspected but not characterised).
As supporting citations accumulate it can be promoted to Tier C
(observed but not mechanistic), and eventually to Tier B (mechanism
understood, parameters uncertain). Each promotion is recorded in
[CHANGELOG.md](../../CHANGELOG.md) under the release's
`Unknown channels` subheading; the channel's supporting and
questioning citation lists are appended (never replaced) so the
history is visible.

## Where to go next

- [`docs/tutorials/hypothesis_workflow.md`](hypothesis_workflow.md) —
  end-to-end walkthrough that includes channel sampling as part of
  the ensemble step.
- [`crates/nidus-unknown/src/registry.rs`](../../crates/nidus-unknown/src/registry.rs)
  — full API reference for the registry, including the
  `RegistryError` set and the deterministic-ordering contract.
