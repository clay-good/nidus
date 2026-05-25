# Nidus Dataset Changelog

The dataset uses semantic versioning, independent of the code.

The format is loosely based on [Keep a Changelog](https://keepachangelog.com/),
and versions follow [Semantic Versioning](https://semver.org/).

## [Unreleased]

### Added
- Phase 2/3 saturation batch (spec 04): 11 more parameters using
  citations already in the dataset; brings the dataset to **223
  parameters / 60 citations**.
  - `maternal_blood.transferrin_saturation_term_pct`,
    `folate_term_ng_per_ml`, `b12_term_pg_per_ml` (Hytten 1980).
  - `maternal_renal.urinary_glucose_term_mg_per_24h` (Davison &
    Hytten 1974), `tubular_phosphate_threshold_term` (Cheung 2013).
  - `placental_structure.syncytiotrophoblast_thickness_term_um`
    (Mayhew 2014).
  - `placental_gas_exchange.co2_diffusing_capacity_term_ml_min_mmhg`
    (Mayhew 1986), `umbilical_vein_pco2_mmhg` and
    `umbilical_artery_pco2_mmhg` (Carter 2009),
    `spiral_artery_po2_estimate_mmhg` (Carter & Pijnenborg 2011).
  - `fetal_circulation.mca_flow_term_ml_per_min` (Mari 1995).
- Phase 2 saturation batch (spec 04): 8 new parameters using
  citations already in the dataset, bringing the dataset to **212
  parameters / 60 citations**.
  - `maternal_cardiovascular.cardiac_output_t1/t2/t3_l_per_min`
    (Mahendru 2014 trimester anchors).
  - `maternal_cardiovascular.baseline_pvr_dyn_s_cm5` and
    `lv_wall_thickness_term_mm` (Sanghavi 2014 review).
  - `maternal_endocrine.cbg_term_mg_per_l` (Carr 1981).
  - `maternal_endocrine.renin_term_ng_per_ml_per_h` (Wilson 1980
    + Cheung 2013).
  - `placental_endocrine.relaxin_t1_ng_per_ml` (Conrad 2001).
- Phase 1 saturation completion (spec 04): 5 new parameters across 4
  subsystems, 2 new citations. Brings the dataset to **204 parameters
  / 60 citations** and closes out the spec-04 Phase 1 column.
  - `maternal_cardiovascular.heart_rate_peak_week` (Mahendru 2014).
  - `maternal_blood.d_dimer_term_ug_per_ml` (Kline 2005).
  - `maternal_renal.cumulative_sodium_retention_g` (Cheung 2013).
  - `placental_structure.placental_thickness_term_cm` (Hoddick 1985,
    new citation).
  - `placental_structure.cord_length_term_cm` (Naeye 1985, new
    citation).
- Initial scaffold for the v0.3.0 dataset-first release.
- JSON Schema (draft 2020-12) for parameters, citations, and tiers in
  `schema/`.
- Tier definitions in `tiers/tiers.json`.

### In progress
- Migration of curated parameters from the legacy `data/parameters/*.toml`
  files to schema-valid JSON under `parameters/`.
- Migration of citation index from the legacy `data/citations/` files
  to `citations/citations.json`.
