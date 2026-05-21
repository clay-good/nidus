# Tier assignment

Choose conservatively. **Tier inflation is a worse error than tier deflation.** When in doubt, drop one level.

## Decision tree

```
Is there any quantitative literature?
├── No  → Tier D (open research question)
└── Yes ↓

Is there a single study, OR cross-sectional only, OR small n (< 100)?
├── Yes → Tier C (provisional)
└── No  ↓

Is there 1–2 longitudinal studies with n ≥ 100 and a plausible mechanism?
├── Yes → Tier B (supported)
└── No  ↓

Are there ≥ 3 independent confirmations with overlapping CIs across populations?
├── Yes → Tier A (well-established)
└── No  → Default to Tier B
```

## Criteria, in detail

### Tier A — Well-established

All four must hold:

1. **≥ 3 independent peer-reviewed studies** report consistent values.
2. **Confidence intervals overlap** across the studies.
3. The **mechanism is biophysically grounded** — the value isn't just a fit; there is a physical reason it takes the range it does.
4. **Validated in ≥ 2 distinct populations** (e.g. nulliparous vs multiparous, or geographically distinct cohorts).

Tier A is rare. Most parameters in pregnancy physiology don't clear all four bars.

### Tier B — Supported

Three loose criteria:

1. **1–2 peer-reviewed longitudinal studies** with reasonable cohort size (n ≥ 100).
2. **Plausible mechanism** — even if the value isn't biophysically derivable from first principles, it fits the broader picture.
3. **No strong contradicting evidence** in the literature.

This is the most common tier in v0.3.

### Tier C — Provisional

Any of:

- **Single study,** OR
- **Cross-sectional only** (no longitudinal data), OR
- **Small n** (< 100).

Plus: the **mechanism is speculative or contested.**

Used only when there is no better data. The downstream consumer needs to know "this is the best we have, treat it with caution".

### Tier D — Unknown

- **No quantitative data** in the published literature.
- The channel or quantity is **hypothesised but unmeasured.**
- Listed for **hypothesis-generation purposes only.**

A Tier D entry is a structured open question; it tells the field what is worth measuring next.

## Tier degradations

Even a Tier-A parameter degrades when applied outside its validated context:

- **Out of range.** Tier degrades by one level when extrapolated outside `valid_range_weeks`. A 12–36 week parameter used at week 8 is Tier B at best.
- **Out of population.** Tier degrades by one level when applied outside `applicability.population`. A singleton parameter used for twins is Tier B at best.

Both degradations stack: a Tier-A parameter used both out-of-range and out-of-population becomes Tier C in the derived quantity. See the [tier system page](../dataset/tiers.md) for the propagation rules.

## How to write a `tier_rationale`

A good rationale is one sentence per claim:

> Multiple longitudinal cohort studies (Mahendru 2014, n=53; Sanghavi 2014 review). CIs overlap across the two cohorts. Mechanism (volume expansion) is biophysically grounded. Validated in nulliparous and multiparous samples.

A bad rationale is hand-waving:

> ~~Pretty well-supported.~~
> ~~Tier B because that feels right.~~

If you can't write the rationale, you don't have enough evidence to assign the tier.

## When to ask for a second opinion

- You think the parameter is Tier A but you're the first to assign it.
- You're promoting an existing Tier B to Tier A.
- The cited paper has obvious methodological issues.

In any of these cases, open a [GitHub Discussion](https://github.com/clay-good/nidus/discussions) before the PR. Tier-A assignments are public-trust claims; a reviewer pair is appropriate.
