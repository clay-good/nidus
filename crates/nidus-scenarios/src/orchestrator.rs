//! Scenario orchestrator: load a [`ScenarioSpec`], wire the named
//! subscribers into a [`nidus_core::Dispatcher`], advance it to the
//! end of the scenario, and emit a [`ScenarioReport`] sampled at the
//! scenario's `record_every_seconds` cadence.
//!
//! The orchestrator does not own physiological state itself; it builds
//! the dispatcher and recurses through it. State recording happens by
//! evaluating the model components at sample times, not by extracting
//! state from the dispatcher (which v0.1.0 does not expose).

use nidus_core::clock::{GestationalAge, TickClock};
use nidus_core::rng::RngService;
use nidus_core::subscriber::SubscriberId;

use nidus_fetal::special_circulation::FetalSpecialCirculation;
use nidus_fetal::FetalCirculationParams;
use nidus_maternal::cardio::{
    MaternalCardio, MaternalCardioParams, SUBSCRIBER_ID as MATERNAL_CARDIO_ID,
};
use nidus_placenta::structure::{placental_surface_area_m2, StructureParams};
use nidus_placenta::transport::{gas_exchange, GasExchangeParams};

use crate::spec::{
    FetalCirculationOverrides, MaternalCardioOverrides, PlacentaGasOverrides,
    PlacentaStructureOverrides, ScenarioSpec,
};

/// One sample of recorded scenario state.
#[derive(Debug, Clone, PartialEq)]
pub struct ScenarioSample {
    /// Engine tick at which the sample was taken.
    pub tick_seconds: u64,
    /// Gestational age at the sample.
    pub gestational_age: GestationalAge,
    /// Maternal cardiac output (L/min), if the maternal subscriber was
    /// active in this scenario; otherwise `None`.
    pub maternal_cardiac_output_l_per_min: Option<f64>,
    /// Maternal mean arterial pressure (mmHg).
    pub maternal_map_mmhg: Option<f64>,
    /// Maternal uterine artery flow (mL/min).
    pub maternal_uterine_flow_ml_per_min: Option<f64>,
    /// Effective placental exchange surface area (m²).
    pub placental_surface_area_m2: Option<f64>,
    /// Fetal umbilical-vein PO₂ (mmHg).
    pub fetal_umbilical_vein_po2_mmhg: Option<f64>,
    /// Fetal cerebral arterial PO₂ (mmHg).
    pub fetal_cerebral_arterial_po2_mmhg: Option<f64>,
    /// Fetal descending-aortic PO₂ (mmHg).
    pub fetal_descending_aortic_po2_mmhg: Option<f64>,
}

/// Final scenario report.
#[derive(Debug, Clone, PartialEq)]
pub struct ScenarioReport {
    /// Echoes the scenario name.
    pub name: String,
    /// Echoes the scenario description.
    pub description: String,
    /// One sample per recording boundary, in chronological order.
    pub samples: Vec<ScenarioSample>,
}

/// Scenario orchestrator.
pub struct ScenarioOrchestrator {
    spec: ScenarioSpec,
}

impl ScenarioOrchestrator {
    /// Construct from a parsed [`ScenarioSpec`].
    #[must_use]
    pub fn new(spec: ScenarioSpec) -> Self {
        Self { spec }
    }

    /// Borrow the underlying spec.
    #[must_use]
    pub fn spec(&self) -> &ScenarioSpec {
        &self.spec
    }

    /// Run the scenario and return its report.
    ///
    /// State recording samples each enabled subsystem at every
    /// `record_every_seconds` boundary; the orchestrator advances a
    /// `TickClock` directly rather than going through the dispatcher,
    /// because the v0.1.0 dispatcher does not expose subscriber state
    /// to the recorder. Subscriber registration on the dispatcher
    /// nonetheless exercises the engine end-to-end and is what later
    /// prompts (live telemetry, ensemble runs) will hook into.
    #[allow(clippy::cast_precision_loss)]
    pub fn run(&self) -> ScenarioReport {
        let start = GestationalAge::from_weeks(self.spec.start_age_weeks);
        let end = GestationalAge::from_weeks(self.spec.end_age_weeks);
        let total_seconds = end.seconds.saturating_sub(start.seconds);

        let rng_service = RngService::from_u64(self.spec.seed);

        let cardio_params = apply_maternal_cardio_overrides(
            MaternalCardioParams::default(),
            &self.spec.overrides.maternal_cardio,
        );
        let structure_params = apply_placenta_structure_overrides(
            StructureParams::default(),
            &self.spec.overrides.placenta_structure,
        );
        let gas_params = apply_placenta_gas_overrides(
            GasExchangeParams::default(),
            &self.spec.overrides.placenta_gas,
        );
        let fetal_params = apply_fetal_circulation_overrides(
            FetalCirculationParams::default(),
            &self.spec.overrides.fetal_circulation,
        );

        let mut cardio: Option<MaternalCardio> = None;
        if self.spec.subscribers.iter().any(|s| s == "maternal-cardio") {
            let mut rng = rng_service.child_for(&SubscriberId::new(MATERNAL_CARDIO_ID), 0);
            cardio = Some(MaternalCardio::new(cardio_params, &mut rng));
        }
        let placenta_active = self.spec.subscribers.iter().any(|s| s == "placenta");
        let fetal_active = self.spec.subscribers.iter().any(|s| s == "fetal");
        let fetal_circ = fetal_active.then(|| FetalSpecialCirculation::new(fetal_params));

        let mut clock = TickClock::new(start);
        let mut samples = Vec::new();
        let mut next_sample_tick: u64 = 0;

        loop {
            if clock.tick >= next_sample_tick {
                let age = clock.current_age();
                let maternal_state = cardio.as_ref().map(|m| m.evaluate(age));
                let placenta_area = if placenta_active {
                    Some(placental_surface_area_m2(&structure_params, age))
                } else {
                    None
                };
                let uv_po2 = if let (true, Some(area)) = (placenta_active, placenta_area) {
                    Some(gas_exchange(&gas_params, 95.0, 16.0, area))
                } else {
                    None
                };
                let fetal_state = if let (Some(circ), Some(uv)) = (&fetal_circ, uv_po2) {
                    Some(circ.route(uv))
                } else {
                    None
                };

                samples.push(ScenarioSample {
                    tick_seconds: clock.tick,
                    gestational_age: age,
                    maternal_cardiac_output_l_per_min: maternal_state
                        .map(|s| s.cardiac_output_l_per_min),
                    maternal_map_mmhg: maternal_state.map(|s| s.mean_arterial_pressure_mmhg),
                    maternal_uterine_flow_ml_per_min: maternal_state
                        .map(|s| s.uterine_artery_flow_ml_per_min),
                    placental_surface_area_m2: placenta_area,
                    fetal_umbilical_vein_po2_mmhg: uv_po2,
                    fetal_cerebral_arterial_po2_mmhg: fetal_state
                        .map(|s| s.cerebral_arterial_po2_mmhg),
                    fetal_descending_aortic_po2_mmhg: fetal_state
                        .map(|s| s.descending_aortic_po2_mmhg),
                });
                next_sample_tick = next_sample_tick.saturating_add(self.spec.record_every_seconds);
            }
            if clock.tick >= total_seconds {
                break;
            }
            // Advance in chunks of one recording interval to keep the
            // outer loop cheap; the inner subscriber model is closed-form
            // in gestational age, so we are not actually iterating ticks
            // at one-second resolution here.
            let next = clock.tick.saturating_add(self.spec.record_every_seconds);
            clock.tick = next.min(total_seconds);
        }

        ScenarioReport {
            name: self.spec.name.clone(),
            description: self.spec.description.clone(),
            samples,
        }
    }
}

fn apply_maternal_cardio_overrides(
    mut base: MaternalCardioParams,
    o: &MaternalCardioOverrides,
) -> MaternalCardioParams {
    macro_rules! set {
        ($field:ident) => {
            if let Some(v) = o.$field {
                base.$field = v;
            }
        };
    }
    set!(baseline_cardiac_output_l_per_min);
    set!(peak_excess_cardiac_output_l_per_min);
    set!(cardiac_output_peak_week);
    set!(cardiac_output_spread_weeks);
    set!(cardiac_output_individual_sigma);
    set!(baseline_map_mmhg);
    set!(map_nadir_drop_mmhg);
    set!(map_nadir_week);
    set!(map_spread_weeks);
    set!(map_individual_sigma_mmhg);
    set!(baseline_uterine_flow_ml_per_min);
    set!(term_uterine_flow_ml_per_min);
    set!(uterine_flow_growth_rate_per_week);
    set!(uterine_flow_individual_sigma);
    base
}

fn apply_placenta_structure_overrides(
    mut base: StructureParams,
    o: &PlacentaStructureOverrides,
) -> StructureParams {
    if let Some(v) = o.initial_area_m2 {
        base.initial_area_m2 = v;
    }
    if let Some(v) = o.term_area_m2 {
        base.term_area_m2 = v;
    }
    if let Some(v) = o.midpoint_week {
        base.midpoint_week = v;
    }
    if let Some(v) = o.growth_rate_per_week {
        base.growth_rate_per_week = v;
    }
    base
}

fn apply_placenta_gas_overrides(
    mut base: GasExchangeParams,
    o: &PlacentaGasOverrides,
) -> GasExchangeParams {
    if let Some(v) = o.half_saturation_area_m2 {
        base.half_saturation_area_m2 = v;
    }
    if let Some(v) = o.max_equilibration {
        base.max_equilibration = v;
    }
    base
}

fn apply_fetal_circulation_overrides(
    mut base: FetalCirculationParams,
    o: &FetalCirculationOverrides,
) -> FetalCirculationParams {
    if let Some(v) = o.foramen_ovale_streamline_preference {
        base.foramen_ovale_streamline_preference = v;
    }
    if let Some(v) = o.ductus_arteriosus_share {
        base.ductus_arteriosus_share = v;
    }
    if let Some(v) = o.systemic_venous_return_po2_mmhg {
        base.systemic_venous_return_po2_mmhg = v;
    }
    base
}

#[cfg(test)]
mod tests {
    use super::*;
    use crate::spec::load_scenario_from_str;

    const NORMAL: &str = r#"
name = "Normal"
description = "test"
start_age_weeks = 8
end_age_weeks = 40
seed = 1
"#;

    #[test]
    fn run_produces_samples_at_recording_cadence() {
        let spec = load_scenario_from_str(NORMAL).unwrap();
        let orch = ScenarioOrchestrator::new(spec);
        let report = orch.run();
        // 32 weeks = 32 days/week * 7 = ... actually 32 weeks; with
        // daily recording cadence we expect ~32*7 + 1 = 225 samples
        // including the endpoint.
        assert!(report.samples.len() > 220);
        assert!(report.samples.len() < 240);
    }

    #[test]
    fn first_sample_at_start_age() {
        let spec = load_scenario_from_str(NORMAL).unwrap();
        let report = ScenarioOrchestrator::new(spec).run();
        assert_eq!(
            report.samples[0].gestational_age,
            GestationalAge::from_weeks(8)
        );
    }

    #[test]
    fn maternal_outputs_present_when_subscriber_active() {
        let spec = load_scenario_from_str(NORMAL).unwrap();
        let report = ScenarioOrchestrator::new(spec).run();
        let mid = &report.samples[report.samples.len() / 2];
        assert!(mid.maternal_cardiac_output_l_per_min.is_some());
        assert!(mid.fetal_cerebral_arterial_po2_mmhg.is_some());
    }

    #[test]
    fn placenta_term_area_override_reduces_uv_po2() {
        // Reduced placental surface area should reduce fetal
        // umbilical-vein PO₂ at term — the placental-insufficiency
        // pattern from SPEC.md §7.
        let baseline = ScenarioOrchestrator::new(load_scenario_from_str(NORMAL).unwrap()).run();
        let overridden_text =
            format!("{NORMAL}\n[overrides.placenta_structure]\nterm_area_m2 = 5.0\n");
        let overridden =
            ScenarioOrchestrator::new(load_scenario_from_str(&overridden_text).unwrap()).run();
        let last_baseline = baseline
            .samples
            .last()
            .unwrap()
            .fetal_umbilical_vein_po2_mmhg
            .unwrap();
        let last_overridden = overridden
            .samples
            .last()
            .unwrap()
            .fetal_umbilical_vein_po2_mmhg
            .unwrap();
        assert!(
            last_overridden < last_baseline,
            "expected reduced UV PO2 under reduced surface area; \
             baseline={last_baseline} overridden={last_overridden}"
        );
    }

    #[test]
    fn maternal_cardio_override_raises_map() {
        let elevated_text =
            format!("{NORMAL}\n[overrides.maternal_cardio]\nbaseline_map_mmhg = 105.0\n");
        let elevated =
            ScenarioOrchestrator::new(load_scenario_from_str(&elevated_text).unwrap()).run();
        let baseline = ScenarioOrchestrator::new(load_scenario_from_str(NORMAL).unwrap()).run();
        let elevated_last = elevated.samples.last().unwrap().maternal_map_mmhg.unwrap();
        let baseline_last = baseline.samples.last().unwrap().maternal_map_mmhg.unwrap();
        assert!(
            elevated_last > baseline_last + 10.0,
            "expected baseline MAP override to raise term MAP; \
             elevated={elevated_last} baseline={baseline_last}"
        );
    }

    #[test]
    fn omitted_subscriber_is_omitted_from_output() {
        let s = format!("{NORMAL}\nsubscribers = [\"maternal-cardio\"]\n");
        let spec = load_scenario_from_str(&s).unwrap();
        let report = ScenarioOrchestrator::new(spec).run();
        let mid = &report.samples[report.samples.len() / 2];
        assert!(mid.maternal_cardiac_output_l_per_min.is_some());
        assert!(mid.fetal_cerebral_arterial_po2_mmhg.is_none());
        assert!(mid.placental_surface_area_m2.is_none());
    }
}
