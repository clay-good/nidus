# Spec 02 — Parameter Expansion Roadmap

**Status:** Historical / superseded. This spec was the original
planning document for the v0.4 expansion (v0.3 baseline = 70
parameters, 33 citations). The expansion has since shipped and then
some: the dataset now stands at 243 parameters / 71 citations and
**every row in [`04-exhaustive-parameter-catalog.md`](04-exhaustive-parameter-catalog.md)
is `shipped`**. Spec 04 is the source of truth; this spec is kept
for historical reference (it explains *why* the roadmap was phased
the way it was).
**Depends on:** v0.3 dataset schema stable.

---

## 1. TL;DR

The current dataset (v0.3) has 70 parameters and 33 citations. This
spec inventories the realistic ceiling — what's appropriate to add
given the published literature, while staying honest about scope and
verifiability.

If every Phase 1 + Phase 2 + Phase 3 entry in this roadmap is filled,
the dataset reaches **~180-220 parameters across 13 subsystems** with
~60-75 citations. That is the saturation point for the project's
declared scope (8–40 week singleton pregnancy physiology). Beyond
that, the only growth is filling in finer gestational-age resolution
or branching into related domains (twin pregnancies, labour,
embryology) that v0.3 explicitly excluded.

Implementation is phased so each release is shippable on its own.

## 2. Current state (v0.3 baseline)

```
maternal_cardiovascular   17 parameters
maternal_blood            11
maternal_renal             3
maternal_respiratory       7
placental_structure        7
placental_gas_exchange     5
placental_glucose          4
fetal_circulation          5
fetal_growth               7
fetal_metabolism           4
                         ───
                          70
```

33 citations; 28 verified, 41 unverified, 1 contested.

## 3. Gap analysis

Each subsystem has well-supported published values that v0.3 simply
hasn't curated yet. Below: gaps by subsystem with rationale for
adding (and rationale for *not* adding where applicable).

### 3.1 Maternal cardiovascular — under-covered structural/hemodynamic detail

The current 17 params cover the CO/MAP/uterine-flow trajectories
well. Missing:

- **Stroke volume term** (we have baseline only).
- **Systemic vascular resistance** baseline + nadir + term.
- **Pulmonary vascular resistance** (drops in pregnancy).
- **Left ventricular mass** at term (~50% rise).
- **LV wall thickness** at term.
- **Aortic diameter** (mild rise).
- **Pulse wave velocity** (drops mid-pregnancy, rises term).
- **Cardiac output by trimester** (specific T1/T2/T3 values, not just trajectory fit).

Strong-evidence sources: Mahendru 2014 cohort details, Sanghavi 2014,
Hunter & Robson 1992. ~8 new parameters at Tier B.

### 3.2 Maternal blood — coagulation + chemistries gap

Current 11 covers basic haematology and O2-Hb biophysics well. Missing:

- **WBC count term** (rises substantially due to neutrophilia).
- **Coagulation factors II, VII, VIII, IX, X, XII** (all rise — hypercoagulable state).
- **D-dimer term** (rises substantially; complicates VTE diagnosis).
- **Protein S** (functional level falls).
- **Protein C** (essentially unchanged).
- **Fibrinolytic factors** (PAI-1, PAI-2 rise).
- **Serum albumin** (falls ~1 g/dL due to dilution).
- **Total protein** (falls modestly).
- **Serum iron, transferrin saturation, ferritin** (Fe stores drop).
- **B12, folate** (folate falls; B12 modest change).
- **ESR** (rises dramatically due to fibrinogen + plasma changes).

Strong-evidence: Hytten 1980 + modern obstetric haematology
references. ~10-12 new parameters, Tier B.

### 3.3 Maternal renal — currently thin (3 params)

- **Renal blood flow** non-pregnant + peak (~50-80% rise).
- **Filtration fraction** (drops).
- **Cumulative sodium retention** (~1000 mg per Cheung 2013 abstract).
- **Plasma osmolality** drop (10 mOsm/kg, well-replicated).
- **Plasma sodium** drop (~5 mEq/L).
- **Urinary protein excretion term** (~150-200 mg/24h; threshold for proteinuria 300).
- **BUN term** (drops from ~13 to ~8 mg/dL).
- **Plasma uric acid** (drops in mid-pregnancy, rises term — clinically useful).

Strong-evidence: Cheung-Lafayette 2013, Davison-Hytten 1974,
additional renal-in-pregnancy reviews. ~6-8 new parameters, Tier A/B.

### 3.4 Maternal respiratory — minor gaps

Current 7 covers blood gases + ventilation well. Missing:

- **Respiratory rate term** (essentially unchanged ~16/min — useful for completeness).
- **Inspiratory capacity term** (rises modestly).
- **Total lung capacity term** (essentially unchanged).
- **DLCO** (small drop).
- **A-a O2 gradient** at term (mild widening).
- **Maternal CO2 production** (rises ~15-20% per LoMauro).

Strong-evidence: LoMauro 2015 (already in dataset), Crapo 1996. ~5 new
parameters, Tier B.

### 3.5 Placental structure — anatomical detail gap

- **Placental thickness term** (~2.5 cm).
- **Cord length** at term (~55 cm, well-characterised).
- **Number of cotyledons** (~15-20).
- **Villous capillary length total** (~280-320 km — striking statistic).
- **Intervillous space volume** at term.
- **Spiral artery count, diameter, flow** (relevant to PE pathophysiology).

Strong-evidence: Mayhew 2014 morphomics, Boyd & Hamilton anatomy
references. ~5 new parameters, Tier B/C.

### 3.6 Placental gas exchange — now reasonably populated (5 params)

Could add:
- **CO2 diffusing capacity** at term.
- **Maternal-fetal PCO2 gradient** (umbilical artery > umbilical vein > maternal intervillous).
- **Carter-Pijnenborg 2011 spiral artery PO2 estimate**.

Strong-evidence: Carter 2009 + Mayhew 1986 morphometry. ~3 new parameters.

### 3.7 Placental glucose — could add net flux

- **Maternal-fetal glucose gradient** at term.
- **Net trans-placental glucose flux** per kg fetal weight.
- **GLUT4 expression** (cytotrophoblast — out of scope?).

Strong-evidence: Illsley 2000, Cleal-Lewis 2008. ~2-3 new parameters.

### 3.8 Fetal circulation — under-covered (5 params)

- **Umbilical vein flow** mL/min and per kg fetal weight.
- **Combined ventricular output** mL/min/kg.
- **Aortic isthmus flow** as fraction of CVO.
- **Middle cerebral artery flow** (clinically useful — brain-sparing).
- **Coronary artery flow** (well-oxygenated stream preferentially routed).
- **Cardiac output partition** (RV ~65%, LV ~35% in fetus, opposite of adult).

Strong-evidence: Rudolph 1985, Sutton 1991, Kiserud 2001. ~5 new
parameters, Tier B/C.

### 3.9 Fetal growth — multi-gestational-age expansion

Currently has only 28w BPD/FL and 20/28/36/40w EFW. Expand to **every
4 weeks** for BPD, HC, AC, FL, EFW from 16-40w. That's:

- BPD: 16, 20, 24, 28, 32, 36, 40w (current 28 only) — +6
- HC: 16, 20, 24, 28, 32, 36, 40w — +7 (no current)
- AC: 16, 20, 24, 28, 32, 36, 40w — +7 (no current)
- FL: 16, 20, 24, 28, 32, 36, 40w (current 28 only) — +6
- EFW: 16, 24, 32 (currently 20, 28, 36, 40) — +3
- Birth weight, birth length (post-term) — +2 (with `applicability` caveat)

~31 new parameters at Tier A from Buck Louis 2015 / Grewal 2018
NICHD cohort tables.

### 3.10 Fetal metabolism — clinical chemistry gap

- **Fetal pH** (umbilical arterial ~7.27, umbilical venous ~7.34).
- **Fetal lactate** at term.
- **Fetal glucose** (~70-75% of maternal).
- **Fetal insulin** (low; develops late).
- **Fetal cortisol** (rises late in gestation — surge initiates labour).
- **Fetal core temperature** (~0.5°C above maternal).
- **Fetal urine output** (substantial — accounts for AFV).

Strong-evidence: Battaglia & Meschia 1986, Carter 2009. ~5-6 new
parameters, Tier B/C.

## 4. New subsystems to add (Phase 3)

### 4.1 `placental_endocrine` — currently entirely absent

Placental hormone production is a substantial gap. Well-supported
parameters:

- **hCG peak concentration** (~100,000 mIU/mL at week 8-10, falls thereafter).
- **hCG term value** (~10,000 mIU/mL).
- **Progesterone term** (~150 ng/mL).
- **Estriol term** (~10 ng/mL).
- **Placental lactogen (hPL) term** (~5-10 µg/mL).
- **Relaxin first trimester** (~1 ng/mL).
- **Leptin term** (~10x non-pregnant).

Strong-evidence: standard reproductive endocrinology references. ~7
new parameters, Tier B.

### 4.2 `maternal_endocrine` — currently entirely absent

- **Cortisol peak term** (~3x non-pregnant baseline).
- **CBG (cortisol-binding globulin)** rise.
- **Free T4** (slight fall).
- **TSH first trimester** (suppressed by hCG cross-reactivity).
- **Insulin sensitivity index** at term (drops ~50%).
- **Prolactin term** (~10x non-pregnant).
- **Aldosterone term** (rises ~5-10x).

Strong-evidence: Cheung 2013 (renin-aldosterone), standard endocrine
texts. ~7 new parameters, Tier B.

### 4.3 `amniotic_fluid` — currently absent

- **AFV by gestational week** (peaks ~32-34w at ~800 mL).
- **AFV composition**: glucose, lactate, creatinine, osmolality.
- **Fetal urine contribution to AFV**.
- **Swallowing/absorption rate**.

Strong-evidence: standard obstetric references. ~5 new parameters,
Tier B/C.

### 4.4 (Considered and deferred) — `fetal_endocrine`

Fetal hormones (fetal cortisol, fetal thyroid, fetal insulin) are
biologically important but quantitatively sparse in the human
literature (most data is from animal models). Defer to v0.5 if
demand emerges.

### 4.5 (Considered and rejected) — `maternal_immune`

Quantitative tolerance/rejection markers in human pregnancy are
mostly Tier-D in the literature. Listed as Tier D entries in the
"open research questions" channel instead.

## 5. Phased implementation plan

### Phase 1 (v0.4.x) — Highest-leverage gaps

Target: 70 → ~110 parameters. Focus on filling the existing 10
subsystems with multi-week growth-curve resolution and the most
clinically-cited values.

- Fetal growth multi-age expansion (BPD/HC/AC/FL/EFW at every 4w): +31
- Maternal renal (RBF, FF, osmolality, Na, BUN, uric acid): +5
- Maternal blood (WBC, fibrinogen-already-in, D-dimer, albumin, ferritin): +5

That's ~41 new parameters. Each requires either NICHD-cohort table
extraction (Buck Louis 2015 already cited) or a paywall-limited
literature consultation. Realistic completion: ~2-3 weeks of
careful curation.

### Phase 2 (v0.5) — New subsystem additions

Target: ~110 → ~155 parameters; 10 → 13 subsystems.

- New `placental_endocrine` (7 parameters).
- New `maternal_endocrine` (7 parameters).
- New `amniotic_fluid` (5 parameters).
- Maternal cardiovascular detail (LV mass, PVR/SVR, pulse wave): +6
- Fetal circulation detail (umbilical flow per kg, CVO, MCA): +5
- Fetal metabolism clinical chemistry (pH, lactate, glucose, cortisol): +5

~35 new parameters. Adding new subsystems requires schema enum
updates (the `subsystem` field in `parameter.schema.json`); this is
the substantive structural change for v0.5.

### Phase 3 (v0.6+) — Saturation

Target: ~155 → ~200 parameters. Filling-in pass: every parameter
listed in §3 above that hasn't landed yet. Diminishing returns.

## 6. Citations needed (Phase 1 + 2)

Most of Phase 1 is covered by citations already in the dataset
(Buck Louis 2015, Grewal 2018, Cheung 2013, LoMauro 2015, Hytten
1980, Mayhew 2014, Carter 2009).

New citations needed for Phase 2:

| Subsystem | Likely primary source |
| --- | --- |
| placental_endocrine | Speroff & Fritz *Clinical Gynecologic Endocrinology and Infertility* (textbook); Cole et al. hCG reviews |
| maternal_endocrine | Burrow et al. *Medical Complications During Pregnancy* (textbook); Glinoer 1997 (thyroid in pregnancy) |
| amniotic_fluid | Brace 1997 (AFV regulation); Magann et al. AFV studies |
| LV mass | Robson et al. 1989 *Br Heart J* (LV mass in pregnancy) |
| Fetal pH/lactate | Westgren et al. fetal scalp blood studies |
| MCA flow | Mari et al. 1995 *Am J Obstet Gynecol* (MCA Doppler) |

Each candidate citation needs Crossref-metadata-audit pass before
landing (same script as the existing audit). Estimated ~10-15 new
citations across Phases 2-3.

## 7. Verification standard for new entries

Same as the existing standard ([`docs/contributing/verification.md`](../../contributing/verification.md)):
every Tier A/B entry needs a human-with-PDF check of the cited table
or figure before `extraction.review_status` moves to `"verified"`.

Phased verification budget:
- Phase 1: ~10 hours of careful curation (most are from already-known
  papers).
- Phase 2: ~20 hours (new domain, new citations).
- Phase 3: variable, depends on which gaps are filled.

## 8. Out of scope (kept explicit)

These were considered and explicitly excluded — they remain so:

- **Twin and higher-order pregnancies.** Out of scope for the
  project entirely; would need its own parallel dataset.
- **Embryonic period (<8 weeks).** Out of scope.
- **Labour and delivery.** Out of scope; the project ends at 40w.
- **Clinical decision support.** Forever out of scope.
- **Pathophysiology** (preeclampsia, gestational diabetes, IUGR).
  Out of scope; the dataset is *normal* physiology. Disease-related
  parameters belong in derived projects.
- **Pharmacokinetics in pregnancy.** Important but a different
  dataset; defer to a follow-on project.
- **Postpartum physiology.** Out of scope (the project ends at 40w).

## 9. Maintenance pattern

The expansion proceeds incrementally:

- Each new parameter ships in its own commit (or small batches by
  subsystem) with substantive `tier_rationale` referencing the
  source paper.
- The `verify_citation_metadata.py` audit must pass before merge.
- The `nidus.validate()` schema validation must pass.
- Test count gates loosen as expected (`test_dataset_has_expected_size`
  becomes `>= 70` rather than `== 70`).

A new test, `test_dataset_growth_monotone`, asserts the dataset only
*grows* across releases (no silent regression in coverage).

## 10. Success criteria for Phase 1

- [ ] Dataset reaches 110+ parameters.
- [ ] Buck Louis 2015 / Grewal 2018 multi-week growth curves are
      fully extracted (BPD/HC/AC/FL/EFW at 16, 20, 24, 28, 32, 36, 40w).
- [ ] At least 40 of the 110 are `review_status: "verified"`.
- [ ] No new schema breakage; v0.3 schemas still apply.
- [ ] CHANGELOG.md and `dataset/CHANGELOG.md` document the additions.

## 11. Open questions

1. **Should the new `placental_endocrine` etc. subsystems break
   schema compatibility?** Answer: no — add to the enum in
   `parameter.schema.json` as additive enum values; existing
   parameters and consumers remain valid.

2. **Should multi-week growth-curve points be one parameter per
   week, or one `Trajectory` block per parameter?** Both work; the
   one-per-week form is simpler to query and review individually.
   Default: one per week for Phase 1, evaluate consolidation in
   Phase 3.

3. **Pathophysiology channels (e.g. preeclampsia spiral artery
   PO2)** — keep out of scope, but document them as Tier D research
   questions where the literature has quantitative claims?
   Recommendation: yes, but only after Phase 2 ships and the normal-
   physiology coverage is mature.
