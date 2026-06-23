# Machine pre-verification review queue

**This is not verification.** A machine fetched each parameter's primary source (open-access full text where available, otherwise the abstract) and compared it to the stored value. Your job: read the quote (and, where needed, the full paper), confirm or correct the value, then set `extraction.review_status` to `verified` (or `contested`) in the dataset. The machine never does that promotion.

## Summary

| Verdict | Count |
| ------- | ----- |
| ❌ mismatch — source appears to report a different value | 4 |
| 🟡 close — same ballpark, confirm exact figure / statistic | 46 |
| ✅ match — source value agrees with stored value | 23 |
| 🔍 not found — value not in fetched text (check table/figure in full PDF) | 130 |
| ⬜ no source — book / paywalled / no abstract retrieved | 40 |
| **Total parameters** | **243** |

Work top-down: mismatches first (a wrong value is worse than an unverified one), then Tier A/B, then the rest.

## ❌ mismatch — source appears to report a different value  (4)

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

### `maternal_cardiovascular.peak_excess_cardiac_output_l_per_min`  ·  Tier B  ·  stored: 2.7 L/min

- **Primary citation:** `mahendru-2014-cardiac-output`  (_evidence: abstract_)
- **Source reports:** Abstract reports the greatest CO increase as Δ0.6±1 l/min (by T2), markedly below the stored peak excess of 2.7 L/min.
- **Quote:** > The greatest increase in cardiac output occurred by the second trimester (Δ: 0.6 ± 1 l/min, P < 0.001)
- **Reviewer note:** Stored 2.7 L/min peak excess vs abstract's Δ0.6±1 l/min for the same CO-rise quantity. Flagged in dataset notes for re-investigation against full results.

## 🟡 close — same ballpark, confirm exact figure / statistic  (46)

### `amniotic_fluid.afv_peak_ml`  ·  Tier A  ·  stored: 800.0 mL

- **Primary citation:** `brace-1989-amniotic-fluid`  (_evidence: abstract_)
- **Source reports:** Abstract reports mean amniotic fluid volume averaged 777 ml between 22 and 39 weeks (95% CI 302-1997 ml). It frames this as a flat average, not a peak, stating volume did not change significantly over that interval. The stored peak central 800 is not stated, but 777 lies within the stored range 600-1000.
- **Quote:** > mean amniotic fluid volume did not change significantly between 22 and 39 weeks and averaged 777 ml, with the 95% confidence interval ranging from 302 to 1997 ml.
- **Reviewer note:** Abstract mean 777 ml falls within stored range 600-1000; but abstract describes a flat plateau, not a peak of 800. Per-week nomogram peak not in abstract.

### `fetal_circulation.fhr_term_bpm`  ·  Tier A  ·  stored: 140.0 bpm

- **Primary citation:** `von-steinburg-2013-fhr`  (_evidence: fulltext_)
- **Source reports:** Table 4: mean FHR baseline at >=37 weeks is 136.0-136.4 bpm (95% CI); weeks 37-42 range ~133-138 bpm. Normal range stated as 120-160 bpm.
- **Quote:** > Gestational age n 95% confidence interval A &lt;28 1230 140.7538 – 141.9422 … &gt;=37 8478 136.0104 – 136.4295
- **Reviewer note:** Source term mean is ~136 bpm, just below stored 140 central but inside stored 130-150 range and the 120-160 normal range; magnitude/direction agree.

### `maternal_cardiovascular.peak_excess_heart_rate_bpm`  ·  Tier A  ·  stored: 15.0 bpm

- **Primary citation:** `mahendru-2014-cardiac-output`  (_evidence: abstract_)
- **Source reports:** Abstract reports HR increased maximally by the third trimester by Δ13±11 bpm; 13 falls within the stored 10–20 bpm range.
- **Quote:** > the heart rate increased maximally by the third trimester (Δ: 13 ± 11  bpm; P = 0.001)
- **Reviewer note:** Reported Δ13±11 bpm vs stored 15 (range 10–20); same quantity and magnitude, central figure differs slightly.

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

### `maternal_cardiovascular.heart_rate_peak_week`  ·  Tier B  ·  stored: 32 week

- **Primary citation:** `mahendru-2014-cardiac-output`  (_evidence: abstract_)
- **Source reports:** Abstract states heart rate increased maximally by the third trimester; week 32 lies in T3, but no numeric peak week is given.
- **Quote:** > the heart rate increased maximally by the third trimester (Δ: 13 ± 11  bpm; P = 0.001)
- **Reviewer note:** Abstract supports T3 timing of HR peak (week 32 is in T3); exact week not stated.

### `maternal_cardiovascular.term_uterine_flow_ml_per_min`  ·  Tier B  ·  stored: 750.0 mL/min

- **Primary citation:** `thaler-1990-uterine-flow`  (_evidence: abstract_)
- **Source reports:** Abstract reports 342 ml/min in the left ascending uterine artery in late gestation (~684 ml/min bilateral), near the stored combined 750 ml/min.
- **Quote:** > from a mean of 94.5 ml/min before pregnancy to a mean of 342 ml/min in late gestation (reflecting a 3.5-fold increase)
- **Reviewer note:** Stored 750 ml/min combined vs ~684 ml/min from doubling Thaler's 342 ml/min single-artery term value; same magnitude.

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

### `maternal_renal.gfr_ml_per_min`  ·  Tier B  ·  stored: 150.0 mL/min

- **Primary citation:** `cheung-lafayette-2013-renal`  (_evidence: abstract_)
- **Source reports:** Abstract states GFR increases 50% in pregnancy but gives no absolute term value in mL/min. A 50% rise on a ~100 mL/min baseline implies ~150 mL/min, consistent with stored, but the abstract supplies only the percentage, not the absolute figure.
- **Quote:** > The glomerular filtration rate increases 50% with subsequent decrease in serum creatinine, urea, and uric acid values.
- **Reviewer note:** Abstract gives +50% rise only; stored 150 mL/min is consistent with 50% over ~100 baseline but the absolute number is inferred, not stated.

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

### `placental_structure.placental_thickness_term_cm`  ·  Tier B  ·  stored: 2.5 cm

- **Primary citation:** `hoddick-1985-placental-thickness`  (_evidence: abstract_)
- **Source reports:** Hoddick abstract states placental thickness increases with menstrual age and the normal placenta never exceeded 4 cm; supports the upper bound but does not state a term central value of 2.5 cm.
- **Quote:** > At no stage of pregnancy was the normal placenta greater than 4 cm in thickness.
- **Reviewer note:** Abstract supports the normal upper bound (<4 cm, stored high 3.5) and the increasing trend; the central 2.5 cm itself is not stated.

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

## ✅ match — source value agrees with stored value  (23)

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

### `placental_endocrine.hcg_peak_week`  ·  Tier A  ·  stored: 10.0 weeks

- **Primary citation:** `cole-2010-hcg`  (_evidence: fulltext_)
- **Source reports:** Fulltext explicitly states hCG reaches a peak at 10 weeks of gestation, matching the stored central value of 10 weeks (range 8-12).
- **Quote:** > As shown in Tables 2 and 3 hCG reaches a peak at 10 weeks of gestation, or almost one month after progesterone promotion is complete, then continues to be produced through the length of pregnancy.
- **Reviewer note:** Confirm the verbatim quote 'hCG reaches a peak at 10 weeks of gestation' supports the stored central value of 10 weeks.

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

### `maternal_renal.cumulative_sodium_retention_g`  ·  Tier B  ·  stored: 1.0 g

- **Primary citation:** `cheung-lafayette-2013-renal`  (_evidence: abstract_)
- **Source reports:** Abstract states a rise in aldosterone produces a net gain of approximately 1000 mg of sodium, equal to the stored 1.0 g cumulative sodium retention.
- **Quote:** > A rise in serum aldosterone results in a net gain of approximately 1000 mg of sodium.
- **Reviewer note:** Direct match: 1000 mg = 1.0 g stated explicitly in the Cheung 2013 abstract.

### `maternal_respiratory.term_arterial_ph`  ·  Tier B  ·  stored: 7.44 dimensionless

- **Primary citation:** `templeton-1976-blood-gas`  (_evidence: secondary_)
- **Source reports:** Composite mean third-trimester arterial pH 7.46 (with PaCO2 26.6, HCO3 18.2) — a compensated respiratory alkalosis on the alkaline side.
- **Quote:** > The composite mean values were pH 7.46, arterial carbon dioxide pressure (PaCO2) 26.6 mmHg, arterial oxygen pressure 88.3 mmHg, and bicarbonate 18.2 mEq/L.
- **Reviewer note:** SECONDARY evidence; third-trimester mean pH 7.46 falls within stored range 7.42-7.46. Cohort studied at moderate altitude (lower PaCO2 than sea level), but pH is comparable.

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

## 🔍 not found — value not in fetched text (check table/figure in full PDF)  (130)

### `amniotic_fluid.afv_20w_ml`  ·  Tier A  ·  stored: 350.0 mL

- **Primary citation:** `brace-1989-amniotic-fluid`  (_evidence: abstract_)
- **Source reports:** Abstract does not report a 20-week AFV. Its only quantitative summary covers the 22-39 week window (mean 777 ml). The 20-week point would come from the nomogram, which is not in the abstract.
- **Reviewer note:** No 20-week value in abstract (covers 22-39 wk only). Requires fulltext nomogram.

### `amniotic_fluid.afv_peak_week`  ·  Tier A  ·  stored: 33.0 weeks

- **Primary citation:** `brace-1989-amniotic-fluid`  (_evidence: abstract_)
- **Source reports:** Abstract gives no gestational week of peak AFV. It states volume did not change significantly between 22 and 39 weeks, which does not support a distinct peak at week 33. The week-by-week nomogram is not in the abstract.
- **Reviewer note:** No peak-week figure in abstract; abstract states no significant change 22-39 wk. Need fulltext/nomogram to verify week 33.

### `amniotic_fluid.afv_term_ml`  ·  Tier A  ·  stored: 600.0 mL

- **Primary citation:** `brace-1989-amniotic-fluid`  (_evidence: abstract_)
- **Source reports:** Abstract reports no term-specific value; it averages 22-39 weeks as 777 ml with no significant change. A distinct decline to ~600 ml at term is not in the abstract (would require the nomogram).
- **Reviewer note:** No term-specific AFV in abstract; abstract reports flat 777 ml mean 22-39 wk. Term value requires fulltext nomogram.

### `fetal_circulation.ua_pi_baseline`  ·  Tier A  ·  stored: 1.5 dimensionless

- **Primary citation:** `acharya-2005-umbilical-pi`  (_evidence: abstract_)
- **Source reports:** Abstract describes constructing reference ranges/percentiles for UA-PI showing continuous reduction through the second half of pregnancy, but gives no numeric PI value for 16-20 weeks.
- **Reviewer note:** No numeric UA-PI figure (~1.5 at mid-T2) in the abstract; reference-range numbers are in tables/full text not available here.

### `fetal_circulation.ua_pi_term`  ·  Tier A  ·  stored: 0.85 dimensionless

- **Primary citation:** `acharya-2005-umbilical-pi`  (_evidence: abstract_)
- **Source reports:** Abstract reports a continuous reduction in UA-PI through the second half of pregnancy without plateau near term, but no numeric term PI value.
- **Reviewer note:** No numeric term UA-PI (~0.85) in the abstract; only qualitative description of the declining trend.

### `fetal_growth.ac_16w_mm`  ·  Tier A  ·  stored: 105.0 mm

- **Primary citation:** `buck-louis-2015-nichd-growth`  (_evidence: abstract_)
- **Reviewer note:** Abstract reports only EFW percentiles at 39w and the gestational week at which racial differences become detectable per biometric; no mm-by-week biometry value is in the abstract. Value lives in an uncaptured growth table.

### `fetal_growth.ac_20w_mm`  ·  Tier A  ·  stored: 152.0 mm

- **Primary citation:** `buck-louis-2015-nichd-growth`  (_evidence: abstract_)
- **Reviewer note:** Abstract reports only EFW percentiles at 39w and the gestational week at which racial differences become detectable per biometric; no mm-by-week biometry value is in the abstract. Value lives in an uncaptured growth table.

### `fetal_growth.ac_24w_mm`  ·  Tier A  ·  stored: 198.0 mm

- **Primary citation:** `buck-louis-2015-nichd-growth`  (_evidence: abstract_)
- **Reviewer note:** Abstract reports only EFW percentiles at 39w and the gestational week at which racial differences become detectable per biometric; no mm-by-week biometry value is in the abstract. Value lives in an uncaptured growth table.

### `fetal_growth.ac_28w_mm`  ·  Tier A  ·  stored: 240.0 mm

- **Primary citation:** `buck-louis-2015-nichd-growth`  (_evidence: abstract_)
- **Reviewer note:** Abstract reports only EFW percentiles at 39w and the gestational week at which racial differences become detectable per biometric; no mm-by-week biometry value is in the abstract. Value lives in an uncaptured growth table.

### `fetal_growth.ac_32w_mm`  ·  Tier A  ·  stored: 282.0 mm

- **Primary citation:** `buck-louis-2015-nichd-growth`  (_evidence: abstract_)
- **Reviewer note:** Abstract reports only EFW percentiles at 39w and the gestational week at which racial differences become detectable per biometric; no mm-by-week biometry value is in the abstract. Value lives in an uncaptured growth table.

### `fetal_growth.ac_36w_mm`  ·  Tier A  ·  stored: 322.0 mm

- **Primary citation:** `buck-louis-2015-nichd-growth`  (_evidence: abstract_)
- **Reviewer note:** Abstract reports only EFW percentiles at 39w and the gestational week at which racial differences become detectable per biometric; no mm-by-week biometry value is in the abstract. Value lives in an uncaptured growth table.

### `fetal_growth.ac_40w_mm`  ·  Tier A  ·  stored: 354.0 mm

- **Primary citation:** `buck-louis-2015-nichd-growth`  (_evidence: abstract_)
- **Reviewer note:** Abstract reports only EFW percentiles at 39w and the gestational week at which racial differences become detectable per biometric; no mm-by-week biometry value is in the abstract. Value lives in an uncaptured growth table.

### `fetal_growth.bpd_16w_mm`  ·  Tier A  ·  stored: 35.0 mm

- **Primary citation:** `buck-louis-2015-nichd-growth`  (_evidence: abstract_)
- **Reviewer note:** Abstract reports only EFW percentiles at 39w and the gestational week at which racial differences become detectable per biometric; no mm-by-week biometry value is in the abstract. Value lives in an uncaptured growth table.

### `fetal_growth.bpd_20w_mm`  ·  Tier A  ·  stored: 47.0 mm

- **Primary citation:** `buck-louis-2015-nichd-growth`  (_evidence: abstract_)
- **Reviewer note:** Abstract reports only EFW percentiles at 39w and the gestational week at which racial differences become detectable per biometric; no mm-by-week biometry value is in the abstract. Value lives in an uncaptured growth table.

### `fetal_growth.bpd_24w_mm`  ·  Tier A  ·  stored: 61.0 mm

- **Primary citation:** `buck-louis-2015-nichd-growth`  (_evidence: abstract_)
- **Reviewer note:** Abstract reports only EFW percentiles at 39w and the gestational week at which racial differences become detectable per biometric; no mm-by-week biometry value is in the abstract. Value lives in an uncaptured growth table.

### `fetal_growth.bpd_28w_mm`  ·  Tier A  ·  stored: 71.5 mm

- **Primary citation:** `buck-louis-2015-nichd-growth`  (_evidence: abstract_)
- **Reviewer note:** Abstract reports only EFW percentiles at 39w and the gestational week at which racial differences become detectable per biometric; no mm-by-week biometry value is in the abstract. Value lives in an uncaptured growth table.

### `fetal_growth.bpd_32w_mm`  ·  Tier A  ·  stored: 82.0 mm

- **Primary citation:** `buck-louis-2015-nichd-growth`  (_evidence: abstract_)
- **Reviewer note:** Abstract reports only EFW percentiles at 39w and the gestational week at which racial differences become detectable per biometric; no mm-by-week biometry value is in the abstract. Value lives in an uncaptured growth table.

### `fetal_growth.bpd_36w_mm`  ·  Tier A  ·  stored: 89.0 mm

- **Primary citation:** `buck-louis-2015-nichd-growth`  (_evidence: abstract_)
- **Reviewer note:** Abstract reports only EFW percentiles at 39w and the gestational week at which racial differences become detectable per biometric; no mm-by-week biometry value is in the abstract. Value lives in an uncaptured growth table.

### `fetal_growth.bpd_40w_mm`  ·  Tier A  ·  stored: 93.0 mm

- **Primary citation:** `buck-louis-2015-nichd-growth`  (_evidence: abstract_)
- **Reviewer note:** Abstract reports only EFW percentiles at 39w and the gestational week at which racial differences become detectable per biometric; no mm-by-week biometry value is in the abstract. Value lives in an uncaptured growth table.

### `fetal_growth.efw_16w_g`  ·  Tier A  ·  stored: 145.0 g

- **Primary citation:** `buck-louis-2015-nichd-growth`  (_evidence: abstract_)
- **Reviewer note:** Abstract reports EFW percentiles only at 39 weeks (race-stratified), not at this gestational week; the week-specific value is in an uncaptured growth table.

### `fetal_growth.efw_20w_g`  ·  Tier A  ·  stored: 331.0 g

- **Primary citation:** `buck-louis-2015-nichd-growth`  (_evidence: abstract_)
- **Reviewer note:** Abstract reports EFW percentiles only at 39 weeks (race-stratified), not at this gestational week; the week-specific value is in an uncaptured growth table.

### `fetal_growth.efw_24w_g`  ·  Tier A  ·  stored: 650.0 g

- **Primary citation:** `buck-louis-2015-nichd-growth`  (_evidence: abstract_)
- **Reviewer note:** Abstract reports EFW percentiles only at 39 weeks (race-stratified), not at this gestational week; the week-specific value is in an uncaptured growth table.

### `fetal_growth.efw_28w_g`  ·  Tier A  ·  stored: 1141.0 g

- **Primary citation:** `buck-louis-2015-nichd-growth`  (_evidence: abstract_)
- **Reviewer note:** Abstract reports EFW percentiles only at 39 weeks (race-stratified), not at this gestational week; the week-specific value is in an uncaptured growth table.

### `fetal_growth.efw_32w_g`  ·  Tier A  ·  stored: 1800.0 g

- **Primary citation:** `buck-louis-2015-nichd-growth`  (_evidence: abstract_)
- **Reviewer note:** Abstract reports EFW percentiles only at 39 weeks (race-stratified), not at this gestational week; the week-specific value is in an uncaptured growth table.

### `fetal_growth.efw_36w_g`  ·  Tier A  ·  stored: 2779.0 g

- **Primary citation:** `buck-louis-2015-nichd-growth`  (_evidence: abstract_)
- **Reviewer note:** Abstract reports EFW percentiles only at 39 weeks (race-stratified), not at this gestational week; the week-specific value is in an uncaptured growth table.

### `fetal_growth.efw_40w_g`  ·  Tier A  ·  stored: 3567.0 g

- **Primary citation:** `buck-louis-2015-nichd-growth`  (_evidence: abstract_)
- **Reviewer note:** Abstract gives 39w (not 40w) race-stratified 50th-percentile EFW; closest figure white 3505 g, vs stored 3567 g. Different gestational week and uncertain provenance (notes flag Hadlock 3619 g at 40w). Exact 40w pooled value not stated -> not_found.

### `fetal_growth.fl_16w_mm`  ·  Tier A  ·  stored: 21.0 mm

- **Primary citation:** `buck-louis-2015-nichd-growth`  (_evidence: abstract_)
- **Reviewer note:** Abstract reports only EFW percentiles at 39w and the gestational week at which racial differences become detectable per biometric; no mm-by-week biometry value is in the abstract. Value lives in an uncaptured growth table.

### `fetal_growth.fl_20w_mm`  ·  Tier A  ·  stored: 33.0 mm

- **Primary citation:** `buck-louis-2015-nichd-growth`  (_evidence: abstract_)
- **Reviewer note:** Abstract reports only EFW percentiles at 39w and the gestational week at which racial differences become detectable per biometric; no mm-by-week biometry value is in the abstract. Value lives in an uncaptured growth table.

### `fetal_growth.fl_24w_mm`  ·  Tier A  ·  stored: 44.0 mm

- **Primary citation:** `buck-louis-2015-nichd-growth`  (_evidence: abstract_)
- **Reviewer note:** Abstract reports only EFW percentiles at 39w and the gestational week at which racial differences become detectable per biometric; no mm-by-week biometry value is in the abstract. Value lives in an uncaptured growth table.

### `fetal_growth.fl_28w_mm`  ·  Tier A  ·  stored: 53.0 mm

- **Primary citation:** `buck-louis-2015-nichd-growth`  (_evidence: abstract_)
- **Reviewer note:** Abstract reports only EFW percentiles at 39w and the gestational week at which racial differences become detectable per biometric; no mm-by-week biometry value is in the abstract. Value lives in an uncaptured growth table.

### `fetal_growth.fl_32w_mm`  ·  Tier A  ·  stored: 62.0 mm

- **Primary citation:** `buck-louis-2015-nichd-growth`  (_evidence: abstract_)
- **Reviewer note:** Abstract reports only EFW percentiles at 39w and the gestational week at which racial differences become detectable per biometric; no mm-by-week biometry value is in the abstract. Value lives in an uncaptured growth table.

### `fetal_growth.fl_36w_mm`  ·  Tier A  ·  stored: 70.0 mm

- **Primary citation:** `buck-louis-2015-nichd-growth`  (_evidence: abstract_)
- **Reviewer note:** Abstract reports only EFW percentiles at 39w and the gestational week at which racial differences become detectable per biometric; no mm-by-week biometry value is in the abstract. Value lives in an uncaptured growth table.

### `fetal_growth.fl_40w_mm`  ·  Tier A  ·  stored: 76.0 mm

- **Primary citation:** `buck-louis-2015-nichd-growth`  (_evidence: abstract_)
- **Reviewer note:** Abstract reports only EFW percentiles at 39w and the gestational week at which racial differences become detectable per biometric; no mm-by-week biometry value is in the abstract. Value lives in an uncaptured growth table.

### `fetal_growth.hadlock_coefficient`  ·  Tier A  ·  stored: 1.3596 log10(g)

- **Primary citation:** `hadlock-1991-fetal-weight`  (_evidence: abstract_)
- **Source reports:** Abstract describes a regression-based in utero weight model but does not print the equation or its intercept; it states the resulting weight range (35 g at 10w to 3,619 g at 40w, SD +/-12.7%).
- **Quote:** > Regression analysis was used to develop an in utero fetal weight model from a population of 392 predominantly middle-class white patients … There was a gradual increase in fetal weight from 35 g at 10 weeks to 3,619 g at 40 weeks, with uniform variance of +/- 12.7% (1 standard deviation) throughout gestation.
- **Reviewer note:** The intercept 1.3596 is the published Hadlock-III formula constant but does not appear in the abstract; abstract confirms the model exists and its weight range but not the coefficient itself.

### `fetal_growth.hc_16w_mm`  ·  Tier A  ·  stored: 124.0 mm

- **Primary citation:** `buck-louis-2015-nichd-growth`  (_evidence: abstract_)
- **Reviewer note:** Abstract reports only EFW percentiles at 39w and the gestational week at which racial differences become detectable per biometric; no mm-by-week biometry value is in the abstract. Value lives in an uncaptured growth table.

### `fetal_growth.hc_20w_mm`  ·  Tier A  ·  stored: 175.0 mm

- **Primary citation:** `buck-louis-2015-nichd-growth`  (_evidence: abstract_)
- **Reviewer note:** Abstract reports only EFW percentiles at 39w and the gestational week at which racial differences become detectable per biometric; no mm-by-week biometry value is in the abstract. Value lives in an uncaptured growth table.

### `fetal_growth.hc_24w_mm`  ·  Tier A  ·  stored: 225.0 mm

- **Primary citation:** `buck-louis-2015-nichd-growth`  (_evidence: abstract_)
- **Reviewer note:** Abstract reports only EFW percentiles at 39w and the gestational week at which racial differences become detectable per biometric; no mm-by-week biometry value is in the abstract. Value lives in an uncaptured growth table.

### `fetal_growth.hc_28w_mm`  ·  Tier A  ·  stored: 267.0 mm

- **Primary citation:** `buck-louis-2015-nichd-growth`  (_evidence: abstract_)
- **Reviewer note:** Abstract reports only EFW percentiles at 39w and the gestational week at which racial differences become detectable per biometric; no mm-by-week biometry value is in the abstract. Value lives in an uncaptured growth table.

### `fetal_growth.hc_32w_mm`  ·  Tier A  ·  stored: 297.0 mm

- **Primary citation:** `buck-louis-2015-nichd-growth`  (_evidence: abstract_)
- **Reviewer note:** Abstract reports only EFW percentiles at 39w and the gestational week at which racial differences become detectable per biometric; no mm-by-week biometry value is in the abstract. Value lives in an uncaptured growth table.

### `fetal_growth.hc_36w_mm`  ·  Tier A  ·  stored: 322.0 mm

- **Primary citation:** `buck-louis-2015-nichd-growth`  (_evidence: abstract_)
- **Reviewer note:** Abstract reports only EFW percentiles at 39w and the gestational week at which racial differences become detectable per biometric; no mm-by-week biometry value is in the abstract. Value lives in an uncaptured growth table.

### `fetal_growth.hc_40w_mm`  ·  Tier A  ·  stored: 343.0 mm

- **Primary citation:** `buck-louis-2015-nichd-growth`  (_evidence: abstract_)
- **Reviewer note:** Abstract reports only EFW percentiles at 39w and the gestational week at which racial differences become detectable per biometric; no mm-by-week biometry value is in the abstract. Value lives in an uncaptured growth table.

### `maternal_blood.o2_hb_hill_coefficient_maternal`  ·  Tier A  ·  stored: 2.7 dimensionless

- **Primary citation:** `severinghaus-1979-o2-hb-dissociation`  (_evidence: abstract_)
- **Source reports:** Abstract gives the dissociation equation S = (((Po2^3 + 150 Po2)^-1 x 23,400) + 1)^-1 but never prints a Hill coefficient of 2.7; the ~2.7 exponent is inferred from the cubic numerator, not stated.
- **Reviewer note:** Hill coefficient 2.7 is derivable from the cubic form but no verbatim '2.7' appears in the available abstract.

### `maternal_blood.oxyhb_bohr_coefficient`  ·  Tier A  ·  stored: -0.48 log(mmHg)/pH

- **Primary citation:** `dash-bassingthwaighte-2010-o2-hb`  (_evidence: abstract_)
- **Source reports:** Dash & Bassingthwaighte 2010 abstract describes invertible Hill-type equations for HbO2/HbCO2 but does not print a Bohr coefficient value of -0.48.
- **Reviewer note:** No numeric Bohr coefficient (-0.48) appears in the available abstract; the rationale itself concedes Dash 2010 does not print the coefficient.

### `maternal_endocrine.cortisol_baseline_ug_per_dl`  ·  Tier A  ·  stored: 10.0 ug/dL

- **Primary citation:** `carr-1981-cortisol`  (_evidence: abstract_)
- **Source reports:** The abstract reports cortisol levels during pregnancy only (149 ng/mL = 14.9 ug/dL at 12 weeks, rising to 352 ng/mL at 26 weeks). No non-pregnant (baseline) cortisol value is given.
- **Reviewer note:** Carr 1981 abstract gives no non-pregnant baseline cortisol; earliest figure is 12-week pregnant (149 ng/mL = 14.9 ug/dL).

### `maternal_renal.baseline_gfr_ml_per_min`  ·  Tier A  ·  stored: 100.0 mL/min

- **Primary citation:** `conrad-2001-relaxin-gfr`  (_evidence: abstract_)
- **Source reports:** Abstract reports the percentage rise of GFR and RPF in pregnancy but gives no absolute non-pregnant GFR baseline value.
- **Quote:** > Glomerular filtration rate (GFR) and renal plasma flow (RPF) increase by 40-65% and 50-85%, respectively, during normal pregnancy in women.
- **Reviewer note:** Conrad 2001 abstract gives only percentage increases; the absolute non-pregnant baseline of 100 mL/min is not stated in the cached source.

### `maternal_renal.bun_term_mg_per_dl`  ·  Tier A  ·  stored: 8.0 mg/dL

- **Primary citation:** `cheung-lafayette-2013-renal`  (_evidence: abstract_)
- **Source reports:** Abstract notes a decrease in serum urea with the GFR rise but reports no numeric BUN value.
- **Quote:** > The glomerular filtration rate increases 50% with subsequent decrease in serum creatinine, urea, and uric acid values.
- **Reviewer note:** Abstract confirms urea falls in pregnancy but gives no numeric term BUN; stored 8 mg/dL not verifiable from abstract.

### `maternal_renal.plasma_creatinine_mg_per_dl_term`  ·  Tier A  ·  stored: 0.6 mg/dL

- **Primary citation:** `cheung-lafayette-2013-renal`  (_evidence: abstract_)
- **Source reports:** Abstract notes a decrease in serum creatinine with the GFR rise but reports no numeric creatinine value. The 0.5 mg/dL Table 1 figure cited in the rationale is from the fulltext, which is not cached.
- **Quote:** > The glomerular filtration rate increases 50% with subsequent decrease in serum creatinine, urea, and uric acid values.
- **Reviewer note:** Abstract confirms direction (creatinine falls) but no numeric term creatinine; specific 0.6 mg/dL not verifiable from abstract.

### `placental_endocrine.hcg_peak_miu_per_ml`  ·  Tier A  ·  stored: 100000.0 mIU/mL

- **Primary citation:** `cole-2010-hcg`  (_evidence: fulltext_)
- **Source reports:** Fulltext confirms hCG peaks at 10 weeks of gestation, but does not state the peak maternal serum concentration in mIU/mL. The only mIU/mL figures in the text concern pituitary hCG during the menstrual cycle (mean 1.54 mIU/mL); Tables 2/3 give term-pregnancy total-hCG ranges in ng/ml (0.21-173 ng/ml; 1.86-1308 ng/ml), not the ~50,000-200,000 mIU/mL peak.
- **Reviewer note:** Confirm the peak hCG concentration (50,000-200,000 mIU/mL) is not in the captured fulltext (lives in figures/tables not extracted as text); peak value appears sourced from general reproductive endocrinology, not an explicit number in this paper.

### `placental_structure.cord_length_term_cm`  ·  Tier A  ·  stored: 55 cm

- **Primary citation:** `naeye-1985-cord-length`  (_evidence: abstract_)
- **Source reports:** Naeye abstract reports analysis of cord length in 35,779 neonates and that the normal range is large, but states no mean (~55 cm) or short/long thresholds (35/80 cm).
- **Reviewer note:** Abstract confirms the cohort but gives no numeric mean or range; central 55 cm and 35-80 cm bounds not in available text.

### `amniotic_fluid.af_creatinine_term_mg_per_dl`  ·  Tier B  ·  stored: 2.0 mg/dL

- **Primary citation:** `underwood-2005-amniotic-fluid`  (_evidence: abstract_)
- **Source reports:** Abstract is a generic review summary with no numeric values; it does not report an AF creatinine concentration at term.
- **Reviewer note:** Underwood 2005 abstract gives no numbers. Term AF creatinine 2 mg/dL would require the review fulltext.

### `amniotic_fluid.af_glucose_term_mmol_per_l`  ·  Tier B  ·  stored: 0.5 mmol/L

- **Primary citation:** `underwood-2005-amniotic-fluid`  (_evidence: abstract_)
- **Source reports:** Abstract is a generic review summary with no numeric values; it does not report an AF glucose concentration at term.
- **Reviewer note:** Underwood 2005 abstract gives no numbers. Term AF glucose 0.5 mmol/L would require the review fulltext.

### `amniotic_fluid.af_lactate_term_mmol_per_l`  ·  Tier B  ·  stored: 4 mmol/L

- **Primary citation:** `underwood-2005-amniotic-fluid`  (_evidence: abstract_)
- **Source reports:** Abstract is a generic review summary with no numeric values; it does not report an AF lactate concentration at term.
- **Reviewer note:** Underwood 2005 abstract gives no numbers. Term AF lactate 4 mmol/L would require the review fulltext.

### `amniotic_fluid.af_osmolality_term_mosm_per_kg`  ·  Tier B  ·  stored: 260 mOsm/kg

- **Primary citation:** `underwood-2005-amniotic-fluid`  (_evidence: abstract_)
- **Source reports:** Abstract is a generic review summary with no numeric values; it does not report an AF osmolality at term.
- **Reviewer note:** Underwood 2005 abstract gives no numbers. Term AF osmolality 260 mOsm/kg would require the review fulltext.

### `amniotic_fluid.afv_early_baseline_ml`  ·  Tier B  ·  stored: 100.0 mL

- **Primary citation:** `brace-1989-amniotic-fluid`  (_evidence: abstract_)
- **Source reports:** Abstract states the data span 8 to 43 weeks but provides no early-pregnancy (~12-14 wk) volume figure. The 50-200 ml early baseline is not quantified in the abstract.
- **Reviewer note:** No early-pregnancy AFV figure in abstract. Requires fulltext nomogram to verify ~100 ml baseline.

### `fetal_circulation.combined_ventricular_output_term_ml_per_min_per_kg`  ·  Tier B  ·  stored: 450.0 mL/min/kg

- **Primary citation:** `sutton-1991-fetal-cardiac`  (_evidence: abstract_)
- **Source reports:** Sutton 1991 abstract computes CVO as the sum of aortic and pulmonary artery flows and expresses lung/foramen flows as fractions of CVO, but reports no absolute per-kg CVO value (mL/min/kg).
- **Reviewer note:** Abstract gives CVO only as a denominator for fraction calculations; no ~450 mL/min/kg numeric value present.

### `fetal_circulation.fhr_baseline_bpm`  ·  Tier B  ·  stored: 170.0 bpm

- **Primary citation:** `von-steinburg-2013-fhr`  (_evidence: fulltext_)
- **Source reports:** This study analyzed CTG tracings collected between 20 and 42 weeks; it reports the highest mean FHR baseline at <28 weeks (140.8-141.9 bpm) and a normal range of 120-160 bpm. It does not cover the first-trimester (~weeks 9-10) peak that the stored 170 bpm represents.
- **Reviewer note:** Source data start at 20 weeks; the first-trimester ~170 bpm peak is outside this study and not present in the text.

### `fetal_circulation.mca_pi_baseline`  ·  Tier B  ·  stored: 1.5 dimensionless

- **Primary citation:** `mari-1995-mca-pi`  (_evidence: abstract_)
- **Source reports:** Abstract reports a parabolic (bell-shaped) MCA-PI pattern with higher values at 25-30 weeks, but provides no numeric PI value for ~20 weeks.
- **Reviewer note:** No numeric early-T2 MCA-PI (~1.5) in the abstract; only the parabolic-pattern description.

### `fetal_circulation.right_ventricular_output_fraction_term`  ·  Tier B  ·  stored: 0.6 dimensionless

- **Primary citation:** `sutton-1991-fetal-cardiac`  (_evidence: abstract_)
- **Source reports:** Sutton 1991 abstract reports lung flow (22% of CVO) and foramen ovale flow (17-31% of CVO) but does not report the RV share of CVO; no ~60% RV-output fraction is stated.
- **Reviewer note:** Abstract does not state RV vs LV output split; stored 0.60 RV fraction not verifiable from available text.

### `fetal_circulation.umbilical_vein_flow_per_kg_term_ml_per_min_per_kg`  ·  Tier B  ·  stored: 80.0 mL/min/kg

- **Primary citation:** `kiserud-2001-umbilical-vein`  (_evidence: abstract_)
- **Source reports:** Abstract reports shunt fractions and growth associations only; no weight-normalised UV flow (mL/min/kg) value is given.
- **Reviewer note:** No mL/min/kg figure in the abstract; the ~80 mL/min/kg term value is not in available text.

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

### `maternal_cardiovascular.baseline_cardiac_output_l_per_min`  ·  Tier B  ·  stored: 4.6 L/min

- **Primary citation:** `mahendru-2014-cardiac-output`  (_evidence: abstract_)
- **Source reports:** Abstract reports only the change in cardiac output (Δ0.6 l/min by T2), not an absolute pre-conception baseline.
- **Reviewer note:** Abstract gives deltas, not the absolute pre-conception CO; baseline 4.6 not stated in available text.

### `maternal_cardiovascular.baseline_heart_rate_bpm`  ·  Tier B  ·  stored: 70.0 bpm

- **Primary citation:** `mahendru-2014-cardiac-output`  (_evidence: abstract_)
- **Source reports:** Abstract reports HR change (Δ13±11 bpm) only; no absolute pre-conception baseline HR value.
- **Reviewer note:** Only HR delta in abstract; absolute baseline 70 bpm not stated.

### `maternal_cardiovascular.baseline_map_mmhg`  ·  Tier B  ·  stored: 85.0 mmHg

- **Primary citation:** `mahendru-2014-cardiac-output`  (_evidence: abstract_)
- **Source reports:** Abstract reports systolic BP changes (deltas) only; no absolute pre-conception MAP value given.
- **Reviewer note:** No absolute MAP in abstract; only delta brachial/central systolic. Baseline 85 unverifiable from text.

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

### `maternal_cardiovascular.cardiac_output_t3_l_per_min`  ·  Tier B  ·  stored: 6.5 L/min

- **Primary citation:** `mahendru-2014-cardiac-output`  (_evidence: abstract_)
- **Source reports:** Abstract gives only the CO change; no absolute T3 CO mean.
- **Reviewer note:** Absolute T3 CO (6.5) not in abstract.

### `maternal_cardiovascular.map_nadir_drop_mmhg`  ·  Tier B  ·  stored: 8.0 mmHg

- **Primary citation:** `mahendru-2014-cardiac-output`  (_evidence: abstract_)
- **Source reports:** Abstract reports systolic BP drops (brachial 4±7, central 7±7 mmHg) in early pregnancy, not a MAP nadir drop.
- **Reviewer note:** Stored quantity is MAP drop (8 mmHg); abstract reports systolic-BP deltas, a different quantity. MAP drop not stated.

### `maternal_cardiovascular.map_nadir_week`  ·  Tier B  ·  stored: 22.0 weeks

- **Primary citation:** `mahendru-2014-cardiac-output`  (_evidence: abstract_)
- **Source reports:** Abstract says greatest BP reduction occurred in early pregnancy and PVR nadir by T2; no explicit MAP-nadir week of 22.
- **Reviewer note:** No explicit week-22 MAP nadir in abstract; timing described qualitatively only.

### `maternal_cardiovascular.term_heart_rate_bpm`  ·  Tier B  ·  stored: 85.0 bpm

- **Primary citation:** `mahendru-2014-cardiac-output`  (_evidence: abstract_)
- **Source reports:** Abstract reports HR increased maximally by T3 by Δ13±11 bpm; no absolute term HR (~85 bpm) is stated.
- **Reviewer note:** Term 85 bpm is baseline+delta inference; abstract gives only the delta, not absolute term HR.

### `maternal_endocrine.cbg_term_mg_per_l`  ·  Tier B  ·  stored: 70 mg/L

- **Primary citation:** `carr-1981-cortisol`  (_evidence: abstract_)
- **Source reports:** The Carr 1981 abstract discusses ACTH and total cortisol only; it never mentions cortisol-binding globulin (CBG) or transcortin and gives no CBG concentration.
- **Reviewer note:** CBG not mentioned anywhere in the Carr 1981 abstract; no value to compare against stored 70 mg/L.

### `maternal_endocrine.homa_ir_baseline`  ·  Tier B  ·  stored: 2.0 dimensionless

- **Primary citation:** `catalano-1991-insulin-sensitivity`  (_evidence: abstract_)
- **Source reports:** Catalano 1991 abstract measures insulin sensitivity via hyperinsulinemic-euglycemic clamp (glucose infusion rate) and insulin release via IVGTT. It reports no HOMA-IR value and no pre-pregnancy baseline HOMA-IR figure.
- **Reviewer note:** Abstract reports clamp-based insulin sensitivity, not HOMA-IR; no baseline HOMA-IR value stated.

### `maternal_renal.filtration_fraction_term`  ·  Tier B  ·  stored: 0.18 dimensionless

- **Primary citation:** `cheung-lafayette-2013-renal`  (_evidence: abstract_)
- **Source reports:** Cheung 2013 abstract does not mention filtration fraction or give any numeric FF value.
- **Reviewer note:** No filtration-fraction data in the Cheung 2013 abstract; stored 0.18 not verifiable from cached source.

### `maternal_renal.gfr_peak_week`  ·  Tier B  ·  stored: 16.0 weeks

- **Primary citation:** `conrad-2001-relaxin-gfr`  (_evidence: abstract_)
- **Source reports:** Abstract describes mechanisms of hyperfiltration but gives no gestational timing for the GFR peak.
- **Reviewer note:** No week-of-peak GFR information in the Conrad 2001 abstract; Dunlop 1981 (also cited in rationale) is not the primary citation here.

### `maternal_renal.plasma_uric_acid_nadir_mg_per_dl`  ·  Tier B  ·  stored: 3.0 mg/dL

- **Primary citation:** `cheung-lafayette-2013-renal`  (_evidence: abstract_)
- **Source reports:** Abstract notes uric acid decreases with the GFR rise but gives no numeric nadir value or timing.
- **Quote:** > The glomerular filtration rate increases 50% with subsequent decrease in serum creatinine, urea, and uric acid values.
- **Reviewer note:** Abstract confirms uric acid falls but no numeric mid-pregnancy nadir; stored 3.0 mg/dL not verifiable from abstract.

### `maternal_renal.plasma_uric_acid_term_mg_per_dl`  ·  Tier B  ·  stored: 4.5 mg/dL

- **Primary citation:** `cheung-lafayette-2013-renal`  (_evidence: abstract_)
- **Source reports:** Abstract notes a pregnancy decrease in uric acid but provides no numeric term value nor any third-trimester rebound figure.
- **Quote:** > The glomerular filtration rate increases 50% with subsequent decrease in serum creatinine, urea, and uric acid values.
- **Reviewer note:** No numeric term uric acid in the Cheung 2013 abstract; stored 4.5 mg/dL not verifiable from cached source.

### `maternal_renal.renal_plasma_flow_baseline_ml_per_min`  ·  Tier B  ·  stored: 600.0 mL/min

- **Primary citation:** `dunlop-1981-renal-plasma-flow`  (_evidence: abstract_)
- **Source reports:** Abstract reports ERPF increased 80% in early pregnancy but provides no absolute non-pregnant ERPF value in mL/min.
- **Quote:** > Compared with non-pregnant values, ERPF increased by 80 percent during early pregnancy but fell significantly from this new level during the third trimester.
- **Reviewer note:** Abstract gives percentage change only; absolute baseline RPF of 600 mL/min not stated in cached source.

### `maternal_renal.urinary_protein_excretion_term_mg_per_24h`  ·  Tier B  ·  stored: 150.0 mg/24h

- **Primary citation:** `cheung-lafayette-2013-renal`  (_evidence: abstract_)
- **Source reports:** Cheung 2013 abstract does not mention urinary protein excretion or proteinuria thresholds.
- **Reviewer note:** No urinary protein data in the Cheung 2013 abstract; stored 150 mg/24h not verifiable from cached source.

### `maternal_respiratory.vco2_term_ml_per_min`  ·  Tier B  ·  stored: 250.0 mL/min

- **Primary citation:** `lomauro-aliverti-2015-respiratory`  (_evidence: fulltext_)
- **Source reports:** Fulltext reports basal metabolic rate (and O2 consumption) rises by up to 14%/21% but gives no CO2-production (VCO2) value, absolute or percent, so the stored 250 mL/min term VCO2 is not present.
- **Reviewer note:** No CO2-production (VCO2) figure in available fulltext; only O2 consumption/metabolic-rate percentages are given.

### `placental_endocrine.hcg_term_miu_per_ml`  ·  Tier B  ·  stored: 10000.0 mIU/mL

- **Primary citation:** `cole-2010-hcg`  (_evidence: fulltext_)
- **Source reports:** Fulltext does not state a term maternal serum hCG concentration of ~10,000 mIU/mL. Term-pregnancy hCG data in Tables 2/3 are described as ng/ml ranges (0.21-173 ng/ml across women) and the underlying per-week table values are not present in the captured text.
- **Reviewer note:** Confirm the term hCG figure (~5,000-20,000 mIU/mL) is absent from the captured fulltext; it appears inferred from the general decline-from-peak narrative rather than an explicit number.

### `placental_endocrine.hpl_baseline_ug_per_ml`  ·  Tier B  ·  stored: 0.0 ug/mL

- **Primary citation:** `handwerger-2010-hpl`  (_evidence: abstract_)
- **Source reports:** The abstract is qualitative and states no numeric non-pregnant baseline concentration. The operationally-zero baseline rests on hPL being exclusively placental, which the abstract supports descriptively but without a number or assay sensitivity figure.
- **Reviewer note:** Confirm the abstract gives no numeric baseline; the 0 (below ~0.1 ug/mL assay sensitivity) value is an operational inference, not an explicit figure in this source.

### `placental_endocrine.hpl_term_ug_per_ml`  ·  Tier B  ·  stored: 7.0 ug/mL

- **Primary citation:** `handwerger-2010-hpl`  (_evidence: abstract_)
- **Source reports:** The abstract is qualitative and describes hPL's physiologic roles (growth/metabolism in mother and fetus). It states no numeric term concentration in ug/mL.
- **Reviewer note:** Confirm the abstract carries no numeric hPL concentration; the ~5-10 ug/mL term value would need the full review text or another source.

### `placental_endocrine.leptin_term_ng_per_ml`  ·  Tier B  ·  stored: 30 ng/mL

- **Primary citation:** `hardie-1997-leptin`  (_evidence: abstract_)
- **Source reports:** The abstract reports leptin was elevated throughout gestation (P<0.05), especially in the second trimester, and fell sharply post-partum, but it gives no numeric leptin concentration (ng/mL) at term.
- **Reviewer note:** Confirm the abstract carries only directional/statistical findings and no numeric term leptin value; the ~30 ng/mL central value would require the paper's tables/figures.

### `placental_endocrine.relaxin_t1_ng_per_ml`  ·  Tier B  ·  stored: 1.0 ng/mL

- **Primary citation:** `conrad-2001-relaxin-gfr`  (_evidence: abstract_)
- **Source reports:** The abstract (a renal-vasodilation/hyperfiltration review) identifies relaxin as the major pregnancy hormone driving renal changes and describes its downstream mediators (ET, NO), but reports no serum relaxin concentration. It gives GFR/RPF increases (40-65% and 50-85%), not a relaxin level.
- **Reviewer note:** Confirm the abstract states no relaxin concentration; the ~1 ng/mL first-trimester value is not supported by this mechanistic-review abstract and may need a dedicated relaxin assay source.

### `placental_gas_exchange.maternal_intervillous_po2_mmhg`  ·  Tier B  ·  stored: 50.0 mmHg

- **Primary citation:** `carter-2009-placental-development`  (_evidence: abstract_)
- **Source reports:** Abstract reviews factors affecting placental oxygen transfer in general/evolutionary terms; it does not state a maternal intervillous-space PO2 value.
- **Reviewer note:** No PO2 figure in abstract; ~50 mmHg claim not verifiable from available text. Fulltext unavailable.

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

### `placental_glucose.glucose_glut3_km_mmol_per_l`  ·  Tier B  ·  stored: 1.5 mmol/L

- **Primary citation:** `baumann-2002-glut3`  (_evidence: abstract_)
- **Source reports:** The Baumann 2002 abstract reviews placental glucose transfer; it states only GLUT1 protein has been identified in the syncytium and gives no numeric Km for GLUT3.
- **Quote:** > only GLUT1 protein has been identified in the syncytium, where its distribution is asymmetric.
- **Reviewer note:** Abstract reports no GLUT3 Km figure; it actually emphasizes GLUT1. Stored '~1-2 mmol/L' Km is not present in the available text.

### `placental_glucose.maternal_fetal_glucose_gradient_term_mmol_per_l`  ·  Tier B  ·  stored: 1.2 mmol/L

- **Primary citation:** `illsley-2000-glut1`  (_evidence: abstract_)
- **Source reports:** The Illsley 2000 abstract does not state a maternal-fetal glucose concentration gradient or a fetal/maternal glucose ratio; it discusses transporter biology qualitatively.
- **Reviewer note:** Abstract-only; no numeric gradient (~1.0-1.5 mmol/L) or 70-75% ratio appears in the available text.

### `placental_glucose.net_glucose_flux_term_mg_per_kg_per_min`  ·  Tier B  ·  stored: 5.0 mg/kg/min

- **Primary citation:** `illsley-2000-glut1`  (_evidence: abstract_)
- **Source reports:** The abstract mentions 'maternal-fetal flux of glucose' only qualitatively; it reports no numeric net trans-placental glucose flux (e.g. 4-7 mg/kg/min).
- **Quote:** > in diabetic pregnancies increases in basal GLUT1 expression and activity have been observed, with significant consequences for the maternal-fetal flux of glucose.
- **Reviewer note:** Abstract references maternal-fetal glucose flux qualitatively but gives no mg/kg/min value. Stored 4-7 mg/kg/min not in available text.

### `placental_structure.initial_area_m2`  ·  Tier B  ·  stored: 0.5 m^2

- **Primary citation:** `mayhew-2014-placental-morphometry`  (_evidence: abstract_)
- **Source reports:** Morphomics review abstract describes methodology and 3D quantification but reports no early-gestation villous surface-area figure.
- **Reviewer note:** Abstract is a methodological 'omics' review; no numeric villous surface area present.

### `placental_structure.membrane_thickness_um`  ·  Tier B  ·  stored: 4.5 micrometres

- **Primary citation:** `mayhew-2014-placental-morphometry`  (_evidence: abstract_)
- **Source reports:** Morphomics review abstract; reports no villous-membrane thickness value.
- **Reviewer note:** No numeric membrane-thickness figure in the abstract; underlying value attributed to Mayhew 1986, not this cached source.

### `placental_structure.placenta_to_fetus_weight_ratio_term`  ·  Tier B  ·  stored: 0.14 fraction

- **Primary citation:** `burton-2010-placental-development`  (_evidence: abstract_)
- **Source reports:** Burton 'What is the placenta?' abstract; qualitative organ description, reports no placental-to-fetal weight ratio.
- **Reviewer note:** No fetoplacental ratio value in the abstract; stored value is a derived/computed quantity.

### `placental_structure.term_area_m2`  ·  Tier B  ·  stored: 11.5 m^2

- **Primary citation:** `mayhew-2014-placental-morphometry`  (_evidence: abstract_)
- **Source reports:** Morphomics review abstract; no term villous surface-area figure present.
- **Reviewer note:** Abstract does not state the ~11-13 m^2 term surface area; value would require fulltext or the cited primary sources.

### `placental_structure.term_weight_g`  ·  Tier B  ·  stored: 470.0 g

- **Primary citation:** `mayhew-2014-placental-morphometry`  (_evidence: abstract_)
- **Source reports:** Morphomics review abstract; reports no placental mass value.
- **Reviewer note:** Rationale itself calls ~470 g a 'canonical clinical-pathology figure'; not present in this abstract.

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

### `maternal_cardiovascular.baseline_stroke_volume_ml`  ·  Tier C  ·  stored: 65.0 mL

- **Primary citation:** `mahendru-2014-cardiac-output`  (_evidence: abstract_)
- **Source reports:** Abstract does not report an absolute stroke-volume value; baseline SV is a CO/HR-derived estimate.
- **Reviewer note:** No SV figure in abstract; stored 65 mL is a derivation per rationale.

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

### `placental_endocrine.placental_gh_term_ng_per_ml`  ·  Tier C  ·  stored: 14 ng/mL

- **Primary citation:** `eriksson-1989-placental-gh`  (_evidence: abstract_)
- **Source reports:** The abstract describes the qualitative shift from episodic pituitary GH to continuous non-pulsatile placental GH-variant secretion in late pregnancy (first seen at 17 weeks), but reports no numeric term placental-GH concentration in ng/mL.
- **Reviewer note:** Confirm the abstract gives only the secretion-pattern finding and no numeric concentration; the ~10-20 ng/mL term value needs the full text or another source.

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

### `placental_gas_exchange.maternal_fetal_pco2_gradient_term_mmhg`  ·  Tier C  ·  stored: 10.0 mmHg

- **Primary citation:** `mayhew-1986-gas-diffusion`  (_evidence: abstract_)
- **Source reports:** Abstract is a morphometric oxygen-diffusion model; it does not discuss CO2 or report any maternal-fetal PCO2 gradient. Rationale itself attributes the value to 'standard fetal-physiology references.'
- **Reviewer note:** Cited abstract is O2-only; no PCO2 gradient stated. Fulltext unavailable.

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

### `placental_structure.spiral_artery_count`  ·  Tier C  ·  stored: 100 count

- **Primary citation:** `pijnenborg-2006-spiral-artery`  (_evidence: abstract_)
- **Source reports:** Pijnenborg 'facts and controversies' abstract discusses spiral-artery remodelling qualitatively; reports no count of spiral arteries.
- **Reviewer note:** No numeric spiral-artery count in the abstract.

### `placental_structure.spiral_artery_diameter_term_mm`  ·  Tier C  ·  stored: 2.5 mm

- **Primary citation:** `pijnenborg-2006-spiral-artery`  (_evidence: abstract_)
- **Source reports:** Pijnenborg abstract describes spiral arteries being remodelled into highly dilated vessels (qualitative); reports no diameter in mm.
- **Reviewer note:** Abstract qualitatively notes dilation but gives no numeric diameter.

### `placental_structure.syncytiotrophoblast_thickness_term_um`  ·  Tier C  ·  stored: 4 um

- **Primary citation:** `mayhew-2014-placental-morphometry`  (_evidence: abstract_)
- **Source reports:** Morphomics review abstract; reports no syncytiotrophoblast thickness figure.
- **Reviewer note:** No numeric syncytial-layer thickness in the abstract.

### `placental_structure.villous_capillary_length_total_km_term`  ·  Tier C  ·  stored: 300.0 km

- **Primary citation:** `mayhew-2014-placental-morphometry`  (_evidence: abstract_)
- **Source reports:** Morphomics review abstract; reports no total villous-capillary length figure.
- **Reviewer note:** No numeric capillary-length figure in the abstract.

### `maternal_blood.fetal_microchimerism_baseline_cells_per_ml`  ·  Tier D  ·  stored: 0.0 cells/mL

- **Primary citation:** `bianchi-1996-microchimerism`  (_evidence: abstract_)
- **Source reports:** Bianchi 1996 abstract is qualitative ('rare nucleated fetal cells circulate within maternal blood') and reports detection rates by PCR; it gives no cells/mL concentration.
- **Reviewer note:** No cells/mL concentration in the abstract; Tier D hypothesis-only value cannot be verified against the source text.

### `maternal_blood.fetal_microchimerism_term_cells_per_ml`  ·  Tier D  ·  stored: 1.0 cells/mL

- **Primary citation:** `bianchi-1996-microchimerism`  (_evidence: abstract_)
- **Source reports:** Bianchi 1996 abstract is qualitative ('rare nucleated fetal cells circulate within maternal blood') and reports detection rates by PCR; it gives no cells/mL concentration.
- **Reviewer note:** No cells/mL concentration in the abstract; Tier D hypothesis-only value cannot be verified against the source text.

## ⬜ no source — book / paywalled / no abstract retrieved  (40)

### `maternal_renal.gfr_first_trimester_ml_per_min`  ·  Tier A  ·  stored: 135.0 mL/min

- **Primary citation:** `davison-hytten-1974-gfr`  (_evidence: none_)
- **Reviewer note:** Davison & Hytten 1974 cached with evidence=none (no abstract/fulltext); first-trimester GFR figure not verifiable from cached source.

### `placental_endocrine.estradiol_term_ng_per_ml`  ·  Tier A  ·  stored: 14.0 ng/mL

- **Primary citation:** `tulchinsky-1972-steroids`  (_evidence: none_)
- **Reviewer note:** Tulchinsky 1972 has no cached text (evidence=none). Reviewer should verify the ~8-25 ng/mL term estradiol value against the primary paper.

### `placental_endocrine.estriol_term_ng_per_ml`  ·  Tier A  ·  stored: 10.0 ng/mL

- **Primary citation:** `tulchinsky-1972-steroids`  (_evidence: none_)
- **Reviewer note:** Tulchinsky 1972 has no cached text (evidence=none). Reviewer should verify the ~6-20 ng/mL term estriol value against the primary paper.

### `placental_endocrine.progesterone_term_ng_per_ml`  ·  Tier A  ·  stored: 150.0 ng/mL

- **Primary citation:** `tulchinsky-1972-steroids`  (_evidence: none_)
- **Reviewer note:** Tulchinsky 1972 has no cached abstract/fulltext (evidence=none). Human reviewer should retrieve the primary paper to verify the ~150 ng/mL term progesterone value.

### `maternal_blood.folate_term_ng_per_ml`  ·  Tier B  ·  stored: 5 ng/mL

- **Primary citation:** `hytten-chamberlain-1980-blood-volume`  (_evidence: none_)
- **Reviewer note:** Hytten & Chamberlain 1980 is a textbook; no abstract or fulltext cached, cannot verify the figure.

### `maternal_blood.haemoglobin_baseline_g_per_dl`  ·  Tier B  ·  stored: 13.5 g/dL

- **Primary citation:** `hytten-chamberlain-1980-blood-volume`  (_evidence: none_)
- **Reviewer note:** Hytten & Chamberlain 1980 is a textbook; no abstract or fulltext cached, cannot verify the figure.

### `maternal_cardiovascular.baseline_svr_dyn_s_cm5`  ·  Tier B  ·  stored: 1300.0 dyn*s/cm^5

- **Primary citation:** `sanghavi-rutherford-2014-cardio-review`  (_evidence: none_)
- **Reviewer note:** Primary source (Sanghavi & Rutherford 2014) has no cached abstract/fulltext (evidence=none); value cannot be checked against text.

### `maternal_cardiovascular.lv_mass_baseline_g`  ·  Tier B  ·  stored: 130.0 g

- **Primary citation:** `sanghavi-rutherford-2014-cardio-review`  (_evidence: none_)
- **Reviewer note:** Primary source (Sanghavi & Rutherford 2014) has no cached abstract/fulltext (evidence=none); value cannot be checked against text.

### `maternal_cardiovascular.lv_mass_term_g`  ·  Tier B  ·  stored: 180.0 g

- **Primary citation:** `sanghavi-rutherford-2014-cardio-review`  (_evidence: none_)
- **Reviewer note:** Primary source (Sanghavi & Rutherford 2014) has no cached abstract/fulltext (evidence=none); value cannot be checked against text.

### `maternal_cardiovascular.peak_excess_stroke_volume_ml`  ·  Tier B  ·  stored: 15.0 mL

- **Primary citation:** `sanghavi-rutherford-2014-cardio-review`  (_evidence: none_)
- **Reviewer note:** Primary source (Sanghavi & Rutherford 2014) has no cached abstract/fulltext (evidence=none); value cannot be checked against text.

### `maternal_cardiovascular.pvr_term_dyn_s_cm5`  ·  Tier B  ·  stored: 80.0 dyn·s·cm^-5

- **Primary citation:** `sanghavi-rutherford-2014-cardio-review`  (_evidence: none_)
- **Reviewer note:** Primary source (Sanghavi & Rutherford 2014) has no cached abstract/fulltext (evidence=none); value cannot be checked against text.

### `maternal_cardiovascular.svr_nadir_dyn_s_cm5`  ·  Tier B  ·  stored: 750.0 dyn·s·cm^-5

- **Primary citation:** `sanghavi-rutherford-2014-cardio-review`  (_evidence: none_)
- **Reviewer note:** Primary source (Sanghavi & Rutherford 2014) has no cached abstract/fulltext (evidence=none); value cannot be checked against text.

### `maternal_cardiovascular.term_svr_dyn_s_cm5`  ·  Tier B  ·  stored: 980.0 dyn*s/cm^5

- **Primary citation:** `sanghavi-rutherford-2014-cardio-review`  (_evidence: none_)
- **Reviewer note:** Primary source (Sanghavi & Rutherford 2014) has no cached abstract/fulltext (evidence=none); value cannot be checked against text.

### `maternal_endocrine.aldosterone_term_ng_per_dl`  ·  Tier B  ·  stored: 40.0 ng/dL

- **Primary citation:** `wilson-1980-renin-aldosterone`  (_evidence: none_)
- **Reviewer note:** Wilson 1980 has no cached abstract or fulltext (evidence=none).

### `maternal_endocrine.free_t4_term_ng_per_dl`  ·  Tier B  ·  stored: 0.9 ng/dL

- **Primary citation:** `glinoer-1997-thyroid`  (_evidence: none_)
- **Reviewer note:** Glinoer 1997 has no cached abstract or fulltext (book/review, evidence=none).

### `maternal_endocrine.prolactin_term_ng_per_ml`  ·  Tier B  ·  stored: 200.0 ng/mL

- **Primary citation:** `tyson-1972-prolactin`  (_evidence: none_)
- **Reviewer note:** Tyson 1972 has no cached abstract or fulltext (evidence=none).

### `maternal_endocrine.renin_term_ng_per_ml_per_h`  ·  Tier B  ·  stored: 12 ng/mL/h

- **Primary citation:** `wilson-1980-renin-aldosterone`  (_evidence: none_)
- **Reviewer note:** Wilson 1980 has no cached abstract or fulltext (evidence=none).

### `maternal_endocrine.tsh_t1_miu_per_l`  ·  Tier B  ·  stored: 0.6 mIU/L

- **Primary citation:** `glinoer-1997-thyroid`  (_evidence: none_)
- **Reviewer note:** Glinoer 1997 has no cached abstract or fulltext (evidence=none).

### `maternal_endocrine.tsh_term_miu_per_l`  ·  Tier B  ·  stored: 2.0 mIU/L

- **Primary citation:** `glinoer-1997-thyroid`  (_evidence: none_)
- **Reviewer note:** Glinoer 1997 has no cached abstract or fulltext (evidence=none).

### `maternal_respiratory.inspiratory_capacity_term_l`  ·  Tier B  ·  stored: 2.7 L

- **Primary citation:** `crapo-1996-pregnancy-respiratory`  (_evidence: none_)
- **Reviewer note:** Primary citation Crapo 1996 is a book chapter with no abstract/fulltext cached (evidence none); cannot verify the 2.7 L term inspiratory capacity.

### `maternal_respiratory.tidal_volume_ml_term`  ·  Tier B  ·  stored: 680.0 mL

- **Primary citation:** `crapo-1996-pregnancy-respiratory`  (_evidence: none_)
- **Reviewer note:** Primary citation Crapo 1996 is a book chapter with no abstract/fulltext cached (evidence none); cannot verify the 680 mL term tidal volume.

### `maternal_respiratory.tlc_term_l`  ·  Tier B  ·  stored: 5.0 L

- **Primary citation:** `crapo-1996-pregnancy-respiratory`  (_evidence: none_)
- **Reviewer note:** Primary citation Crapo 1996 is a book chapter with no abstract/fulltext cached (evidence none); cannot verify the 5.0 L term TLC. (LoMauro review fulltext states TLC stays stable/constant but gives no absolute liters.)

### `placental_endocrine.estradiol_baseline_ng_per_ml`  ·  Tier B  ·  stored: 0.1 ng/mL

- **Primary citation:** `tulchinsky-1972-steroids`  (_evidence: none_)
- **Reviewer note:** Tulchinsky 1972 has no cached text (evidence=none); rationale also cites O'Leary 1991. Reviewer should verify the mid-luteal ~0.05-0.25 ng/mL baseline against an appropriate non-pregnant source.

### `placental_endocrine.progesterone_baseline_ng_per_ml`  ·  Tier B  ·  stored: 10.0 ng/mL

- **Primary citation:** `tulchinsky-1972-steroids`  (_evidence: none_)
- **Reviewer note:** Tulchinsky 1972 has no cached text (evidence=none). Reviewer should verify the mid-luteal baseline ~5-20 ng/mL against the primary paper (or a more appropriate non-pregnant reference).

### `placental_structure.cotyledon_count`  ·  Tier B  ·  stored: 18 count

- **Primary citation:** `benirschke-2012-placental-pathology`  (_evidence: none_)
- **Reviewer note:** Primary citation is a textbook with no cached abstract/fulltext (evidence=none).

### `amniotic_fluid.fetal_swallowing_term_ml_per_24h`  ·  Tier C  ·  stored: 700 mL/24h

- **Primary citation:** `pritchard-1966-fetal-swallowing`  (_evidence: none_)
- **Reviewer note:** Evidence level none (book/pre-index, no abstract or fulltext cached). Cannot verify 700 mL/24h swallowing rate.

### `fetal_circulation.aortic_isthmus_flow_fraction_cvo_term`  ·  Tier C  ·  stored: 0.1 dimensionless

- **Primary citation:** `rudolph-1985-fetal-circulation`  (_evidence: none_)
- **Reviewer note:** Rudolph 1985 lamb book chapter; evidence=none, cannot verify the ~10% aortic isthmus CVO fraction.

### `fetal_circulation.coronary_flow_fraction_cvo_term`  ·  Tier C  ·  stored: 0.03 dimensionless

- **Primary citation:** `rudolph-1985-fetal-circulation`  (_evidence: none_)
- **Reviewer note:** Rudolph 1985 lamb book chapter; evidence=none, cannot verify the ~3% coronary CVO fraction.

### `fetal_circulation.ductus_arteriosus_share`  ·  Tier C  ·  stored: 0.85 fraction

- **Primary citation:** `rudolph-1985-fetal-circulation`  (_evidence: none_)
- **Reviewer note:** Rudolph 1985 lamb book chapter; evidence=none, no abstract/fulltext cached to verify the 0.85 RV-to-ductus share.

### `fetal_circulation.foramen_ovale_streamline_preference`  ·  Tier C  ·  stored: 0.8 fraction

- **Primary citation:** `rudolph-1985-fetal-circulation`  (_evidence: none_)
- **Reviewer note:** Rudolph 1985 lamb book chapter; evidence=none, cannot verify the 0.80 streamline-preference weight.

### `fetal_metabolism.fetal_urine_output_ml_per_kg_h_term`  ·  Tier C  ·  stored: 50.0 mL/kg/h

- **Primary citation:** `battaglia-meschia-1986-fetal-metabolism`  (_evidence: none_)
- **Reviewer note:** Textbook source; no abstract or fulltext cached (evidence=none).

### `maternal_cardiovascular.aortic_root_diameter_term_mm`  ·  Tier C  ·  stored: 30.0 mm

- **Primary citation:** `sanghavi-rutherford-2014-cardio-review`  (_evidence: none_)
- **Reviewer note:** Primary source (Sanghavi & Rutherford 2014) has no cached abstract/fulltext (evidence=none); value cannot be checked against text.

### `maternal_cardiovascular.baseline_pvr_dyn_s_cm5`  ·  Tier C  ·  stored: 120 dyn·s·cm⁻⁵

- **Primary citation:** `sanghavi-rutherford-2014-cardio-review`  (_evidence: none_)
- **Reviewer note:** Primary source (Sanghavi & Rutherford 2014) has no cached abstract/fulltext (evidence=none); value cannot be checked against text.

### `maternal_cardiovascular.lv_wall_thickness_term_mm`  ·  Tier C  ·  stored: 11 mm

- **Primary citation:** `sanghavi-rutherford-2014-cardio-review`  (_evidence: none_)
- **Reviewer note:** Primary source (Sanghavi & Rutherford 2014) has no cached abstract/fulltext (evidence=none); value cannot be checked against text.

### `maternal_cardiovascular.map_individual_sigma_mmhg`  ·  Tier C  ·  stored: 5.0 mmHg

- **Primary citation:** `sanghavi-rutherford-2014-cardio-review`  (_evidence: none_)
- **Reviewer note:** Primary source (Sanghavi & Rutherford 2014) has no cached abstract/fulltext (evidence=none); value cannot be checked against text.

### `maternal_cardiovascular.map_spread_weeks`  ·  Tier C  ·  stored: 8.0 weeks

- **Primary citation:** `sanghavi-rutherford-2014-cardio-review`  (_evidence: none_)
- **Reviewer note:** Primary source (Sanghavi & Rutherford 2014) has no cached abstract/fulltext (evidence=none); value cannot be checked against text.

### `maternal_cardiovascular.pulse_wave_velocity_term_m_per_s`  ·  Tier C  ·  stored: 7.5 m/s

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

