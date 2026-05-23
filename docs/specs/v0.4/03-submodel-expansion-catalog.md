# Spec 03 — Submodel Expansion Catalog

**Status:** Phase A **complete** (12/12). Phase B **complete** (10/10).
Phase C **complete** (4/4 shipped): `maternal_fetal_igg_transfer`,
`placental_cortisol_gradient`, `maternal_microchimerism_trajectory`,
and `fetal_pulmonary_fluid_trajectory`, all marked
`nidus:reviewStatus = "hypothesis-only"` with "DO NOT USE FOR
PREDICTION" warnings in the SBML/CellML output. Registry totals 41
submodels — the catalog's projected saturation point. Companion to
`02-parameter-expansion-roadmap.md`.
Where `02` inventories candidate *parameters* (data), this spec
inventories candidate *mechanistic submodels* (equations) that could
ship as additional `nidus.export` registry entries beyond the 11
already in v0.4.

**Depends on:** v0.4 export module (`registry.py`, `sbml.py`,
`cellml.py`, `composed.py`).

---

## 1. TL;DR

v0.4 ships 11 mechanistic submodels in SBML / CellML / PhysioCell.
Every submodel is an algebraic or first-order relationship whose
parameters are already curated in the nidus dataset. This spec lists
**~22 additional submodels** that are honest candidates — meaning each
has either a closed-form equation with literature backing or an
ODE/PDE simple enough to encode in a single SBML model.

The selection criterion is *not* "is this physiologically interesting"
(nearly all of pregnancy is). It is:

1. **Equation form is published** (textbook or peer-reviewed paper).
2. **All inputs already are, or could be honestly curated as, nidus
   parameters** at Tier B or better.
3. **The equation runs in well under 1 ms** evaluated in pure NumPy
   on a single timepoint (so the round-trip validation loop stays
   tractable).
4. **Mechanism is dominant** over noise — not e.g. an EHR-derived
   prediction model whose coefficients are dataset-specific.

Submodels are grouped by subsystem; each entry lists the equation
form, the parameter ids it would consume, the citation it would be
annotated with (`bqbiol:isDescribedBy`), and the implementation cost.

If the full catalog ships, nidus exports cover **~33 submodels** — a
realistic saturation point for the declared scope.

## 2. Phase A — high confidence (recommended)

These are submodels with strong citations whose inputs are already in
the v0.3 dataset or are scheduled for Phase 1 of the parameter
expansion roadmap. Each is ~30–80 lines of generator code.

### 2.1 Maternal CO components (stroke volume × heart rate) — **BOTH SHIPPED**

- **Equation:** `CO(t) = SV(t) * HR(t)`
- **Form:** Two Gaussian-bump trajectories whose product yields a
  third, which can be cross-checked against the existing
  `maternal_cardiac_output_trajectory`.
- **Why:** Lets a researcher hold HR fixed and vary SV (or vice versa).
- **Citations:** Mahendru 2014 (PMID 25053730), Sanghavi 2014.
- **Inputs (new):** `maternal_cardiovascular.baseline_stroke_volume_ml`,
  `peak_excess_stroke_volume_ml`, `baseline_heart_rate_bpm`,
  `peak_excess_heart_rate_bpm` + spread/peak weeks.
- **Implementation cost:** ~60 LOC SBML, ~80 LOC CellML, ~30 LOC NumPy.

### 2.2 Systemic vascular resistance trajectory — **SHIPPED**

- **Equation:** `SVR(t) = MAP(t) * 80 / CO(t)` (with the conventional
  80-factor converting mmHg·min/L to dyn·s·cm⁻⁵).
- **Form:** Derived from existing CO + MAP trajectories — pure
  algebraic.
- **Why:** SVR is what hypertension/preeclampsia work actually wants.
- **Citations:** Sanghavi 2014 (PMC4172642).
- **Inputs:** All already in the dataset.
- **Implementation cost:** ~20 LOC; reuses parameters.

### 2.3 Tidal volume + minute ventilation trajectory — **BOTH SHIPPED**

- **Equation:** `VE(t) = VT(t) * RR(t)`; VT rises ~40% by term, RR
  rises modestly.
- **Form:** Sigmoidal VT, near-constant RR.
- **Citations:** LoMauro 2015 (PMID 25624458), Hegewald 2011.
- **Inputs (new):** `maternal_respiratory.baseline_tidal_volume_ml`,
  `term_tidal_volume_ml`, `baseline_respiratory_rate_bpm`,
  `term_respiratory_rate_bpm`.
- **Implementation cost:** ~50 LOC.

### 2.4 Maternal arterial PaO₂ trajectory — **SHIPPED**

- **Equation:** Modest linear rise (≈100 → 105 mmHg) reflecting
  hyperventilation-induced respiratory alkalosis.
- **Form:** Linear interpolation between trimester anchors.
- **Citations:** Templeton & Kelman 1976 (PMID 1247088), Hegewald 2011.
- **Inputs (new):** trimester-1, -2, -3 PaO₂ anchors.
- **Implementation cost:** ~30 LOC.

### 2.5 Acid-base: maternal arterial pH trajectory — **SHIPPED**

- **Equation:** Linear rise from ~7.40 to ~7.44 (compensated
  respiratory alkalosis).
- **Citations:** Hegewald 2011, Lim 1976.
- **Inputs (new):** baseline pH, term pH.
- **Implementation cost:** ~25 LOC.

### 2.6 GFR trajectory (logistic) — **SHIPPED**

- **Equation:** Logistic rise from baseline (~100 mL/min/1.73 m²) to
  ~150 mL/min/1.73 m² peak at ~T2/T3.
- **Citations:** Conrad 2001 (PMID 11489744), Cheung 2013.
- **Inputs:** v0.3 has `baseline_gfr` only — needs peak + peak week +
  spread.
- **Implementation cost:** ~40 LOC.

### 2.7 Renal plasma flow trajectory — **SHIPPED**

- **Equation:** Bell-shaped (rises early, drops near term).
- **Citations:** Dunlop 1981 (PMID 7259294).
- **Inputs (new):** baseline RPF, peak RPF, peak week, spread.
- **Implementation cost:** ~50 LOC.

### 2.8 Fetal abdominal circumference growth (Hadlock biometry) — **SHIPPED**

- **Equation:** Polynomial regression `AC(GA)` in cm vs gestational
  age in weeks.
- **Citations:** Hadlock 1982 (PMID 7058748).
- **Inputs (new):** Hadlock AC polynomial coefficients (a/b/c).
- **Implementation cost:** ~30 LOC; mirrors `hadlock_fetal_weight`.

### 2.9 Fetal femur length growth — **SHIPPED**

- **Equation:** Polynomial `FL(GA)`.
- **Citations:** Hadlock 1982 (PMID 7034201).
- **Inputs (new):** FL polynomial coefficients.
- **Implementation cost:** ~30 LOC.

### 2.10 Fetal biparietal diameter growth — **SHIPPED**

- **Equation:** Polynomial `BPD(GA)`.
- **Citations:** Hadlock 1982.
- **Inputs (new):** BPD polynomial coefficients.
- **Implementation cost:** ~30 LOC.

### 2.11 Fetal head circumference growth — **SHIPPED**

- **Equation:** Polynomial `HC(GA)`.
- **Citations:** Hadlock 1982.
- **Inputs (new):** HC polynomial coefficients.
- **Implementation cost:** ~30 LOC.

### 2.12 Amniotic fluid volume trajectory — **SHIPPED**

- **Equation:** Roughly piecewise: linear rise from 12–22 weeks, plateau
  through ~33 weeks, then decline.
- **Form:** Piecewise polynomial fit to Brace & Wolf 1989.
- **Citations:** Brace & Wolf 1989 (PMID 2782359).
- **Inputs (new):** amniotic fluid volume at trimester anchors; new
  subsystem `amniotic_fluid`.
- **Implementation cost:** ~60 LOC.

## 3. Phase B — moderate confidence (after Phase A lands)

These have either weaker single-source citations or require modest
ODE integration. Each is ~50–150 LOC.

### 3.1 Lactogen / hCG trajectory (placental endocrinology) — **BOTH SHIPPED**

- **Equation:** Sigmoidal for hPL (rises steadily), bell-shaped for
  hCG (peaks ~10 weeks then declines).
- **Citations:** Cole 2010 (PMID 20089136) for hCG kinetics,
  Handwerger 2010 for hPL.
- **Inputs (new):** new `placental_endocrine` subsystem.
- **Note:** Tier C–B; substantial inter-individual variation.
- **Cost:** ~80 LOC across 2 submodels.

### 3.2 Estradiol / progesterone trajectories — **BOTH SHIPPED**

- **Equation:** Sigmoidal rises through gestation.
- **Citations:** O'Leary 1991, Tulchinsky 1972.
- **Inputs (new):** estradiol/progesterone trimester anchors.
- **Cost:** ~60 LOC.

### 3.3 Cortisol diurnal-rhythm trajectory — **SIGMOIDAL TRAJECTORY SHIPPED** (diurnal overlay deferred)

- **Equation:** Cosine on a rising baseline.
- **Citations:** Allolio 1990, Jung 2011.
- **Inputs (new):** baseline + term mean cortisol, diurnal amplitude.
- **Note:** Tier C; diurnal data are sparse longitudinally.
- **Cost:** ~50 LOC.

### 3.4 Thyroid: TSH suppression by hCG — **PIECEWISE-LINEAR SHIPPED** (Hill coupling deferred)

- **Equation:** Inverse relationship via a Hill-like saturation.
- **Citations:** Glinoer 1997, Korevaar 2014.
- **Inputs (new):** TSH baseline, hCG-effect coefficient.
- **Cost:** ~40 LOC.

### 3.5 Insulin resistance trajectory (HOMA-IR) — **SHIPPED**

- **Equation:** Sigmoidal rise through T2/T3.
- **Citations:** Catalano 1991, Sonagra 2014.
- **Inputs (new):** baseline + term HOMA-IR.
- **Cost:** ~40 LOC.

### 3.6 Fetal heart rate trajectory — **SHIPPED**

- **Equation:** Sigmoidal fall from ~170 bpm (T1) to ~140 bpm (term).
- **Citations:** Pildner von Steinburg 2013, von Steinburg 2013.
- **Inputs (new):** baseline + term FHR.
- **Cost:** ~30 LOC.

### 3.7 Umbilical artery pulsatility index trajectory — **SHIPPED**

- **Equation:** Decreasing exponential — PI falls as placental
  resistance falls.
- **Citations:** Acharya 2005 (PMID 15776417).
- **Inputs (new):** baseline + term PI.
- **Cost:** ~40 LOC.

### 3.8 Cerebroplacental ratio (CPR) — **SHIPPED**

- **Equation:** `MCA-PI / UA-PI` — derived; flags fetal compromise
  when < 1.0.
- **Citations:** Baschat 2003.
- **Inputs:** Reuses MCA-PI + UA-PI submodels.
- **Cost:** ~20 LOC; pure algebraic combinator.

### 3.9 Fetal middle cerebral artery PI trajectory — **SHIPPED**

- **Equation:** Bell-shaped — rises then falls.
- **Citations:** Mari 1995 (PMID 7900181).
- **Inputs (new):** trimester anchors.
- **Cost:** ~40 LOC.

### 3.10 Placental weight ~ fetal weight allometry — **SHIPPED**

- **Equation:** `placental_weight = a * (fetal_weight)^b`.
- **Citations:** Hutcheon 2012, Burton 2010.
- **Inputs (new):** allometric a, b.
- **Cost:** ~25 LOC.

## 4. Phase C — speculative / structured open questions

Tier-D / hypothetical models. Encoded for *research-question*
purposes — they make the open question explicit rather than promising
quantitative output. The export carries
`nidus:reviewStatus = "hypothesis-only"` so downstream consumers
cannot accidentally treat them as Tier-A.

- **Maternal-fetal IgG transfer** (FcRn-mediated; transfer ratio rises
  through T3, exact kinetics open) — **SHIPPED** as
  `maternal_fetal_igg_transfer`.
- **Placental cortisol metabolism gradient** (11β-HSD2 saturation —
  textbook qualitative, quantitatively under-pinned) — **SHIPPED** as
  `placental_cortisol_gradient`.
- **Maternal microchimerism uptake/clearance** (cells in maternal
  circulation, dynamics unsettled) — **SHIPPED** as
  `maternal_microchimerism_trajectory` (sigmoidal accumulation; an ODE
  upgrade with explicit uptake/clearance rates remains an open
  research question).
- **Fetal pulmonary fluid secretion → resorption near term** (rate
  curves are species-extrapolated) — **SHIPPED** as
  `fetal_pulmonary_fluid_trajectory`.

All Phase C entries ship with explicit "DO NOT USE FOR PREDICTION"
annotations on the SBML/CellML models.

## 5. Cross-cutting infrastructure additions

Beyond per-submodel work, the catalog suggests a small set of
generator-side improvements that pay off as the registry grows:

- **`registry.expand_polynomial_fit()` helper** — many candidate
  submodels are polynomial regressions in GA. A shared generator that
  takes (coefficients tuple, parameter id) saves ~30 LOC per submodel.
- **Per-submodel reference-kernel parametrization in tests** — already
  applied to `_ALL_SUBMODEL_IDS`; extend to a round-trip parametrized
  test using tellurium for every algebraic submodel.
- **SED-ML simulation descriptor generation** — write a SED-ML XML
  alongside each SBML so the COMBINE archive contains both the model
  AND a canonical simulation experiment. (~80 LOC; standard format,
  well-supported.)
- **Symbolic equation export (Mathjax / LaTeX)** — every submodel
  already carries an English equation in its `description`; emitting
  LaTeX alongside makes the docs much better. **SHIPPED** as
  `nidus.export.equation_latex(submodel_id)` /
  `nidus.export.list_equations()`. ~40 entries covering the
  canonical kernel families (logistic, Gaussian-bump, linear,
  Michaelis-Menten, Hill, polynomial, algebraic combinator,
  piecewise hCG). Returns plain LaTeX fragments suitable for
  MathJax, matplotlib `text(usetex=True)`, or Quarto.
- **Sensitivity-analysis scaffold** — a top-level `nidus.export.sweep`
  utility that re-evaluates a chosen submodel across a parameter
  range and emits a CSV. Pure-Python, ~80 LOC. **SHIPPED.** Exposed
  as `nidus.export.sweep` + `nidus.export.write_sweep_csv`; works
  against any reference kernel from `nidus.export.reference`.

## 6. What is explicitly NOT in this catalog

These are mechanistic but are off-scope for nidus:

- **Labour and delivery mechanics** (uterine activity, cervical
  ripening, force-pressure dynamics). Out of declared scope.
- **Embryonic development before 8 weeks** (organogenesis, gastrulation).
- **Twin / higher-order multiple pregnancy** physiology.
- **Animal-only models** (rodent / primate / sheep gestational
  parameters). Even where excellent data exist, nidus is a *human*
  dataset.
- **Pharmacology / pharmacokinetics**. The pregnancy-PK literature is
  large; that is its own project. Nidus stays in physiology.
- **Population-genetic / ancestry-stratified parameters**. The
  literature is thin and dataset-stratification ethically fraught;
  out of scope.

The boundary is honest scope, not capacity. Many of the excluded
domains are perfectly tractable for a focused project — just a
different focused project.

## 7. Estimated total work

| Phase | Submodels | LOC (gen + tests) | Calendar effort (solo) |
| ----- | --------- | ----------------- | ---------------------- |
| A     | 12        | ~600              | ~2 weeks               |
| B     | 10        | ~900              | ~3 weeks               |
| C     | 4         | ~250              | ~1 week                |

Total ceiling: **33 submodels** (current 11 + 22 here). The dataset
side ceiling (`02-parameter-expansion-roadmap.md`) is **~200
parameters**. Both ceilings are honest stopping points for the project
as scoped; exceeding either implies a scope change that should be
re-litigated against the v0.3 / v0.4 overview specs.

## 8. Implementation policy

When adding a Phase A submodel:

1. Add or promote the underlying parameters in the dataset first;
   ship that as its own PR with explicit verification of every
   citation against Crossref/PubMed.
2. Add the `Submodel` registry entry referencing the new parameter
   ids; the worst-tier propagation should compute correctly.
3. Implement the reference NumPy kernel and add at least one
   sanity-check test against a textbook value.
4. Implement the SBML builder; assert the libSBML consistency check
   passes with zero errors.
5. Implement the CellML builder; verify `libcellml.Validator` is
   clean.
6. Confirm the submodel is automatically included in
   `nidus export --format omex` (it ships once the registry entry
   exists).
7. Update [00-overview.md](00-overview.md) submodel count and the
   README submodel table.
8. Tag the work in `CHANGELOG.md` under `## Unreleased`.

Phase B follows the same flow but with the additional step of
documenting the Tier-C or Tier-D rationale prominently in both the
parameter's `extraction.tier_rationale` and the submodel's
`Submodel.description`. Phase C ships *only* with the
`hypothesis-only` review-status marker and a clear "DO NOT USE FOR
PREDICTION" annotation in both the SBML notes and the README.
