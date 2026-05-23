# Nidus Changelog

This changelog covers the Python package, dashboard, and tooling. The
dataset has its own changelog at [`dataset/CHANGELOG.md`](dataset/CHANGELOG.md).

The format is loosely based on [Keep a Changelog](https://keepachangelog.com/),
and versions follow [Semantic Versioning](https://semver.org/).

## [Unreleased]

### Added
- **`nidus.export.equation_latex` — LaTeX equations for submodels.**
  Spec 03 §5 cross-cutting infrastructure item. Exposes one LaTeX
  fragment per registry entry for documentation, dashboard tooltips,
  paper appendices, or matplotlib `text(usetex=True)`. ~40 entries
  cover the canonical kernel families (logistic, Gaussian bump,
  linear, Michaelis-Menten, Hill, polynomial, algebraic combinator,
  piecewise hCG); `equation_latex(unknown_id)` returns `None`. Tests
  verify the family-representative set, that every map key resolves
  to a real Submodel id, and that no entry is empty.

- **`nidus.export.sweep` — sensitivity-analysis utility.** Spec 03 §5
  cross-cutting infrastructure item. One-parameter sweeps over any
  pure-NumPy reference kernel from `nidus.export.reference`, returning
  tidy long-form NumPy arrays; companion `write_sweep_csv` emits a
  long-format CSV (one row per (sweep_value, independent) cell). The
  utility is kernel-agnostic — it takes the kernel callable and its
  kwargs directly rather than a submodel id, which keeps the surface
  small and removes a mapping liability. Four new tests (shape,
  monotonicity, rejection of conflicting kwargs, CSV round-trip).

- **Phase 3 saturation pass — final batch: vascular resistances,
  lung volumes, gas-exchange gradient, parallel-circulation routing.**
  Nine new Tier-B/C dataset parameters (190 → **199 parameters**),
  all sourced from citations already in the index. The dataset is
  now at the **~200-parameter saturation ceiling** declared in spec
  02 §2.
  - `maternal_blood.haemoglobin_baseline_g_per_dl` (Tier B, ~13.5;
    pre-pregnancy anchor for the haemodilution-driven term fall)
  - `maternal_blood.mcv_term_fl` (Tier B, ~92 fL; modest rise from
    reticulocytosis)
  - `maternal_respiratory.inspiratory_capacity_term_l` (Tier B,
    ~2.7 L; rib-cage expansion compensates the FRC fall)
  - `maternal_respiratory.tlc_term_l` (Tier B, ~5.0 L; essentially
    unchanged)
  - `maternal_cardiovascular.svr_nadir_dyn_s_cm5` (Tier B, ~750;
    completes baseline → nadir → term SVR trajectory anchors)
  - `maternal_cardiovascular.pvr_term_dyn_s_cm5` (Tier B, ~80;
    parallel pulmonary vasodilation accommodates CO rise)
  - `placental_gas_exchange.maternal_fetal_pco2_gradient_term_mmhg`
    (Tier C, ~10 mmHg; coupled to maternal respiratory alkalosis)
  - `fetal_circulation.aortic_isthmus_flow_fraction_cvo_term`
    (Tier C, ~0.10; the narrow segment between LV and RV outputs)
  - `fetal_circulation.coronary_flow_fraction_cvo_term` (Tier C,
    ~0.03; brain-and-heart sparing routing of the best-oxygenated
    stream)
  Spec 02 §3.1, §3.2, §3.4, §3.6, and §3.8 gaps close. No new
  citations.

- **Phase 3 saturation pass — fetal homeostasis + placental glucose
  flux + maternal protein/coagulation anchors.** Six new Tier-B/C
  dataset parameters (184 → **190 parameters**), all sourced from
  citations already in the index.
  - `fetal_metabolism.fetal_core_temperature_c_term` (Tier B,
    ~37.6 °C; ~0.3-0.5 °C above maternal core)
  - `fetal_metabolism.fetal_urine_output_ml_per_kg_h_term` (Tier C,
    ~50 mL/kg/h; dominant source of amniotic fluid in late gestation)
  - `placental_glucose.maternal_fetal_glucose_gradient_term_mmol_per_l`
    (Tier B, ~1.2 mmol/L; couples maternal and fetal glucose
    parameters)
  - `placental_glucose.net_glucose_flux_term_mg_per_kg_per_min`
    (Tier B, ~5 mg/kg/min; matches fetal utilisation under steady-
    state)
  - `maternal_blood.total_protein_term_g_per_dl` (Tier B, ~6.0;
    couples with the albumin decrement)
  - `maternal_blood.fibrinogen_baseline_g_per_l` (Tier B, ~3.0;
    pre-pregnancy anchor for the term fibrinogen entry — the
    near-doubling is one of the robust haemostatic shifts of
    pregnancy)
  Spec 02 §3.2 (haematology), §3.7 (placental glucose net flux), and
  §3.10 (fetal clinical chemistry) gaps close further. The
  ~200-parameter saturation ceiling from §2 is now within reach of
  one more pass.

- **Phase 3 saturation pass — maternal cardiac remodelling and
  iron-status gaps.** Six new Tier-B/C dataset parameters
  (178 → **184 parameters**), all sourced from citations already in
  the index.
  - `maternal_cardiovascular.lv_mass_baseline_g` (Tier B, ~130 g
    pre-pregnancy anchor)
  - `maternal_cardiovascular.lv_mass_term_g` (Tier B, ~180 g; ~30-50%
    rise via eccentric volume-loaded hypertrophy)
  - `maternal_cardiovascular.aortic_root_diameter_term_mm` (Tier C,
    ~30 mm; small remodelling rise)
  - `maternal_cardiovascular.pulse_wave_velocity_term_m_per_s`
    (Tier C, ~7.5 m/s; mid-pregnancy nadir is the clinically useful
    timepoint)
  - `maternal_blood.serum_iron_term_ug_per_dl` (Tier B, ~60 µg/dL;
    wide range driven by supplementation status)
  - `maternal_blood.ferritin_term_ng_per_ml` (Tier B, ~15 ng/mL;
    crosses WHO depleted-stores threshold in ~half of unsupplemented
    pregnancies)
  Spec 02 §3.1 (maternal cardiovascular structural detail) and the
  iron-status subset of §3.2 close further toward the saturation
  ceiling. No new citations.

- **Phase 3 saturation pass — fetal-circulation and placental
  morphomic gaps.** Six new Tier-B/C dataset parameters (172 →
  **178 parameters**), all sourced from citations already in the
  index.
  - `fetal_circulation.umbilical_vein_flow_term_ml_per_min` (Tier B,
    ~290 mL/min; Kiserud 2001)
  - `fetal_circulation.umbilical_vein_flow_per_kg_term_ml_per_min_per_kg`
    (Tier B, ~80 mL/min/kg; declines through late gestation)
  - `fetal_circulation.combined_ventricular_output_term_ml_per_min_per_kg`
    (Tier B, ~450 mL/min/kg; Sutton 1991, Rudolph 1985)
  - `fetal_circulation.right_ventricular_output_fraction_term`
    (Tier B, ~0.60; RV-dominant in the fetus, opposite to adult)
  - `placental_structure.intervillous_space_volume_term_ml`
    (Tier C, ~175 mL; Mayhew 2014 stereology)
  - `placental_structure.villous_capillary_length_total_km_term`
    (Tier C, ~300 km total — one of the striking quantitative
    placental statistics)
  Spec 02 §3.5 (placental structure) and §3.8 (fetal circulation)
  gaps close. No new citations.

- **Phase 3 saturation pass — maternal-renal and maternal-respiratory
  gaps.** Six new Tier-B/C dataset parameters (166 → **172
  parameters**), all sourced from citations already in the index.
  - `maternal_renal.urinary_protein_excretion_term_mg_per_24h`
    (Tier B, ~150 mg/24h; clinical proteinuria threshold 300)
  - `maternal_renal.plasma_uric_acid_nadir_mg_per_dl` (Tier B,
    ~3.0 mg/dL mid-pregnancy)
  - `maternal_renal.plasma_uric_acid_term_mg_per_dl` (Tier B,
    ~4.5 mg/dL; supporting biomarker for preeclampsia >6)
  - `maternal_respiratory.vco2_term_ml_per_min` (Tier B, ~250
    mL/min; rises ~15-20% with VO2, keeps RER ≈ 0.85)
  - `maternal_respiratory.dlco_term_ml_per_min_per_mmhg` (Tier C,
    ~24 mL/min/mmHg; modest fall from non-pregnant baseline)
  - `maternal_respiratory.aa_o2_gradient_term_mmhg` (Tier C, ~13
    mmHg; widens vs non-pregnant due to closing-volume encroachment)
  Spec 02 §3.3 (renal) and §3.4 (respiratory) gaps each move closer
  to the saturation ceiling. No new citations.

- **Phase 3 saturation pass — maternal-blood and fetal clinical
  chemistry gaps.** Seven new Tier-B/C dataset parameters (159 →
  166 parameters), all sourced from citations already in the
  index (no new citation entries; the existing
  `hytten-chamberlain-1980-blood-volume` and
  `battaglia-meschia-1986-fetal-metabolism` cover both clusters).
  - `maternal_blood.wbc_count_term_x10e9_per_l` (Tier B, neutrophilia-
    driven rise to ~10.5 ×10^9/L at term)
  - `maternal_blood.serum_albumin_term_g_per_dl` (Tier B,
    haemodilution-driven fall to ~3.0 g/dL at term)
  - `maternal_blood.esr_term_mm_per_h` (Tier B, fibrinogen- and
    haemodilution-driven rise to ~50 mm/h at term)
  - `fetal_metabolism.umbilical_artery_ph_term` (Tier B, ~7.27)
  - `fetal_metabolism.umbilical_vein_ph_term` (Tier B, ~7.34)
  - `fetal_metabolism.umbilical_artery_lactate_term_mmol_per_l`
    (Tier C, ~3.5 mmol/L)
  - `fetal_metabolism.fetal_glucose_term_mmol_per_l` (Tier B, ~3.5
    mmol/L, ~70-75% of maternal)
  Spec 02 §3.2 maternal-blood gaps and §3.10 fetal-metabolism gaps
  each move one step closer to the saturation ceiling.

- **Phase C complete (4/4).** Registry now stands at **41 submodels**
  total (Phase A 12 + Phase B 10 + Phase C 4 + the legacy
  `hadlock_fetal_weight` + the 14 v0.4 core submodels). The two new
  Phase C entries both carry `nidus:reviewStatus = "hypothesis-only"`
  and the `nidus:warning = "DO NOT USE FOR PREDICTION"` RDF annotation:
  - `maternal_microchimerism_trajectory` — sigmoidal accumulation of
    fetal microchimeric cells in maternal blood from ~0 cells/mL
    (T1 baseline) to ~1 cell/mL at term, midpoint week 24. Bianchi
    1996 (PMID 8570620) documents trafficking and decades-long
    postpartum persistence; an uptake/clearance ODE upgrade with
    explicit rate constants remains an open research question.
  - `fetal_pulmonary_fluid_trajectory` — sigmoidal decline from net
    chloride-driven secretion (~+5 mL/kg/h mid-gestation) to active
    sodium-driven reabsorption (~-5 mL/kg/h near term), midpoint
    week 36. Strang 1991 (PMID 1924551) reviews the qualitative
    switch; human in vivo rates are species-extrapolated.
- **Four new Tier-D dataset parameters** (155 → **159 parameters**),
  all marked "DO NOT USE FOR PREDICTION" in their tier rationale:
  - `maternal_blood.fetal_microchimerism_baseline_cells_per_ml`
  - `maternal_blood.fetal_microchimerism_term_cells_per_ml`
  - `fetal_metabolism.pulmonary_fluid_net_rate_baseline_ml_per_kg_h`
  - `fetal_metabolism.pulmonary_fluid_net_rate_term_ml_per_kg_h`
- **Two new citations** (56 → 58): `bianchi-1996-microchimerism`,
  `strang-1991-fetal-lung-liquid`.
- Reference kernels `maternal_microchimerism_trajectory` and
  `fetal_pulmonary_fluid_trajectory` with sanity tests; the
  hypothesis-only-warning-carrying SBML test now covers all four
  Phase C submodels.

- **Phase C opens with two hypothesis-only submodels.** Registry
  previously stood at **39 submodels** (Phase A + Phase B + 2 of 4
  Phase C). Phase C submodels carry `nidus:reviewStatus = "hypothesis-only"`
  and a `nidus:warning = "DO NOT USE FOR PREDICTION"` RDF annotation
  in their SBML/CellML output, ensuring downstream consumers cannot
  accidentally treat them as predictive.
  - `maternal_fetal_igg_transfer` — sigmoidal FcRn-mediated IgG ratio
    rising from ~0.2 mid-pregnancy to >1.0 at term (Palmeira 2012,
    PMID 22235228). Exact kinetics are FcRn-saturation-dependent and
    open.
  - `placental_cortisol_gradient` — algebraic
    fetal_cortisol = maternal_cortisol * (1 - HSD2_inactivation),
    encoding the textbook qualitative shape (Benediktsson 1997,
    PMID 9326655). The actual saturable 11β-HSD2 kinetics are not
    captured.
- **New `Submodel.review_status` field** (default `"shipped"`,
  alternative `"hypothesis-only"`). The SBML annotation helper reads
  this and emits the warning + reviewStatus lines only for hypothesis-
  only submodels — backwards-compatible with the 37 shipped models.
- **Three new Tier-D dataset parameters** (152 → **155 parameters**),
  all in `placental_structure`, each with explicit
  "DO NOT USE FOR PREDICTION" tier rationale:
  - `igg_transfer_ratio_baseline` (Tier D, Palmeira 2012)
  - `igg_transfer_ratio_term` (Tier D, Palmeira 2012)
  - `hsd2_cortisol_inactivation_fraction` (Tier D, Benediktsson 1997)
- **Two new citations** (54 → 56): `palmeira-2012-igg-transfer`,
  `benediktsson-1997-11bhsd2`.
- Reference kernels `maternal_fetal_igg_transfer` and
  `placental_cortisol_gradient` with sanity tests; two new SBML-output
  tests assert (a) hypothesis-only submodels carry the warning, and
  (b) `shipped` submodels do NOT carry the warning (no false
  positives in the existing 37 models).

- **Phase B complete (10/10):** final Phase B submodel
  `placental_fetal_allometry` ships the allometric scaling
  PW = a · FW^b. Central nidus values (a = 0.4, b = 0.85) reproduce
  the canonical ~1:6-1:9 term placental:fetal weight ratio
  (Hutcheon 2012, PMID 22845665; Burton 2010). Registry now stands
  at **37 submodels** — both Phase A and Phase B of the catalog are
  complete.
- **Two new dataset parameters** (150 → **152 parameters**), both
  Tier C in `placental_structure`:
  - `allometric_coefficient_a`
  - `allometric_exponent_b`
- One new citation: `hutcheon-2012-placental-weight` (53 → 54).
- Reference kernel `placental_fetal_allometry` with a term-ratio
  sanity test asserting the canonical 1:6-1:9 placental:fetal weight
  ratio at a 3500 g term fetal weight.

- **Three more Phase B submodels** (fetal Doppler PI cluster),
  bringing the registry to **36 submodels** and Phase B to **9 of 10**:
  - `umbilical_artery_pi_trajectory` — sigmoidal UA-PI fall from
    ~1.5 at 16 weeks to ~0.85 at term as placental vascular
    resistance drops (Acharya 2005, PMID 15776417).
  - `mca_pi_trajectory` — Gaussian bell with mid-pregnancy peak
    (~2.0 at ~28 weeks), reflecting fetal cerebral vasodilation
    dynamics (Mari 1995, PMID 7900181). Peak week + spread are
    hardcoded.
  - `cerebroplacental_ratio` — derived CPR(t) = MCA-PI(t) / UA-PI(t).
    Normal pregnancies: CPR > 1; CPR < 1 flags fetal compromise
    (Baschat 2003). Reuses the four PI parameters above.
- **Four new dataset parameters** (146 → **150 parameters**), all
  in `fetal_circulation`:
  - `ua_pi_baseline` (Tier A, Acharya 2005)
  - `ua_pi_term` (Tier A, Acharya 2005)
  - `mca_pi_baseline` (Tier B, Mari 1995)
  - `mca_pi_peak` (Tier B, Mari 1995)
- Two new citations in `citations.json`: `acharya-2005-umbilical-pi`,
  `mari-1995-mca-pi`. Citation count 51 → 53.
- Reference kernels `umbilical_artery_pi`, `mca_pi`,
  `cerebroplacental_ratio` with endpoint + shape sanity tests. The
  CPR test asserts CPR > 1 across normal-pregnancy timepoints.

- **Three more Phase B submodels**, bringing the registry to
  **33 submodels** and Phase B to **8 of 10**:
  - `estradiol_trajectory` — sigmoidal estradiol rise from mid-luteal
    baseline (~0.1 ng/mL) to term (~14 ng/mL); ~100x rise driven by
    placental aromatisation. Tulchinsky 1972 / O'Leary 1991.
  - `fetal_heart_rate_trajectory` — sigmoidal FHR fall from T1 peak
    (~170 bpm) to term (~140 bpm) as parasympathetic tone develops.
    The same baseline → term sigmoid form encodes the fall because
    `(term - baseline)` is negative. Pildner von Steinburg 2013
    (PMID 23740338).
  - `hcg_trajectory` — first non-sigmoidal Phase B submodel:
    piecewise quadratic rise from zero to peak by `hcg_peak_week`,
    then exponential decline to `hcg_term` at week 40. The decline
    rate is fit at build time so the curve passes exactly through
    the curated peak and term values. Cole 2010 (PMID 20089136).
- **Three new dataset parameters** (143 → **146 parameters**), all
  Tier A or B:
  - `placental_endocrine.estradiol_baseline_ng_per_ml` (Tier B)
  - `fetal_circulation.fhr_baseline_bpm` (Tier B)
  - `fetal_circulation.fhr_term_bpm` (Tier A — NICHD definitions)
- Reference kernels `maternal_estradiol`, `fetal_heart_rate`,
  `maternal_hcg` with endpoint + shape sanity tests. The hCG test
  asserts exact pass-through of the (peak_week, peak) anchor and the
  (40w, term) anchor, validating the build-time decay-rate fit.

- **Two more Phase B submodels** (placental endocrine), bringing the
  registry to **30 submodels** and Phase B to **5 of 10**:
  - `hpl_trajectory` — sigmoidal hPL rise from undetectable
    non-pregnant baseline to ~7 ug/mL at term (Handwerger 2010 /
    Handwerger 1991). hPL is a major driver of maternal insulin
    resistance.
  - `progesterone_trajectory` — sigmoidal progesterone rise from the
    mid-luteal pre-pregnancy baseline (~10 ng/mL) to term
    (~150 ng/mL); 10-20x rise. A single sigmoid simplifies the
    actual two-source kinetics (corpus luteum then placental
    takeover at ~8 weeks). Tulchinsky 1972.
- **Two new dataset parameters** (141 → **143 parameters**), both
  Tier B, in `placental_endocrine`:
  - `hpl_baseline_ug_per_ml` — ~0 (below assay sensitivity).
  - `progesterone_baseline_ng_per_ml` — ~10 ng/mL (mid-luteal pre-
    pregnancy reference).
- Reference kernels `maternal_hpl` and `maternal_progesterone` with
  endpoint + magnitude sanity tests (the progesterone test asserts
  the canonical >10x rise).

- **First three Phase B submodels** with full export support, bringing
  the registry to **28 submodels** and opening Phase B (3 of 10 shipped):
  - `homa_ir_trajectory` — sigmoidal insulin resistance rise across
    gestation using existing `maternal_endocrine.homa_ir_baseline` /
    `homa_ir_term` (Catalano 1991, PMID 1957840; Sonagra 2014).
  - `tsh_trajectory` — piecewise-linear: constant at the T1 hCG-
    suppressed nadir before week 12, then linear toward term recovery
    using existing `tsh_t1_miu_per_l` / `tsh_term_miu_per_l` (Glinoer
    1997, Korevaar 2014). The full Hill-form coupling to hCG (catalog
    item 3.4) is deferred until a coupling-coefficient parameter
    lands.
  - `cortisol_trajectory` — sigmoidal total cortisol rise using
    existing `cortisol_baseline_ug_per_dl` / `cortisol_term_ug_per_dl`
    (Allolio 1990, Jung 2011). The diurnal-rhythm overlay (catalog
    item 3.3) needs a separate amplitude parameter and is deferred.
- Reference kernels `maternal_homa_ir`, `maternal_tsh`,
  `maternal_cortisol` in `nidus.export.reference`, with endpoint +
  midpoint sanity tests. A new `_build_sigmoid_baseline_term` helper
  in `sbml.py` (and matching CellML form) consolidates the standard
  baseline → term logistic emission, reused by all three.
- Generators learned the SBML/MathML `piecewise` construct (TSH is
  the first piecewise submodel in the registry).

- **Four Hadlock biometry growth submodels** — `hadlock_bpd_growth`,
  `hadlock_hc_growth`, `hadlock_ac_growth`, `hadlock_fl_growth` —
  closing out Phase A of the submodel-expansion catalog (12/12 shipped).
  Registry now stands at **25 submodels**. Each fits a cubic
  polynomial at build time to the seven weekly Hadlock 1982
  (PMID 7058748) anchors already in the dataset (16w-40w in 4-week
  steps). Fit residuals: BPD <1 mm, HC ~2.4 mm, AC ~1.4 mm, FL <0.5 mm
  — well inside published longitudinal scatter. The seven anchors
  are carried as nidus parameters in the SBML/CellML output so the
  Hadlock 1982 citation + Tier A annotations propagate cleanly; the
  fit coefficients themselves are derived constants embedded in the
  assignment rule.
- `hadlock_biometry_cubic` and `hadlock_biometry_cubic_coefficients`
  helpers in `nidus.export.reference`; a parametrised fit-residual
  test asserts the cubic reproduces all four biometries within
  per-biometry tolerance, plus a monotonicity check across 16-40w.

- **Two more Phase A submodels** with full export support
  (SBML L3v2 + CellML 2.0/1.1 + PhysioCell + COMBINE), bringing the
  registry to **21 submodels**:
  - `minute_ventilation_trajectory` — derived VE(t) = VT(t) · RR(t)
    using existing maternal_respiratory tidal-volume and respiratory-
    rate baseline/term parameters. The product reproduces the ~30-50%
    pregnancy VE rise (LoMauro 2015, PMID 25624458; Hegewald 2011).
  - `arterial_ph_trajectory` — linear pH rise from non-pregnant
    baseline (~7.40) to term (~7.44) reflecting compensated
    respiratory alkalosis (Templeton & Kelman 1976, PMID 1247088).
- **One new dataset parameter** (140 → **141 parameters**):
  - `maternal_respiratory.term_arterial_ph` — pH at term, Tier B from
    Templeton & Kelman 1976 / LoMauro 2015 convergence. Citation list
    unchanged (existing entries cover the new parameter).
- Reference kernels `maternal_minute_ventilation` and
  `maternal_arterial_ph` with endpoint sanity tests; CellML factor-
  out helper `_sigmoid_baseline_term` consolidates the common
  baseline→term sigmoid MathML.

- **Three more Phase A submodels** with full export support
  (SBML L3v2 + CellML 2.0/1.1 + PhysioCell + COMBINE), bringing the
  registry to **19 submodels**:
  - `heart_rate_trajectory` — sigmoidal HR rise from non-pregnant
    baseline to term using existing `baseline_heart_rate_bpm` and
    `term_heart_rate_bpm` (Mahendru 2014, PMID 25053730).
  - `stroke_volume_trajectory` — Gaussian-bump SV trajectory sharing
    peak week and spread with the CO submodel, using existing
    `baseline_stroke_volume_ml` and `peak_excess_stroke_volume_ml`.
    SV is the larger driver of the CO peak (Mahendru 2014); the
    product SV(t) * HR(t) reconstructs the CO bump.
  - `renal_plasma_flow_trajectory` — Gaussian bell-shape RPF
    trajectory with fixed 8-week spread, using existing
    `renal_plasma_flow_baseline_ml_per_min`, `_peak_ml_per_min`, and
    `rpf_peak_week` (Dunlop 1981, PMID 7259294).
- Reference kernels `maternal_heart_rate`, `maternal_stroke_volume`,
  and `renal_plasma_flow` with endpoint + peak sanity tests. No new
  dataset parameters required for any of the three.

- **Three additional Phase A submodels** with full export support
  (SBML L3v2 + CellML 2.0/1.1 + PhysioCell + COMBINE), bringing the
  registry to **16 submodels**:
  - `svr_trajectory` — derived systemic vascular resistance
    SVR(t) = MAP(t)·80 / CO(t), the conventional CGS form used in
    obstetric haemodynamics. All inputs are the four MAP and four CO
    Gaussian-trajectory parameters already in the dataset; no new
    dataset parameters required. Sanghavi 2014 (PMC4172642) reference.
  - `pao2_trajectory_linear` — linear PaO₂ rise from non-pregnant
    baseline to term reflecting hyperventilation-induced respiratory
    alkalosis. Uses existing
    `maternal_respiratory.baseline_pao2_mmhg` and `pao2_mmhg_term`.
    Templeton & Kelman 1976 (PMID 1247088), Hegewald 2011.
  - `tidal_volume_trajectory` — sigmoidal tidal-volume rise from
    baseline to term. Uses existing
    `maternal_respiratory.baseline_tidal_volume_ml` and
    `tidal_volume_ml_term`. LoMauro 2015 (PMID 25624458),
    Hegewald 2011.
- Reference kernels `maternal_svr_trajectory`,
  `maternal_pao2_linear`, and `maternal_tidal_volume` in
  `nidus.export.reference`, with endpoint + physiological-shape
  sanity tests. The SVR test confirms the mid-pregnancy drop and
  late-pregnancy recovery characteristic of normal haemodynamic
  adaptation.
- Parametrised SBML + CellML test coverage extended to the three new
  submodels; `test_write_sbml_produces_all_files` /
  `test_write_cellml_both_versions` floor lifted from 13 → 16.

- **Two new Phase A submodels** with full export support (SBML L3v2 +
  CellML 2.0/1.1 + PhysioCell + COMBINE), bringing the registry to
  **13 submodels**:
  - `gfr_logistic_trajectory` — logistic maternal GFR rise from
    baseline (~100 mL/min) to plateau (~150 mL/min). Inputs from the
    Phase 1 maternal_renal expansion (baseline_gfr, gfr_ml_per_min,
    gfr_peak_week, gfr_logistic_rate). Conrad 2001 mechanistic
    citation.
  - `amniotic_fluid_volume_trajectory` — Gaussian-bump approximation
    to the Brace & Wolf 1989 (PMID 2782359) curve. Inputs from the
    new `amniotic_fluid` subsystem (peak, peak week, plus two added
    parameters: early baseline and Gaussian spread). Worst-input
    tier is C (the spread parameter); the submodel inherits Tier C
    in exported annotations.
- Reference-kernel functions `maternal_gfr_logistic` and
  `amniotic_fluid_volume` in `nidus.export.reference`, parametrised
  unit tests covering endpoint values and the Gaussian peak.
- Parametrised SBML + CellML test coverage extended to the two new
  submodels; `test_write_sbml_produces_all_files` and
  `test_write_cellml_both_versions` updated to assert ≥13 outputs.


- **Phase 1 + partial Phase 2 dataset expansion:** 70 → **138 parameters**
  across 13 subsystems (was 10). Three new subsystems land additively
  in the schema enum: `maternal_endocrine`, `placental_endocrine`,
  `amniotic_fluid`.
  - Fetal growth: full multi-week Hadlock/Buck Louis biometry — BPD,
    HC, AC, FL at 16/20/24/28/32/36/40w; EFW at 16/24/32w (+29 params).
  - Maternal cardiovascular: HR baseline + peak excess; stroke volume
    baseline + peak excess; SVR baseline + term (+6 params, but 4 net
    after de-duplication against shipped entries).
  - Maternal renal: baseline GFR, GFR peak week + logistic rate, RPF
    baseline/peak/peak-week, filtration fraction, osmolality + sodium
    drops, BUN at term (+10 params).
  - Maternal respiratory: baseline VT, baseline + term RR, baseline
    PaO₂, baseline arterial pH (+5 params).
  - **New `maternal_endocrine`:** cortisol baseline + term, free T4
    term, TSH T1 + term, prolactin, aldosterone, HOMA-IR baseline +
    term (+9 params).
  - **New `placental_endocrine`:** hCG peak + week + term, hPL term,
    progesterone term, estradiol term, estriol term (+7 params).
  - **New `amniotic_fluid`:** AFV peak + peak week + term + 20w
    anchor (+4 params).
- **18 new peer-reviewed citations** spanning the Phase 1 + 2 expansion
  (Conrad 2001, Dunlop 1981, Davison 1981, Pitkin 1979, Kline 2005,
  Larsson 2008, Carr 1981, Glinoer 1997, Tyson 1972, Wilson 1980,
  Catalano 1991, Cole 2010, Tulchinsky 1972, Handwerger 1991, Brace
  1989, Kiserud 2000, Rudolph 1985, Pildner von Steinburg 2013,
  Templeton & Kelman 1976). Total citations 33 → 51.
- **New spec `docs/specs/v0.4/04-exhaustive-parameter-catalog.md`:**
  the project's ceiling. Every parameter the project could honestly
  include given the literature within the declared scope (8–40 week
  human singleton, normal physiology), indexed by subsystem with
  status (`shipped` / `phase1` / `phase2` / `phase3`) and primary
  citation. ~210 parameters at saturation.
- **README rewrite:** adds a narrative on the three-genome negotiation
  in pregnancy (maternal/paternal/fetal evolutionary-conflict framing),
  the clinical consequences when it fails (PE, FGR, GDM, VTE, PPH),
  and why a calibrated parameter dataset is the load-bearing piece.
  Subsystems table extended to 13; submodel table extended with the
  five trajectories described in spec 03 (Phase A submodels remain
  catalogued; SBML/CellML builders are follow-on work tracked in
  [`docs/specs/v0.4/03-submodel-expansion-catalog.md`](docs/specs/v0.4/03-submodel-expansion-catalog.md)).
- `scripts/expand_v04.py` — one-shot, idempotent expansion script that
  produced this batch. Future Phase 2/3 batches follow the same
  pattern.

### Changed
- **v0.3 reframes nidus around its durable contribution.** Earlier
  Rust-prototype work (preserved at the `v0.2-archive` git tag)
  explored a coupled maternal-placental-fetal physiology engine. v0.3
  distils that exploration into the artefact that is actually
  transferable: a citation-verified, tier-annotated parameter dataset,
  distributed as `pip install nidus` with a Streamlit dashboard. The
  form factor matches the audience (biomedical researchers, almost all
  Python/R users); the maintenance scope matches what one person can
  sustain. See
  [`docs/specs/v0.3/00-overview.md`](docs/specs/v0.3/00-overview.md)
  for the design rationale.

### Removed
- The Rust prototype: `crates/`, `Cargo.toml`, `Cargo.lock`, `target/`,
  scenario configurations (`scenarios/`), examples (`examples/`),
  output artefacts (`out/`), and the implementation-progress tracker
  (`PROGRESS.md`). All recoverable from the `v0.2-archive` tag.

### Added
- Repository scaffold for the v0.3 design: `dataset/`, `python/`,
  `dashboard/`, `notebooks/`, `scripts/`.
- JSON Schema (draft 2020-12) for parameters, citations, and tiers in
  `dataset/schema/`. JSON-LD context for FAIR linked-data consumption.
- Pure-Python `nidus` package: `nidus.load()`, `nidus.validate()`,
  dataclass models, schema validation, citation resolution, multi-axis
  filtering. Test suite of 36 cases covering load, filter, citations,
  and validation.
- 54 parameters across 10 subsystems, 32 citations migrated from the
  v0.2 curation into schema-valid JSON.
- GitHub Actions CI: lint (`ruff`), typecheck (`mypy --strict`), test
  matrix (Python 3.10/3.11/3.12), dataset validation, wheel + sdist
  build with smoke test of the installed wheel.
- Weekly citation-reachability cron with automated issue creation on
  failures.
- Release pipeline (PyPI Trusted Publishing + GitHub Releases) wired
  for tag-driven publishing.
- `CITATION.cff` and `LICENSE-DATASET` (CC-BY-4.0).
- `CLAUDE.md` at repo root to orient fresh Claude Code sessions.
- `nidus` console-script entry point (`nidus version`, `nidus validate`,
  `nidus info`, `nidus export --format csv|bibtex`).
- Reference notebooks (5) embedded as docs pages via mkdocs-jupyter.
- Auto-generated API reference via mkdocstrings.
- `docs/about/essay.md` — "Confidence tiers for pregnancy physiology",
  ~2,500 words, with three seeded figures committed under
  `docs/assets/essay/`.
- Citation audit + repair tooling:
  `scripts/verify_citation_metadata.py` cross-checks every citation
  against Crossref / PubMed publisher records;
  `scripts/repair_citation_identifiers.py` finds the correct DOI for
  any citation whose stored identifier resolves to the wrong paper.

### Data integrity (this release)

- 22 of 30 citations in the original v0.2 corpus had DOI/PMID
  identifiers pointing to the wrong papers. Crossref-search-and-replace
  repaired all of them; the corpus now passes the metadata audit
  cleanly (30/30 with identifiers; 2 books legitimately have none).
- 23 additional PMIDs added via NCBI IdConverter / EPMC lookups.
- Six papers (the PMC-accessible subset) were read at the abstract or
  table level. Five parameters were promoted to
  `extraction.review_status: "verified"` based on direct confirmation:
  `maternal_blood.plasma_volume_l` (de Haas 2017 meta-analysis pooled
  +1.13 L third-trimester rise), `maternal_blood.plasma_volume_early_l`
  (Bernstein 2001 2.32 L at 12 weeks), `maternal_blood.o2_hb_p50_maternal`
  (Severinghaus 1979 Eq. 4 explicit P50=26.6 mmHg),
  `maternal_respiratory.paco2_mmhg_term` (LoMauro 2015 plateau at 32),
  `maternal_respiratory.pao2_mmhg_term` (LoMauro 2015 third-trimester
  range 101-104).
- One parameter promoted to `contested`:
  `maternal_cardiovascular.baseline_uterine_flow_ml_per_min` —
  Thaler 1990's pre-pregnancy bilateral estimate (~189 mL/min) is
  meaningfully larger than the dataset's stored 50 mL/min, needs
  human investigation.
- Two more parameters carry `notes` flagging discrepancies for human
  re-investigation: `peak_excess_cardiac_output_l_per_min` (Mahendru
  2014 abstract's 0.6 L/min tension with the dataset's 2.7), and the
  four `efw_*_g` records (Hadlock 1991 ±12.7% CV pattern is closer to
  the dataset than Buck Louis 2015's racial-percentile values —
  primary citation may have been mis-attributed in v0.2).
- All 31 placeholder `tier_rationale` fields rewritten with
  substantive evidence from the verified citation abstracts.
- 100% test coverage of `nidus.validate`; total package coverage 95%.
