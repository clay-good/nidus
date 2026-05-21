# The tier system

Every parameter in nidus carries one of four confidence tiers describing the strength of evidence behind it. The tier system is the most rare and load-bearing thing about the dataset — treat it as central, not decorative.

## Definitions

| Tier | Label              | Criteria                                                                                                                                                                                       |
| ---- | ------------------ | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **A** | Well-established  | Three or more independent peer-reviewed studies · CIs overlap across studies · Mechanism is biophysically grounded · Validated in two or more distinct populations.                            |
| **B** | Supported         | One or two peer-reviewed longitudinal studies (n ≥ 100) · Plausible mechanism · No strong contradicting evidence in the literature.                                                            |
| **C** | Provisional       | Single study, or cross-sectional only, or small n · Mechanism speculative or contested · Used as a model parameter only when no better data exists.                                            |
| **D** | Unknown           | No quantitative data in the published literature · Channel or quantity hypothesised but unmeasured · Listed for hypothesis-generation purposes only.                                           |

The machine-readable definitions live in [`dataset/tiers/tiers.json`](https://github.com/claygood/nidus/blob/main/dataset/tiers/tiers.json).

## Why four levels

- Three feels too coarse — you lose the distinction between "single careful study" and "no quantitative data at all".
- Five or more introduces decision fatigue without epistemic gain.
- A/B/C/D matches established academic conventions, lowering adoption friction for researchers who already use [GRADE](https://www.gradeworkinggroup.org/) and similar frameworks.

## Tier propagation

A derived quantity inherits the **lowest** (worst) tier among its inputs. The reasoning is conservative: a derived quantity cannot be better-supported than its weakest input.

```python
TIER_ORDER = ["A", "B", "C", "D"]

def propagate(*params):
    return max((p.tier for p in params), key=TIER_ORDER.index)
```

Two additional degradations:

- **Out of range.** Tier degrades by one level when a parameter is extrapolated outside its validated `valid_range_weeks` (e.g. a 8–40 week parameter used at week 6).
- **Out of population.** Tier degrades by one level when a parameter is applied outside its `applicability.population` (e.g. a singleton parameter used for a twin pregnancy).

Both degradations stack: a Tier-A parameter used both out-of-range and out-of-population becomes Tier C in the derived quantity.

## Distribution in this dataset

At v0.3.0:

| Tier | Count |
| ---- | ----- |
| A    | 14    |
| B    | 25    |
| C    | 15    |
| D    | 0     |

Tier D is currently empty. Structured open questions land via the [research-question issue template](https://github.com/claygood/nidus/issues/new?template=hypothesis-proposal.yml) and graduate to Tier D entries in the dataset.

## How to assign a tier

When proposing a parameter, choose conservatively. **Tier inflation is a worse error than tier deflation.** When in doubt, drop one level.

A decision tree:

1. **Is there no quantitative literature at all?** → Tier D.
2. **Is there a single study, OR cross-sectional, OR small n (< 100)?** → Tier C.
3. **Is there 1–2 longitudinal studies with n ≥ 100 and plausible mechanism?** → Tier B.
4. **Are there ≥ 3 independent confirmations with overlapping CIs across populations?** → Tier A.

See the [tier-assignment contributing guide](../contributing/tier-assignment.md) for the longer version.
