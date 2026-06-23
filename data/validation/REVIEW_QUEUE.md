# Machine pre-verification review queue

**This is not verification.** A machine fetched each parameter's primary source (open-access full text where available, otherwise the abstract) and compared it to the stored value. Your job: read the quote (and, where needed, the full paper), confirm or correct the value, then set `extraction.review_status` to `verified` (or `contested`) in the dataset. The machine never does that promotion.

## Summary

| Verdict | Count |
| ------- | ----- |
| ❌ mismatch — source appears to report a different value | 11 |
| 🟡 close — same ballpark, confirm exact figure / statistic | 117 |
| ✅ match — source value agrees with stored value | 51 |
| 🔍 not found — value not in fetched text (check table/figure in full PDF) | 46 |
| ⬜ no source — book / paywalled / no abstract retrieved | 18 |
| **Total parameters** | **243** |

Work top-down: mismatches first (a wrong value is worse than an unverified one), then Tier A/B, then the rest.

## ❌ mismatch — source appears to report a different value  (11)

### `fetal_circulation.umbilical_vein_flow_per_kg_term_ml_per_min_per_kg`  ·  Tier B  ·  stored: 80.0 mL/min/kg

- **Primary citation:** `kiserud-2001-umbilical-vein`  (_evidence: secondary_)
- **Source reports:** Human term PC-MRI reports weight-normalised umbilical-vein flow of 134 mL/min/kg (2 SD 62-206), well above the stored 80 mL/min/kg. PC-MRI systematically yields higher umbilical flows than Doppler velocimetry (the basis of the Kiserud-derived stored value).
- **Quote:** > Umbilical vein: 134 (62, 206)
- **Reviewer note:** SECONDARY: PC-MRI UV flow 134 mL/min/kg exceeds stored 80 (65-100); discrepancy attributable to MRI-vs-Doppler modality difference, not necessarily an error in the Doppler-based stored value.

### `maternal_blood.plasma_volume_early_l`  ·  Tier B  ·  stored: 3.05 L

- **Primary citation:** `bernstein-ziegler-2001-plasma-volume`  (_evidence: abstract_)
- **Source reports:** Bernstein 2001 reports plasma volume of 2320 +/- 280 mL (= 2.32 L) at 12 menstrual weeks, well below the stored central 3.05 L and below the stored low bound of 2.75 L.
- **Quote:** > Plasma volume at LH surge + 70 days (12 menstrual weeks, 2320 +/- 280 mL) was greater than either menstrual cycle estimates or early pregnancy estimates of plasma volume.
- **Reviewer note:** Source 12-week plasma volume is 2.32 L; stored 3.05 L (range 2.75-3.35) is ~0.7 L higher and the source value falls below the stored range. Flag for human review.

### `maternal_blood.protein_s_free_term_pct`  ·  Tier B  ·  stored: 45 %

- **Primary citation:** `faught-1995-protein-s-c`  (_evidence: abstract_)
- **Source reports:** Faught 1995 reports free protein S fell to a mean of 0.26 U/mL by the second trimester with no further fall in the third (so term ~0.26 U/mL ~= 26%). The stored 45% matches the FIRST-trimester mean (0.45 U/mL), not term; the source term value (~26%) falls below the stored range (30-60%).
- **Quote:** > Free protein S levels fell significantly from first to second trimesters (0.45 U/ml mean to 0.26 U/ml mean, p < 0.001), but no further fall occurred during the third trimester.
- **Reviewer note:** Stored term value 45% equals the source's first-trimester mean (0.45 U/mL); the source's actual term (3rd-trimester) free protein S is ~0.26 U/mL (~26%), below the stored low bound of 30%. Flag for human review.

### `maternal_cardiovascular.baseline_uterine_flow_ml_per_min`  ·  Tier B  ·  stored: 50.0 mL/min

- **Primary citation:** `thaler-1990-uterine-flow`  (_evidence: abstract_)
- **Source reports:** Abstract reports 94.5 ml/min in the left ascending uterine artery before pregnancy (i.e. ~189 ml/min bilateral), far above the stored 50 ml/min.
- **Quote:** > a steady increase in volume flow rate in the left ascending uterine artery from a mean of 94.5 ml/min before pregnancy
- **Reviewer note:** Stored 50 ml/min combined vs Thaler's 94.5 ml/min single-artery pre-pregnancy (~189 bilateral). Already flagged in dataset notes; ~3.8x discrepancy.

### `maternal_cardiovascular.lv_mass_term_g`  ·  Tier B  ·  stored: 180.0 g

- **Primary citation:** `sanghavi-rutherford-2014-cardio-review`  (_evidence: secondary_)
- **Source reports:** Authoritative pregnancy-specific position statement: LV mass increases only 5-10% in pregnancy. Applied to a ~130 g baseline that is ~137-143 g, far below the stored 180 g (a ~38% rise). Larger percentages in the literature generally refer to wall thickness, not chamber LV mass.
- **Quote:** > There is a 5-10% overall increase in left ventricular mass and wall thickness of 25-30% above pre-pregnancy levels, all staying within normal values.
- **Reviewer note:** SECONDARY: pregnancy LV-mass rise is 5-10% per BSE position statement; stored 180 g implies ~38% and looks too high.

### `maternal_cardiovascular.peak_excess_cardiac_output_l_per_min`  ·  Tier B  ·  stored: 2.7 L/min

- **Primary citation:** `mahendru-2014-cardiac-output`  (_evidence: abstract_)
- **Source reports:** Abstract reports the greatest CO increase as Δ0.6±1 l/min (by T2), markedly below the stored peak excess of 2.7 L/min.
- **Quote:** > The greatest increase in cardiac output occurred by the second trimester (Δ: 0.6 ± 1 l/min, P < 0.001)
- **Reviewer note:** Stored 2.7 L/min peak excess vs abstract's Δ0.6±1 l/min for the same CO-rise quantity. Flagged in dataset notes for re-investigation against full results.

### `maternal_endocrine.cbg_term_mg_per_l`  ·  Tier B  ·  stored: 70 mg/L

- **Primary citation:** `carr-1981-cortisol`  (_evidence: secondary_)
- **Source reports:** Total CBG in pregnant women (third trimester) 877 +/- 27 nmol/L vs 466 +/- 13 in non-pregnant controls (~1.9x rise). Converting at CBG MW ~52 kDa: 877 nmol/L ~ 45.6 mg/L, below the stored range 55-90 (central 70). Direction and ~2x fold-rise agree, but the converted absolute value is lower than stored.
- **Quote:** > Total CBG concentrations were greater in pregnant women than control subjects (877 +/- 27 vs 466 +/- 13 nmol/L; P < 0.0001)
- **Reviewer note:** SECONDARY: term total CBG 877 nmol/L ~ 45.6 mg/L (MW ~52 kDa) is below stored 55-90 (central 70); ~1.9x rise vs non-pregnant agrees in direction but absolute converted value is lower.

### `placental_structure.placenta_to_fetus_weight_ratio_term`  ·  Tier B  ·  stored: 0.14 fraction

- **Primary citation:** `burton-2010-placental-development`  (_evidence: secondary_)
- **Source reports:** Mean fetoplacental (fetus:placenta) weight ratio in the normal group was 5.52, i.e. placenta:fetus = 1/5.52 = 0.181.
- **Quote:** > The mean of the fetoplacental ratio in the normal group was 5.52 ± 0.07
- **Reviewer note:** SECONDARY: reported fetoplacental ratio 5.52 inverts to placenta:fetus 0.181, above stored 0.14 (range 0.11-0.17).

### `maternal_cardiovascular.lv_wall_thickness_term_mm`  ·  Tier C  ·  stored: 11 mm

- **Primary citation:** `sanghavi-rutherford-2014-cardio-review`  (_evidence: secondary_)
- **Source reports:** Pregnancy-specific position statement reports septal/posterior wall thickness of 7-8 mm during pregnancy (IVSd 0.7 cm, PWTd 0.8 cm), rising 25-30% but staying within normal values (<~9 mm). Stored 11 mm exceeds these reference values.
- **Quote:** > wall thickness of 25-30% above pre-pregnancy levels, all staying within normal values
- **Reviewer note:** SECONDARY: pregnant LV wall thickness ~7-9 mm per BSE; stored 11 mm appears too high.

### `maternal_cardiovascular.pulse_wave_velocity_term_m_per_s`  ·  Tier C  ·  stored: 7.5 m/s

- **Primary citation:** `sanghavi-rutherford-2014-cardio-review`  (_evidence: secondary_)
- **Source reports:** In normotensive third-trimester women, pulse wave velocity was 5.0 m/s (IQR 1.2). Stored 7.5 m/s is well above this measured value, though absolute PWV is strongly method/device dependent.
- **Quote:** > Pulse wave velocity was significantly higher in preeclamptic than normotensive women (6.6 IQR 1.8 versus 5.0 IQR 1.2; p = 0.000).
- **Reviewer note:** SECONDARY: measured normotensive third-trimester PWV ~5.0 m/s; stored 7.5 m/s higher (method-dependent caveat).

### `placental_structure.villous_capillary_length_total_km_term`  ·  Tier C  ·  stored: 300.0 km

- **Primary citation:** `mayhew-2014-placental-morphometry`  (_evidence: secondary_)
- **Source reports:** Normal human placental capillary network estimated at 550 km length and 15 m^2 surface area.
- **Quote:** > the capillary network in a normal human placenta is estimated to be 550 km in length and 15 square meters in surface area
- **Reviewer note:** SECONDARY: review cites ~550 km, well above stored 300 km (range 280-320).

## 🟡 close — same ballpark, confirm exact figure / statistic  (117)

### `amniotic_fluid.afv_20w_ml`  ·  Tier A  ·  stored: 350.0 mL

- **Primary citation:** `brace-1989-amniotic-fluid`  (_evidence: secondary_)
- **Source reports:** Secondary textbook chapter's 50th-percentile AFV table gives 425.8 mL at 20 weeks. This brackets the stored central 350 mL (which sits below the median but within the normal spread for this gestational age).
- **Quote:** > Amniotic fluid volumes are in milliliters ... 425.8 mL at 20 weeks' gestation at the 50th percentile
- **Reviewer note:** SECONDARY: median 425.8 mL at 20 wk brackets stored 350 mL (below median, plausible).

### `amniotic_fluid.afv_peak_ml`  ·  Tier A  ·  stored: 800.0 mL

- **Primary citation:** `brace-1989-amniotic-fluid`  (_evidence: abstract_)
- **Source reports:** Abstract reports mean amniotic fluid volume averaged 777 ml between 22 and 39 weeks (95% CI 302-1997 ml). It frames this as a flat average, not a peak, stating volume did not change significantly over that interval. The stored peak central 800 is not stated, but 777 lies within the stored range 600-1000.
- **Quote:** > mean amniotic fluid volume did not change significantly between 22 and 39 weeks and averaged 777 ml, with the 95% confidence interval ranging from 302 to 1997 ml.
- **Reviewer note:** Abstract mean 777 ml falls within stored range 600-1000; but abstract describes a flat plateau, not a peak of 800. Per-week nomogram peak not in abstract.

### `amniotic_fluid.afv_term_ml`  ·  Tier A  ·  stored: 600.0 mL

- **Primary citation:** `brace-1989-amniotic-fluid`  (_evidence: secondary_)
- **Source reports:** Secondary textbook chapter's 50th-percentile AFV table gives 543.5 mL at 40 weeks. This brackets the stored term central 600 mL. (Other reviews quote ~800 mL at 40 wk; nomograms differ, so the stored 600 mL sits within the cross-source spread.)
- **Quote:** > the same table shows 543.5 mL at 40 weeks' gestation at the 50th percentile
- **Reviewer note:** SECONDARY: median 543.5 mL at 40 wk brackets stored 600 mL; reviews span ~540-800 mL.

### `fetal_circulation.fhr_term_bpm`  ·  Tier A  ·  stored: 140.0 bpm

- **Primary citation:** `von-steinburg-2013-fhr`  (_evidence: fulltext_)
- **Source reports:** Table 4: mean FHR baseline at >=37 weeks is 136.0-136.4 bpm (95% CI); weeks 37-42 range ~133-138 bpm. Normal range stated as 120-160 bpm.
- **Quote:** > Gestational age n 95% confidence interval A &lt;28 1230 140.7538 – 141.9422 … &gt;=37 8478 136.0104 – 136.4295
- **Reviewer note:** Source term mean is ~136 bpm, just below stored 140 central but inside stored 130-150 range and the 120-160 normal range; magnitude/direction agree.

### `fetal_circulation.ua_pi_baseline`  ·  Tier A  ·  stored: 1.5 dimensionless

- **Primary citation:** `acharya-2005-umbilical-pi`  (_evidence: secondary_)
- **Source reports:** Large international cohort reports a 50th-centile UA-PI of 1.10 at 24 weeks, falling to 0.79 at 40 weeks. The stored 1.5 at 16-20 weeks lies earlier on the same monotonically declining curve, but modern large cohorts give a somewhat lower mid-second-trimester median than the stored central value.
- **Quote:** > Gestational age 24+0, Centile 50th: 1.10 ... Gestational age 40+0, Centile 50th: 0.79
- **Reviewer note:** SECONDARY: median UA-PI 1.10 at 24 wk on a declining curve; stored 1.5 at 16-20 wk plausibly higher earlier but exceeds modern-cohort medians, so consistency is approximate.

### `fetal_growth.ac_16w_mm`  ·  Tier A  ·  stored: 105.0 mm

- **Primary citation:** `buck-louis-2015-nichd-growth`  (_evidence: secondary_)
- **Source reports:** INTERGROWTH-21st 50th-centile AC at 16 completed weeks = 103.2 mm (stored 105.0; 1.7% diff).
- **Quote:** > 16  93.0 94.3 96.3  103.2  110.1 112.1 113.4
- **Reviewer note:** SECONDARY and DIFFERENT standard: INTERGROWTH-21st (Papageorghiou Lancet 2014 / Stirnemann UOG 2016), not the cited NICHD/Buck Louis. 50th-centile 103.2 mm brackets stored 105.0 mm (1.7% diff).

### `fetal_growth.ac_20w_mm`  ·  Tier A  ·  stored: 152.0 mm

- **Primary citation:** `buck-louis-2015-nichd-growth`  (_evidence: secondary_)
- **Source reports:** INTERGROWTH-21st 50th-centile AC at 20 completed weeks = 147.7 mm (stored 152.0; 2.9% diff).
- **Quote:** > 20  133.4 135.2 138.0  147.7  157.5 160.3 162.1
- **Reviewer note:** SECONDARY and DIFFERENT standard: INTERGROWTH-21st (Papageorghiou Lancet 2014 / Stirnemann UOG 2016), not the cited NICHD/Buck Louis. 50th-centile 147.7 mm brackets stored 152.0 mm (2.9% diff).

### `fetal_growth.ac_24w_mm`  ·  Tier A  ·  stored: 198.0 mm

- **Primary citation:** `buck-louis-2015-nichd-growth`  (_evidence: secondary_)
- **Source reports:** INTERGROWTH-21st 50th-centile AC at 24 completed weeks = 191.2 mm (stored 198.0; 3.6% diff).
- **Quote:** > 24  173.3 175.6 179.0  191.2  203.3 206.8 209.0
- **Reviewer note:** SECONDARY and DIFFERENT standard: INTERGROWTH-21st (Papageorghiou Lancet 2014 / Stirnemann UOG 2016), not the cited NICHD/Buck Louis. 50th-centile 191.2 mm brackets stored 198.0 mm (3.6% diff).

### `fetal_growth.ac_28w_mm`  ·  Tier A  ·  stored: 240.0 mm

- **Primary citation:** `buck-louis-2015-nichd-growth`  (_evidence: secondary_)
- **Source reports:** INTERGROWTH-21st 50th-centile AC at 28 completed weeks = 233.3 mm (stored 240.0; 2.9% diff).
- **Quote:** > 28  212.1 214.7 218.8  233.3  247.8 251.9 254.5
- **Reviewer note:** SECONDARY and DIFFERENT standard: INTERGROWTH-21st (Papageorghiou Lancet 2014 / Stirnemann UOG 2016), not the cited NICHD/Buck Louis. 50th-centile 233.3 mm brackets stored 240.0 mm (2.9% diff).

### `fetal_growth.ac_36w_mm`  ·  Tier A  ·  stored: 322.0 mm

- **Primary citation:** `buck-louis-2015-nichd-growth`  (_evidence: secondary_)
- **Source reports:** INTERGROWTH-21st 50th-centile AC at 36 completed weeks = 312.8 mm (stored 322.0; 2.9% diff).
- **Quote:** > 36  280.8 284.8 291.0  312.8  334.6 340.9 344.9
- **Reviewer note:** SECONDARY and DIFFERENT standard: INTERGROWTH-21st (Papageorghiou Lancet 2014 / Stirnemann UOG 2016), not the cited NICHD/Buck Louis. 50th-centile 312.8 mm brackets stored 322.0 mm (2.9% diff).

### `fetal_growth.ac_40w_mm`  ·  Tier A  ·  stored: 354.0 mm

- **Primary citation:** `buck-louis-2015-nichd-growth`  (_evidence: secondary_)
- **Source reports:** INTERGROWTH-21st 50th-centile AC at 40 completed weeks = 349.8 mm (stored 354.0; 1.2% diff).
- **Quote:** > 40  307.7 312.9 321.1  349.8  378.5 386.7 392.0
- **Reviewer note:** SECONDARY and DIFFERENT standard: INTERGROWTH-21st (Papageorghiou Lancet 2014 / Stirnemann UOG 2016), not the cited NICHD/Buck Louis. 50th-centile 349.8 mm brackets stored 354.0 mm (1.2% diff).

### `fetal_growth.bpd_16w_mm`  ·  Tier A  ·  stored: 35.0 mm

- **Primary citation:** `buck-louis-2015-nichd-growth`  (_evidence: secondary_)
- **Source reports:** INTERGROWTH-21st 50th-centile BPD at 16 completed weeks = 35.7 mm (stored 35.0; 2.0% diff).
- **Quote:** > 16  32.0 32.5 33.2  35.7  38.1 38.8 39.3
- **Reviewer note:** SECONDARY and DIFFERENT standard: INTERGROWTH-21st (Papageorghiou Lancet 2014 / Stirnemann UOG 2016), not the cited NICHD/Buck Louis. 50th-centile 35.7 mm brackets stored 35.0 mm (2.0% diff).

### `fetal_growth.bpd_20w_mm`  ·  Tier A  ·  stored: 47.0 mm

- **Primary citation:** `buck-louis-2015-nichd-growth`  (_evidence: secondary_)
- **Source reports:** INTERGROWTH-21st 50th-centile BPD at 20 completed weeks = 48.4 mm (stored 47.0; 2.9% diff).
- **Quote:** > 20  44.1 44.7 45.5  48.4  51.4 52.2 52.8
- **Reviewer note:** SECONDARY and DIFFERENT standard: INTERGROWTH-21st (Papageorghiou Lancet 2014 / Stirnemann UOG 2016), not the cited NICHD/Buck Louis. 50th-centile 48.4 mm brackets stored 47.0 mm (2.9% diff).

### `fetal_growth.bpd_24w_mm`  ·  Tier A  ·  stored: 61.0 mm

- **Primary citation:** `buck-louis-2015-nichd-growth`  (_evidence: secondary_)
- **Source reports:** INTERGROWTH-21st 50th-centile BPD at 24 completed weeks = 61.4 mm (stored 61.0; 0.7% diff).
- **Quote:** > 24  56.4 57.0 58.0  61.4  64.8 65.7 66.4
- **Reviewer note:** SECONDARY and DIFFERENT standard: INTERGROWTH-21st (Papageorghiou Lancet 2014 / Stirnemann UOG 2016), not the cited NICHD/Buck Louis. 50th-centile 61.4 mm brackets stored 61.0 mm (0.7% diff).

### `fetal_growth.bpd_28w_mm`  ·  Tier A  ·  stored: 71.5 mm

- **Primary citation:** `buck-louis-2015-nichd-growth`  (_evidence: secondary_)
- **Source reports:** INTERGROWTH-21st 50th-centile BPD at 28 completed weeks = 73.5 mm (stored 71.5; 2.7% diff).
- **Quote:** > 28  67.9 68.6 69.7  73.5  77.3 78.3 79.0
- **Reviewer note:** SECONDARY and DIFFERENT standard: INTERGROWTH-21st (Papageorghiou Lancet 2014 / Stirnemann UOG 2016), not the cited NICHD/Buck Louis. 50th-centile 73.5 mm brackets stored 71.5 mm (2.7% diff).

### `fetal_growth.bpd_32w_mm`  ·  Tier A  ·  stored: 82.0 mm

- **Primary citation:** `buck-louis-2015-nichd-growth`  (_evidence: secondary_)
- **Source reports:** INTERGROWTH-21st 50th-centile BPD at 32 completed weeks = 83.8 mm (stored 82.0; 2.1% diff).
- **Quote:** > 32  77.8 78.5 79.7  83.8  87.8 89.0 89.8
- **Reviewer note:** SECONDARY and DIFFERENT standard: INTERGROWTH-21st (Papageorghiou Lancet 2014 / Stirnemann UOG 2016), not the cited NICHD/Buck Louis. 50th-centile 83.8 mm brackets stored 82.0 mm (2.1% diff).

### `fetal_growth.bpd_36w_mm`  ·  Tier A  ·  stored: 89.0 mm

- **Primary citation:** `buck-louis-2015-nichd-growth`  (_evidence: secondary_)
- **Source reports:** INTERGROWTH-21st 50th-centile BPD at 36 completed weeks = 91.2 mm (stored 89.0; 2.4% diff).
- **Quote:** > 36  84.7 85.5 86.8  91.2  95.7 96.9 97.7
- **Reviewer note:** SECONDARY and DIFFERENT standard: INTERGROWTH-21st (Papageorghiou Lancet 2014 / Stirnemann UOG 2016), not the cited NICHD/Buck Louis. 50th-centile 91.2 mm brackets stored 89.0 mm (2.4% diff).

### `fetal_growth.bpd_40w_mm`  ·  Tier A  ·  stored: 93.0 mm

- **Primary citation:** `buck-louis-2015-nichd-growth`  (_evidence: secondary_)
- **Source reports:** INTERGROWTH-21st 50th-centile BPD at 40 completed weeks = 94.9 mm (stored 93.0; 2.0% diff).
- **Quote:** > 40  87.5 88.4 89.9  94.9  99.9 101.3 102.3
- **Reviewer note:** SECONDARY and DIFFERENT standard: INTERGROWTH-21st (Papageorghiou Lancet 2014 / Stirnemann UOG 2016), not the cited NICHD/Buck Louis. 50th-centile 94.9 mm brackets stored 93.0 mm (2.0% diff).

### `fetal_growth.efw_24w_g`  ·  Tier A  ·  stored: 650.0 g

- **Primary citation:** `buck-louis-2015-nichd-growth`  (_evidence: secondary_)
- **Source reports:** INTERGROWTH-21st 50th-centile EFW at 24 completed weeks = 668 g (stored 650.0; 2.7% diff).
- **Quote:** > 24  575 585 602  668  751 778 796
- **Reviewer note:** SECONDARY and DIFFERENT standard: INTERGROWTH-21st (Papageorghiou Lancet 2014 / Stirnemann UOG 2016), not the cited NICHD/Buck Louis. 50th-centile 668 g brackets stored 650.0 g (2.7% diff).

### `fetal_growth.efw_28w_g`  ·  Tier A  ·  stored: 1141.0 g

- **Primary citation:** `buck-louis-2015-nichd-growth`  (_evidence: secondary_)
- **Source reports:** INTERGROWTH-21st 50th-centile EFW at 28 completed weeks = 1097 g (stored 1141.0; 4.0% diff).
- **Quote:** > 28  892 915 951  1097  1277 1335 1376
- **Reviewer note:** SECONDARY and DIFFERENT standard: INTERGROWTH-21st (Papageorghiou Lancet 2014 / Stirnemann UOG 2016), not the cited NICHD/Buck Louis. 50th-centile 1097 g brackets stored 1141.0 g (4.0% diff).

### `fetal_growth.efw_32w_g`  ·  Tier A  ·  stored: 1800.0 g

- **Primary citation:** `buck-louis-2015-nichd-growth`  (_evidence: secondary_)
- **Source reports:** NICHD 50th-centile EFW at 32w = 1837-1960 g by group (Asian 1830) vs stored 1800 g; stored just below NICHD band.
- **Quote:** > NICHD White: 1960, NICHD Hispanic: 1879, NICHD Asian: 1830, NICHD Black: 1837
- **Reviewer note:** SECONDARY: NICHD Fetal Growth Studies 50th-centile reproduced in Grantz (AJOG 2018, PMC5807181); same NICHD standard family as the cited Buck Louis 2015 source.

### `fetal_growth.efw_36w_g`  ·  Tier A  ·  stored: 2779.0 g

- **Primary citation:** `buck-louis-2015-nichd-growth`  (_evidence: secondary_)
- **Source reports:** INTERGROWTH-21st 50th-centile EFW at 36 completed weeks = 2594 g (stored 2779.0; 7.1% diff).
- **Quote:** > 36  1951 2024 2146  2594  3086 3237 3331
- **Reviewer note:** SECONDARY and DIFFERENT standard: INTERGROWTH-21st (Papageorghiou Lancet 2014 / Stirnemann UOG 2016), not the cited NICHD/Buck Louis. 50th-centile 2594 g brackets stored 2779.0 g (7.1% diff).

### `fetal_growth.efw_40w_g`  ·  Tier A  ·  stored: 3567.0 g

- **Primary citation:** `buck-louis-2015-nichd-growth`  (_evidence: secondary_)
- **Source reports:** INTERGROWTH-21st 50th-centile EFW at 40 completed weeks = 3338 g (stored 3567.0; 6.9% diff).
- **Quote:** > 40  2554 2670 2805  3338  3871 4006 4121
- **Reviewer note:** SECONDARY and DIFFERENT standard: INTERGROWTH-21st (Papageorghiou Lancet 2014 / Stirnemann UOG 2016), not the cited NICHD/Buck Louis. 50th-centile 3338 g brackets stored 3567.0 g (6.9% diff).

### `fetal_growth.fl_16w_mm`  ·  Tier A  ·  stored: 21.0 mm

- **Primary citation:** `buck-louis-2015-nichd-growth`  (_evidence: secondary_)
- **Source reports:** INTERGROWTH-21st 50th-centile FL at 16 completed weeks = 19.5 mm (stored 21.0; 7.7% diff).
- **Quote:** > 16  16.4 16.8 17.4  19.5  21.5 22.1 22.5
- **Reviewer note:** SECONDARY and DIFFERENT standard: INTERGROWTH-21st (Papageorghiou Lancet 2014 / Stirnemann UOG 2016), not the cited NICHD/Buck Louis. 50th-centile 19.5 mm brackets stored 21.0 mm (7.7% diff).

### `fetal_growth.fl_20w_mm`  ·  Tier A  ·  stored: 33.0 mm

- **Primary citation:** `buck-louis-2015-nichd-growth`  (_evidence: secondary_)
- **Source reports:** INTERGROWTH-21st 50th-centile FL at 20 completed weeks = 31.3 mm (stored 33.0; 5.4% diff).
- **Quote:** > 20  28.0 28.4 29.0  31.3  33.6 34.2 34.6
- **Reviewer note:** SECONDARY and DIFFERENT standard: INTERGROWTH-21st (Papageorghiou Lancet 2014 / Stirnemann UOG 2016), not the cited NICHD/Buck Louis. 50th-centile 31.3 mm brackets stored 33.0 mm (5.4% diff).

### `fetal_growth.fl_24w_mm`  ·  Tier A  ·  stored: 44.0 mm

- **Primary citation:** `buck-louis-2015-nichd-growth`  (_evidence: secondary_)
- **Source reports:** INTERGROWTH-21st 50th-centile FL at 24 completed weeks = 41.9 mm (stored 44.0; 5.0% diff).
- **Quote:** > 24  38.3 38.7 39.4  41.9  44.4 45.1 45.5
- **Reviewer note:** SECONDARY and DIFFERENT standard: INTERGROWTH-21st (Papageorghiou Lancet 2014 / Stirnemann UOG 2016), not the cited NICHD/Buck Louis. 50th-centile 41.9 mm brackets stored 44.0 mm (5.0% diff).

### `fetal_growth.fl_28w_mm`  ·  Tier A  ·  stored: 53.0 mm

- **Primary citation:** `buck-louis-2015-nichd-growth`  (_evidence: secondary_)
- **Source reports:** INTERGROWTH-21st 50th-centile FL at 28 completed weeks = 51.3 mm (stored 53.0; 3.3% diff).
- **Quote:** > 28  47.3 47.8 48.6  51.3  54.0 54.8 55.3
- **Reviewer note:** SECONDARY and DIFFERENT standard: INTERGROWTH-21st (Papageorghiou Lancet 2014 / Stirnemann UOG 2016), not the cited NICHD/Buck Louis. 50th-centile 51.3 mm brackets stored 53.0 mm (3.3% diff).

### `fetal_growth.fl_32w_mm`  ·  Tier A  ·  stored: 62.0 mm

- **Primary citation:** `buck-louis-2015-nichd-growth`  (_evidence: secondary_)
- **Source reports:** NICHD 50th-centile FL at 32w = 60-61 mm vs stored 62 mm (~3%).
- **Quote:** > NICHD White: 60, NICHD Hispanic: 60, NICHD Asian: 60, NICHD Black: 61
- **Reviewer note:** SECONDARY: NICHD Fetal Growth Studies 50th-centile reproduced in Grantz (AJOG 2018, PMC5807181); same NICHD standard family as the cited Buck Louis 2015 source.

### `fetal_growth.fl_36w_mm`  ·  Tier A  ·  stored: 70.0 mm

- **Primary citation:** `buck-louis-2015-nichd-growth`  (_evidence: secondary_)
- **Source reports:** INTERGROWTH-21st 50th-centile FL at 36 completed weeks = 66.4 mm (stored 70.0; 5.4% diff).
- **Quote:** > 36  61.3 61.9 62.9  66.4  69.9 70.9 71.5
- **Reviewer note:** SECONDARY and DIFFERENT standard: INTERGROWTH-21st (Papageorghiou Lancet 2014 / Stirnemann UOG 2016), not the cited NICHD/Buck Louis. 50th-centile 66.4 mm brackets stored 70.0 mm (5.4% diff).

### `fetal_growth.fl_40w_mm`  ·  Tier A  ·  stored: 76.0 mm

- **Primary citation:** `buck-louis-2015-nichd-growth`  (_evidence: secondary_)
- **Source reports:** INTERGROWTH-21st 50th-centile FL at 40 completed weeks = 72.1 mm (stored 76.0; 5.4% diff).
- **Quote:** > 40  66.1 66.8 68.0  72.1  76.2 77.4 78.2
- **Reviewer note:** SECONDARY and DIFFERENT standard: INTERGROWTH-21st (Papageorghiou Lancet 2014 / Stirnemann UOG 2016), not the cited NICHD/Buck Louis. 50th-centile 72.1 mm brackets stored 76.0 mm (5.4% diff).

### `fetal_growth.hc_16w_mm`  ·  Tier A  ·  stored: 124.0 mm

- **Primary citation:** `buck-louis-2015-nichd-growth`  (_evidence: secondary_)
- **Source reports:** INTERGROWTH-21st 50th-centile HC at 16 completed weeks = 122.9 mm (stored 124.0; 0.9% diff).
- **Quote:** > 16  111.1 112.6 114.9  122.9  130.9 133.2 134.7
- **Reviewer note:** SECONDARY and DIFFERENT standard: INTERGROWTH-21st (Papageorghiou Lancet 2014 / Stirnemann UOG 2016), not the cited NICHD/Buck Louis. 50th-centile 122.9 mm brackets stored 124.0 mm (0.9% diff).

### `fetal_growth.hc_20w_mm`  ·  Tier A  ·  stored: 175.0 mm

- **Primary citation:** `buck-louis-2015-nichd-growth`  (_evidence: secondary_)
- **Source reports:** INTERGROWTH-21st 50th-centile HC at 20 completed weeks = 172.5 mm (stored 175.0; 1.4% diff).
- **Quote:** > 20  158.5 160.2 163.0  172.5  182.0 184.7 186.5
- **Reviewer note:** SECONDARY and DIFFERENT standard: INTERGROWTH-21st (Papageorghiou Lancet 2014 / Stirnemann UOG 2016), not the cited NICHD/Buck Louis. 50th-centile 172.5 mm brackets stored 175.0 mm (1.4% diff).

### `fetal_growth.hc_24w_mm`  ·  Tier A  ·  stored: 225.0 mm

- **Primary citation:** `buck-louis-2015-nichd-growth`  (_evidence: secondary_)
- **Source reports:** INTERGROWTH-21st 50th-centile HC at 24 completed weeks = 219.1 mm (stored 225.0; 2.7% diff).
- **Quote:** > 24  203.5 205.4 208.5  219.1  229.7 232.7 234.7
- **Reviewer note:** SECONDARY and DIFFERENT standard: INTERGROWTH-21st (Papageorghiou Lancet 2014 / Stirnemann UOG 2016), not the cited NICHD/Buck Louis. 50th-centile 219.1 mm brackets stored 225.0 mm (2.7% diff).

### `fetal_growth.hc_28w_mm`  ·  Tier A  ·  stored: 267.0 mm

- **Primary citation:** `buck-louis-2015-nichd-growth`  (_evidence: secondary_)
- **Source reports:** INTERGROWTH-21st 50th-centile HC at 28 completed weeks = 260.4 mm (stored 267.0; 2.5% diff).
- **Quote:** > 28  243.6 245.7 248.9  260.4  271.8 275.1 277.2
- **Reviewer note:** SECONDARY and DIFFERENT standard: INTERGROWTH-21st (Papageorghiou Lancet 2014 / Stirnemann UOG 2016), not the cited NICHD/Buck Louis. 50th-centile 260.4 mm brackets stored 267.0 mm (2.5% diff).

### `fetal_growth.hc_36w_mm`  ·  Tier A  ·  stored: 322.0 mm

- **Primary citation:** `buck-louis-2015-nichd-growth`  (_evidence: secondary_)
- **Source reports:** INTERGROWTH-21st 50th-centile HC at 36 completed weeks = 319.4 mm (stored 322.0; 0.8% diff).
- **Quote:** > 36  299.2 301.7 305.6  319.4  333.2 337.1 339.6
- **Reviewer note:** SECONDARY and DIFFERENT standard: INTERGROWTH-21st (Papageorghiou Lancet 2014 / Stirnemann UOG 2016), not the cited NICHD/Buck Louis. 50th-centile 319.4 mm brackets stored 322.0 mm (0.8% diff).

### `fetal_growth.hc_40w_mm`  ·  Tier A  ·  stored: 343.0 mm

- **Primary citation:** `buck-louis-2015-nichd-growth`  (_evidence: secondary_)
- **Source reports:** INTERGROWTH-21st 50th-centile HC at 40 completed weeks = 333.9 mm (stored 343.0; 2.7% diff).
- **Quote:** > 40  309.6 312.7 317.4  333.9  350.5 355.2 358.3
- **Reviewer note:** SECONDARY and DIFFERENT standard: INTERGROWTH-21st (Papageorghiou Lancet 2014 / Stirnemann UOG 2016), not the cited NICHD/Buck Louis. 50th-centile 333.9 mm brackets stored 343.0 mm (2.7% diff).

### `maternal_cardiovascular.peak_excess_heart_rate_bpm`  ·  Tier A  ·  stored: 15.0 bpm

- **Primary citation:** `mahendru-2014-cardiac-output`  (_evidence: abstract_)
- **Source reports:** Abstract reports HR increased maximally by the third trimester by Δ13±11 bpm; 13 falls within the stored 10–20 bpm range.
- **Quote:** > the heart rate increased maximally by the third trimester (Δ: 13 ± 11  bpm; P = 0.001)
- **Reviewer note:** Reported Δ13±11 bpm vs stored 15 (range 10–20); same quantity and magnitude, central figure differs slightly.

### `maternal_endocrine.cortisol_baseline_ug_per_dl`  ·  Tier A  ·  stored: 10.0 ug/dL

- **Primary citation:** `carr-1981-cortisol`  (_evidence: secondary_)
- **Source reports:** StatPearls states a morning cortisol >18 mcg/dL is a normal finding (excludes Addison disease). This anchors the upper part of the non-pregnant normal morning range; the stored non-pregnant central 10 with range 5-20 ug/dL is consistent in magnitude (single-digit to low-twenties ug/dL), with the >18 threshold sitting just below the stored high of 20.
- **Quote:** > A morning cortisol level >18 mcg/dL is a normal finding and may exclude an Addison disease diagnosis
- **Reviewer note:** SECONDARY: StatPearls gives a normal morning cortisol threshold (>18 mcg/dL), confirming the order of magnitude and upper bound of the stored 5-20 ug/dL range but not pinning the central value.

### `maternal_renal.gfr_first_trimester_ml_per_min`  ·  Tier A  ·  stored: 135.0 mL/min

- **Primary citation:** `davison-hytten-1974-gfr`  (_evidence: secondary_)
- **Source reports:** Review reports creatinine clearance (a GFR proxy) rising ~25% by gestational week 4 and ~45% by week 9; applied to a non-pregnant baseline of ~90-100 mL/min this yields a first-trimester GFR of roughly 120-135 mL/min, bracketing the stored central of 135 at its upper edge.
- **Quote:** > creatinine clearance increased 20% at 4 weeks post-menses, 25% as early as gestational week 4, and 45% by gestational week 9
- **Reviewer note:** SECONDARY: source gives first-trimester GFR as a ~25-45% rise over baseline, not an absolute mL/min; stored 135 sits at the upper edge of the implied range.

### `maternal_renal.plasma_sodium_drop_meq_per_l`  ·  Tier A  ·  stored: 5.0 mEq/L

- **Primary citation:** `davison-1981-osmoregulation`  (_evidence: abstract_)
- **Source reports:** Abstract states changes in plasma sodium accounted for the majority of the ~10 mOsm/kg osmolality decrement but gives no numeric sodium drop in mEq/L.
- **Quote:** > Changes in plasma sodium (and its attendant anion) accounted for the majority of the decrement.
- **Reviewer note:** Abstract attributes most of the 10 mOsm/kg fall to sodium; a ~5 mEq/L drop is mechanistically consistent but no explicit sodium figure is stated.

### `maternal_respiratory.baseline_pao2_mmhg`  ·  Tier A  ·  stored: 100.0 mmHg

- **Primary citation:** `templeton-1976-blood-gas`  (_evidence: abstract_)
- **Source reports:** Abstract reports mean arterial PO2 consistently greater than 100 mmHg throughout pregnancy (106.4 at 12 wk falling to 101.8 at 38 wk); a non-pregnant baseline of ~100 mmHg is consistent with these values though not stated as a separate non-pregnant figure.
- **Quote:** > Mean arterial PO2 was consistently greater than 100 mm Hg throughout pregnancy, although the value decreased from 106.4 mm Hg at 12 weeks of gestation to 101.8 mm Hg at the 38th week.
- **Reviewer note:** Abstract gives pregnant PaO2 values >100 mmHg; supports ~100 mmHg baseline magnitude but no explicit non-pregnant figure.

### `maternal_respiratory.baseline_tidal_volume_ml`  ·  Tier A  ·  stored: 450.0 mL

- **Primary citation:** `lomauro-aliverti-2015-respiratory`  (_evidence: secondary_)
- **Source reports:** Normal adult resting tidal volume is ~500 mL (male) and ~400 mL (female); stored 450 mL sits between.
- **Quote:** > It measures around 500 mL in an average healthy adult male and approximately 400 mL in a healthy female.
- **Reviewer note:** SECONDARY evidence; female ~400 mL / male ~500 mL bracket stored central 450 mL (range 400-500).

### `placental_endocrine.estriol_term_ng_per_ml`  ·  Tier A  ·  stored: 10.0 ng/mL

- **Primary citation:** `tulchinsky-1972-steroids`  (_evidence: secondary_)
- **Source reports:** Endotext states estriol rises to approximately 10-30 ng/ml at term; stored central 10 (6-20) ng/mL brackets the lower end of this range.
- **Quote:** > estriol increases gradually to a range of approximately 10-30 ng/ml at term
- **Reviewer note:** SECONDARY: Endotext term estriol 10-30 ng/mL; stored central 10 (6-20) ng/mL overlaps but sits at/below the source's lower bound.

### `amniotic_fluid.af_creatinine_term_mg_per_dl`  ·  Tier B  ·  stored: 2.0 mg/dL

- **Primary citation:** `underwood-2005-amniotic-fluid`  (_evidence: secondary_)
- **Source reports:** Term (36-42 wk) AF creatinine was 1.83 +/- 0.42 mg/dL; the article also states the maturity range is 1.5 to 2.0 mg/dl. Stored 2.0 mg/dL sits at the top of both the +/-1SD span (1.41-2.25) and the cited maturity range.
- **Quote:** > Creatinine (mg/dl) ... (36-42 weeks) 1.83 +/- 0.42 ... Creatinine values in the amniotic fluid that best represent fetal maturity are 1.5 to 2.0 mg/dl
- **Reviewer note:** SECONDARY: term AF creatinine 1.83 mg/dL; stored 2.0 within range 1.5-2.0 and +/-1SD.

### `amniotic_fluid.af_glucose_term_mmol_per_l`  ·  Tier B  ·  stored: 0.5 mmol/L

- **Primary citation:** `underwood-2005-amniotic-fluid`  (_evidence: secondary_)
- **Source reports:** Term (36-42 wk) AF glucose was 17.94 +/- 13.53 mg/dL (methods state glucose reported as mg/dl; table header 'mg/ml' is a typo). That mean equals ~1.0 mmol/L, and the +/-1SD span (~0.24-1.75 mmol/L) brackets the stored 0.5 mmol/L.
- **Quote:** > Glucose (mg/ml) ... (36-42 weeks) 17.94 +/- 13.53
- **Reviewer note:** SECONDARY: term AF glucose 17.94 mg/dL (~1.0 mmol/L); stored 0.5 mmol/L within wide +/-1SD.

### `amniotic_fluid.af_osmolality_term_mosm_per_kg`  ·  Tier B  ·  stored: 260 mOsm/kg

- **Primary citation:** `underwood-2005-amniotic-fluid`  (_evidence: secondary_)
- **Source reports:** AF osmolality was 264.81 +/- 9.54 mOsm/l at 13-20 wk, 259.62 +/- 15.34 at 27-34 wk, and 237.54 +/- 31.42 at 36-42 wk. The stored 260 mOsm/kg falls within the term +/-1SD span (206-269) and matches the late-second/third-trimester means.
- **Quote:** > Osmolality (mOsm/l) (13-20 weeks) 264.81 +/- 9.54 ... (27-34 weeks) 259.62 +/- 15.34 ... (36-42 weeks) 237.54 +/- 31.42
- **Reviewer note:** SECONDARY: AF osmolality declines ~265->238 mOsm/l to term; stored 260 within term +/-1SD.

### `amniotic_fluid.afv_early_baseline_ml`  ·  Tier B  ·  stored: 100.0 mL

- **Primary citation:** `brace-1989-amniotic-fluid`  (_evidence: secondary_)
- **Source reports:** GLOWM review reports AF volume of 60 ml at 12 weeks and 175 ml at 16 weeks. These early-pregnancy figures bracket the stored early-baseline central of 100 mL (range 50-200).
- **Quote:** > At 12 weeks' gestation, the average volume is 60 ml. By 16 weeks, when genetic amniocentesis is often performed, the mean volume is 175 ml.
- **Reviewer note:** SECONDARY: 60 ml (12 wk) and 175 ml (16 wk) bracket stored 100 mL early baseline.

### `fetal_circulation.mca_pi_baseline`  ·  Tier B  ·  stored: 1.5 dimensionless

- **Primary citation:** `mari-1995-mca-pi`  (_evidence: secondary_)
- **Source reports:** Normal MCA-PI nomogram gives a 50th-centile value of 1.71 at 20 weeks, rising to a peak of 2.05 at 28 weeks then declining (parabolic pattern). The stored early-second-trimester value of 1.5 sits just below the 1.71 median at 20 weeks.
- **Quote:** > median MCA-PI was 1.71 (50th percentile column for gestational week 20); peak PI value 2.05 at 28 weeks of gestation
- **Reviewer note:** SECONDARY: 20-wk median MCA-PI 1.71 (parabolic, peak 2.05 at 28 wk); brackets stored 1.5 (1.3-1.7) at the upper edge.

### `fetal_circulation.mca_pi_peak`  ·  Tier B  ·  stored: 2.0 dimensionless

- **Primary citation:** `mari-1995-mca-pi`  (_evidence: abstract_)
- **Source reports:** Abstract states MCA-PI was higher at 25-30 weeks (parabolic pattern peaking mid-gestation) but gives no numeric peak PI value.
- **Quote:** > The pulsatility index values of the middle cerebral artery were higher at 25 to 30 weeks' gestation
- **Reviewer note:** Abstract confirms a mid-gestation peak at 25-30 wk consistent with stored ~28 wk peak, but the numeric value 2.0 is not stated.

### `fetal_metabolism.fetal_core_temperature_c_term`  ·  Tier B  ·  stored: 37.6 °C

- **Primary citation:** `battaglia-meschia-1986-fetal-metabolism`  (_evidence: secondary_)
- **Source reports:** The fetus runs 0.3-0.5 °C warmer than the mother via placental/uterine heat transfer.
- **Quote:** > heat is transferred to the fetus via the placenta and the uterus, resulting in a 0.3C° to 0.5C° higher temperature than that of the mother
- **Reviewer note:** SECONDARY evidence: source confirms maternal-fetal gradient (+0.3-0.5 C); 37.6 C implied from maternal ~37.0-37.1 + gradient. No absolute fetal core temperature quoted.

### `fetal_metabolism.fetal_glucose_term_mmol_per_l`  ·  Tier B  ·  stored: 3.5 mmol/L

- **Primary citation:** `battaglia-meschia-1986-fetal-metabolism`  (_evidence: secondary_)
- **Source reports:** At term: umbilical vein glucose 4.09, umbilical artery 3.71, maternal radial artery 4.71 mmol/L; gradient 1.22 mmol/L.
- **Quote:** > The transplacental maternal-fetal glucose gradient was 1.22 (0.42) mmol/L.
- **Reviewer note:** SECONDARY evidence: measured fetal glucose (UA 3.71, UV 4.09 mmol/L) sits above stored central 3.5 but within stored range 2.8-4.5; fetal/maternal ratio ~0.7 confirmed.

### `fetal_metabolism.fetal_hb_concentration_g_per_dl_term`  ·  Tier B  ·  stored: 17.0 g/dL

- **Primary citation:** `hytten-chamberlain-1980-blood-volume`  (_evidence: secondary_)
- **Source reports:** Cord blood haemoglobin median 15.8 g/dL, 95% reference interval 12.4-19.7 g/dL.
- **Quote:** > HGB = 15.8 [12.4–19.7] g/dL
- **Reviewer note:** SECONDARY evidence: cited 95% RI 12.4-19.7 brackets stored 17.0; cohort median (15.8) below stored central.

### `fetal_metabolism.oxygen_consumption_ml_per_kg_per_min`  ·  Tier B  ·  stored: 6.5 mL O2/kg/min

- **Primary citation:** `battaglia-meschia-1986-fetal-metabolism`  (_evidence: secondary_)
- **Source reports:** Mean near-term fetal sheep oxygen consumption is 8.4 +/- 1.9 mL/min/kg.
- **Quote:** > The mean oxygen consumption was 8.4 +/- 1.9 ml/min/kg in the near-term fetal sheep.
- **Reviewer note:** SECONDARY evidence (ovine, human-extrapolated): same magnitude; cited 8.4 mL/kg/min runs above stored central 6.5.

### `maternal_blood.d_dimer_term_ug_per_ml`  ·  Tier B  ·  stored: 1.5 ug/mL

- **Primary citation:** `kline-2005-d-dimer`  (_evidence: secondary_)
- **Source reports:** Siennicka 2020 reports an unadjusted third-trimester D-dimer reference interval of 483-2256 ng/mL (= 0.483-2.256 ug/mL) in physiological pregnancy. The stored term central of 1.5 ug/mL falls inside this interval.
- **Quote:** > Reference value ranges for D-D without adjustment for the entire group for successive trimesters were 167-721, 298-1653, and 483-2256 ng/mL.
- **Reviewer note:** SECONDARY (Siennicka 2020), not the cited Kline 2005 primary; third-trimester interval 0.483-2.256 ug/mL contains stored 1.5 ug/mL.

### `maternal_blood.esr_term_mm_per_h`  ·  Tier B  ·  stored: 50.0 mm/h

- **Primary citation:** `hytten-chamberlain-1980-blood-volume`  (_evidence: secondary_)
- **Source reports:** GLOWM's sample third-trimester reference interval for ESR is 13-70 mm/h (median 32). The stored term central of 50 mm/h falls inside this interval; the source's median is lower than 50.
- **Quote:** > Erythrocyte sedimentation rate (ESR) (mm/h) … 13–70 (32)
- **Reviewer note:** SECONDARY (GLOWM), not the cited Hytten & Chamberlain 1980 primary; third-trimester ESR 13-70 mm/h contains stored 50 mm/h.

### `maternal_blood.factor_x_term_pct`  ·  Tier B  ·  stored: 145 %

- **Primary citation:** `stirling-1984-coagulation-factors`  (_evidence: abstract_)
- **Source reports:** Stirling 1984 names factor X among those that 'rose markedly throughout pregnancy', supporting the direction and magnitude class, but gives no percentage figure for the term value.
- **Quote:** > Factors VII, VIII:C, VIIIR:Ag, X, fibrinogen and alpha 1-antitrypsin, rose markedly throughout pregnancy.
- **Reviewer note:** Factor X confirmed to rise markedly; stored 145% is plausible but the exact figure is not stated in the abstract.

### `maternal_blood.ferritin_term_ng_per_ml`  ·  Tier B  ·  stored: 15.0 ng/mL

- **Primary citation:** `hytten-chamberlain-1980-blood-volume`  (_evidence: secondary_)
- **Source reports:** Yang 2019 reports a third-trimester serum-ferritin reference interval of 7.2-122.2 mg/L (ug/L, equivalent to ng/mL) in pregnant women. The stored term central of 15 ng/mL falls inside this interval. GLOWM's pregnancy table gives a similar 5-110 ng/ml third-trimester range.
- **Quote:** > In the third trimester, the reference intervals for serum ferritin, serum iron, total iron-binding capacity and transferrin saturation are 7.2–122.2 mg/L, 5.83–21.52 µmol/L, 49.40–122.76 µmol/L and 8.22–52.75%, respectively.
- **Reviewer note:** SECONDARY (Yang 2019), not the cited Hytten & Chamberlain 1980 primary; ferritin 7.2-122.2 ug/L (=ng/mL) contains stored 15 ng/mL.

### `maternal_blood.fibrinogen_baseline_g_per_l`  ·  Tier B  ·  stored: 3.0 g/L

- **Primary citation:** `hytten-chamberlain-1980-blood-volume`  (_evidence: secondary_)
- **Source reports:** StatPearls gives the normal (non-pregnant) adult plasma fibrinogen range as 200-400 mg/dL, i.e. 2.0-4.0 g/L. The stored pre-pregnancy baseline of 3.0 g/L sits at the centre of this range.
- **Quote:** > Plasma concentrations typically range between 200 and 400 mg/dL.
- **Reviewer note:** SECONDARY (StatPearls), not the cited Hytten & Chamberlain 1980 primary; 200-400 mg/dL = 2-4 g/L brackets the stored 3.0 g/L baseline.

### `maternal_blood.fibrinogen_term_g_per_l`  ·  Tier B  ·  stored: 5.5 g/L

- **Primary citation:** `hytten-chamberlain-1980-blood-volume`  (_evidence: secondary_)
- **Source reports:** StatPearls gives the normal third-trimester fibrinogen as nearly 500 mg/dL (~5.0 g/L), the same magnitude and direction as the stored 5.5 g/L term value (stored range 4.5-6.5 g/L).
- **Quote:** > The normal fibrinogen concentration in the third trimester is nearly 500 mg/dL.
- **Reviewer note:** SECONDARY (StatPearls), not the cited Hytten & Chamberlain 1980 primary; ~500 mg/dL = ~5.0 g/L, close to stored 5.5 g/L.

### `maternal_blood.haemoglobin_g_per_dl_term`  ·  Tier B  ·  stored: 11.5 g/dL

- **Primary citation:** `hytten-chamberlain-1980-blood-volume`  (_evidence: secondary_)
- **Source reports:** GLOWM's sample third-trimester haemoglobin reference interval is 9.5-15 g/dL. The stored term central of 11.5 g/dL falls inside this interval, though the interval is wide and does not pin the central value.
- **Quote:** > Hemoglobin (Hb) (g/dL) … 9.5–15
- **Reviewer note:** SECONDARY (GLOWM), not the cited Hytten & Chamberlain 1980 primary; third-trimester Hb 9.5-15 g/dL is wide but contains stored 11.5 g/dL.

### `maternal_blood.mcv_term_fl`  ·  Tier B  ·  stored: 92.0 fL

- **Primary citation:** `hytten-chamberlain-1980-blood-volume`  (_evidence: secondary_)
- **Source reports:** Chandra 2012 states MCV rises by an average of ~4 fL in iron-replete pregnancy. From a non-pregnant baseline of ~87-88 fL this gives a term MCV around 91-92 fL, consistent with the stored 92 fL term value; the absolute term figure is not stated.
- **Quote:** > there is a small increase in mean corpuscular volume (MCV), of an average of 4 fl in an iron-replete woman
- **Reviewer note:** SECONDARY (Chandra 2012), not the cited Hytten & Chamberlain 1980 primary; source gives the ~4 fL rise, consistent with stored 92 fL term value above an ~88 fL baseline.

### `maternal_blood.plasma_volume_l`  ·  Tier B  ·  stored: 3.85 L

- **Primary citation:** `de-haas-2017-plasma-volume-meta`  (_evidence: abstract_)
- **Source reports:** de Haas 2017 meta-analysis reports a pooled maximum third-trimester increase of 1.13 L (45.6%) over the non-pregnant reference, not an absolute term plasma volume. 1.13 L on a ~2.7 L baseline is consistent with ~3.85 L absolute, but the absolute figure is not stated.
- **Quote:** > Plasma volume continued to increase in the third trimester with a pooled maximum increase of 1.13 L (95% CI, 1.07-1.19 L), an increase of 45.6% (95% CI, 43.0-48.1%) in physiological pregnancies compared with the reference value.
- **Reviewer note:** Source gives the term INCREASE (1.13 L), consistent in magnitude with stored 3.85 L absolute, but does not state the absolute term volume.

### `maternal_blood.platelet_count_term_x10e9_per_l`  ·  Tier B  ·  stored: 220.0 10^9/L

- **Primary citation:** `hytten-chamberlain-1980-blood-volume`  (_evidence: secondary_)
- **Source reports:** GLOWM's sample third-trimester platelet reference interval is 145-400 x10^9/L. The stored term central of 220 x10^9/L falls inside this interval.
- **Quote:** > Platelets (×10⁹/L) … 145–400
- **Reviewer note:** SECONDARY (GLOWM), not the cited Hytten & Chamberlain 1980 primary; third-trimester platelets 145-400 x10^9/L contains stored 220.

### `maternal_blood.red_cell_mass_l`  ·  Tier B  ·  stored: 1.65 L

- **Primary citation:** `hytten-chamberlain-1980-blood-volume`  (_evidence: secondary_)
- **Source reports:** Merck gives the red-cell-mass increase as 15 to 25% in a singleton pregnancy, not an absolute litre value. On a ~1.4 L non-pregnant baseline that is ~1.61-1.75 L, consistent with the stored 1.65 L term value, but the absolute figure is not stated.
- **Quote:** > red blood cell (RBC) mass increases by 15 to 25% in a singleton pregnancy
- **Reviewer note:** SECONDARY (Merck Manual), not the cited Hytten & Chamberlain 1980 primary; source gives the percentage increase, not the absolute term mass.

### `maternal_blood.serum_iron_term_ug_per_dl`  ·  Tier B  ·  stored: 60.0 ug/dL

- **Primary citation:** `hytten-chamberlain-1980-blood-volume`  (_evidence: secondary_)
- **Source reports:** Yang 2019 reports a third-trimester serum-iron reference interval of 5.83-21.52 umol/L in pregnant women, which converts to ~32.6-120.2 ug/dL (x5.585). The stored term central of 60 ug/dL falls inside this interval.
- **Quote:** > In the third trimester, the reference intervals for serum ferritin, serum iron, total iron-binding capacity and transferrin saturation are 7.2–122.2 mg/L, 5.83–21.52 µmol/L, 49.40–122.76 µmol/L and 8.22–52.75%, respectively.
- **Reviewer note:** SECONDARY (Yang 2019), not the cited Hytten & Chamberlain 1980 primary; serum iron 5.83-21.52 umol/L = ~32.6-120.2 ug/dL contains stored 60 ug/dL.

### `maternal_blood.total_protein_term_g_per_dl`  ·  Tier B  ·  stored: 6.0 g/dL

- **Primary citation:** `hytten-chamberlain-1980-blood-volume`  (_evidence: secondary_)
- **Source reports:** The perinatology.com reference table (citing Abbassi-Ghanavati 2009 Obstet Gynecol and Williams Obstetrics) gives a third-trimester total-protein range of 5.6-6.7 g/dL. The stored term central of 6.0 g/dL falls inside this range.
- **Quote:** > Total Protein … 3rd Trimester … 5.6 – 6.7 g/dL
- **Reviewer note:** SECONDARY (perinatology.com table citing Abbassi-Ghanavati 2009), not the cited Hytten & Chamberlain 1980 primary; third-trimester 5.6-6.7 g/dL contains stored 6.0 g/dL.

### `maternal_blood.transferrin_saturation_term_pct`  ·  Tier B  ·  stored: 20 %

- **Primary citation:** `hytten-chamberlain-1980-blood-volume`  (_evidence: secondary_)
- **Source reports:** Yang 2019 reports a third-trimester transferrin-saturation reference interval of 8.22-52.75% in pregnant women. The stored term central of 20% falls inside this interval.
- **Quote:** > In the third trimester, the reference intervals for serum ferritin, serum iron, total iron-binding capacity and transferrin saturation are 7.2–122.2 mg/L, 5.83–21.52 µmol/L, 49.40–122.76 µmol/L and 8.22–52.75%, respectively.
- **Reviewer note:** SECONDARY (Yang 2019), not the cited Hytten & Chamberlain 1980 primary; transferrin saturation 8.22-52.75% contains stored 20%.

### `maternal_blood.volume_l`  ·  Tier B  ·  stored: 5.6 L

- **Primary citation:** `hytten-chamberlain-1980-blood-volume`  (_evidence: secondary_)
- **Source reports:** StatPearls states total blood volume rises by about 1.5 L during pregnancy and reaches about 30% above baseline near term. On a non-pregnant baseline of ~4.0-4.5 L this gives a term total around 5.5-6.0 L, consistent with the stored 5.6 L, though the absolute term value is not printed.
- **Quote:** > During pregnancy, the total blood volume increases by about 1.5 liters … A little before reaching full term, the volume of maternal blood is about 30% above baseline.
- **Reviewer note:** SECONDARY (StatPearls), not the cited Hytten & Chamberlain 1980 primary; source gives the increase (+1.5 L / +30%), consistent with stored 5.6 L absolute.

### `maternal_blood.wbc_count_term_x10e9_per_l`  ·  Tier B  ·  stored: 10.5 10^9/L

- **Primary citation:** `hytten-chamberlain-1980-blood-volume`  (_evidence: secondary_)
- **Source reports:** GLOWM's sample third-trimester WBC reference interval is 6-16 x10^9/L. The stored term central of 10.5 x10^9/L falls inside this interval.
- **Quote:** > White blood cells (WBC) (×10⁹/L) … 6–16
- **Reviewer note:** SECONDARY (GLOWM), not the cited Hytten & Chamberlain 1980 primary; third-trimester WBC 6-16 x10^9/L contains stored 10.5.

### `maternal_cardiovascular.baseline_cardiac_output_l_per_min`  ·  Tier B  ·  stored: 4.6 L/min

- **Primary citation:** `mahendru-2014-cardiac-output`  (_evidence: secondary_)
- **Source reports:** Clark 1989: post-partum (non-pregnant surrogate) cardiac output 4.3 +/- 0.9 L/min. StatPearls: resting CO ~5-6 L/min in a healthy adult. Stored 4.6 lies between these and within Clark's SD.
- **Quote:** > Cardiac output (L/min)                4.3 ± 0.9        6.2 ± 1.0    44           0.0003
- **Reviewer note:** SECONDARY: stored 4.6 within 1 SD of Clark post-partum CO 4.3 +/- 0.9; below textbook ~5 L/min but in range.

### `maternal_cardiovascular.baseline_svr_dyn_s_cm5`  ·  Tier B  ·  stored: 1300.0 dyn*s/cm^5

- **Primary citation:** `sanghavi-rutherford-2014-cardio-review`  (_evidence: secondary_)
- **Source reports:** Clark 1989: post-partum (non-pregnant surrogate) SVR 1530 +/- 520 dyn*s/cm^5. Stored 1300 lies below the point estimate but well within +/-1 SD and within commonly cited non-pregnant ranges (~1200-1530).
- **Quote:** > Systemic vascular resistance         1530 ± 520       1210 ± 266    -21          0.100
- **Reviewer note:** SECONDARY: stored 1300 within 1 SD of Clark post-partum SVR 1530 +/- 520; sources vary 1200-1530.

### `maternal_cardiovascular.cardiac_output_t3_l_per_min`  ·  Tier B  ·  stored: 6.5 L/min

- **Primary citation:** `mahendru-2014-cardiac-output`  (_evidence: secondary_)
- **Source reports:** Clark 1989: at-term cardiac output 6.2 +/- 1.0 L/min (a 44% rise from post-partum). Stored 6.5 lies within Clark's SD of the at-term value.
- **Quote:** > Cardiac output (L/min)                4.3 ± 0.9        6.2 ± 1.0    44           0.0003
- **Reviewer note:** SECONDARY: stored 6.5 within 1 SD of Clark at-term CO 6.2 +/- 1.0 (+44%).

### `maternal_cardiovascular.heart_rate_peak_week`  ·  Tier B  ·  stored: 32 week

- **Primary citation:** `mahendru-2014-cardiac-output`  (_evidence: abstract_)
- **Source reports:** Abstract states heart rate increased maximally by the third trimester; week 32 lies in T3, but no numeric peak week is given.
- **Quote:** > the heart rate increased maximally by the third trimester (Δ: 13 ± 11  bpm; P = 0.001)
- **Reviewer note:** Abstract supports T3 timing of HR peak (week 32 is in T3); exact week not stated.

### `maternal_cardiovascular.lv_mass_baseline_g`  ·  Tier B  ·  stored: 130.0 g

- **Primary citation:** `sanghavi-rutherford-2014-cardio-review`  (_evidence: secondary_)
- **Source reports:** BSE reference guideline: normal LV mass for women 51-173 g. Stored 130 g falls within this range (upper-middle).
- **Quote:** > Left ventricular mass (grams): 51-173
- **Reviewer note:** SECONDARY: stored 130 g within BSE normal female LV-mass range 51-173 g; no central pregnancy-specific value found.

### `maternal_cardiovascular.map_nadir_drop_mmhg`  ·  Tier B  ·  stored: 8.0 mmHg

- **Primary citation:** `mahendru-2014-cardiac-output`  (_evidence: secondary_)
- **Source reports:** Review states the mid-pregnancy MAP reduction is typically 8-10 mmHg (just under a 10% decline from pre-pregnancy). Stored 8 mmHg is the lower bound of that stated range.
- **Quote:** > The reduction is typically 8-10 mm Hg or just less than a 10% decline from pre-pregnancy levels.
- **Reviewer note:** SECONDARY: stored 8 mmHg is the lower bound of the stated 8-10 mmHg MAP nadir drop.

### `maternal_cardiovascular.map_nadir_week`  ·  Tier B  ·  stored: 22.0 weeks

- **Primary citation:** `mahendru-2014-cardiac-output`  (_evidence: secondary_)
- **Source reports:** StatPearls: blood pressure reaches its lowest point at about 20-24 weeks of gestation. Stored 22 weeks lies in the middle of this range.
- **Quote:** > blood pressure reaching its lowest point at about 20-24 weeks gestation
- **Reviewer note:** SECONDARY: stored 22 weeks within the stated 20-24 week BP-nadir window.

### `maternal_cardiovascular.term_heart_rate_bpm`  ·  Tier B  ·  stored: 85.0 bpm

- **Primary citation:** `mahendru-2014-cardiac-output`  (_evidence: secondary_)
- **Source reports:** Clark 1989: at-term heart rate 83 +/- 1.0 bpm (a 17% rise from post-partum 71). Stored 85 is within ~2 bpm of the at-term value.
- **Quote:** > Heart rate (beats/min)                 71 ± 10          83 ± 1.0    17           0.015
- **Reviewer note:** SECONDARY: stored 85 close to Clark at-term HR 83 bpm (+17%).

### `maternal_cardiovascular.term_svr_dyn_s_cm5`  ·  Tier B  ·  stored: 980.0 dyn*s/cm^5

- **Primary citation:** `sanghavi-rutherford-2014-cardio-review`  (_evidence: secondary_)
- **Source reports:** Clark 1989: at-term SVR 1210 +/- 266 dyn*s/cm^5 (a 21% fall). Soma-Pillay 2016 states a 25-30% fall. Stored 980 sits just within 1 SD of Clark's at-term value (944-1476) and is consistent with a 25-30% fall from a ~1300 baseline.
- **Quote:** > Systemic vascular resistance         1530 ± 520       1210 ± 266    -21          0.100
- **Reviewer note:** SECONDARY: stored 980 within 1 SD of Clark at-term SVR 1210 +/- 266; consistent with 25-30% fall.

### `maternal_cardiovascular.term_uterine_flow_ml_per_min`  ·  Tier B  ·  stored: 750.0 mL/min

- **Primary citation:** `thaler-1990-uterine-flow`  (_evidence: abstract_)
- **Source reports:** Abstract reports 342 ml/min in the left ascending uterine artery in late gestation (~684 ml/min bilateral), near the stored combined 750 ml/min.
- **Quote:** > from a mean of 94.5 ml/min before pregnancy to a mean of 342 ml/min in late gestation (reflecting a 3.5-fold increase)
- **Reviewer note:** Stored 750 ml/min combined vs ~684 ml/min from doubling Thaler's 342 ml/min single-artery term value; same magnitude.

### `maternal_endocrine.aldosterone_term_ng_per_dl`  ·  Tier B  ·  stored: 40.0 ng/dL

- **Primary citation:** `wilson-1980-renin-aldosterone`  (_evidence: secondary_)
- **Source reports:** Normotensive third-trimester aldosterone median 970.5 pmol/L (IQR 468.3-1586.0). Converting (1 ng/dL = 27.74 pmol/L): median 35.0 ng/dL, IQR 16.9-57.2 ng/dL. Stored central 40 ng/dL and range 25-60 fall within / overlap the converted interval.
- **Quote:** > Aldosterone, pmol/L First trimester 386.1 (226.2-626.2) Third trimester 970.5 (468.3-1586.0)
- **Reviewer note:** SECONDARY: normotensive third-trimester aldosterone median 970.5 pmol/L = 35.0 ng/dL (factor 27.74); stored central 40 within the converted IQR 16.9-57.2 ng/dL.

### `maternal_endocrine.cortisol_term_ug_per_dl`  ·  Tier B  ·  stored: 30.0 ug/dL

- **Primary citation:** `carr-1981-cortisol`  (_evidence: abstract_)
- **Source reports:** Cortisol reached 352 +/- 90 ng/mL (= 35.2 ug/dL) at 26 weeks and 'changed minimally thereafter until labor.' During labor it reached 706 ng/mL (= 70.6 ug/dL). The plateau value 35.2 ug/dL falls within the stored range 25-40.
- **Quote:** > As pregnancy advanced, the concentration of cortisol in plasma increased progressively from 149 +/- 34 ng/ml (mean and SEM) at 12 weeks to 352 +/- 90 ng/ml at 26 weeks' gestation but changed minimally thereafter until labor commenced, during which values of 706 +/- 148 ng/ml were achieved.
- **Reviewer note:** Pre-labor plateau ~352 ng/mL = 35.2 ug/dL falls in stored range 25-40; stored central 30 slightly below the abstract figure (unit conversion 10 ng/mL = 1 ug/dL).

### `maternal_endocrine.homa_ir_term`  ·  Tier B  ·  stored: 4.0 dimensionless

- **Primary citation:** `catalano-1991-insulin-sensitivity`  (_evidence: abstract_)
- **Source reports:** Catalano 1991 reports a 56% decrease in insulin sensitivity by 36 weeks (i.e. insulin resistance roughly doubles), consistent in direction/magnitude with HOMA-IR rising from ~2 to ~4, but reports no HOMA-IR figure (uses clamp glucose infusion rate).
- **Quote:** > There was a significant (p = 0.0003) 56% decrease in insulin sensitivity through 36 weeks' gestation.
- **Reviewer note:** 56% fall in insulin sensitivity supports ~2x rise in resistance (HOMA-IR 2->4) in direction/magnitude, but no HOMA-IR value reported.

### `maternal_endocrine.prolactin_term_ng_per_ml`  ·  Tier B  ·  stored: 200.0 ng/mL

- **Primary citation:** `tyson-1972-prolactin`  (_evidence: secondary_)
- **Source reports:** Third-trimester prolactin reference interval 4087.33-9733.65 uIU/mL. Using the WHO 3rd IS conversion (1 ng/mL ~ 21.2 uIU/mL, supported by the study's non-pregnant 178.89-757.52 uIU/mL = ~8.4-35.7 ng/mL matching standard prolactin ranges), this is ~193-459 ng/mL. Stored central 200 sits at the low end and the stored range 150-300 overlaps the lower part of the reported interval.
- **Quote:** > first trimester, 621.20-3584.00 microIU/mL; second trimester, 1432.00-5349.68 microIU/mL; third trimester, 4087.33-9733.65 microIU/mL
- **Reviewer note:** SECONDARY: third-trimester interval 4087-9734 uIU/mL ~ 193-459 ng/mL (factor 21.2); stored central 200 brackets the lower bound, consistent magnitude after unit conversion.

### `maternal_endocrine.tsh_t1_miu_per_l`  ·  Tier B  ·  stored: 0.6 mIU/L

- **Primary citation:** `glinoer-1997-thyroid`  (_evidence: secondary_)
- **Source reports:** Secondary reference-interval study (n=540): first-trimester TSH 5th-95th centile 0.04-3.77 uIU/mL with mean 1.51. Stored T1 central 0.6 sits low within this interval; the stored range 0.1-2.5 is well bracketed by the reported interval.
- **Quote:** > Trimester specific normal ranges of TSH in microIU/mL were 0.04-3.77, 0.30-3.21 and 0.6-4.5 microIU/mL, respectively, for first, second and third trimesters.
- **Reviewer note:** SECONDARY: stored T1 central 0.6 and range 0.1-2.5 fall within the reported first-trimester interval 0.04-3.77 (mean 1.51); consistent magnitude, not an exact central match.

### `maternal_endocrine.tsh_term_miu_per_l`  ·  Tier B  ·  stored: 2.0 mIU/L

- **Primary citation:** `glinoer-1997-thyroid`  (_evidence: secondary_)
- **Source reports:** Third-trimester TSH 5th-95th centile 0.6-4.5 uIU/mL with mean 1.87. Stored term central 2.0 and range 0.4-4.0 fall within this reported third-trimester interval.
- **Quote:** > Trimester specific normal ranges of TSH in microIU/mL were 0.04-3.77, 0.30-3.21 and 0.6-4.5 microIU/mL, respectively, for first, second and third trimesters.
- **Reviewer note:** SECONDARY: stored term central 2.0 lies within the reported third-trimester interval 0.6-4.5 (mean 1.87); consistent magnitude.

### `maternal_renal.filtration_fraction_term`  ·  Tier B  ·  stored: 0.18 dimensionless

- **Primary citation:** `cheung-lafayette-2013-renal`  (_evidence: secondary_)
- **Source reports:** StatPearls defines filtration fraction as GFR/RPF and gives the normal (non-pregnant) value as about 20% (~0.20). Filtration fraction dips early in pregnancy (RPF rises faster than GFR) then returns toward this ~0.20 baseline by the third trimester, consistent with the stored term value of 0.18 just below 0.20.
- **Quote:** > Filtration fraction (FF) is the fraction of renal plasma flow (RPF) filtered across the glomerulus. The equation is GFR divided by RPF. FF is about 20%
- **Reviewer note:** SECONDARY: source gives non-pregnant FF ~0.20; stored term 0.18 (0.16-0.20) sits just below as FF recovers toward baseline by term.

### `maternal_renal.gfr_ml_per_min`  ·  Tier B  ·  stored: 150.0 mL/min

- **Primary citation:** `cheung-lafayette-2013-renal`  (_evidence: abstract_)
- **Source reports:** Abstract states GFR increases 50% in pregnancy but gives no absolute term value in mL/min. A 50% rise on a ~100 mL/min baseline implies ~150 mL/min, consistent with stored, but the abstract supplies only the percentage, not the absolute figure.
- **Quote:** > The glomerular filtration rate increases 50% with subsequent decrease in serum creatinine, urea, and uric acid values.
- **Reviewer note:** Abstract gives +50% rise only; stored 150 mL/min is consistent with 50% over ~100 baseline but the absolute number is inferred, not stated.

### `maternal_renal.plasma_uric_acid_term_mg_per_dl`  ·  Tier B  ·  stored: 4.5 mg/dL

- **Primary citation:** `cheung-lafayette-2013-renal`  (_evidence: secondary_)
- **Source reports:** The normotensive control group (mean gestational age 37.98 +/- 3.83 weeks, i.e. third trimester/term) had a mean serum uric acid of 4.43 +/- 1.38 mg/dL, consistent with the stored term central 4.5 mg/dL and within the stored range 3.5-5.5.
- **Quote:** > Serum Uric Acid: 4.43 ± 1.38 mg/dL
- **Reviewer note:** SECONDARY: term normotensive control mean 4.43 mg/dL approximates stored 4.5; value is a case-control control-group mean, not a formal reference interval.

### `maternal_renal.renal_plasma_flow_peak_ml_per_min`  ·  Tier B  ·  stored: 900.0 mL/min

- **Primary citation:** `dunlop-1981-renal-plasma-flow`  (_evidence: abstract_)
- **Source reports:** Abstract reports ERPF increased 80% in early pregnancy. Applied to the stored ~600 mL/min baseline, +80% gives ~1080 mL/min; the stored peak of 900 mL/min (+50%) is within the stored high bound (1050) but lower than the 80% rise the abstract emphasizes. No absolute peak value is stated.
- **Quote:** > Compared with non-pregnant values, ERPF increased by 80 percent during early pregnancy but fell significantly from this new level during the third trimester.
- **Reviewer note:** Abstract supports a large early-pregnancy RPF rise (~80%); stored 900 mL/min is the same magnitude but no absolute peak number is given, and +80% would imply higher (~1080).

### `maternal_renal.rpf_peak_week`  ·  Tier B  ·  stored: 24.0 weeks

- **Primary citation:** `dunlop-1981-renal-plasma-flow`  (_evidence: abstract_)
- **Source reports:** Abstract states ERPF rose in early pregnancy and fell in the third trimester, implying a mid-pregnancy peak, but gives no specific peak week.
- **Quote:** > ERPF increased by 80 percent during early pregnancy but fell significantly from this new level during the third trimester.
- **Reviewer note:** Abstract implies a mid-pregnancy RPF peak (rise early, fall in T3) consistent with ~24 weeks, but no explicit peak week is reported.

### `maternal_respiratory.frc_term_l`  ·  Tier B  ·  stored: 2.0 L

- **Primary citation:** `lomauro-aliverti-2015-respiratory`  (_evidence: fulltext_)
- **Source reports:** Fulltext states FRC decreases by 9.5-25% at term but gives no absolute liter value, so the stored 2.0 L central cannot be confirmed numerically; only the directional/percent fall is supported.
- **Quote:** > FRC then decreases (by 9.5–25%) while inspiratory capacity increases at the same rate in order to maintain stable TLC
- **Reviewer note:** Source supports an FRC fall (~9.5-25%) but no absolute 2.0 L value; percent-only claim.

### `maternal_respiratory.minute_ventilation_l_per_min`  ·  Tier B  ·  stored: 10.5 L/min

- **Primary citation:** `lomauro-aliverti-2015-respiratory`  (_evidence: fulltext_)
- **Source reports:** Review reports minute ventilation increases significantly (by up to 48%) in the first trimester and is then maintained, driven by tidal-volume rise with unchanged respiratory rate. No absolute term value (e.g. ~10.5 L/min) is stated; only a percent change is given.
- **Quote:** > Minute ventilation ( V ′ E ) starts to increase significantly (by up to 48%) during the first trimester of gestation, due to higher tidal volume ( V T ) with unchanged respiratory rate. This ventilatory pattern is then maintained throughout the course of pregnancy
- **Reviewer note:** Source gives a percent increase (up to 48%) not the absolute 10.5 L/min; direction/magnitude consistent. Confirm percent-only claim.

### `maternal_respiratory.p50_shift_mmhg`  ·  Tier B  ·  stored: 3.0 mmHg

- **Primary citation:** `kelman-1966-o2-saturation`  (_evidence: secondary_)
- **Source reports:** Mean P-50 rises from 26.7 mmHg (nonpregnant) to 30.4 mmHg at/near term, a rightward shift of about 3.7 mmHg.
- **Quote:** > The mean P-50 values for normal nonpregnant women, normal pregnant women in first trimester, second trimester, and at or near term were 26.7 +/- 0.11 mmHg, 27.8 +/- 0.08 mmHg, 28.8 +/- 0.17 mmHg, and 30.4 +/- 0.20 mmHg, respectively.
- **Reviewer note:** SECONDARY evidence; source reports ~3.7 mmHg term shift vs stored central 3.0 (range 2-4) — same direction, within bracketing range.

### `maternal_respiratory.vo2_term_ml_per_min`  ·  Tier B  ·  stored: 300.0 mL O2/min

- **Primary citation:** `lomauro-aliverti-2015-respiratory`  (_evidence: fulltext_)
- **Source reports:** Fulltext states oxygen consumption increases by up to 21% in pregnancy but gives no absolute mL/min value, so the stored 300 mL/min term central cannot be confirmed numerically; only the percent rise is supported.
- **Quote:** > Oxygen consumption and basal metabolic rate increase (by up to 21% and 14%, respectively), but to a lesser extent than ventilatory augmentation
- **Reviewer note:** Source gives ~21% O2-consumption rise, not absolute 300 mL/min; percent-only claim.

### `placental_endocrine.estradiol_baseline_ng_per_ml`  ·  Tier B  ·  stored: 0.1 ng/mL

- **Primary citation:** `tulchinsky-1972-steroids`  (_evidence: secondary_)
- **Source reports:** Endotext states non-pregnant 17beta-estradiol is <0.1 ng/mL (follicular) and ~0.4 ng/mL (luteal). Stored mid-luteal baseline 0.1 (0.05-0.25) ng/mL is consistent in magnitude; the source's luteal point (0.4) is above the stored high.
- **Quote:** > Concentrations of 17β-estradiol are less than 0.1 ng/mL during the follicular phase of the cycle and reach about 0.4 ng/mL during the luteal phase of normal menstrual cycles
- **Reviewer note:** SECONDARY: Endotext non-pregnant estradiol <0.1 ng/mL (follicular) to ~0.4 ng/mL (luteal); stored 0.1 (0.05-0.25) ng/mL same order, source luteal value slightly above stored high.

### `placental_endocrine.hcg_term_miu_per_ml`  ·  Tier B  ·  stored: 10000.0 mIU/mL

- **Primary citation:** `cole-2010-hcg`  (_evidence: secondary_)
- **Source reports:** Cleveland Clinic reference table gives a third-trimester (25-40 weeks) hCG range of 3,640-117,000 mIU/mL, which brackets the stored term value of 10,000 (5,000-20,000) mIU/mL.
- **Quote:** > 25 to 40 [weeks]: 3,640-117,000 [mIU/mL]
- **Reviewer note:** SECONDARY: stored 10,000 (5,000-20,000) falls within the Cleveland Clinic 25-40 wk range 3,640-117,000 mIU/mL; reference interval is much wider than stored band.

### `placental_endocrine.leptin_term_ng_per_ml`  ·  Tier B  ·  stored: 30 ng/mL

- **Primary citation:** `hardie-1997-leptin`  (_evidence: secondary_)
- **Source reports:** Peer-reviewed study reports mean third-trimester maternal serum leptin in the normal control group of 56.66+/-34.18 ng/mL. Stored term central 30 (15-60) ng/mL overlaps this; inter-study leptin values vary widely (other cohorts report much lower means).
- **Quote:** > The mean serum leptin in the control group (56.66±34.18) was significantly higher than the preterm (33.65±16.70) group.
- **Reviewer note:** SECONDARY: control-group term leptin 56.66+/-34.18 ng/mL (PMC5147755) is within stored 15-60 range but near upper end; reported normal leptin varies widely between cohorts (BMI-dependent).

### `placental_endocrine.progesterone_baseline_ng_per_ml`  ·  Tier B  ·  stored: 10.0 ng/mL

- **Primary citation:** `tulchinsky-1972-steroids`  (_evidence: secondary_)
- **Source reports:** Endotext states luteal-phase progesterone reaches a plateau of approximately 10-35 ng/mL; stored mid-luteal baseline 10 (5-20) ng/mL sits at the lower end of this range.
- **Quote:** > progesterone concentrations rise from about 1-2 ng/mL on the day of the LH surge to a plateau of approximately 10-35 ng/mL over the subsequent 7 days.
- **Reviewer note:** SECONDARY: Endotext luteal progesterone plateau 10-35 ng/mL; stored 10 (5-20) ng/mL consistent at lower end.

### `placental_gas_exchange.maternal_intervillous_po2_mmhg`  ·  Tier B  ·  stored: 50.0 mmHg

- **Primary citation:** `carter-2009-placental-development`  (_evidence: secondary_)
- **Source reports:** Intervillous (maternal plasma bathing villi) PO2 is 40-80 mmHg through the 2nd and 3rd trimesters.
- **Quote:** > The oxygen tension in the maternal plasma bathing placental villi is <20 mm Hg until 10-12 weeks' gestation, rising to 40-80 mmHg and remaining in this range throughout the second and third trimesters.
- **Reviewer note:** SECONDARY: stored 50 falls within the 40-80 mmHg intervillous range; stored low-high 40-60 brackets the lower half.

### `placental_glucose.glucose_glut3_km_mmol_per_l`  ·  Tier B  ·  stored: 1.5 mmol/L

- **Primary citation:** `baumann-2002-glut3`  (_evidence: secondary_)
- **Source reports:** Review of the human GLUT transporters states GLUT3 is the high-affinity isoform with Km = 1.4 mM for glucose.
- **Quote:** > GLUT3 exhibits a high affinity for glucose (KM = 1.4 mM)
- **Reviewer note:** SECONDARY: GLUT3 Km 1.4 mM brackets stored 1.5 mmol/L; intrinsic transporter affinity (not placenta-specific).

### `placental_glucose.net_glucose_flux_term_mg_per_kg_per_min`  ·  Tier B  ·  stored: 5.0 mg/kg/min

- **Primary citation:** `illsley-2000-glut1`  (_evidence: secondary_)
- **Source reports:** Clinical review of in utero fuel homeostasis states fetal glucose utilization rates are 5-7 mg/kg/min, higher than adult rates of 2-3 mg/kg/min.
- **Quote:** > Fetal glucose utilization rates (5-7 mg/kg/min) are higher than in adults (2-3 mg/kg/min).
- **Reviewer note:** SECONDARY: fetal glucose utilization 5-7 mg/kg/min (= net flux at steady state) brackets stored 5.0 mg/kg/min.

### `placental_structure.cotyledon_count`  ·  Tier B  ·  stored: 18 count

- **Primary citation:** `benirschke-2012-placental-pathology`  (_evidence: secondary_)
- **Source reports:** Mature placenta consists of 15-28 cotyledons.
- **Quote:** > A mature placenta weighs about 500–600 grams and consists of 15–28 “cotyledons.”
- **Reviewer note:** SECONDARY: NCBI Bookshelf 15-28 cotyledons brackets stored central 18 (range 10-30).

### `placental_structure.placental_thickness_term_cm`  ·  Tier B  ·  stored: 2.5 cm

- **Primary citation:** `hoddick-1985-placental-thickness`  (_evidence: abstract_)
- **Source reports:** Hoddick abstract states placental thickness increases with menstrual age and the normal placenta never exceeded 4 cm; supports the upper bound but does not state a term central value of 2.5 cm.
- **Quote:** > At no stage of pregnancy was the normal placenta greater than 4 cm in thickness.
- **Reviewer note:** Abstract supports the normal upper bound (<4 cm, stored high 3.5) and the increasing trend; the central 2.5 cm itself is not stated.

### `placental_structure.term_weight_g`  ·  Tier B  ·  stored: 470.0 g

- **Primary citation:** `mayhew-2014-placental-morphometry`  (_evidence: secondary_)
- **Source reports:** Normal term placenta weighs about a pound (~454 g).
- **Quote:** > A normal placenta is round or oval-shaped and about 22 cm in diameter. It is 2 cm to 2.5 cm thick and weighs about a pound.
- **Reviewer note:** SECONDARY: StatPearls 'about a pound' (~454 g) is close to stored 470 g; figure is qualitative.

### `amniotic_fluid.fetal_swallowing_term_ml_per_24h`  ·  Tier C  ·  stored: 700 mL/24h

- **Primary citation:** `pritchard-1966-fetal-swallowing`  (_evidence: secondary_)
- **Source reports:** Secondary textbook chapter states the near-term fetus swallows an estimated 210 to 760 mL/day. The stored 700 mL/24h falls within this range.
- **Quote:** > An estimated 210 to 760 mL/day is swallowed by the near term fetus.
- **Reviewer note:** SECONDARY: stored 700 mL/24h within near-term swallowing range 210-760 mL/day.

### `fetal_circulation.ductus_arteriosus_share`  ·  Tier C  ·  stored: 0.85 fraction

- **Primary citation:** `rudolph-1985-fetal-circulation`  (_evidence: secondary_)
- **Source reports:** Secondary human-physiology text states only ~8% of combined ventricular output reaches the lungs and the remainder of right-ventricular output passes via the ductus arteriosus to the descending aorta, supporting a high (~0.85) ductal share of RV output. Human PC-MRI (Prsa 2014: ductus 41% vs main PA 56% of CVO) gives a somewhat lower ductal share (~0.73 of RV output) as pulmonary flow rises near term.
- **Quote:** > Only 8 per cent of the combined ventricular output passes to the pulmonary circulation; the remainder passes directly via the ductus arteriosus to the descending aorta
- **Reviewer note:** SECONDARY: human text supports the bulk of RV output via ductus (~0.85-0.9); PC-MRI suggests ~0.73 near term. Stored 0.85 brackets the upper end.

### `fetal_metabolism.fetal_cortisol_term_ug_per_dl`  ·  Tier C  ·  stored: 15 ug/dL

- **Primary citation:** `murphy-1973-fetal-cortisol`  (_evidence: secondary_)
- **Source reports:** Mean umbilical cord total cortisol in vertex delivery 493 +/- 125 nmol/L (~17.9 ug/dL); breech 790 +/- 363 nmol/L.
- **Quote:** > The mean umbilical cord total cortisol concentration was 790 +/- 363 nmol/liter in breech delivery as compared with 493 +/- 125 nmol/liter in vertex delivery.
- **Reviewer note:** SECONDARY evidence: vertex cord cortisol 493 nmol/L ~ 17.9 ug/dL, within stored range 7-30, near central 15 (labour elevates vs caesarean).

### `fetal_metabolism.fetal_insulin_term_pmol_per_l`  ·  Tier C  ·  stored: 50 pmol/L

- **Primary citation:** `economides-1989-fetal-insulin`  (_evidence: secondary_)
- **Source reports:** Cord plasma insulin in healthy term AGA neonates 68.4 +/- 54.6 pmol/L (LGA 82.1 +/- 56.2).
- **Quote:** > 68.4 ± 54.6
- **Reviewer note:** SECONDARY evidence: cited AGA cord insulin 68.4 pmol/L same magnitude as stored 50; wide SD brackets stored 20-120 range.

### `maternal_blood.b12_term_pg_per_ml`  ·  Tier C  ·  stored: 250 pg/mL

- **Primary citation:** `hytten-chamberlain-1980-blood-volume`  (_evidence: secondary_)
- **Source reports:** GLOWM's sample third-trimester total vitamin B12 reference interval is 60-390 pmol/L (median 170), which converts to ~81-529 pg/mL (1 pg/mL = 0.738 pmol/L). The stored term central of 250 pg/mL falls inside this interval.
- **Quote:** > Total vitamin B12 (pmol/L) … 60–390 (170)
- **Reviewer note:** SECONDARY (GLOWM), not the cited Hytten & Chamberlain 1980 primary; B12 60-390 pmol/L = ~81-529 pg/mL contains stored 250 pg/mL.

### `maternal_blood.pai1_term_ng_per_ml`  ·  Tier C  ·  stored: 80 ng/mL

- **Primary citation:** `kruithof-1987-fibrinolysis`  (_evidence: abstract_)
- **Source reports:** Kruithof 1987 reports PAI-1 antigen rose from 54 +/- 17 ng/mL (non-pregnant) to 144 +/- 25 ng/mL at term. The source term value (144) is higher than the stored central (80) but falls within the stored range (40-150).
- **Quote:** > its antigen level, measured by a radioimmunoassay, increased from 54 +/- 17 ng/mL to 144 +/- 25 ng/mL.
- **Reviewer note:** Source term PAI-1 antigen ~144 ng/mL vs stored central 80; same magnitude and 144 lies within stored range 40-150, but stored central is notably lower.

### `maternal_cardiovascular.baseline_stroke_volume_ml`  ·  Tier C  ·  stored: 65.0 mL

- **Primary citation:** `mahendru-2014-cardiac-output`  (_evidence: secondary_)
- **Source reports:** StatPearls: average resting stroke volume ~70 mL for a 70-kg adult; normal range 55-100 mL. Stored 65 is within the normal range, slightly below the 70 mL average.
- **Quote:** > The average stroke volume of a 70 kg male is 70 mL.
- **Reviewer note:** SECONDARY: stored 65 within StatPearls normal SV range 55-100 mL (general adult, not pregnancy-specific).

### `placental_endocrine.placental_gh_term_ng_per_ml`  ·  Tier C  ·  stored: 14 ng/mL

- **Primary citation:** `eriksson-1989-placental-gh`  (_evidence: secondary_)
- **Source reports:** Review states placental variant GH rises from ~20 weeks until term, reaching levels of 20-40 ng/ml. Stored central 14 (8-25) ng/mL overlaps the lower bound (20-25) but the source centres higher than stored.
- **Quote:** > There is a tonical secretion of the variant GH, which increases from the twentieth week of gestation until term, reaching levels of 20–40 ng/ml
- **Reviewer note:** SECONDARY: review gives term placental GH 20-40 ng/ml (PMC5526045); stored 14 (8-25) ng/mL same order but source-centred higher, overlapping only at 20-25.

### `placental_gas_exchange.maternal_fetal_pco2_gradient_term_mmhg`  ·  Tier C  ·  stored: 10.0 mmHg

- **Primary citation:** `mayhew-1986-gas-diffusion`  (_evidence: secondary_)
- **Source reports:** Fetal umbilical artery PCO2 ~52 mmHg vs maternal uterine artery PCO2 ~40 mmHg, a difference of ~12 mmHg.
- **Quote:** > fetal blood has higher levels of [H+] and PCO2 than maternal blood; fetal umbilical artery PCO2 52 mmHg and maternal uterine artery PCO2 40 mmHg
- **Reviewer note:** SECONDARY: stored 10 vs source-implied ~12 mmHg maternal-fetal PCO2 gradient; stored range 6-14 brackets 12. Gradient is reconstructed from the chapter's component PCO2 values, not a single reported figure.

### `placental_structure.spiral_artery_count`  ·  Tier C  ·  stored: 100 count

- **Primary citation:** `pijnenborg-2006-spiral-artery`  (_evidence: secondary_)
- **Source reports:** About 120 spiral arterial entries into the intervillous space at term.
- **Quote:** > It has been estimated that there are about 120 spiral arterial entries into the intervillous space at term.
- **Reviewer note:** SECONDARY: NCBI Bookshelf ~120 entries at term within stored range 80-150 (central 100).

### `fetal_metabolism.pulmonary_fluid_net_rate_term_ml_per_kg_h`  ·  Tier D  ·  stored: -5.0 mL/kg/h

- **Primary citation:** `strang-1991-fetal-lung-liquid`  (_evidence: secondary_)
- **Source reports:** Near term/labour net flux falls toward zero and reverses to reabsorption (-0.4 to -0.8 mL/kg/h observed).
- **Quote:** > this animal reabsorbed liquid both in early (-0.4 ml kg−1 h−1) and advanced labour (-0.8 ml kg−1 h−1).
- **Reviewer note:** SECONDARY evidence (ovine, hypothesis-tier): confirms sign reversal to reabsorption near term; observed magnitudes (-0.4 to -0.8) smaller than stored -5.0, within stored range -10 to 0.

### `placental_structure.hsd2_cortisol_inactivation_fraction`  ·  Tier D  ·  stored: 0.85 dimensionless

- **Primary citation:** `benediktsson-1997-11bhsd2`  (_evidence: abstract_)
- **Source reports:** Abstract states most maternally administered cortisol was metabolized to cortisone (qualitative), with no numeric inactivation fraction reported.
- **Quote:** > Most of the maternally administered cortisol was metabolized to cortisone
- **Reviewer note:** 'Most' is qualitatively consistent with the stored 0.85 (0.7-0.95) but the abstract gives no percentage; verdict close, not match.

### `placental_structure.igg_transfer_ratio_baseline`  ·  Tier D  ·  stored: 0.2 dimensionless

- **Primary citation:** `palmeira-2012-igg-transfer`  (_evidence: fulltext_)
- **Source reports:** Fulltext gives fetal/maternal IgG as 5-10% at weeks 17-22 rising to 50% at weeks 28-32; the stored mid-pregnancy central 0.2 (range 0.1-0.4) falls within this rising trajectory but is not stated as a single figure.
- **Quote:** > Fetal IgG concentrations were only 5%–10% of the maternal levels at weeks 17–22 but reached 50% of the maternal concentrations at weeks 28–32.
- **Reviewer note:** Source brackets mid-pregnancy ratio (0.05-0.10 at wk17-22; 0.50 at wk28-32); stored 0.2 (0.1-0.4) sits within the rising trajectory but is not a stated figure.

## ✅ match — source value agrees with stored value  (51)

### `amniotic_fluid.afv_peak_week`  ·  Tier A  ·  stored: 33.0 weeks

- **Primary citation:** `brace-1989-amniotic-fluid`  (_evidence: secondary_)
- **Source reports:** Secondary textbook chapter summarizing the Brace & Wolf (1989) nomogram reports the peak AFV occurring at 33.8 weeks, matching the stored peak week of 33.
- **Quote:** > They reported a peak AFV of 931 mL at 33.8 weeks with a decrease in the AFV thereafter
- **Reviewer note:** SECONDARY: 33.8 wk peak (Brace & Wolf via textbook) matches stored 33 wk.

### `fetal_circulation.ua_pi_term`  ·  Tier A  ·  stored: 0.85 dimensionless

- **Primary citation:** `acharya-2005-umbilical-pi`  (_evidence: secondary_)
- **Source reports:** Median UA-PI in normal-growth singletons is 0.83 at 39 weeks and 0.77 at 40 weeks, bracketing the stored term value of 0.85. INTERGROWTH-21st gives a median of 0.79 at 40 weeks.
- **Quote:** > At 39 weeks gestation Median UA-PI: 0.83; At 40 weeks gestation Median UA-PI: 0.77
- **Reviewer note:** SECONDARY: median term UA-PI 0.77-0.83 brackets stored 0.85 (0.7-1.0).

### `fetal_growth.ac_32w_mm`  ·  Tier A  ·  stored: 282.0 mm

- **Primary citation:** `buck-louis-2015-nichd-growth`  (_evidence: secondary_)
- **Source reports:** NICHD Hispanic 50th-centile AC at 32w = 282 mm = stored 282 mm exactly (White 287).
- **Quote:** > NICHD White: 287, NICHD Hispanic: 282, NICHD Asian: 279, NICHD Black: 275
- **Reviewer note:** SECONDARY: NICHD Fetal Growth Studies 50th-centile reproduced in Grantz (AJOG 2018, PMC5807181); same NICHD standard family as the cited Buck Louis 2015 source.

### `fetal_growth.hadlock_coefficient`  ·  Tier A  ·  stored: 1.3596 log10(g)

- **Primary citation:** `hadlock-1991-fetal-weight`  (_evidence: secondary_)
- **Source reports:** Published Hadlock-4 sonographic weight equation; the intercept constant is 1.3596.
- **Quote:** > Hadlock 4: Log10(weight) = 1.3596 - 0.00386·AC·FL + 0.0064·HC + 0.00061·BPD·AC + 0.0424·AC + 0.174·FL
- **Reviewer note:** SECONDARY: Perinatology.com reproduces canonical Hadlock-4 (BPD+HC+AC+FL) equation citing Hadlock 1991 Radiology 181:129-133; intercept 1.3596 matches stored exactly.

### `fetal_growth.hc_32w_mm`  ·  Tier A  ·  stored: 297.0 mm

- **Primary citation:** `buck-louis-2015-nichd-growth`  (_evidence: secondary_)
- **Source reports:** NICHD White 50th-centile HC at 32w = 299 mm vs stored 297 mm (<1%).
- **Quote:** > NICHD White: 299, NICHD Hispanic: 295, NICHD Asian: 295, NICHD Black: 294
- **Reviewer note:** SECONDARY: NICHD Fetal Growth Studies 50th-centile reproduced in Grantz (AJOG 2018, PMC5807181); same NICHD standard family as the cited Buck Louis 2015 source.

### `fetal_metabolism.fetal_p50_mmhg`  ·  Tier A  ·  stored: 19.5 mmHg

- **Primary citation:** `bauer-1969-fetal-hb-affinity`  (_evidence: secondary_)
- **Source reports:** Fetal hemoglobin P50 is 19 mmHg versus 27 mmHg for adult HbA.
- **Quote:** > The partial pressure at which HbF is half saturated with oxygen (P50) is 19 mm Hg, compared to 27 mm Hg for HbA.
- **Reviewer note:** SECONDARY evidence: cited HbF P50 19 mmHg within stored range 18.5-20.5; adult ~27 consistent.

### `maternal_blood.o2_hb_p50_maternal`  ·  Tier A  ·  stored: 26.6 mmHg

- **Primary citation:** `severinghaus-1979-o2-hb-dissociation`  (_evidence: abstract_)
- **Source reports:** The standard P50 constant 26.6 appears verbatim in Severinghaus eq 4 (the Bohr-coefficient equation), where it is the reference Po2 at half-saturation.
- **Quote:** > delta In Po2/delta pH = (Po2/26.6)(0.184) - 2.2 (4)
- **Reviewer note:** 26.6 appears verbatim as the standard P50 constant embedded in eq 4; consistent with stored 26.6 mmHg.

### `maternal_renal.baseline_gfr_ml_per_min`  ·  Tier A  ·  stored: 100.0 mL/min

- **Primary citation:** `conrad-2001-relaxin-gfr`  (_evidence: secondary_)
- **Source reports:** StatPearls gives normal creatinine clearance (a GFR proxy) for younger healthy adult females as 90 to 110 mL/min, matching the stored non-pregnant baseline central 100 and range 90-110.
- **Quote:** > The normal range for CrCl is age-dependent, but for younger, healthy adults, it is about 100 to 120 mL/min in males and 90 to 110 mL/min in females.
- **Reviewer note:** SECONDARY: StatPearls female CrCl 90-110 mL/min matches stored central 100 (90-110) exactly.

### `maternal_renal.bun_term_mg_per_dl`  ·  Tier A  ·  stored: 8.0 mg/dL

- **Primary citation:** `cheung-lafayette-2013-renal`  (_evidence: secondary_)
- **Source reports:** Review Table 1 of typical laboratory values during pregnancy lists blood urea nitrogen as 9.0 mg/dL, which falls within the stored range 6-11 and near the stored central of 8.
- **Quote:** > Blood urea nitrogen 9.0 mg/dL
- **Reviewer note:** SECONDARY: review Table 1 BUN 9.0 mg/dL sits within stored 6-11, near central 8.

### `maternal_renal.plasma_creatinine_mg_per_dl_term`  ·  Tier A  ·  stored: 0.6 mg/dL

- **Primary citation:** `cheung-lafayette-2013-renal`  (_evidence: secondary_)
- **Source reports:** Systematic review of normal-pregnancy serum creatinine gives the third-trimester upper limit of normal as 77 umol/l = 0.87 mg/dL; the stored central 0.6 mg/dL (0.5-0.7) lies comfortably within the normal third-trimester range implied by this upper limit.
- **Quote:** > serum creatinine values greater than 76 μmol/l (0.86 mg/dl) in the first trimester, 72 μmol/l (0.81 mg/dl) in the second trimester, and 77 μmol/l (0.87 mg/dl) in the third trimester should be considered to be outside the upper limit of normal
- **Reviewer note:** SECONDARY: systematic-review third-trimester upper limit 0.87 mg/dL; stored term central 0.6 (0.5-0.7) is well within the normal range.

### `maternal_renal.plasma_osmolality_drop_mosm_per_kg`  ·  Tier A  ·  stored: 10.0 mOsm/kg

- **Primary citation:** `davison-1981-osmoregulation`  (_evidence: abstract_)
- **Source reports:** Abstract explicitly reports plasma osmolality fell to 10 mOsm/kg below preconception by the tenth week (and 9 mOsm/kg lower in the last trimester vs postpartum), matching the stored 10 mOsm/kg drop.
- **Quote:** > plasma osmolality (Posm) … was 10 mosmol/kg lower than preconception values by the tenth week, changing little thereafter.
- **Reviewer note:** Direct verbatim match: 10 mOsm/kg drop stated explicitly in the Davison 1981 abstract.

### `maternal_respiratory.baseline_arterial_ph`  ·  Tier A  ·  stored: 7.4 dimensionless

- **Primary citation:** `templeton-1976-blood-gas`  (_evidence: secondary_)
- **Source reports:** Normal arterial pH reference range is 7.35-7.45, with 7.40 used as the reference value.
- **Quote:** > pH (7.35-7.45)
- **Reviewer note:** SECONDARY evidence; stored non-pregnant baseline pH 7.40 (range 7.38-7.42) matches the standard 7.35-7.45 arterial reference centred on 7.40.

### `maternal_respiratory.baseline_respiratory_rate_bpm`  ·  Tier A  ·  stored: 16.0 breaths/min

- **Primary citation:** `lomauro-aliverti-2015-respiratory`  (_evidence: secondary_)
- **Source reports:** Normal resting adult respiratory rate is 12 to 20 breaths per minute.
- **Quote:** > the regular respiratory rate changes with age, with 12 to 20 respirations per minute for a resting adult.
- **Reviewer note:** SECONDARY evidence; stored central 16 sits within the quoted 12-20/min adult range.

### `maternal_respiratory.paco2_mmhg_term`  ·  Tier A  ·  stored: 32.0 mmHg

- **Primary citation:** `lomauro-aliverti-2015-respiratory`  (_evidence: fulltext_)
- **Source reports:** Fulltext states arterial carbon dioxide tension plateaus around 32 mmHg (alveolar around 27 mmHg) at term, exactly matching the stored central of 32 mmHg (range 30-34).
- **Quote:** > alveolar and arterial carbon dioxide tension ( P CO 2 ) levels decrease to plateaux around 27 and 32 mmHg, respectively
- **Reviewer note:** Arterial PaCO2 plateau 32 mmHg quoted verbatim, matches stored central 32. (Source also mentions ~30 mmHg in a clinical box.)

### `maternal_respiratory.pao2_mmhg_term`  ·  Tier A  ·  stored: 103.0 mmHg

- **Primary citation:** `lomauro-aliverti-2015-respiratory`  (_evidence: fulltext_)
- **Source reports:** Fulltext states arterial oxygen tension reaches 101-104 mmHg in the third trimester; stored central 103 mmHg (range 101-105) falls inside this window.
- **Quote:** > arterial oxygen tension increases, reaching 106–108 mmHg and 101–104 mmHg in the first and third trimesters, respectively
- **Reviewer note:** Third-trimester 101-104 mmHg quoted verbatim; stored 103 sits within it.

### `maternal_respiratory.term_respiratory_rate_bpm`  ·  Tier A  ·  stored: 16.0 breaths/min

- **Primary citation:** `lomauro-aliverti-2015-respiratory`  (_evidence: secondary_)
- **Source reports:** Respiratory rate is unchanged in pregnancy from the nonpregnant state (normal adult 12-20/min), so the term rate equals baseline.
- **Quote:** > The respiratory rate remains unchanged from the nonpregnant state.
- **Reviewer note:** SECONDARY evidence; source states RR is unchanged in pregnancy, so stored term 16/min equals the non-pregnant 12-20/min range.

### `placental_endocrine.estradiol_term_ng_per_ml`  ·  Tier A  ·  stored: 14.0 ng/mL

- **Primary citation:** `tulchinsky-1972-steroids`  (_evidence: secondary_)
- **Source reports:** Endotext states 17beta-estradiol rises to 6-30 ng/mL at term; stored central 14 (8-25) ng/mL sits within this range.
- **Quote:** > Following fertilization, 17β-estradiol increases gradually to a range of 6-30 ng/mL at term
- **Reviewer note:** SECONDARY: Endotext term estradiol 6-30 ng/mL; stored 14 (8-25) ng/mL consistent.

### `placental_endocrine.hcg_peak_miu_per_ml`  ·  Tier A  ·  stored: 100000.0 mIU/mL

- **Primary citation:** `cole-2010-hcg`  (_evidence: secondary_)
- **Source reports:** Average peak hCG ~110,000 mIU/mL at 10 weeks; StatPearls notes many normal pregnancies reach >100,000 mIU/mL at the 8-11 week peak. Stored central 100,000 (range 50,000-200,000) is consistent.
- **Quote:** > The average peak hCG level is approximately 110,000 mIU/mL and occurs at 10 weeks' gestation
- **Reviewer note:** SECONDARY: Endotext review states average peak ~110,000 mIU/mL at 10 wk; consistent with stored 100,000 (50,000-200,000).

### `placental_endocrine.hcg_peak_week`  ·  Tier A  ·  stored: 10.0 weeks

- **Primary citation:** `cole-2010-hcg`  (_evidence: fulltext_)
- **Source reports:** Fulltext explicitly states hCG reaches a peak at 10 weeks of gestation, matching the stored central value of 10 weeks (range 8-12).
- **Quote:** > As shown in Tables 2 and 3 hCG reaches a peak at 10 weeks of gestation, or almost one month after progesterone promotion is complete, then continues to be produced through the length of pregnancy.
- **Reviewer note:** Confirm the verbatim quote 'hCG reaches a peak at 10 weeks of gestation' supports the stored central value of 10 weeks.

### `placental_endocrine.progesterone_term_ng_per_ml`  ·  Tier A  ·  stored: 150.0 ng/mL

- **Primary citation:** `tulchinsky-1972-steroids`  (_evidence: secondary_)
- **Source reports:** Endotext states term progesterone ranges 100-300 ng/mL; stored central 150 (100-200) ng/mL is consistent and sits within this band.
- **Quote:** > At term, progesterone concentrations can range from 100-300 ng/mL
- **Reviewer note:** SECONDARY: Endotext term progesterone 100-300 ng/mL; stored 150 (100-200) ng/mL consistent.

### `placental_structure.cord_length_term_cm`  ·  Tier A  ·  stored: 55 cm

- **Primary citation:** `naeye-1985-cord-length`  (_evidence: secondary_)
- **Source reports:** Average umbilical cord length 50 to 60 cm.
- **Quote:** > Average length ranges from 50 to 60 cm, with a diameter of approximately 1 cm.
- **Reviewer note:** SECONDARY: StatPearls 50-60 cm brackets stored 55 cm central.

### `fetal_circulation.combined_ventricular_output_term_ml_per_min_per_kg`  ·  Tier B  ·  stored: 450.0 mL/min/kg

- **Primary citation:** `sutton-1991-fetal-cardiac`  (_evidence: secondary_)
- **Source reports:** Human PC-MRI reference-range study at term reports combined ventricular output of 465 mL/min/kg (2 SD 351-579), bracketing the stored 450 mL/min/kg.
- **Quote:** > Combined ventricular output: 465 (351, 579)
- **Reviewer note:** SECONDARY: human term PC-MRI CVO 465 mL/min/kg matches stored 450 (within 380-520 range).

### `fetal_circulation.ductus_venosus_shunt_fraction_late_pregnancy`  ·  Tier B  ·  stored: 0.2 fraction

- **Primary citation:** `kiserud-2000-fetal-circulation`  (_evidence: abstract_)
- **Source reports:** Shunt fraction reduced from 30% to 20% across the second half of pregnancy; 20% is the late-pregnancy endpoint.
- **Quote:** > The mean fraction of umbilical blood shunted through the ductus is reduced from 30% to 20% during the second half of the human pregnancy
- **Reviewer note:** Stored 0.20 matches the 20% late-pregnancy endpoint stated in the abstract.

### `fetal_circulation.ductus_venosus_shunt_fraction_mid_pregnancy`  ·  Tier B  ·  stored: 0.3 fraction

- **Primary citation:** `kiserud-2000-fetal-circulation`  (_evidence: abstract_)
- **Source reports:** Mean fraction of umbilical blood shunted through the ductus reduced from 30% to 20% during the second half of pregnancy; the 30% is the earlier (mid-pregnancy) value.
- **Quote:** > The mean fraction of umbilical blood shunted through the ductus is reduced from 30% to 20% during the second half of the human pregnancy
- **Reviewer note:** Stored 0.30 matches the 30% mid-pregnancy starting fraction stated in the abstract.

### `fetal_circulation.fhr_baseline_bpm`  ·  Tier B  ·  stored: 170.0 bpm

- **Primary citation:** `von-steinburg-2013-fhr`  (_evidence: secondary_)
- **Source reports:** Open review states the fetal heart rate rises to 170 bpm at the 9th week of gestation, then declines, matching the stored first-trimester baseline peak of 170 bpm.
- **Quote:** > in healthy fetuses, the heart rate (HR) increases from 110 bpm at the 5th week of gestation to 170 bpm at the 9th week of gestation
- **Reviewer note:** SECONDARY: first-trimester FHR peak of 170 bpm at week 9 matches stored 170 bpm baseline.

### `fetal_circulation.right_ventricular_output_fraction_term`  ·  Tier B  ·  stored: 0.6 dimensionless

- **Primary citation:** `sutton-1991-fetal-cardiac`  (_evidence: secondary_)
- **Source reports:** Main pulmonary artery flow equals right ventricular output; the study reports it as 56% (2 SD 44-68) of combined ventricular output, consistent with the stored RV fraction of 0.60.
- **Quote:** > Main pulmonary artery: 56 (44, 68)
- **Reviewer note:** SECONDARY: human term PC-MRI gives RV (main PA) = 56% of CVO; matches stored 0.60 (0.55-0.65). thoracickey corroborates 'right ventricle contributes approximately two-thirds'.

### `fetal_metabolism.glucose_utilisation_mg_per_kg_per_min`  ·  Tier B  ·  stored: 5.0 mg/kg/min

- **Primary citation:** `battaglia-meschia-1986-fetal-metabolism`  (_evidence: secondary_)
- **Source reports:** Fetal glucose utilization 5.58 mg/min/kg ([14C]) in fed normoglycemic sheep; umbilical uptake 4.77 mg/min/kg.
- **Quote:** > 5.58 mg.min-1.kg-1 +/- 0.54 SE
- **Reviewer note:** SECONDARY evidence (ovine, human-extrapolated): cited 5.58 mg/kg/min within stored range 4.0-6.0, near central 5.0.

### `fetal_metabolism.umbilical_artery_ph_term`  ·  Tier B  ·  stored: 7.27 pH

- **Primary citation:** `battaglia-meschia-1986-fetal-metabolism`  (_evidence: secondary_)
- **Source reports:** Mean umbilical arterial pH in uncomplicated term deliveries is 7.24 to 7.27.
- **Quote:** > Studies showed that in term infants with uncomplicated delivery, the mean cord arterial pH is 7.24 to 7.27, and the mean cord venous pH 7.32 to 7.34.
- **Reviewer note:** SECONDARY evidence: stored 7.27 equals top of cited mean arterial range 7.24-7.27.

### `fetal_metabolism.umbilical_vein_ph_term`  ·  Tier B  ·  stored: 7.34 pH

- **Primary citation:** `battaglia-meschia-1986-fetal-metabolism`  (_evidence: secondary_)
- **Source reports:** Mean umbilical venous pH in uncomplicated term deliveries is 7.32 to 7.34.
- **Quote:** > Studies showed that in term infants with uncomplicated delivery, the mean cord arterial pH is 7.24 to 7.27, and the mean cord venous pH 7.32 to 7.34.
- **Reviewer note:** SECONDARY evidence: stored 7.34 equals top of cited mean venous range 7.32-7.34.

### `maternal_blood.haematocrit_term`  ·  Tier B  ·  stored: 0.335 fraction

- **Primary citation:** `hytten-chamberlain-1980-blood-volume`  (_evidence: secondary_)
- **Source reports:** The Merck Manual states the average haematocrit falls to about 34% late in a singleton pregnancy, i.e. 0.34, essentially matching the stored term central of 0.335 and sitting inside the stored 0.31-0.36 range.
- **Quote:** > thus an increased hematocrit (Hct) decrease from 38 to 45% in healthy nonpregnant women to about 34% late in a singleton pregnancy
- **Reviewer note:** SECONDARY (Merck Manual), not the cited Hytten & Chamberlain 1980 primary; 34% = 0.34 matches stored 0.335.

### `maternal_blood.protein_c_term_pct`  ·  Tier B  ·  stored: 100 %

- **Primary citation:** `faught-1995-protein-s-c`  (_evidence: abstract_)
- **Source reports:** Faught 1995 found no statistically significant change in protein C during normal pregnancy, consistent with the stored ~100% (unchanged) term value.
- **Quote:** > There was no statistically significant change in antigenic or functional protein C levels during normal pregnancy.
- **Reviewer note:** Source explicitly reports protein C unchanged in pregnancy, supporting stored 100%.

### `maternal_blood.serum_albumin_term_g_per_dl`  ·  Tier B  ·  stored: 3.0 g/dL

- **Primary citation:** `hytten-chamberlain-1980-blood-volume`  (_evidence: secondary_)
- **Source reports:** The review states serum albumin declines from a mean of 42 g/L in non-pregnant women to 31 g/L near the end of pregnancy. 31 g/L = 3.1 g/dL, essentially matching the stored term central of 3.0 g/dL (stored range 2.8-3.4).
- **Quote:** > Research has indicated that in healthy pregnancies, serum albumin concentrations decline from a mean of 42 g/L in nonpregnant women to 31 g/L near the end of pregnancy due to an increase in plasma volume
- **Reviewer note:** SECONDARY (Wang 2025 review, citing Elliott & O'Kell 1971), not the cited Hytten & Chamberlain 1980 primary; 31 g/L = 3.1 g/dL matches stored 3.0 g/dL.

### `maternal_cardiovascular.baseline_heart_rate_bpm`  ·  Tier B  ·  stored: 70.0 bpm

- **Primary citation:** `mahendru-2014-cardiac-output`  (_evidence: secondary_)
- **Source reports:** Clark 1989: post-partum (non-pregnant surrogate) heart rate 71 +/- 10 bpm. Stored 70 essentially identical.
- **Quote:** > Heart rate (beats/min)                 71 ± 10          83 ± 1.0    17           0.015
- **Reviewer note:** SECONDARY: post-partum HR 71 bpm matches stored 70.

### `maternal_cardiovascular.baseline_map_mmhg`  ·  Tier B  ·  stored: 85.0 mmHg

- **Primary citation:** `mahendru-2014-cardiac-output`  (_evidence: secondary_)
- **Source reports:** Clark 1989: post-partum (non-pregnant surrogate) mean arterial pressure 86.4 +/- 7.5 mmHg. Stored 85 essentially identical.
- **Quote:** > Mean arterial pressure (mmHg)        86.4 ± 7.5       90.3 ± 5.8    4.5          0.210
- **Reviewer note:** SECONDARY: post-partum MAP 86.4 mmHg matches stored 85.

### `maternal_cardiovascular.pvr_term_dyn_s_cm5`  ·  Tier B  ·  stored: 80.0 dyn·s·cm^-5

- **Primary citation:** `sanghavi-rutherford-2014-cardio-review`  (_evidence: secondary_)
- **Source reports:** Clark 1989 invasive study: at-term PVR 78 +/- 22 dyn*s/cm^5 (a 34% fall); stored 80 essentially identical.
- **Quote:** > Pulmonary vascular resistance         119 ± 47          78 ± 22     -34          0.022
- **Reviewer note:** SECONDARY: at-term PVR 78 dyn*s/cm^5 (-34%) matches stored 80.

### `maternal_endocrine.free_t4_term_ng_per_dl`  ·  Tier B  ·  stored: 0.9 ng/dL

- **Primary citation:** `glinoer-1997-thyroid`  (_evidence: secondary_)
- **Source reports:** Third-trimester free T4 5th-95th centile 0.7-1.20 ng/dL with mean 0.90 ng/dL. The reported mean (0.90) equals the stored central (0.9); the stored range 0.7-1.1 closely matches the reported 0.7-1.20.
- **Quote:** > For Free T4, the trimester specific reference ranges were 0.8-1.53, 0.7-1.20 and 0.7-1.20 ng/dL for first, second and third trimesters, respectively.
- **Reviewer note:** SECONDARY: reported third-trimester free T4 mean 0.90 ng/dL equals stored central 0.9; ranges agree closely.

### `maternal_renal.cumulative_sodium_retention_g`  ·  Tier B  ·  stored: 1.0 g

- **Primary citation:** `cheung-lafayette-2013-renal`  (_evidence: abstract_)
- **Source reports:** Abstract states a rise in aldosterone produces a net gain of approximately 1000 mg of sodium, equal to the stored 1.0 g cumulative sodium retention.
- **Quote:** > A rise in serum aldosterone results in a net gain of approximately 1000 mg of sodium.
- **Reviewer note:** Direct match: 1000 mg = 1.0 g stated explicitly in the Cheung 2013 abstract.

### `maternal_renal.plasma_uric_acid_nadir_mg_per_dl`  ·  Tier B  ·  stored: 3.0 mg/dL

- **Primary citation:** `cheung-lafayette-2013-renal`  (_evidence: secondary_)
- **Source reports:** Review states serum uric acid falls in early pregnancy to a nadir of 2 to 3.0 mg/dL by 22 to 24 weeks; the stored central 3.0 mg/dL (2.5-3.5) sits at the top of this quoted nadir band.
- **Quote:** > Serum uric acid levels fall in early pregnancy, reaching a nadir of 2 to 3.0 mg/dL by 22 to 24 weeks, followed by gradual rise to normal by term.
- **Reviewer note:** SECONDARY: quoted nadir 2-3.0 mg/dL at 22-24 wk; stored central 3.0 is the upper bound of that band.

### `maternal_renal.urinary_protein_excretion_term_mg_per_24h`  ·  Tier B  ·  stored: 150.0 mg/24h

- **Primary citation:** `cheung-lafayette-2013-renal`  (_evidence: secondary_)
- **Source reports:** Review reports that Higby et al studied 270 healthy pregnant women and found the 95th percentile for 24-hour urinary protein excretion to be 259.4 mg; this upper bound matches the stored upper range value of 260 mg/24h, with the stored central 150 falling within the normal-pregnancy distribution.
- **Quote:** > Higby et al subsequently evaluated 270 healthy pregnant women and reported the 95th percentile for 24-hour urinary protein excretion to be 259.4 mg.
- **Reviewer note:** SECONDARY: Higby 95th-percentile 259.4 mg/24h matches stored upper bound 260; stored central 150 lies within the normal range.

### `maternal_respiratory.term_arterial_ph`  ·  Tier B  ·  stored: 7.44 dimensionless

- **Primary citation:** `templeton-1976-blood-gas`  (_evidence: secondary_)
- **Source reports:** Composite mean third-trimester arterial pH 7.46 (with PaCO2 26.6, HCO3 18.2) — a compensated respiratory alkalosis on the alkaline side.
- **Quote:** > The composite mean values were pH 7.46, arterial carbon dioxide pressure (PaCO2) 26.6 mmHg, arterial oxygen pressure 88.3 mmHg, and bicarbonate 18.2 mEq/L.
- **Reviewer note:** SECONDARY evidence; third-trimester mean pH 7.46 falls within stored range 7.42-7.46. Cohort studied at moderate altitude (lower PaCO2 than sea level), but pH is comparable.

### `placental_endocrine.hpl_baseline_ug_per_ml`  ·  Tier B  ·  stored: 0.0 ug/mL

- **Primary citation:** `handwerger-2010-hpl`  (_evidence: secondary_)
- **Source reports:** Cleveland Clinic states the non-pregnant hPL level is 0.00-0.10 mcg/mL, matching the stored operational baseline of 0 (0-0.1) ug/mL.
- **Quote:** > If you're not pregnant, the level is 0.00-0.10 mcg/mL (micrograms per milliliter).
- **Reviewer note:** SECONDARY: non-pregnant hPL 0.00-0.10 mcg/mL per Cleveland Clinic matches stored baseline 0 (0-0.1) ug/mL.

### `placental_endocrine.hpl_term_ug_per_ml`  ·  Tier B  ·  stored: 7.0 ug/mL

- **Primary citation:** `handwerger-2010-hpl`  (_evidence: secondary_)
- **Source reports:** Cleveland Clinic gives a third-trimester hPL reference range of 4.50-12.80 mcg/mL; Endotext review gives a term rise to ~3.5-25 ug/mL. Stored central 7 (5-10) ug/mL sits within both.
- **Quote:** > In the third trimester, the level reaches 4.50-12.80 mcg/mL.
- **Reviewer note:** SECONDARY: stored 7 (5-10) ug/mL falls within Cleveland Clinic third-trimester range 4.50-12.80 mcg/mL.

### `placental_endocrine.relaxin_t1_ng_per_ml`  ·  Tier B  ·  stored: 1.0 ng/mL

- **Primary citation:** `conrad-2001-relaxin-gfr`  (_evidence: secondary_)
- **Source reports:** Peer-reviewed OA review states serum relaxin peaks at ~1 ng/ml at the end of the first trimester; stored central 1.0 (0.6-1.5) ng/mL matches.
- **Quote:** > Relaxin is detectable in the circulation of women during the luteal phase, and, if conception occurs, serum concentrations rapidly rise, reaching a peak of ∼1 ng/ml at the end of the first trimester.
- **Reviewer note:** SECONDARY: PMC3154715 review states relaxin peaks ~1 ng/ml end of first trimester; matches stored 1.0 (0.6-1.5) ng/mL.

### `placental_glucose.maternal_fetal_glucose_gradient_term_mmol_per_l`  ·  Tier B  ·  stored: 1.2 mmol/L

- **Primary citation:** `illsley-2000-glut1`  (_evidence: secondary_)
- **Source reports:** Human in vivo study of healthy term pregnancies measured the transplacental maternal-fetal glucose gradient as 1.22 (SD 0.42) mmol/L.
- **Quote:** > The transplacental maternal-fetal glucose gradient was 1.22 (0.42) mmol/L.
- **Reviewer note:** SECONDARY: measured term maternal-fetal gradient 1.22 mmol/L matches stored 1.2 mmol/L.

### `placental_structure.membrane_thickness_um`  ·  Tier B  ·  stored: 4.5 micrometres

- **Primary citation:** `mayhew-2014-placental-morphometry`  (_evidence: secondary_)
- **Source reports:** Arithmetic mean villous membrane thickness at term 4.53 microns (harmonic mean 3.65).
- **Quote:** > The villous membrane, defined as the outer surface of the syncytiotrophoblast (excluding the microvilli) to the inner surface of the capillary endothelium, was estimated to have an arithmetic mean thickness of 4.53 microns and a harmonic mean thickness of 3.65 microns.
- **Reviewer note:** SECONDARY: arithmetic mean 4.53 um matches stored 4.5 um (arithmetic mean villous membrane thickness).

### `placental_structure.term_area_m2`  ·  Tier B  ·  stored: 11.5 m^2

- **Primary citation:** `mayhew-2014-placental-morphometry`  (_evidence: secondary_)
- **Source reports:** Syncytiotrophoblast exchange surface area reaches 11-12 m^2 at term.
- **Quote:** > The surface area of syncytiotrophoblasts is about 5 square meters at 28 weeks' gestation and reaches up to 11–12 square meters at term
- **Reviewer note:** SECONDARY: NCBI Bookshelf chapter states 11-12 m^2 at term; brackets stored 11.5 m^2.

### `fetal_metabolism.umbilical_artery_lactate_term_mmol_per_l`  ·  Tier C  ·  stored: 3.5 mmol/L

- **Primary citation:** `battaglia-meschia-1986-fetal-metabolism`  (_evidence: secondary_)
- **Source reports:** Population umbilical artery lactate median (50th percentile) is 3.4 mmol/L.
- **Quote:** > Lactate values at the 50th, 90th, and 97th percentile were 3.4, 7.0, and 9.0 mmol/L.
- **Reviewer note:** SECONDARY evidence: stored central 3.5 ~ cited median 3.4 mmol/L; cohort all gestations/modes.

### `maternal_blood.pai2_term_ng_per_ml`  ·  Tier C  ·  stored: 250 ng/mL

- **Primary citation:** `kruithof-1987-fibrinolysis`  (_evidence: abstract_)
- **Source reports:** Kruithof 1987 reports PAI-2 rose from below the detection limit (~10 ng/mL) to 260 ng/mL at term, consistent with the stored central 250 ng/mL (within rounding and the stored range 150-400).
- **Quote:** > Its level, quantified with a radioimmunoassay, increased from below the detection limit (approximately 10 ng/mL) in normal plasma to 260 ng/mL at term.
- **Reviewer note:** Source term PAI-2 of 260 ng/mL closely matches stored 250 ng/mL.

### `maternal_cardiovascular.baseline_pvr_dyn_s_cm5`  ·  Tier C  ·  stored: 120 dyn·s·cm⁻⁵

- **Primary citation:** `sanghavi-rutherford-2014-cardio-review`  (_evidence: secondary_)
- **Source reports:** Clark 1989 invasive (PA-catheter) study: post-partum (non-pregnant surrogate) PVR 119 +/- 47 dyn*s/cm^5; stored 120 essentially identical.
- **Quote:** > Pulmonary vascular resistance         119 ± 47          78 ± 22     -34          0.022
- **Reviewer note:** SECONDARY: post-partum (non-pregnant) PVR 119 dyn*s/cm^5 matches stored 120.

### `fetal_metabolism.pulmonary_fluid_net_rate_baseline_ml_per_kg_h`  ·  Tier D  ·  stored: 5.0 mL/kg/h

- **Primary citation:** `strang-1991-fetal-lung-liquid`  (_evidence: secondary_)
- **Source reports:** Pre-labour fetal sheep lung liquid secretion rate begins ~5.3 mL/kg/h, declining toward labour.
- **Quote:** > In the first phase of its decline, mean secretion rate fell from 5.3 to 3.1 ml kg−1 h−1, before decreasing in the second phase to 1.8 ml kg−1 h−1.
- **Reviewer note:** SECONDARY evidence (ovine, hypothesis-tier): baseline secretion ~5.3 mL/kg/h equals stored central 5.0 within range 3.0-6.0.

### `placental_structure.igg_transfer_ratio_term`  ·  Tier D  ·  stored: 1.2 dimensionless

- **Primary citation:** `palmeira-2012-igg-transfer`  (_evidence: fulltext_)
- **Source reports:** Fulltext states fetal IgG concentrations usually exceed maternal ones by 20-30% at full term, i.e. a fetal/maternal ratio of ~1.2-1.3, consistent with the stored central 1.2 (range 1.0-1.5).
- **Quote:** > fetal IgG concentrations usually exceed maternal ones by 20%–30% at full term
- **Reviewer note:** 20-30% excess => ratio 1.2-1.3; stored central 1.2 matches the lower bound of the source statement.

## 🔍 not found — value not in fetched text (check table/figure in full PDF)  (46)

### `fetal_growth.efw_16w_g`  ·  Tier A  ·  stored: 145.0 g

- **Primary citation:** `buck-louis-2015-nichd-growth`  (_evidence: abstract_)
- **Reviewer note:** Abstract reports EFW percentiles only at 39 weeks (race-stratified), not at this gestational week; the week-specific value is in an uncaptured growth table.

### `fetal_growth.efw_20w_g`  ·  Tier A  ·  stored: 331.0 g

- **Primary citation:** `buck-louis-2015-nichd-growth`  (_evidence: abstract_)
- **Reviewer note:** Abstract reports EFW percentiles only at 39 weeks (race-stratified), not at this gestational week; the week-specific value is in an uncaptured growth table.

### `maternal_blood.o2_hb_hill_coefficient_maternal`  ·  Tier A  ·  stored: 2.7 dimensionless

- **Primary citation:** `severinghaus-1979-o2-hb-dissociation`  (_evidence: abstract_)
- **Source reports:** Abstract gives the dissociation equation S = (((Po2^3 + 150 Po2)^-1 x 23,400) + 1)^-1 but never prints a Hill coefficient of 2.7; the ~2.7 exponent is inferred from the cubic numerator, not stated.
- **Reviewer note:** Hill coefficient 2.7 is derivable from the cubic form but no verbatim '2.7' appears in the available abstract.

### `maternal_blood.oxyhb_bohr_coefficient`  ·  Tier A  ·  stored: -0.48 log(mmHg)/pH

- **Primary citation:** `dash-bassingthwaighte-2010-o2-hb`  (_evidence: abstract_)
- **Source reports:** Dash & Bassingthwaighte 2010 abstract describes invertible Hill-type equations for HbO2/HbCO2 but does not print a Bohr coefficient value of -0.48.
- **Reviewer note:** No numeric Bohr coefficient (-0.48) appears in the available abstract; the rationale itself concedes Dash 2010 does not print the coefficient.

### `amniotic_fluid.af_lactate_term_mmol_per_l`  ·  Tier B  ·  stored: 4 mmol/L

- **Primary citation:** `underwood-2005-amniotic-fluid`  (_evidence: abstract_)
- **Source reports:** Abstract is a generic review summary with no numeric values; it does not report an AF lactate concentration at term.
- **Reviewer note:** Underwood 2005 abstract gives no numbers. Term AF lactate 4 mmol/L would require the review fulltext.

### `fetal_circulation.umbilical_vein_flow_term_ml_per_min`  ·  Tier B  ·  stored: 290.0 mL/min

- **Primary citation:** `kiserud-2001-umbilical-vein`  (_evidence: abstract_)
- **Source reports:** Abstract reports DV shunt fractions (28-32% at 18-20 wk down to 18% at 31 wk) and growth associations, but gives no absolute umbilical-vein flow value in mL/min.
- **Reviewer note:** Abstract focuses on shunt fraction; the absolute ~290 mL/min term UV flow is not stated in available text.

### `maternal_blood.antithrombin_term_pct`  ·  Tier B  ·  stored: 95 %

- **Primary citation:** `faught-1995-protein-s-c`  (_evidence: abstract_)
- **Source reports:** Faught 1995 measured only protein C and protein S; antithrombin is not mentioned in the abstract.
- **Reviewer note:** Primary citation (Faught 1995) does not report antithrombin; the ~95% term value cannot be verified against this source.

### `maternal_blood.factor_ix_term_pct`  ·  Tier B  ·  stored: 130 %

- **Primary citation:** `stirling-1984-coagulation-factors`  (_evidence: abstract_)
- **Source reports:** Stirling 1984 abstract lists factors VII, VIII, X and fibrinogen as rising markedly but does not mention factor IX at all.
- **Reviewer note:** Factor IX is not named in the abstract; the ~130% term value cannot be verified.

### `maternal_blood.factor_xii_term_pct`  ·  Tier B  ·  stored: 160 %

- **Primary citation:** `stirling-1984-coagulation-factors`  (_evidence: abstract_)
- **Source reports:** Stirling 1984 abstract does not mention factor XII; only VII, VIII, X, fibrinogen, II, V and several inhibitors are named.
- **Reviewer note:** Factor XII is not named in the abstract; the ~160% term value cannot be verified.

### `maternal_cardiovascular.cardiac_output_peak_week`  ·  Tier B  ·  stored: 30.0 weeks

- **Primary citation:** `mahendru-2014-cardiac-output`  (_evidence: abstract_)
- **Source reports:** Abstract states the greatest CO increase occurred by the second trimester; no explicit peak week ~30 reported.
- **Reviewer note:** Abstract locates greatest CO rise at T2, not a numeric peak week of 30; specific value not in text.

### `maternal_cardiovascular.cardiac_output_t1_l_per_min`  ·  Tier B  ·  stored: 5.5 L/min

- **Primary citation:** `mahendru-2014-cardiac-output`  (_evidence: abstract_)
- **Source reports:** Abstract gives only the CO change (Δ0.6 l/min) and no absolute trimester-stratified CO means.
- **Reviewer note:** Absolute T1 CO (5.5) not in abstract; only deltas reported.

### `maternal_cardiovascular.cardiac_output_t2_l_per_min`  ·  Tier B  ·  stored: 6.4 L/min

- **Primary citation:** `mahendru-2014-cardiac-output`  (_evidence: abstract_)
- **Source reports:** Abstract gives only the CO change (Δ0.6 l/min greatest by T2); no absolute T2 CO mean.
- **Reviewer note:** Absolute T2 CO (6.4) not in abstract; only the delta is reported.

### `maternal_endocrine.homa_ir_baseline`  ·  Tier B  ·  stored: 2.0 dimensionless

- **Primary citation:** `catalano-1991-insulin-sensitivity`  (_evidence: abstract_)
- **Source reports:** Catalano 1991 abstract measures insulin sensitivity via hyperinsulinemic-euglycemic clamp (glucose infusion rate) and insulin release via IVGTT. It reports no HOMA-IR value and no pre-pregnancy baseline HOMA-IR figure.
- **Reviewer note:** Abstract reports clamp-based insulin sensitivity, not HOMA-IR; no baseline HOMA-IR value stated.

### `maternal_renal.gfr_peak_week`  ·  Tier B  ·  stored: 16.0 weeks

- **Primary citation:** `conrad-2001-relaxin-gfr`  (_evidence: abstract_)
- **Source reports:** Abstract describes mechanisms of hyperfiltration but gives no gestational timing for the GFR peak.
- **Reviewer note:** No week-of-peak GFR information in the Conrad 2001 abstract; Dunlop 1981 (also cited in rationale) is not the primary citation here.

### `maternal_renal.renal_plasma_flow_baseline_ml_per_min`  ·  Tier B  ·  stored: 600.0 mL/min

- **Primary citation:** `dunlop-1981-renal-plasma-flow`  (_evidence: abstract_)
- **Source reports:** Abstract reports ERPF increased 80% in early pregnancy but provides no absolute non-pregnant ERPF value in mL/min.
- **Quote:** > Compared with non-pregnant values, ERPF increased by 80 percent during early pregnancy but fell significantly from this new level during the third trimester.
- **Reviewer note:** Abstract gives percentage change only; absolute baseline RPF of 600 mL/min not stated in cached source.

### `maternal_respiratory.vco2_term_ml_per_min`  ·  Tier B  ·  stored: 250.0 mL/min

- **Primary citation:** `lomauro-aliverti-2015-respiratory`  (_evidence: fulltext_)
- **Source reports:** Fulltext reports basal metabolic rate (and O2 consumption) rises by up to 14%/21% but gives no CO2-production (VCO2) value, absolute or percent, so the stored 250 mL/min term VCO2 is not present.
- **Reviewer note:** No CO2-production (VCO2) figure in available fulltext; only O2 consumption/metabolic-rate percentages are given.

### `placental_gas_exchange.umbilical_artery_pco2_mmhg`  ·  Tier B  ·  stored: 50 mmHg

- **Primary citation:** `carter-2009-placental-development`  (_evidence: abstract_)
- **Source reports:** Abstract reviews placental oxygen transfer; it does not report any umbilical-artery PCO2 value.
- **Reviewer note:** No UA PCO2 figure in abstract. Fulltext unavailable.

### `placental_gas_exchange.umbilical_artery_po2_mmhg`  ·  Tier B  ·  stored: 17.0 mmHg

- **Primary citation:** `carter-2009-placental-development`  (_evidence: abstract_)
- **Source reports:** Abstract reviews placental oxygen-transfer factors; it does not report an umbilical-artery PO2 value.
- **Reviewer note:** No UA PO2 figure in abstract. Fulltext unavailable.

### `placental_gas_exchange.umbilical_vein_pco2_mmhg`  ·  Tier B  ·  stored: 40 mmHg

- **Primary citation:** `carter-2009-placental-development`  (_evidence: abstract_)
- **Source reports:** Abstract reviews placental oxygen transfer; it does not report any umbilical-vein PCO2 value.
- **Reviewer note:** No UV PCO2 figure in abstract. Fulltext unavailable.

### `placental_gas_exchange.umbilical_vein_po2_mmhg`  ·  Tier B  ·  stored: 30.0 mmHg

- **Primary citation:** `carter-2009-placental-development`  (_evidence: abstract_)
- **Source reports:** Abstract reviews placental oxygen-transfer factors and globin/oxygen-affinity evolution; it does not report an umbilical-vein PO2 value.
- **Reviewer note:** No UV PO2 figure in abstract. Fulltext unavailable.

### `placental_glucose.glucose_glut1_km_mmol_per_l`  ·  Tier B  ·  stored: 2.5 mmol/L

- **Primary citation:** `illsley-2000-glut1`  (_evidence: abstract_)
- **Source reports:** The abstract is a qualitative review of placental GLUT isoform localization, regulation, and functional significance. It does not report any numeric Michaelis constant (Km) for GLUT1.
- **Reviewer note:** Abstract-only; no numeric Km in available text. The '2-5 mmol/L' claim lives in the dataset rationale, not the cited abstract.

### `placental_structure.initial_area_m2`  ·  Tier B  ·  stored: 0.5 m^2

- **Primary citation:** `mayhew-2014-placental-morphometry`  (_evidence: abstract_)
- **Source reports:** Morphomics review abstract describes methodology and 3D quantification but reports no early-gestation villous surface-area figure.
- **Reviewer note:** Abstract is a methodological 'omics' review; no numeric villous surface area present.

### `amniotic_fluid.afv_spread_weeks`  ·  Tier C  ·  stored: 9.0 weeks

- **Primary citation:** `brace-1989-amniotic-fluid`  (_evidence: abstract_)
- **Source reports:** This is an empirical Gaussian-fit spread (sigma) parameter derived downstream, not a quantity Brace & Wolf report. The abstract contains no such curve-shape parameter.
- **Reviewer note:** Derived Gaussian-fit parameter, not reported by the source; abstract has no curve sigma. Per rationale it is a single-fit modeling value.

### `fetal_circulation.mca_flow_term_ml_per_min`  ·  Tier C  ·  stored: 30 mL/min

- **Primary citation:** `mari-1995-mca-pi`  (_evidence: abstract_)
- **Source reports:** Mari 1995 abstract reports MCA pulsatility-index waveforms only; it gives no absolute MCA flow value in mL/min.
- **Reviewer note:** Abstract is about MCA-PI, not absolute flow; the ~30 mL/min term MCA flow is not in available text.

### `fetal_circulation.systemic_venous_return_po2_mmhg`  ·  Tier C  ·  stored: 15.0 mmHg

- **Primary citation:** `kiserud-2000-fetal-circulation`  (_evidence: abstract_)
- **Source reports:** Kiserud DV review abstract discusses shunt fractions (30%->20%) and DV regulation but reports no PO2 figure for systemic venous return.
- **Reviewer note:** Abstract contains no PO2/oxygen-tension value; the 15 mmHg systemic-venous-return PO2 is not in the available text.

### `maternal_cardiovascular.cardiac_output_individual_sigma`  ·  Tier C  ·  stored: 0.13 fraction

- **Primary citation:** `hunter-robson-1992-cardiac-output`  (_evidence: abstract_)
- **Source reports:** Abstract describes the qualitative shape of cardiac adaptation; it reports no between-individual sigma figure.
- **Reviewer note:** Qualitative review; 13% individual sigma is a model-fit abstraction, not in source.

### `maternal_cardiovascular.cardiac_output_spread_weeks`  ·  Tier C  ·  stored: 12.0 weeks

- **Primary citation:** `hunter-robson-1992-cardiac-output`  (_evidence: abstract_)
- **Source reports:** Abstract describes timing qualitatively (HR rises 2–5 weeks, SV later) but reports no Gaussian spread parameter.
- **Reviewer note:** Spread (weeks) is a curve-fit parameter; not reported in the qualitative abstract.

### `maternal_cardiovascular.uterine_flow_growth_rate_per_week`  ·  Tier C  ·  stored: 0.22 1/week

- **Primary citation:** `thaler-1990-uterine-flow`  (_evidence: abstract_)
- **Source reports:** Abstract reports flow means at sampled timepoints, not a logistic growth-rate parameter.
- **Reviewer note:** 0.22/week is a fit parameter; growth-rate constant not reported in abstract.

### `maternal_cardiovascular.uterine_flow_individual_sigma`  ·  Tier C  ·  stored: 0.2 fraction

- **Primary citation:** `thaler-1990-uterine-flow`  (_evidence: abstract_)
- **Source reports:** Abstract reports population means; it does not report a fractional between-individual sigma in the available text.
- **Reviewer note:** Fractional sigma (0.2) is model-fit; not stated in abstract.

### `maternal_renal.gfr_logistic_rate_per_week`  ·  Tier C  ·  stored: 0.4 1/week

- **Primary citation:** `conrad-2001-relaxin-gfr`  (_evidence: abstract_)
- **Source reports:** Abstract contains no logistic-fit rate parameter; this is an empirical model-fit value, not reported by the source.
- **Reviewer note:** Logistic rate is a derived curve-fit parameter; not present in the Conrad 2001 abstract.

### `maternal_renal.tubular_phosphate_threshold_term`  ·  Tier C  ·  stored: 0.85 mmol/L

- **Primary citation:** `cheung-lafayette-2013-renal`  (_evidence: abstract_)
- **Source reports:** Cheung 2013 abstract does not mention phosphate handling or any TmP/GFR value.
- **Reviewer note:** No phosphate-threshold data in the Cheung 2013 abstract; stored 0.85 mmol/L not verifiable from cached source.

### `placental_gas_exchange.co2_diffusing_capacity_term_ml_min_mmhg`  ·  Tier C  ·  stored: 6 mL/min/mmHg

- **Primary citation:** `mayhew-1986-gas-diffusion`  (_evidence: abstract_)
- **Source reports:** Abstract estimates the oxygen-diffusing capacity of the term placenta morphometrically but reports no numeric value and does not give a CO2 diffusing capacity. Rationale notes the CO2 value is back-calculated by analogy to O2.
- **Reviewer note:** Abstract gives no numeric diffusing-capacity value and does not address CO2. Fulltext unavailable.

### `placental_gas_exchange.gas_half_saturation_area_m2`  ·  Tier C  ·  stored: 6.0 m^2

- **Primary citation:** `mayhew-1986-gas-diffusion`  (_evidence: abstract_)
- **Source reports:** Abstract describes a morphometric diffusing-capacity model and ranks the influence of villous-membrane thickness, villous and capillary surface areas, but gives no numeric half-saturation surface area. Rationale states the half-saturation area is an explicit model-fit abstraction, not directly reported.
- **Reviewer note:** Phenomenological model-fit parameter; abstract has no numeric villous-area value. Fulltext unavailable.

### `placental_gas_exchange.gas_max_equilibration`  ·  Tier C  ·  stored: 0.78 fraction

- **Primary citation:** `carter-pijnenborg-2011-gas-exchange`  (_evidence: abstract_)
- **Source reports:** Abstract is an evolutionary review of invasive placentation in primates; it contains no fraction or equilibration figure. Rationale states the value is a model abstraction derived to reproduce the textbook UV PO2 window.
- **Reviewer note:** Model abstraction; cited abstract is qualitative evolutionary review with no numeric value. Fulltext unavailable.

### `placental_gas_exchange.spiral_artery_po2_estimate_mmhg`  ·  Tier C  ·  stored: 80 mmHg

- **Primary citation:** `carter-pijnenborg-2011-gas-exchange`  (_evidence: abstract_)
- **Source reports:** Abstract is an evolutionary review of invasive placentation; it discusses spiral-artery trophoblast invasion qualitatively but gives no spiral-artery PO2 value. Rationale states the value is estimated indirectly and is model-dependent.
- **Reviewer note:** No PO2 figure in abstract; indirect model estimate. Fulltext unavailable.

### `placental_glucose.glucose_glut1_vmax_per_area_mmol_per_min_per_m2`  ·  Tier C  ·  stored: 0.075 mmol/min/m^2

- **Primary citation:** `illsley-2000-glut1`  (_evidence: abstract_)
- **Source reports:** The abstract discusses GLUT1 expression and activity qualitatively but reports no maximum transport rate (Vmax) and no per-area flux figure.
- **Reviewer note:** Abstract-only; no Vmax value present. Stored value is an acknowledged Tier-C extrapolation not quantified in the abstract.

### `placental_glucose.glucose_glut3_vmax_per_area_mmol_per_min_per_m2`  ·  Tier C  ·  stored: 0.02 mmol/min/m^2

- **Primary citation:** `brown-2011-glut3`  (_evidence: abstract_)
- **Source reports:** Brown 2011 abstract reports relative GLUT3 protein expression across gestation (2nd trimester 48 +/- 7% of 1st; 3rd trimester 34 +/- 10% of 1st) but gives no absolute Vmax or per-area flux value.
- **Quote:** > GLUT3 expression in microvillous membranes detected by Western blot decreased through the trimesters such that expression in the second trimester (wks 14-26) was 48 ± 7% of that in the first trimester and by the third trimester (wks 31-40) only 34 ± 10% of first trimester expression.
- **Reviewer note:** Only relative expression percentages reported; no absolute mmol/min/m^2 Vmax. Stored value is an acknowledged Tier-C inference from relative expression.

### `placental_structure.allometric_coefficient_a`  ·  Tier C  ·  stored: 0.4 g^(1-b)

- **Primary citation:** `hutcheon-2012-placental-weight`  (_evidence: abstract_)
- **Source reports:** Hutcheon abstract reports placental-weight z-score associations with perinatal outcomes (e.g., stillbirth OR 2.0); contains no allometric PW=a*FW^b regression coefficient.
- **Reviewer note:** Allometric prefactor is derived; the abstract reports outcome odds ratios, not a regression prefactor.

### `placental_structure.allometric_exponent_b`  ·  Tier C  ·  stored: 0.85 dimensionless

- **Primary citation:** `hutcheon-2012-placental-weight`  (_evidence: abstract_)
- **Source reports:** Hutcheon abstract; reports no allometric exponent for the placental-fetal weight relation.
- **Reviewer note:** Exponent is a derived fit; abstract contains only z-score outcome statistics.

### `placental_structure.growth_rate_per_week`  ·  Tier C  ·  stored: 0.18 1/week

- **Primary citation:** `carter-2009-placental-development`  (_evidence: abstract_)
- **Source reports:** Review abstract of evolutionary factors in placental oxygen transfer; reports no logistic growth-rate coefficient for villous surface-area expansion.
- **Reviewer note:** Logistic fit parameter; the cited abstract contains no numeric growth-rate value (notes themselves state 'not reported directly in source').

### `placental_structure.intervillous_space_volume_term_ml`  ·  Tier C  ·  stored: 175.0 mL

- **Primary citation:** `mayhew-2014-placental-morphometry`  (_evidence: abstract_)
- **Source reports:** Morphomics review abstract; reports no intervillous-space volume figure.
- **Reviewer note:** No numeric intervillous volume in the abstract.

### `placental_structure.midpoint_week`  ·  Tier C  ·  stored: 22.0 weeks

- **Primary citation:** `carter-2009-placental-development`  (_evidence: abstract_)
- **Source reports:** Carter evolutionary review abstract; reports no gestational week for a villous-area logistic midpoint.
- **Reviewer note:** Logistic-curve inflection week; notes state 'not reported directly in source.'

### `placental_structure.spiral_artery_diameter_term_mm`  ·  Tier C  ·  stored: 2.5 mm

- **Primary citation:** `pijnenborg-2006-spiral-artery`  (_evidence: abstract_)
- **Source reports:** Pijnenborg abstract describes spiral arteries being remodelled into highly dilated vessels (qualitative); reports no diameter in mm.
- **Reviewer note:** Abstract qualitatively notes dilation but gives no numeric diameter.

### `placental_structure.syncytiotrophoblast_thickness_term_um`  ·  Tier C  ·  stored: 4 um

- **Primary citation:** `mayhew-2014-placental-morphometry`  (_evidence: abstract_)
- **Source reports:** Morphomics review abstract; reports no syncytiotrophoblast thickness figure.
- **Reviewer note:** No numeric syncytial-layer thickness in the abstract.

### `maternal_blood.fetal_microchimerism_baseline_cells_per_ml`  ·  Tier D  ·  stored: 0.0 cells/mL

- **Primary citation:** `bianchi-1996-microchimerism`  (_evidence: abstract_)
- **Source reports:** Bianchi 1996 abstract is qualitative ('rare nucleated fetal cells circulate within maternal blood') and reports detection rates by PCR; it gives no cells/mL concentration.
- **Reviewer note:** No cells/mL concentration in the abstract; Tier D hypothesis-only value cannot be verified against the source text.

### `maternal_blood.fetal_microchimerism_term_cells_per_ml`  ·  Tier D  ·  stored: 1.0 cells/mL

- **Primary citation:** `bianchi-1996-microchimerism`  (_evidence: abstract_)
- **Source reports:** Bianchi 1996 abstract is qualitative ('rare nucleated fetal cells circulate within maternal blood') and reports detection rates by PCR; it gives no cells/mL concentration.
- **Reviewer note:** No cells/mL concentration in the abstract; Tier D hypothesis-only value cannot be verified against the source text.

## ⬜ no source — book / paywalled / no abstract retrieved  (18)

### `maternal_blood.folate_term_ng_per_ml`  ·  Tier B  ·  stored: 5 ng/mL

- **Primary citation:** `hytten-chamberlain-1980-blood-volume`  (_evidence: none_)
- **Reviewer note:** Hytten & Chamberlain 1980 is a textbook; no abstract or fulltext cached, cannot verify the figure.

### `maternal_blood.haemoglobin_baseline_g_per_dl`  ·  Tier B  ·  stored: 13.5 g/dL

- **Primary citation:** `hytten-chamberlain-1980-blood-volume`  (_evidence: none_)
- **Reviewer note:** Hytten & Chamberlain 1980 is a textbook; no abstract or fulltext cached, cannot verify the figure.

### `maternal_cardiovascular.peak_excess_stroke_volume_ml`  ·  Tier B  ·  stored: 15.0 mL

- **Primary citation:** `sanghavi-rutherford-2014-cardio-review`  (_evidence: none_)
- **Reviewer note:** Primary source (Sanghavi & Rutherford 2014) has no cached abstract/fulltext (evidence=none); value cannot be checked against text.

### `maternal_cardiovascular.svr_nadir_dyn_s_cm5`  ·  Tier B  ·  stored: 750.0 dyn·s·cm^-5

- **Primary citation:** `sanghavi-rutherford-2014-cardio-review`  (_evidence: none_)
- **Reviewer note:** Primary source (Sanghavi & Rutherford 2014) has no cached abstract/fulltext (evidence=none); value cannot be checked against text.

### `maternal_endocrine.renin_term_ng_per_ml_per_h`  ·  Tier B  ·  stored: 12 ng/mL/h

- **Primary citation:** `wilson-1980-renin-aldosterone`  (_evidence: none_)
- **Reviewer note:** Wilson 1980 has no cached abstract or fulltext (evidence=none).

### `maternal_respiratory.inspiratory_capacity_term_l`  ·  Tier B  ·  stored: 2.7 L

- **Primary citation:** `crapo-1996-pregnancy-respiratory`  (_evidence: none_)
- **Reviewer note:** Primary citation Crapo 1996 is a book chapter with no abstract/fulltext cached (evidence none); cannot verify the 2.7 L term inspiratory capacity.

### `maternal_respiratory.tidal_volume_ml_term`  ·  Tier B  ·  stored: 680.0 mL

- **Primary citation:** `crapo-1996-pregnancy-respiratory`  (_evidence: none_)
- **Reviewer note:** Primary citation Crapo 1996 is a book chapter with no abstract/fulltext cached (evidence none); cannot verify the 680 mL term tidal volume.

### `maternal_respiratory.tlc_term_l`  ·  Tier B  ·  stored: 5.0 L

- **Primary citation:** `crapo-1996-pregnancy-respiratory`  (_evidence: none_)
- **Reviewer note:** Primary citation Crapo 1996 is a book chapter with no abstract/fulltext cached (evidence none); cannot verify the 5.0 L term TLC. (LoMauro review fulltext states TLC stays stable/constant but gives no absolute liters.)

### `fetal_circulation.aortic_isthmus_flow_fraction_cvo_term`  ·  Tier C  ·  stored: 0.1 dimensionless

- **Primary citation:** `rudolph-1985-fetal-circulation`  (_evidence: none_)
- **Reviewer note:** Rudolph 1985 lamb book chapter; evidence=none, cannot verify the ~10% aortic isthmus CVO fraction.

### `fetal_circulation.coronary_flow_fraction_cvo_term`  ·  Tier C  ·  stored: 0.03 dimensionless

- **Primary citation:** `rudolph-1985-fetal-circulation`  (_evidence: none_)
- **Reviewer note:** Rudolph 1985 lamb book chapter; evidence=none, cannot verify the ~3% coronary CVO fraction.

### `fetal_circulation.foramen_ovale_streamline_preference`  ·  Tier C  ·  stored: 0.8 fraction

- **Primary citation:** `rudolph-1985-fetal-circulation`  (_evidence: none_)
- **Reviewer note:** Rudolph 1985 lamb book chapter; evidence=none, cannot verify the 0.80 streamline-preference weight.

### `fetal_metabolism.fetal_urine_output_ml_per_kg_h_term`  ·  Tier C  ·  stored: 50.0 mL/kg/h

- **Primary citation:** `battaglia-meschia-1986-fetal-metabolism`  (_evidence: none_)
- **Reviewer note:** Textbook source; no abstract or fulltext cached (evidence=none).

### `maternal_cardiovascular.aortic_root_diameter_term_mm`  ·  Tier C  ·  stored: 30.0 mm

- **Primary citation:** `sanghavi-rutherford-2014-cardio-review`  (_evidence: none_)
- **Reviewer note:** Primary source (Sanghavi & Rutherford 2014) has no cached abstract/fulltext (evidence=none); value cannot be checked against text.

### `maternal_cardiovascular.map_individual_sigma_mmhg`  ·  Tier C  ·  stored: 5.0 mmHg

- **Primary citation:** `sanghavi-rutherford-2014-cardio-review`  (_evidence: none_)
- **Reviewer note:** Primary source (Sanghavi & Rutherford 2014) has no cached abstract/fulltext (evidence=none); value cannot be checked against text.

### `maternal_cardiovascular.map_spread_weeks`  ·  Tier C  ·  stored: 8.0 weeks

- **Primary citation:** `sanghavi-rutherford-2014-cardio-review`  (_evidence: none_)
- **Reviewer note:** Primary source (Sanghavi & Rutherford 2014) has no cached abstract/fulltext (evidence=none); value cannot be checked against text.

### `maternal_renal.urinary_glucose_term_mg_per_24h`  ·  Tier C  ·  stored: 90 mg/24h

- **Primary citation:** `davison-hytten-1974-gfr`  (_evidence: none_)
- **Reviewer note:** Davison & Hytten 1974 cached with evidence=none; no text available to verify 24-hour urinary glucose.

### `maternal_respiratory.aa_o2_gradient_term_mmhg`  ·  Tier C  ·  stored: 13.0 mmHg

- **Primary citation:** `crapo-1996-pregnancy-respiratory`  (_evidence: none_)
- **Reviewer note:** Primary citation Crapo 1996 is a book chapter with no abstract/fulltext cached (evidence none); cannot verify the 13 mmHg term A-a O2 gradient. (Templeton 1976 abstract notes A-a gradient unchanged but is not the primary citation here.)

### `maternal_respiratory.dlco_term_ml_per_min_per_mmhg`  ·  Tier C  ·  stored: 24.0 mL/min/mmHg

- **Primary citation:** `crapo-1996-pregnancy-respiratory`  (_evidence: none_)
- **Reviewer note:** Primary citation Crapo 1996 is a book chapter with no abstract/fulltext cached (evidence none); cannot verify the 24 mL/min/mmHg term DLCO.

