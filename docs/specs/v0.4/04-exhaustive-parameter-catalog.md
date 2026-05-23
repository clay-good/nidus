# Spec 04 — Exhaustive Parameter Catalog

**Status:** Reference. Names every parameter and citation that nidus
could honestly include given the scope (8–40 week human singleton
pregnancy, *normal* physiology). This spec is the project's *ceiling*.
**Depends on:** Specs 01, 02, 03.

---

## 1. TL;DR

If the project filled every entry below it would carry **~210
parameters across 13 subsystems**, backed by **~70 citations**.

**Current state (as of dataset v0.3.0-dev):** the catalog stands at
**199 parameters / 58 citations**. Almost all "phase 1" items have
shipped; phase 2 is mostly complete; phase 3 is the remaining
residual. The "Status" column on each subsystem table is the source
of truth.

This spec extends `02-parameter-expansion-roadmap.md` from a *planning*
document (phased, with rationale per gap) to a *catalog* document
(every parameter, indexed, with the citation that would back it).
After this catalog, growth is filling-in only; the structural design
question is settled.

Three explicit principles govern what *does not* appear here:

1. **Normal physiology only.** Pre-eclampsia, gestational diabetes,
   IUGR, infection, stillbirth, drug exposures, pharmacokinetics —
   all out of scope. They are derived datasets, not this one.
2. **Human only.** Even where rodent / primate / sheep data are
   excellent, this is a human dataset.
3. **8–40 weeks, singleton.** Embryology (<8w), multiples, labour,
   postpartum — out of scope.

Inside that envelope, the catalog below is intended to be *complete*.
If you find a parameter that fits the envelope, is published, and is
not listed, open an issue: that is the contribution loop.

## 2. How to read this catalog

Each subsystem section has:

- A short summary of what the subsystem covers.
- A table of parameters. Columns:
    - **Parameter id** — the dotted id used in the dataset JSON.
    - **What** — one-line description.
    - **Typical value** — central estimate; not authoritative, just a
      sniff-test number to anchor the reader.
    - **Tier** — anticipated tier based on the strength of the
      candidate citation. May change on review.
    - **Status** — `shipped`, `phase1`, `phase2`, `phase3`, or
      `deferred`.
    - **Primary citation** — the single load-bearing source.
- Citations needed (if any are new to the project).
- Notes on what is *out of scope* within the subsystem.

The "Status" column is the source of truth for what is in the current
dataset vs what is planned.

## 3. Subsystem catalogs

### 3.1 `maternal_cardiovascular`

The mother's haemodynamic adaptation: cardiac output rises ~50%,
systemic vascular resistance falls, mean arterial pressure dips
mid-pregnancy and recovers, the heart hypertrophies modestly, and
uterine flow rises from ~50 to ~600 mL/min.

| Parameter id | What | Typical | Tier | Status | Primary citation |
| --- | --- | --- | --- | --- | --- |
| `baseline_cardiac_output_l_per_min` | Non-pregnant CO | 4.5 L/min | B | shipped | Mahendru 2014 |
| `peak_excess_cardiac_output_l_per_min` | Gaussian-fit peak excess | 2.0 L/min | B | shipped | Mahendru 2014 |
| `cardiac_output_peak_week` | Week of CO peak | 32 | B | shipped | Mahendru 2014 |
| `cardiac_output_spread_weeks` | Gaussian σ | 9 | B | shipped | Mahendru 2014 |
| `baseline_map_mmhg` | Non-pregnant MAP | 87 | A | shipped | Mahendru 2014 |
| `map_nadir_drop_mmhg` | MAP nadir below baseline | 8 | A | shipped | Mahendru 2014 |
| `map_nadir_week` | Week of MAP nadir | 22 | A | shipped | Mahendru 2014 |
| `map_spread_weeks` | Gaussian σ for MAP curve | 8 | B | shipped | Mahendru 2014 |
| `baseline_uterine_flow_ml_per_min` | Non-pregnant UA flow | 50 | B | shipped | Thaler 1990 |
| `term_uterine_flow_ml_per_min` | Term UA flow | 600 | B | shipped | Thaler 1990 |
| `uterine_flow_growth_rate_per_week` | Logistic rate | 0.25 | B | shipped | Thaler 1990 |
| `baseline_heart_rate_bpm` | Non-pregnant HR | 70 | A | shipped | Mahendru 2014 |
| `peak_excess_heart_rate_bpm` | HR rise to term | 15 | A | shipped | Mahendru 2014 |
| `heart_rate_peak_week` | Week of HR peak | 32 | B | phase1 | Mahendru 2014 |
| `baseline_stroke_volume_ml` | Non-pregnant SV | 70 | B | shipped | Sanghavi 2014 |
| `peak_excess_stroke_volume_ml` | SV rise | 15 | B | shipped | Sanghavi 2014 |
| `baseline_svr_dyn_s_cm5` | Non-pregnant SVR | 1300 | B | shipped | Sanghavi 2014 |
| `svr_nadir_dyn_s_cm5` | Mid-pregnancy SVR nadir | 750 | B | shipped | Sanghavi 2014 |
| `term_svr_dyn_s_cm5` | Term SVR | 980 | B | shipped | Sanghavi 2014 |
| `baseline_pvr_dyn_s_cm5` | Non-pregnant PVR | 120 | C | phase2 | Robson 1989 |
| `pvr_term_dyn_s_cm5` | Term PVR | 80 | B | shipped | Sanghavi 2014 |
| `lv_mass_baseline_g` | LV mass non-pregnant | 130 | B | shipped | Sanghavi 2014 |
| `lv_mass_term_g` | LV mass at term | 180 | B | shipped | Sanghavi 2014 |
| `lv_wall_thickness_term_mm` | LV wall at term | 11 | C | phase2 | Robson 1989 |
| `aortic_root_diameter_term_mm` | Aortic root diameter at term | 30 | C | shipped | Sanghavi 2014 |
| `pulse_wave_velocity_term_m_per_s` | PWV at term | 7.5 | C | shipped | Sanghavi 2014 |
| `cardiac_output_t1_l_per_min` | CO in T1 anchor | 5.5 | B | phase2 | Mahendru 2014 |
| `cardiac_output_t2_l_per_min` | CO in T2 anchor | 6.4 | B | phase2 | Mahendru 2014 |
| `cardiac_output_t3_l_per_min` | CO in T3 anchor | 6.5 | B | phase2 | Mahendru 2014 |

**Citations needed (new):** none. Mahendru 2014, Sanghavi 2014, Robson
1989 cover all of the above. The Robson 1989 *Br Heart J* paper is the
single canonical LV-mass-in-pregnancy citation.

**Out of scope:** preeclampsia haemodynamics (a derived dataset),
exercise haemodynamics, postpartum return to baseline.

### 3.2 `maternal_blood`

Plasma volume up ~45%, RBC mass up ~25% (physiologic anaemia of
pregnancy follows from the mismatch), coagulation factors up sharply
(II, VII, VIII, IX, X, XII, fibrinogen, D-dimer), some down (protein
S, antithrombin). Iron and folate stores drop. WBC count rises.

| Parameter id | What | Typical | Tier | Status | Primary citation |
| --- | --- | --- | --- | --- | --- |
| `plasma_volume_early_l` | Early-pregnancy PV anchor | 2.6 | B | shipped | Bernstein 2001 |
| `plasma_volume_l` | Term PV | 3.8 | B | shipped | de Haas 2017 |
| `rbc_mass_term_l` | Term RBC mass | 1.8 | B | shipped | Hytten 1980 |
| `haematocrit_term_pct` | Term Hct | 33 | A | shipped | Bothwell 1979 |
| `haemoglobin_term_g_per_dl` | Term Hb | 11.5 | A | shipped | Bothwell 1979 |
| `o2_hb_p50_maternal` | Adult P50 | 26.6 | A | shipped | Severinghaus 1979 |
| `o2_hb_hill_coefficient_maternal` | Hill n adult | 2.7 | A | shipped | Severinghaus 1979 |
| `dpg_term_umol_per_g_hb` | 2,3-DPG term | 14 | B | shipped | Bauer 1969 |
| `fibrinogen_baseline_g_per_l` | Fibrinogen pre-pregnancy | 3.0 | B | shipped | Hytten 1980 |
| `fibrinogen_term_g_per_l` | Fibrinogen at term | 5.5 | A | shipped | Hytten 1980 |
| `factor_vii_term_pct` | Factor VII activity | 170 | B | shipped | Stirling 1984 |
| `factor_viii_term_pct` | Factor VIII activity | 220 | B | shipped | Stirling 1984 |
| `haemoglobin_baseline_g_per_dl` | Hb pre-pregnancy | 13.5 | B | shipped | Hytten 1980 |
| `mcv_term_fl` | MCV at term | 92 | B | shipped | Hytten 1980 |
| `platelet_count_term_x10e9_per_l` | Platelets at term | 220 | B | shipped | Hytten 1980 |
| `wbc_count_term_x10e9_per_l` | WBC at term | 10.5 | B | shipped | Hytten 1980 |
| `d_dimer_term_ug_per_ml` | D-dimer at term | 1.5 | B | phase1 | Kline 2005 |
| `factor_ix_term_pct` | Factor IX activity | 130 | B | phase2 | Stirling 1984 |
| `factor_x_term_pct` | Factor X activity | 145 | B | phase2 | Stirling 1984 |
| `factor_xii_term_pct` | Factor XII activity | 160 | B | phase2 | Stirling 1984 |
| `protein_s_free_term_pct` | Free protein S | 45 | B | phase2 | Faught 1995 |
| `protein_c_term_pct` | Protein C activity | 100 | B | phase2 | Faught 1995 |
| `antithrombin_term_pct` | Antithrombin activity | 95 | B | phase2 | Faught 1995 |
| `pai1_term_ng_per_ml` | PAI-1 at term | 80 | C | phase3 | Kruithof 1987 |
| `pai2_term_ng_per_ml` | PAI-2 at term | 250 | C | phase3 | Kruithof 1987 |
| `serum_albumin_term_g_per_dl` | Albumin at term | 3.0 | B | shipped | Hytten 1980 |
| `total_protein_term_g_per_dl` | Total protein term | 6.0 | B | shipped | Hytten 1980 |
| `serum_iron_term_ug_per_dl` | Iron at term | 60 | B | shipped | Hytten 1980 |
| `transferrin_saturation_term_pct` | Tsat at term | 20 | B | phase2 | Hytten 1980 |
| `ferritin_term_ng_per_ml` | Ferritin at term | 15 | B | shipped | Hytten 1980 |
| `folate_term_ng_per_ml` | Folate at term | 5 | B | phase2 | Hytten 1980 |
| `b12_term_pg_per_ml` | B12 at term | 250 | C | phase2 | Hytten 1980 |
| `esr_term_mm_per_h` | ESR at term | 50 | B | shipped | Hytten 1980 |
| `fetal_microchimerism_baseline_cells_per_ml` | Fetal-cell baseline (T1) | 0.0 | D | shipped (hypothesis-only) | Bianchi 1996 |
| `fetal_microchimerism_term_cells_per_ml` | Fetal-cell term | 1.0 | D | shipped (hypothesis-only) | Bianchi 1996 |

**Citations needed (new):** Stirling 1984 (Thromb Haemost), Faught
1995 (Thromb Haemost), Kruithof 1987 (Blood), Pitkin 1979, Kline 2005,
Larsson 2008.

**Out of scope:** disorders of haemostasis in pregnancy
(antiphospholipid, factor V Leiden); transfusion thresholds.

### 3.3 `maternal_renal`

GFR rises ~50% (one of the largest non-pathological changes in adult
physiology). Plasma osmolality drops 10 mOsm/kg, sodium 5 mEq/L,
creatinine ~30%. The mother retains ~1000 mg total sodium over
pregnancy.

| Parameter id | What | Typical | Tier | Status | Primary citation |
| --- | --- | --- | --- | --- | --- |
| `gfr_ml_per_min` | Term GFR | 150 | B | shipped | Cheung 2013 |
| `gfr_first_trimester_ml_per_min` | T1 GFR | 135 | A | shipped | Davison 1974 |
| `plasma_creatinine_mg_per_dl_term` | Term creatinine | 0.6 | A | shipped | Cheung 2013 |
| `baseline_gfr_ml_per_min` | Non-pregnant GFR | 100 | A | shipped | Conrad 2001 |
| `gfr_peak_week` | Week of GFR peak | 16 | B | shipped | Conrad 2001 |
| `gfr_logistic_rate_per_week` | Logistic rate | 0.4 | B | shipped | Conrad 2001 |
| `renal_plasma_flow_baseline_ml_per_min` | Non-pregnant RPF | 600 | B | shipped | Dunlop 1981 |
| `renal_plasma_flow_peak_ml_per_min` | Peak RPF | 900 | B | shipped | Dunlop 1981 |
| `rpf_peak_week` | Week of RPF peak | 24 | B | shipped | Dunlop 1981 |
| `filtration_fraction_term` | FF at term | 0.18 | B | shipped | Cheung 2013 |
| `plasma_osmolality_drop_mosm_per_kg` | Osmolality drop | 10 | A | shipped | Davison 1981 |
| `plasma_sodium_drop_meq_per_l` | Sodium drop | 5 | A | shipped | Davison 1981 |
| `cumulative_sodium_retention_g` | Total Na retained | 1.0 | B | phase1 | Cheung 2013 |
| `bun_term_mg_per_dl` | Term BUN | 8 | A | shipped | Cheung 2013 |
| `plasma_uric_acid_nadir_mg_per_dl` | Mid-pregnancy uric-acid nadir | 3 | B | shipped | Cheung 2013 |
| `plasma_uric_acid_term_mg_per_dl` | Term uric acid | 4.5 | B | shipped | Cheung 2013 |
| `urinary_protein_excretion_term_mg_per_24h` | 24h proteinuria | 150 | B | shipped | Cheung 2013 |
| `urinary_glucose_term_mg_per_24h` | 24h glucose | 90 | C | phase3 | Davison 1974 |
| `tubular_phosphate_threshold_term` | TmP/GFR ratio | 0.85 | C | phase3 | Cheung 2013 |

**Citations needed:** Davison 1981 (osmoregulation), Higby 1994 (24h
urinary protein in normal pregnancy), Conrad 2001 (relaxin-driven GFR
rise).

**Out of scope:** pre-eclampsia proteinuria, diabetic nephropathy,
gestational AKI.

### 3.4 `maternal_respiratory`

Minute ventilation rises ~40% (chemoreceptor reset by progesterone),
predominantly via tidal volume. Maternal PaCO₂ drops to ~30 mmHg;
respiratory alkalosis compensated by renal bicarbonate loss.

| Parameter id | What | Typical | Tier | Status | Primary citation |
| --- | --- | --- | --- | --- | --- |
| `minute_ventilation_term_l_per_min` | Term VE | 9.5 | A | shipped | LoMauro 2015 |
| `tidal_volume_term_ml` | Term VT | 600 | A | shipped | LoMauro 2015 |
| `paco2_term_mmhg` | Term PaCO₂ | 30 | A | shipped | LoMauro 2015 |
| `pao2_term_mmhg` | Term PaO₂ | 105 | B | shipped | LoMauro 2015 |
| `frc_term_l` | FRC at term | 2.0 | B | shipped | LoMauro 2015 |
| `bicarbonate_term_meq_per_l` | Bicarb at term | 20 | A | shipped | LoMauro 2015 |
| `arterial_ph_term` | Term arterial pH | 7.44 | A | shipped | LoMauro 2015 |
| `baseline_tidal_volume_ml` | Non-pregnant VT | 450 | A | shipped | LoMauro 2015 |
| `baseline_respiratory_rate_bpm` | Non-pregnant RR | 16 | A | shipped | LoMauro 2015 |
| `term_respiratory_rate_bpm` | Term RR | 16 | A | shipped | LoMauro 2015 |
| `baseline_pao2_mmhg` | Non-pregnant PaO₂ | 100 | A | shipped | Templeton 1976 |
| `baseline_arterial_ph` | Non-pregnant pH | 7.40 | A | shipped | Lim 1976 |
| `term_arterial_ph` | Term pH | 7.44 | A | shipped | LoMauro 2015 |
| `inspiratory_capacity_term_l` | IC at term | 2.7 | B | shipped | Crapo 1996 |
| `tlc_term_l` | TLC at term | 5.0 | B | shipped | Crapo 1996 |
| `dlco_term_ml_per_min_per_mmhg` | DLCO at term | 24 | C | shipped | Crapo 1996 |
| `aa_o2_gradient_term_mmhg` | A-a gradient term | 13 | C | shipped | Crapo 1996 |
| `vco2_term_ml_per_min` | Maternal VCO₂ | 250 | B | shipped | LoMauro 2015 |

**Citations needed:** Templeton 1976 (blood-gas during pregnancy), Lim
1976 (acid-base), Crapo 1996 (DLCO reference).

### 3.5 `maternal_endocrine` (NEW subsystem)

Cortisol triples; prolactin rises ~10x; aldosterone rises ~5–10x;
thyroid axis adapts (hCG cross-reactivity suppresses TSH in T1; thyroid
binding globulin rises; free T4 dips slightly); insulin sensitivity
falls ~50%.

| Parameter id | What | Typical | Tier | Status | Primary citation |
| --- | --- | --- | --- | --- | --- |
| `cortisol_term_ug_per_dl` | Term plasma cortisol | 30 | B | shipped | Allolio 1990 |
| `cortisol_baseline_ug_per_dl` | Non-pregnant cortisol | 10 | A | shipped | Allolio 1990 |
| `cbg_term_mg_per_l` | CBG at term | 70 | B | phase2 | Carr 1981 |
| `free_t4_term_ng_per_dl` | Free T4 at term | 0.9 | B | shipped | Glinoer 1997 |
| `tsh_t1_miu_per_l` | TSH in T1 | 0.6 | B | shipped | Glinoer 1997 |
| `tsh_term_miu_per_l` | TSH at term | 2.0 | B | shipped | Glinoer 1997 |
| `prolactin_term_ng_per_ml` | Prolactin at term | 200 | B | shipped | Tulchinsky 1972 |
| `aldosterone_term_ng_per_dl` | Aldosterone term | 40 | B | shipped | Cheung 2013 |
| `renin_term_ng_per_ml_per_h` | PRA at term | 12 | B | phase2 | Wilson 1980 |
| `homa_ir_term` | HOMA-IR at term | 4.0 | B | shipped | Catalano 1991 |
| `homa_ir_baseline` | Non-pregnant HOMA-IR | 2.0 | B | shipped | Catalano 1991 |
| `placental_gh_term_ng_per_ml` | Placental GH at term | 14 | C | phase3 | Eriksson 1989 |

**Citations needed:** Carr 1981, Glinoer 1997, Tyson 1972, Wilson
1980, Catalano 1991, Eriksson 1989.

**Out of scope:** thyroid disease in pregnancy; hyperemesis-related
endocrinology; Cushing's; PCOS effects.

### 3.6 `placental_structure`

Surface area rises from ~3 m² mid-pregnancy to ~12 m² at term. Cord
length ~55 cm. Capillary length is one of the most striking statistics
in human biology — ~300 km in a term placenta.

| Parameter id | What | Typical | Tier | Status | Primary citation |
| --- | --- | --- | --- | --- | --- |
| `initial_area_m2` | Mid-pregnancy area | 3.0 | B | shipped | Mayhew 2014 |
| `term_area_m2` | Term area | 12.0 | B | shipped | Mayhew 2014 |
| `growth_rate_per_week` | Logistic rate | 0.2 | B | shipped | Mayhew 2014 |
| `midpoint_week` | Logistic midpoint | 24 | B | shipped | Mayhew 2014 |
| `term_weight_g` | Placental weight at term | 470 | A | shipped | Thompson 2007 |
| `placental_thickness_term_cm` | Placental thickness | 2.5 | B | phase1 | Hoddick 1985 |
| `cord_length_term_cm` | Term cord length | 55 | A | phase1 | Naeye 1985 |
| `cotyledon_count` | Number of cotyledons | 18 | B | phase2 | Benirschke 2012 |
| `villous_capillary_length_total_km_term` | Total capillary length | 300 | C | shipped | Mayhew 2014 |
| `intervillous_space_volume_term_ml` | IVS volume at term | 175 | C | shipped | Mayhew 2014 |
| `placenta_to_fetus_weight_ratio_term` | PW/FW ratio at term | 0.17 | B | shipped | Hutcheon 2012 |
| `allometric_coefficient_a` | PW = a·FW^b coefficient | 0.4 | C | shipped | Hutcheon 2012 |
| `allometric_exponent_b` | PW = a·FW^b exponent | 0.85 | C | shipped | Hutcheon 2012 |
| `igg_transfer_ratio_baseline` | FcRn IgG ratio (T1) | 0.2 | D | shipped (hypothesis-only) | Palmeira 2012 |
| `igg_transfer_ratio_term` | FcRn IgG ratio (term) | 1.2 | D | shipped (hypothesis-only) | Palmeira 2012 |
| `hsd2_cortisol_inactivation_fraction` | 11β-HSD2 inactivation | 0.85 | D | shipped (hypothesis-only) | Benediktsson 1997 |
| `spiral_artery_count` | Spiral arteries supplying IVS | 100 | C | phase3 | Pijnenborg 2006 |
| `spiral_artery_diameter_term_mm` | Spiral artery diameter | 2.5 | C | phase3 | Pijnenborg 2006 |
| `syncytiotrophoblast_thickness_term_um` | Syncytium thickness | 4 | C | phase3 | Mayhew 2014 |

**Citations needed:** Hoddick 1985, Naeye 1985, Benirschke 2012,
Pijnenborg 2006.

**Out of scope:** preeclampsia spiral-artery remodelling failure
(belongs in a derived dataset); placenta accreta/increta anatomy.

### 3.7 `placental_gas_exchange`

Intervillous PO₂ ~50 mmHg, umbilical vein PO₂ ~30 mmHg, umbilical
artery PO₂ ~15 mmHg. CO₂ moves the other way; the maternal–fetal CO₂
gradient is ~10 mmHg.

| Parameter id | What | Typical | Tier | Status | Primary citation |
| --- | --- | --- | --- | --- | --- |
| `maternal_intervillous_po2_mmhg` | Intervillous PO₂ | 50 | B | shipped | Carter 2009 |
| `gas_max_equilibration` | UV PO₂ / IVS PO₂ | 0.6 | B | shipped | Carter 2009 |
| `umbilical_vein_po2_mmhg` | UV PO₂ | 30 | B | shipped | Carter 2009 |
| `umbilical_artery_po2_mmhg` | UA PO₂ | 15 | B | shipped | Carter 2009 |
| `o2_diffusing_capacity_term_ml_min_mmhg` | DO2 placenta | 6 | C | shipped | Mayhew 1986 |
| `co2_diffusing_capacity_term_ml_min_mmhg` | DCO2 placenta | 6 | C | phase2 | Mayhew 1986 |
| `maternal_fetal_pco2_gradient_term_mmhg` | mPCO₂ − fPCO₂ | 10 | C | shipped | Mayhew 1986 |
| `umbilical_vein_pco2_mmhg` | UV PCO₂ | 40 | B | phase2 | Carter 2009 |
| `umbilical_artery_pco2_mmhg` | UA PCO₂ | 50 | B | phase2 | Carter 2009 |
| `spiral_artery_po2_estimate_mmhg` | Pre-IVS PO₂ | 80 | C | phase3 | Carter 2011 |

**Citations needed:** Mayhew 1986, Carter 2011.

### 3.8 `placental_glucose`

GLUT1 (lower affinity, higher Vmax) on the syncytial basal membrane;
GLUT3 (higher affinity) on the microvillous membrane. Maternal–fetal
glucose gradient is the driver; fetal glucose is ~70% of maternal.

| Parameter id | What | Typical | Tier | Status | Primary citation |
| --- | --- | --- | --- | --- | --- |
| `glucose_glut1_km_mmol_per_l` | GLUT1 Km | 17 | B | shipped | Illsley 2000 |
| `glucose_glut1_vmax_per_area_mmol_per_min_per_m2` | GLUT1 Vmax | 0.5 | B | shipped | Illsley 2000 |
| `glucose_glut3_km_mmol_per_l` | GLUT3 Km | 3 | B | shipped | Illsley 2000 |
| `glucose_glut3_vmax_per_area_mmol_per_min_per_m2` | GLUT3 Vmax | 0.1 | B | shipped | Illsley 2000 |
| `maternal_fetal_glucose_gradient_term_mmol_per_l` | M-F glucose gradient | 1.2 | B | shipped | Illsley 2000 |
| `net_glucose_flux_term_mg_per_kg_per_min` | Net glucose flux | 5 | B | shipped | Illsley 2000 |

**Citations needed:** Cleal 2008, Hay 2006, Battaglia 1986.

**Out of scope:** gestational diabetes glucose kinetics; fetal hyperinsulinaemia.

### 3.9 `placental_endocrine` (NEW subsystem)

The placenta is the largest endocrine organ a body ever hosts. hCG
rescues the corpus luteum in T1, then yields to placental progesterone
production. hPL accumulates linearly. Estriol is a fetal-placental
co-production (placenta lacks 16α-hydroxylase).

| Parameter id | What | Typical | Tier | Status | Primary citation |
| --- | --- | --- | --- | --- | --- |
| `hcg_peak_miu_per_ml` | hCG peak | 100000 | A | shipped | Cole 2010 |
| `hcg_peak_week` | Week of hCG peak | 10 | A | shipped | Cole 2010 |
| `hcg_term_miu_per_ml` | hCG at term | 10000 | A | shipped | Cole 2010 |
| `hpl_baseline_ug_per_ml` | hPL baseline (T1) | 0.5 | B | shipped | Handwerger 2010 |
| `hpl_term_ug_per_ml` | hPL at term | 7 | B | shipped | Handwerger 2010 |
| `progesterone_baseline_ng_per_ml` | Progesterone baseline | 25 | A | shipped | Tulchinsky 1972 |
| `progesterone_term_ng_per_ml` | Progesterone term | 150 | A | shipped | Tulchinsky 1972 |
| `estradiol_baseline_ng_per_ml` | Estradiol baseline | 1 | A | shipped | Tulchinsky 1972 |
| `estradiol_term_ng_per_ml` | Estradiol term | 14 | A | shipped | Tulchinsky 1972 |
| `estriol_term_ng_per_ml` | Estriol term | 10 | A | phase2 | Tulchinsky 1972 |
| `relaxin_t1_ng_per_ml` | Relaxin in T1 | 1.0 | B | phase2 | Conrad 2001 |
| `leptin_term_ng_per_ml` | Leptin at term | 30 | B | phase3 | Hardie 1997 |

**Citations needed:** Cole 2010, Handwerger 2010, Tulchinsky 1972,
Hardie 1997.

### 3.10 `fetal_circulation`

Fetal circulation is in parallel (not series): right and left ventricles
both pump to the body, the combined ventricular output is ~450
mL/min/kg, the RV does ~65% of it, and three shunts (ductus venosus,
foramen ovale, ductus arteriosus) direct the best-oxygenated blood to
the brain and heart.

| Parameter id | What | Typical | Tier | Status | Primary citation |
| --- | --- | --- | --- | --- | --- |
| `fetal_p50_mmhg` | (cross-link to fetal_metabolism) | 19.5 | A | shipped | Bauer 1969 |
| `umbilical_vein_flow_term_ml_per_min` | UV flow at term | 290 | B | shipped | Kiserud 2001 |
| `umbilical_vein_flow_per_kg_term_ml_per_min_per_kg` | UV flow per kg | 80 | B | shipped | Kiserud 2001 |
| `combined_ventricular_output_term_ml_per_min_per_kg` | CVO/kg | 450 | B | shipped | Sutton 1991 |
| `right_ventricular_output_fraction_term` | RV fraction of CVO | 0.60 | B | shipped | Sutton 1991 |
| `ductus_venosus_shunt_fraction_mid_pregnancy` | DV shunt fraction (mid) | 0.30 | B | shipped | Kiserud 2000 |
| `ductus_venosus_shunt_fraction_late_pregnancy` | DV shunt fraction (late) | 0.20 | B | shipped | Kiserud 2000 |
| `foramen_ovale_streamline_preference` | FO streamline preference | 0.55 | B | shipped | Rudolph 1985 |
| `ductus_arteriosus_share` | DA share of CVO | 0.55 | B | shipped | Rudolph 1985 |
| `aortic_isthmus_flow_fraction_cvo_term` | Isthmus/CVO | 0.10 | C | shipped | Rudolph 1985 |
| `coronary_flow_fraction_cvo_term` | Coronary/CVO | 0.03 | C | shipped | Rudolph 1985 |
| `mca_flow_term_ml_per_min` | MCA flow term | 30 | C | phase3 | Mari 1995 |
| `fhr_baseline_bpm` | FHR in T1 | 170 | A | shipped | von Steinburg 2013 |
| `fhr_term_bpm` | FHR at term | 140 | A | shipped | von Steinburg 2013 |
| `ua_pi_baseline` | UA PI baseline | 1.5 | B | shipped | Acharya 2005 |
| `ua_pi_term` | UA PI at term | 0.85 | B | shipped | Acharya 2005 |
| `mca_pi_baseline` | MCA PI baseline | 1.4 | C | shipped | Mari 1995 |
| `mca_pi_peak` | MCA PI peak | 1.9 | C | shipped | Mari 1995 |

**Citations needed:** Kiserud 2001, Rudolph 1985, Sutton 1991, Mari
1995, von Steinburg 2013, Acharya 2005.

### 3.11 `fetal_growth`

Hadlock biometry (BPD, HC, AC, FL → EFW) is the standard worldwide.
The NICHD Buck Louis 2015 cohort provides race-stratified longitudinal
curves; we use the all-cohort means at 4-week resolution.

| Parameter id | What | Typical | Tier | Status | Primary citation |
| --- | --- | --- | --- | --- | --- |
| `efw_20w_g` | EFW at 20w | 330 | A | shipped | Buck Louis 2015 |
| `efw_28w_g` | EFW at 28w | 1100 | A | shipped | Buck Louis 2015 |
| `efw_36w_g` | EFW at 36w | 2800 | A | shipped | Buck Louis 2015 |
| `efw_40w_g` | EFW at term | 3500 | A | shipped | Buck Louis 2015 |
| `bpd_28w_mm` | BPD at 28w | 71 | A | shipped | Hadlock 1982 |
| `fl_28w_mm` | FL at 28w | 53 | A | shipped | Hadlock 1982 |
| `hadlock_coefficient` | Pseudo-parameter | — | A | shipped | Hadlock 1991 |
| `efw_16w_g` | EFW at 16w | 145 | A | shipped | Buck Louis 2015 |
| `efw_24w_g` | EFW at 24w | 650 | A | shipped | Buck Louis 2015 |
| `efw_32w_g` | EFW at 32w | 1800 | A | shipped | Buck Louis 2015 |
| `bpd_16w_mm` | BPD at 16w | 35 | A | shipped | Buck Louis 2015 |
| `bpd_20w_mm` | BPD at 20w | 47 | A | shipped | Buck Louis 2015 |
| `bpd_24w_mm` | BPD at 24w | 61 | A | shipped | Buck Louis 2015 |
| `bpd_32w_mm` | BPD at 32w | 82 | A | shipped | Buck Louis 2015 |
| `bpd_36w_mm` | BPD at 36w | 89 | A | shipped | Buck Louis 2015 |
| `bpd_40w_mm` | BPD at 40w | 93 | A | shipped | Buck Louis 2015 |
| `hc_16w_mm` | HC at 16w | 124 | A | shipped | Buck Louis 2015 |
| `hc_20w_mm` | HC at 20w | 175 | A | shipped | Buck Louis 2015 |
| `hc_24w_mm` | HC at 24w | 225 | A | shipped | Buck Louis 2015 |
| `hc_28w_mm` | HC at 28w | 267 | A | shipped | Buck Louis 2015 |
| `hc_32w_mm` | HC at 32w | 297 | A | shipped | Buck Louis 2015 |
| `hc_36w_mm` | HC at 36w | 322 | A | shipped | Buck Louis 2015 |
| `hc_40w_mm` | HC at 40w | 343 | A | shipped | Buck Louis 2015 |
| `ac_16w_mm` | AC at 16w | 105 | A | shipped | Buck Louis 2015 |
| `ac_20w_mm` | AC at 20w | 152 | A | shipped | Buck Louis 2015 |
| `ac_24w_mm` | AC at 24w | 198 | A | shipped | Buck Louis 2015 |
| `ac_28w_mm` | AC at 28w | 240 | A | shipped | Buck Louis 2015 |
| `ac_32w_mm` | AC at 32w | 282 | A | shipped | Buck Louis 2015 |
| `ac_36w_mm` | AC at 36w | 322 | A | shipped | Buck Louis 2015 |
| `ac_40w_mm` | AC at 40w | 354 | A | shipped | Buck Louis 2015 |
| `fl_16w_mm` | FL at 16w | 21 | A | shipped | Buck Louis 2015 |
| `fl_20w_mm` | FL at 20w | 33 | A | shipped | Buck Louis 2015 |
| `fl_24w_mm` | FL at 24w | 44 | A | shipped | Buck Louis 2015 |
| `fl_32w_mm` | FL at 32w | 62 | A | shipped | Buck Louis 2015 |
| `fl_36w_mm` | FL at 36w | 70 | A | shipped | Buck Louis 2015 |
| `fl_40w_mm` | FL at 40w | 76 | A | shipped | Buck Louis 2015 |

**Citations needed:** none (Buck Louis 2015 + Hadlock 1991 cover it).

### 3.12 `fetal_metabolism`

Fetal blood is intrinsically more acidic and more lactate-rich than
maternal (it accepts CO₂; it has limited gluconeogenic capacity).
Fetal cortisol rises late and is thought to be one of the initiators
of parturition.

| Parameter id | What | Typical | Tier | Status | Primary citation |
| --- | --- | --- | --- | --- | --- |
| `fetal_p50_mmhg` | HbF P50 | 19.5 | A | shipped | Bauer 1969 |
| `fetal_haematocrit_term_pct` | Fetal Hct term | 50 | A | shipped | Saling 1968 |
| `fetal_haemoglobin_term_g_per_dl` | Fetal Hb term | 17 | A | shipped | Saling 1968 |
| `fetal_oxygen_consumption_ml_per_kg_per_min` | VO₂/kg fetal | 8 | B | shipped | Battaglia 1986 |
| `umbilical_artery_ph_term` | UA pH at term | 7.27 | B | shipped | Battaglia 1986 |
| `umbilical_vein_ph_term` | UV pH at term | 7.34 | B | shipped | Battaglia 1986 |
| `umbilical_artery_lactate_term_mmol_per_l` | UA lactate | 3.5 | C | shipped | Battaglia 1986 |
| `fetal_glucose_term_mmol_per_l` | Fetal glucose | 3.5 | B | shipped | Battaglia 1986 |
| `fetal_insulin_term_pmol_per_l` | Term fetal insulin | 50 | C | phase3 | Economides 1989 |
| `fetal_cortisol_term_ug_per_dl` | Term fetal cortisol | 15 | C | phase3 | Murphy 1973 |
| `fetal_core_temperature_c_term` | Fetal core temp | 37.6 | B | shipped | Battaglia 1986 |
| `fetal_urine_output_ml_per_kg_h_term` | Fetal urine output | 50 | C | shipped | Battaglia 1986 |
| `pulmonary_fluid_net_rate_baseline_ml_per_kg_h` | Lung-liquid secretion (mid) | 5 | D | shipped (hypothesis-only) | Strang 1991 |
| `pulmonary_fluid_net_rate_term_ml_per_kg_h` | Lung-liquid net rate (term) | -5 | D | shipped (hypothesis-only) | Strang 1991 |

**Citations needed:** Westgren 1995, Economides 1989, Murphy 1973,
Asakura 2004, Rabinowitz 1989.

### 3.13 `amniotic_fluid` (NEW subsystem)

AFV rises through 32–34 weeks (~800 mL peak) and declines toward term.
Composition shifts: glucose falls, creatinine rises, osmolality falls
modestly as fetal urine dominates the source.

| Parameter id | What | Typical | Tier | Status | Primary citation |
| --- | --- | --- | --- | --- | --- |
| `afv_peak_ml` | AFV peak volume | 800 | A | shipped | Brace 1989 |
| `afv_peak_week` | Week of AFV peak | 33 | A | shipped | Brace 1989 |
| `afv_term_ml` | AFV at term | 600 | A | shipped | Brace 1989 |
| `afv_20w_ml` | AFV at 20w | 350 | A | shipped | Brace 1989 |
| `afv_early_baseline_ml` | AFV early-pregnancy baseline | 50 | B | shipped | Brace 1989 |
| `afv_spread_weeks` | AFV piecewise spread | 4 | C | shipped | Brace 1989 |
| `af_glucose_term_mmol_per_l` | AF glucose term | 0.5 | B | phase3 | Magann 2007 |
| `af_lactate_term_mmol_per_l` | AF lactate term | 4 | B | phase3 | Magann 2007 |
| `af_creatinine_term_mg_per_dl` | AF creatinine term | 2.0 | B | phase3 | Magann 2007 |
| `af_osmolality_term_mosm_per_kg` | AF osmolality | 260 | B | phase3 | Magann 2007 |
| `fetal_swallowing_term_ml_per_24h` | Fetal swallow rate | 700 | C | phase3 | Pritchard 1966 |

**Citations needed:** Brace 1989, Magann 2007, Pritchard 1966.

## 4. Citation catalog (full)

The dataset already contains **58 citations**. The lists below are
the original catalog plan; ✓ marks citations that have since landed.
Each remaining new citation must pass the Crossref-metadata audit
before merge.

### Phase 1 citations (~6 new)

- Kline 2005 — D-dimer in pregnancy
- Larsson 2008 — serum proteins in pregnancy *(superseded; albumin/total protein parameters are sourced from Hytten 1980 instead)*
- Pitkin 1979 — WBC in pregnancy *(superseded; WBC parameter is sourced from Hytten 1980 instead)*
- ✓ Templeton 1976 — blood gases in pregnancy
- ✓ Lim 1976 — acid-base in pregnancy
- ✓ Conrad 2001 — relaxin-driven GFR rise

### Phase 2 citations (~25 new)

- Stirling 1984 — clotting factors longitudinal
- Faught 1995 — protein S/C/AT in pregnancy
- ✓ Davison 1981 — osmoregulation in pregnancy
- Higby 1994 — 24h urinary protein normal pregnancy *(superseded; sourced from Cheung 2013)*
- Carr 1981 — cortisol/CBG in pregnancy
- ✓ Glinoer 1997 — thyroid axis in pregnancy
- Tyson 1972 — prolactin in pregnancy *(superseded; sourced from Tulchinsky 1972)*
- Wilson 1980 — renin-aldosterone in pregnancy *(superseded; sourced from Cheung 2013)*
- ✓ Catalano 1991 — HOMA-IR / insulin sensitivity
- ✓ Cole 2010 — hCG kinetics
- ✓ Handwerger 2010 — hPL
- ✓ Tulchinsky 1972 — steroid hormones in pregnancy
- Hoddick 1985 — placental thickness ultrasound
- Naeye 1985 — umbilical cord length
- ✓ Mayhew 1986 — placental diffusing capacity
- Carter 2011 — pre-IVS spiral artery PO₂
- Cleal 2008 — placental glucose flux *(superseded; sourced from Illsley 2000)*
- Hay 2006 — transplacental glucose *(superseded; sourced from Illsley 2000)*
- ✓ Battaglia 1986 — fetal substrate metabolism (textbook)
- ✓ Kiserud 2001 — umbilical vein flow Doppler
- ✓ Rudolph 1985 — fetal circulation distribution
- Westgren 1995 — fetal scalp blood gases *(superseded; sourced from Battaglia 1986)*
- ✓ von Steinburg 2013 — fetal heart rate longitudinal
- ✓ Brace 1989 — AFV regulation
- Rabinowitz 1989 — fetal urine output *(superseded; sourced from Battaglia 1986)*

### Phase 3 citations (~15 new)

- Kruithof 1987 — PAI-1/PAI-2
- Robson 1989 *Br Heart J* — LV mass in pregnancy *(superseded; sourced from Sanghavi 2014)*
- ✓ Crapo 1996 — DLCO reference
- Eriksson 1989 — placental GH
- Benirschke 2012 — placental anatomy textbook
- Pijnenborg 2006 — spiral artery anatomy
- ✓ Sutton 1991 — fetal aortic isthmus
- ✓ Mari 1995 — MCA Doppler
- ✓ Acharya 2005 — umbilical artery PI
- Hardie 1997 — leptin in pregnancy
- Economides 1989 — fetal endocrine
- Murphy 1973 — fetal cortisol
- Asakura 2004 — fetal temperature *(superseded; sourced from Battaglia 1986)*
- Magann 2007 — amniotic fluid chemistry
- Pritchard 1966 — fetal swallowing

### Additional citations landed (outside the original phase plan)

- ✓ Bianchi 1996 — fetal microchimerism (hypothesis-only)
- ✓ Strang 1991 — fetal lung liquid secretion/reabsorption (hypothesis-only)
- ✓ Palmeira 2012 — placental IgG transfer (hypothesis-only)
- ✓ Benediktsson 1997 — placental 11β-HSD2 (hypothesis-only)
- ✓ Hutcheon 2012 — placental weight allometry
- ✓ Burton 2010 — placental development

## 5. Schema-level changes implied by this catalog

Three new subsystems are introduced (`maternal_endocrine`,
`placental_endocrine`, `amniotic_fluid`). The `subsystem` enum in
`dataset/schema/parameter.schema.json` is extended additively — no
breaking change for existing consumers.

No other schema fields are added. Value units, trajectory shapes,
extraction blocks, and applicability blocks already cover everything
in the catalog.

## 6. Verification budget

If every catalogued parameter ships at its anticipated tier and review
status, the total dataset would contain:

- Tier A: ~80 parameters
- Tier B: ~100 parameters
- Tier C: ~30 parameters
- Tier D: 0 (the catalog deliberately does not include hypothetical
  channels — those live in spec 03's Phase C)

Reaching `review_status: verified` for all Tier A/B entries requires
~80–100 hours of careful, paywall-tolerant curation. That is the honest
solo-maintainer cost of completing the project to its declared ceiling.

## 7. Explicit non-goals (final, locked)

Listed once more so this doc can stand alone:

- **Pre-eclampsia, FGR, gestational diabetes, infection, stillbirth,
  PPH, drug exposure, PK** — derived datasets, not this one.
- **Twin / higher-order pregnancy** — its own dataset.
- **Embryology < 8w, labour, postpartum** — out of scope.
- **Animal data** — even where excellent.
- **Pathophysiology and clinical decision support** — forever out of
  scope. Researchers build those on top of nidus, not inside it.

The boundary is not capability. It is honest scope.

## 8. Living-document policy

This catalog is updated when:

- A new parameter ships → status moves from `phaseN` to `shipped`.
- A new citation lands → moves from "needed" to "in dataset".
- A new gap is identified → added with `phaseN` status and a draft
  citation.

The catalog is the *index*; the dataset JSON is the *truth*. If they
disagree, the JSON wins and this doc gets corrected.
