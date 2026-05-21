# Spec 02 — Subsystem Completion

## Context

SPEC.md §§5–8 promise a maternal subsystem with cardiovascular,
respiratory, renal, metabolic, endocrine, and immune components; a
placental subsystem with structure, gas transport, glucose transport,
amino acid transport, endocrine production, and barrier function; and
a fetal subsystem with circulation, growth, cardiac, metabolism, organ
maturation, neurology, and endocrine development.

The v0.1 reality:

- Maternal ships **cardio only**
  ([`crates/nidus-maternal/src/cardio.rs`](../crates/nidus-maternal/src/cardio.rs)).
  Respiratory, renal, metabolic, endocrine, immune are absent.
- Placental ships **structure + gas + glucose**
  ([`crates/nidus-placenta/src/`](../crates/nidus-placenta/src/)).
  Amino acid, lipid, lactate, endocrine, barrier, trophoblast
  maturation, intervillous perfusion are absent.
- Fetal ships **special circulation only**
  ([`crates/nidus-fetal/src/special_circulation.rs`](../crates/nidus-fetal/src/special_circulation.rs)).
  Growth, cardiac output, metabolism, organ maturation, neurology,
  endocrine are absent.

This spec adds the missing modules. Each new module follows the
established pattern: a `Subscriber` impl, a `Params` struct backed by
the parameter database (via Spec 01), telemetry emission, unit tests
covering trajectory shape and seed determinism, and a one-page module
doc (Spec 07).

## Deliverables

Twelve new physiological modules, all wired into the dispatcher and
all driven by database-resident parameters.

## Dependencies

Requires Spec 01 (parameter database) for the parameters each module
needs. Module prompts can begin once their parameter entries exist;
parameter entries can be written in parallel.

## Numbered prompts

### Prompt 02.1 — Maternal respiratory

File: new [`crates/nidus-maternal/src/respiratory.rs`](../crates/nidus-maternal/src/respiratory.rs).

Model:
- Minute ventilation rises ~40 % by term (LoMauro & Aliverti 2015).
- PaCO₂ falls to ~30 mmHg by mid-gestation; PaO₂ rises to ~104 mmHg.
- Functional residual capacity drops 20 %.
- Oxyhaemoglobin P50 shifts right (~2 mmHg) — feeds gas exchange.

Subscriber: `MaternalRespiratory` ticks at `TickTier::Minute`,
emits `maternal.respiratory.{minute_ventilation_l_per_min,
paco2_mmhg, pao2_mmhg, frc_l, p50_shift_mmhg}` telemetry.

Params loaded via `from_database`.

Tests: trimester trajectory shape; seed determinism; dispatcher wiring.

### Prompt 02.2 — Maternal renal

File: new [`crates/nidus-maternal/src/renal.rs`](../crates/nidus-maternal/src/renal.rs).

Model GFR (+50 % peak ~16 wk, Cheung & Lafayette 2013), plasma
creatinine fall, glycosuria threshold drop. Same subscriber pattern.

Telemetry: `maternal.renal.{gfr_ml_per_min, creatinine_mg_per_dl}`.

### Prompt 02.3 — Maternal metabolic

File: new [`crates/nidus-maternal/src/metabolic.rs`](../crates/nidus-maternal/src/metabolic.rs).

Model: insulin resistance rises with gestation; fasting glucose
falls; postprandial glucose rises; free fatty acid mobilisation
increases in third trimester. Couples to placental glucose transport
in Spec 02.5.

Telemetry: `maternal.metabolic.{fasting_glucose_mmol_per_l,
insulin_resistance_index, free_fatty_acid_mmol_per_l}`.

### Prompt 02.4 — Maternal endocrine

File: new [`crates/nidus-maternal/src/endocrine.rs`](../crates/nidus-maternal/src/endocrine.rs).

Model trajectories for hCG (peak ~10 wk), progesterone, oestradiol,
hPL (rises through term). These are pre-computed scalars but feed
placental endocrine and maternal metabolic.

Telemetry: `maternal.endocrine.{hcg_iu_per_l, progesterone_ng_per_ml,
estradiol_pg_per_ml, hpl_ng_per_ml}`.

### Prompt 02.5 — Placental amino-acid transport

File: new [`crates/nidus-placenta/src/amino_acid.rs`](../crates/nidus-placenta/src/amino_acid.rs).

Active transport via System A (Na-coupled, neutral AA) and System L
(neutral exchanger). Param db: `placenta.aa.system_a_vmax`,
`placenta.aa.system_l_vmax`, Km values per substrate class.

Telemetry: `placenta.aa.{system_a_flux_mmol_per_min,
system_l_flux_mmol_per_min, total_aa_flux_mmol_per_min}`.

Tests: flux scales with maternal AA concentration and surface area.

### Prompt 02.6 — Placental endocrine

File: new [`crates/nidus-placenta/src/endocrine.rs`](../crates/nidus-placenta/src/endocrine.rs).

Placental contribution to hCG, hPL, progesterone, oestrogen. Couples
to maternal endocrine; the placental module is the *source*, the
maternal module the *systemic level*.

Telemetry: `placenta.endocrine.{hcg_production_iu_per_min, ...}`.

Tier C is acceptable — flag prominently in module docs.

### Prompt 02.7 — Placental barrier

File: new [`crates/nidus-placenta/src/barrier.rs`](../crates/nidus-placenta/src/barrier.rs).

Model IgG transfer (FcRn-mediated, rising late gestation) and
small-molecule passive diffusion. Sufficient for v0.2 if it tracks
maternal-side concentrations and emits a transfer-fraction.

Telemetry: `placenta.barrier.{igg_transfer_fraction,
passive_permeability_factor}`.

### Prompt 02.8 — Fetal growth

File: new [`crates/nidus-fetal/src/growth.rs`](../crates/nidus-fetal/src/growth.rs).

NICHD-aligned weight, length, head/abdominal circumference
trajectories with population variability. Couples to placental
substrate flux: terminal weight responds to time-integrated
glucose+AA flux.

Telemetry: `fetal.growth.{weight_g, length_cm, head_circ_cm,
abdominal_circ_cm}`, all carrying tier and citation list.

Tests: NICHD median trajectory falls inside the modelled distribution;
restricted-flux scenario produces smaller weights.

### Prompt 02.9 — Fetal cardiac

File: new [`crates/nidus-fetal/src/cardiac.rs`](../crates/nidus-fetal/src/cardiac.rs).

Combined ventricular output (Rudolph 1985), heart-rate trajectory
(rises to ~170 bpm at 10 wk, settles to ~140 bpm at term). Feeds the
existing special circulation module.

Telemetry: `fetal.cardiac.{cvo_ml_per_min_per_kg, heart_rate_bpm}`.

### Prompt 02.10 — Fetal metabolism

File: new [`crates/nidus-fetal/src/metabolism.rs`](../crates/nidus-fetal/src/metabolism.rs).

Glucose oxidation rate, lactate production, insulin signalling
development. Consumes placental flux; emits substrate balance.

Telemetry: `fetal.metabolism.{glucose_uptake_mg_per_kg_per_min,
lactate_production_mmol_per_kg_per_min}`.

### Prompt 02.11 — Fetal organ maturation

File: new [`crates/nidus-fetal/src/organ_maturation.rs`](../crates/nidus-fetal/src/organ_maturation.rs).

Track maturation indices (0..1) for: lung surfactant pool (sharp
rise 32–36 wk), hepatic enzyme capacity, renal nephrogenesis (done
~36 wk), gut motility. Tier C — citations include Avery & Mead,
Burri 2006.

Telemetry: `fetal.maturation.{lung_index, hepatic_index,
renal_index, gut_index}`.

### Prompt 02.12 — Fetal endocrine

File: new [`crates/nidus-fetal/src/endocrine.rs`](../crates/nidus-fetal/src/endocrine.rs).

Fetal insulin, cortisol (HPA axis), thyroid hormones. Mostly Tier C/D;
its main value is providing an explicit surface for unknown channels
(Spec 11 — hypothesis generalisation).

Telemetry: `fetal.endocrine.{insulin_uu_per_ml, cortisol_ng_per_ml,
tsh_miu_per_l, t4_ug_per_dl}`.

### Prompt 02.13 — Module registration and dispatcher wiring

File: [`crates/nidus-scenarios/src/orchestrator.rs`](../crates/nidus-scenarios/src/orchestrator.rs).

For every module added in 02.1–02.12, register the subscriber with
the dispatcher at the orchestrator level, behind a feature flag in
`ScenarioSpec` (`enabled_modules: ["maternal.respiratory", ...]`)
defaulting to all-on for the bundled scenarios.

Verification: `cargo run --bin nidus -- run normal_term --emit ndjson -`
prints telemetry from all twelve new sources within the first 24
simulated hours.

### Prompt 02.14 — Inter-module coupling tests

File: new [`crates/nidus-scenarios/tests/coupling.rs`](../crates/nidus-scenarios/tests/coupling.rs).

Integration tests covering the coupling edges:
- Maternal respiratory P50 shift increases placental O₂ flux.
- Maternal metabolic insulin-resistance increase shifts maternal
  glucose, which shifts placental glucose flux, which shifts fetal
  glucose uptake and weight trajectory.
- Placental gas exchange reduction (insufficiency scenario) reduces
  fetal weight via metabolism module.
- Maternal endocrine hPL feeds back into maternal metabolic
  insulin-resistance.

Verification: `cargo test -p nidus-scenarios coupling` green.

## Acceptance for Spec 02

- [ ] Twelve new module files exist, each with subscriber, params,
  telemetry, and ≥ 4 unit tests.
- [ ] All twelve module params load via `from_database`.
- [ ] No new code path introduces `Default` outside `#[cfg(test)]`.
- [ ] Inter-module coupling tests pass.
- [ ] `nidus list parameters --coverage` reports zero unfilled
  references across all new modules.
- [ ] `cargo clippy --workspace --all-targets -- -D warnings` clean.
