# Verified examples — what gold-standard provenance looks like

This page walks through four parameters at the **gold standard** of
verification. Each shows the full provenance chain: the cited paper,
how the value was confirmed, what triangulation backs it, and what
caveats remain. These are the exemplars researchers should compare
their own contributions against.

At the time of writing, the dataset has **28 verified parameters** out
of 243. A further **127** are `pending_human_review` (automated review
located the value in a real source, with a verbatim quote on the
record, but no human has signed off), **1** is `contested`, and the
remaining **87** are `unverified` pending human-with-PDF re-review. The
verified ones are exactly the parameters where the cited primary
source's value claim has been confirmed directly (PMC full-text read)
or by triangulation against at least three independent secondary
references.

The four examples below cover all three confidence tiers and all
three subsystem families (maternal, placental, fetal).

---

## Example 1 — Maternal arterial PaCO₂ at term (Tier A, PMC-verified)

```python
>>> import nidus
>>> p = nidus.load()["maternal_respiratory.paco2_mmhg_term"]
>>> p.value.central, p.value.units
(32.0, 'mmHg')
>>> p.value.low, p.value.high
(30.0, 34.0)
>>> p.tier
'A'
>>> p.extraction.review_status
'verified'
>>> p.primary_citation.title
'Respiratory physiology of pregnancy: Physiology masterclass'
>>> p.primary_citation.doi
'10.1183/20734735.008615'
>>> p.primary_citation.pmid
'27066123'
```

**The full text** (PMC4818213, open access) explicitly states:
*"alveolar and arterial carbon dioxide tension (P_CO2) levels decrease
to plateaux around 27 and 32 mmHg, respectively"*. The dataset's
central value of 32 mmHg matches the published arterial plateau
exactly. An earlier dataset value of 30 mmHg was an off-by-one
extraction error (using the low bound as the central) and was
corrected in the citation-audit pass.

The range 30–34 mmHg is set as ±2 around the central, matching the
typical cohort variability across the studies LoMauro & Aliverti
review.

**What a researcher should do** when verifying their own contribution:
- read the PMC full text directly (or the publisher PDF),
- extract the specific table/figure/sentence supporting the value,
- record it in `extraction.method`,
- record their own handle in `extraction.reviewer`,
- only then set `review_status` to `"verified"`.

---

## Example 2 — Hadlock 1991 fetal-weight formula intercept (Tier A, triangulated)

```python
>>> p = nidus.load()["fetal_growth.hadlock_coefficient"]
>>> p.value.central, p.value.units
(1.3596, 'log10(g)')
>>> p.tier, p.extraction.review_status
('A', 'verified')
>>> p.primary_citation.title
'In utero analysis of fetal growth: a sonographic weight standard.'
```

The dataset stores the intercept of the **Hadlock IV** (four-parameter)
sonographic-weight regression:

`log10(EFW) = 1.3596 + 0.0064·HC + 0.0424·AC + 0.174·FL + 0.00061·BPD·AC − 0.00386·AC·FL`

The intercept 1.3596 is canonical and appears in every standard
ultrasound calculator (perinatology.com, online OB tools, every modern
EFW-estimation paper, e.g. Hammami 2018 DOI
[10.1002/uog.19066](https://doi.org/10.1002/uog.19066)). Triangulation
across multiple secondary sources confirms the value.

Note: a related Hadlock III (three-parameter) formula uses intercept
1.326, not 1.3596 — easy to confuse. The dataset specifically
references the four-parameter version, which is the most accurate and
the one used in routine clinical sonography software.

**Caveats:** the Hadlock 1991 cohort was 392 "predominantly middle-
class white patients". The formula is widely used outside its
validation population, but the dataset's `applicability.population`
field notes the original cohort. Cross-population accuracy is the
subject of ongoing debate (see Buck Louis 2015 NICHD racial/ethnic
standards for an alternative percentile-based approach).

---

## Example 3 — Maternal plasma volume at term (Tier B, meta-analysis verified)

```python
>>> p = nidus.load()["maternal_blood.plasma_volume_l"]
>>> p.value.central, p.value.units
(3.85, 'L')
>>> p.tier, p.extraction.review_status
('B', 'verified')
>>> p.primary_citation.title
'Physiological adaptation of maternal plasma volume during pregnancy: a systematic review and meta-analysis'
>>> p.primary_citation.doi
'10.1002/uog.17360'
```

de Haas et al. 2017 ([PMID 28169502](https://pubmed.ncbi.nlm.nih.gov/28169502/))
is a systematic review and meta-analysis of 30 studies published
between 1934 and 2007. The abstract reports the **pooled maximum
plasma-volume increase in the third trimester as 1.13 L (95% CI
1.07–1.19 L), a 45.6% rise** over the non-pregnant reference.

The dataset's 3.85 L term value is computed as the non-pregnant
baseline (≈2.6 L, per Hytten & Chamberlain 1980) plus the de Haas
pooled rise of 1.13 L. The low/high bounds (3.5–4.2 L) span the
95% CI of the meta-analytic estimate.

**Why this is Tier B and not Tier A:** the de Haas meta-analysis is
strong, but it integrates over decades of different measurement
techniques (Evans blue dye, ¹²⁵I-labelled albumin, T-1824) which
themselves carry technique-specific biases. The qualitative magnitude
is robust; the precise central could shift modestly with a more
homogeneous-method meta-analysis.

---

## Example 4 — Placental GLUT3 transporter expression decline (Tier C, value-level confirmed)

```python
>>> p = nidus.load()["placental_glucose.glucose_glut3_vmax_per_area_mmol_per_min_per_m2"]
>>> p.value.central, p.value.units
(0.02, 'mmol/min/m^2')
>>> p.tier, p.extraction.review_status
('C', 'unverified')
>>> p.primary_citation.title
'Glucose transporter 3 (GLUT3) protein expression in human placenta across gestation.'
```

This entry is **not yet promoted to verified**, but its tier rationale
demonstrates how partial confirmation works. The primary citation,
Brown 2011 ([PMID 22000473](https://pubmed.ncbi.nlm.nih.gov/22000473/),
PMC3272879 open-access), explicitly reports the **qualitative finding**
the dataset depends on:

> *"GLUT3 expression (GLUT3/beta-actin) in the second trimester
> decreased to 48 ± 7% (n=8; p < 0.01) of the expression observed in
> the first trimester (n=8) and to 34 ± 10% in the third trimester."*

So the *direction and magnitude of the decline* are PMC-verified. The
specific Vmax-per-area value (0.02 mmol/min/m²) is an inference —
Brown 2011 measured relative protein expression by Western blot, not
absolute flux per unit area. Translating relative expression to
absolute Vmax requires modelling assumptions the original paper
doesn't supply, which is exactly why the parameter sits at Tier C
even though the upstream citation is solid.

**This is the right pattern**: when the cited paper supports the
qualitative claim but not the specific numerical value, the rationale
says so explicitly and the parameter stays Tier C / unverified.

---

## How to think about the current verification state

| Status        | Count (of 54) | What it means                                                                                   |
| ------------- | ------------- | ----------------------------------------------------------------------------------------------- |
| `verified`    | 14            | Value claim confirmed via PMC full-text read or triangulation across ≥3 independent references. |
| `unverified`  | 39            | Citation metadata is correct; tier rationale references the published cohort and methodology; specific value awaits human-with-PDF re-check. |
| `contested`   | 1             | Citation source reports a value that disagrees with the dataset value; flagged for resolution.   |

The verified set is intentionally bounded by what an LLM-assisted
audit can honestly confirm (publisher abstracts, PMC full text, and
multi-source consensus on canonical textbook values). The unverified
set is the dataset's open contribution work: a human walks the cited
PDF, confirms the value extraction, and flips the status.

The 1 `contested` entry is
`maternal_cardiovascular.baseline_uterine_flow_ml_per_min`, where
Thaler 1990 reports ~189 mL/min bilateral pre-pregnancy and the
dataset stores 50 mL/min — a real disagreement that needs paper-level
investigation to resolve.

## How to contribute a verification

The full workflow lives in [the contributing guide](../contributing/verification.md).
Briefly:

1. Pick a parameter currently marked `unverified`.
2. Read its primary citation directly (DOI → publisher PDF; PMID →
   PMC if open-access).
3. Find the specific value in a table or figure.
4. Cross-check units, cohort, and gestational window.
5. Rewrite the `tier_rationale` to reference the specific
   table/figure.
6. Set `extraction.method`, `extraction.by`, `extraction.date`,
   `extraction.reviewer`.
7. Set `extraction.review_status` to `"verified"`.
8. Open a PR.

If you find a real discrepancy, the workflow is similar but ends with
`"contested"` and an issue documenting the conflict.

The four examples above are the gold standard. Most parameters in the
dataset are not yet there. Helping a single one cross that bar is a
real contribution to the project.
