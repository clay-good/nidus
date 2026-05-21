# Architecture Overview

Read alongside [SPEC.md §§4–8](../../SPEC.md). This page is a
working summary of the architecture as it stands at v0.1.0, not a
re-derivation of the spec.

## Subsystem map

```
┌────────────────────────────────────────────────────────────────────────┐
│                          Researcher-facing surfaces                    │
│  nidus-cli                       (planned: web dashboard, Jupyter)     │
└──────────────┬─────────────────────────────────────────────┬───────────┘
               │                                             │
        ┌──────▼──────┐                              ┌───────▼────────┐
        │ nidus-      │                              │   nidus-       │
        │ scenarios   │                              │   hypothesis   │
        └──────┬──────┘                              └───────┬────────┘
               │                                             │
               │                                             │
        ┌──────▼──────────────────────────────────────────┐  │
        │            Biological model layer                │ │
        │  nidus-maternal  nidus-placenta  nidus-fetal     │ │
        │  nidus-unknown                                    │ │
        └──────┬──────────────────────────────────────────┘  │
               │                                             │
        ┌──────▼──────────────────────────────────────────┐  │
        │   nidus-core (engine: ticks, RNG, dispatcher,    │◄┘
        │   confidence tiers, snapshots, fixed-point)       │
        └──────┬──────────────────────────────────────────┘
               │
        ┌──────▼──────────────────────────────────────────┐
        │   Data + observability + validation              │
        │   nidus-data   nidus-observability               │
        │   nidus-validation                               │
        └──────────────────────────────────────────────────┘
```

## Determinism contract

Two ingredients guarantee bit-identical reproducibility across
architectures (x86, ARM, WebAssembly) and across re-runs:

1. **Integer-only engine arithmetic.** The clock advances in whole
   seconds; biological quantities are stored in Q32.32 fixed-point;
   arithmetic uses checked operations with arithmetic-shift rounding
   (truncation toward negative infinity). See
   [`nidus-core::numerics`](../../crates/nidus-core/src/numerics/).
2. **Per-(subscriber, tick) RNG derivation.** Streams are derived from
   `(master_seed, subscriber_id, tick)` rather than being stateful, so
   reordering subscribers or adding new ones cannot perturb existing
   subscribers' RNG output. See
   [`nidus-core::rng`](../../crates/nidus-core/src/rng.rs).

The end-to-end consequence: any `(seed, scenario)` pair maps to a
unique simulation trajectory whose value is independent of the host
machine and the order in which the engine internally iterates.

## Confidence tier propagation

`nidus-core::Tiered<T>` carries every value, its tier, and the list of
citations that support it. Arithmetic operators on `Tiered<T>` are
implemented to:

- combine values normally (`+`, `-`, `*`, `/`, `Neg`),
- combine tiers via [`ConfidenceTier::combine`] (the less-confident of
  the two inputs wins),
- merge citation lists by deduplicated union.

This is the load-bearing invariant of the project's epistemology: a
Tier B value combined with a Tier C value publishes at Tier C, and the
citations on that combined value remain auditable back to the original
literature.

[`ConfidenceTier::combine`]: ../../crates/nidus-core/src/tier.rs

## Tick hierarchy

Four tiers: `Second`, `Minute`, `Hour`, `Day`. At every tick boundary
the dispatcher iterates subscribers in deterministic id order
(BTreeMap) and fires only those whose tier matches the current
boundary, in fine-to-coarse order. See SPEC.md §6.
