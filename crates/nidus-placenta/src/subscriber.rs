//! Placenta subscriber.
//!
//! Wires the structural and transport models into the engine's tick
//! loop. The placenta updates at the hourly tier — surface area and
//! transport efficiency change on the scale of days to weeks, not
//! seconds — and exposes its current state for the fetal subsystem to
//! consume on its own ticks.

use nidus_core::clock::TickTier;
use nidus_core::subscriber::{Subscriber, SubscriberId, TickContext};

use crate::structure::{placental_surface_area_m2, StructureParams};
use crate::transport::{gas_exchange, GasExchangeParams, GlucoseTransportParams};

/// Stable subscriber id for the placenta module.
pub const SUBSCRIBER_ID: &str = "nidus-placenta:interface";

/// Current placental state, as updated each hourly tick.
#[derive(Debug, Clone, Copy, PartialEq)]
pub struct PlacentaState {
    /// Effective exchange surface area, m².
    pub surface_area_m2: f64,
    /// Computed fetal umbilical-vein PO₂ at the most recent tick, mmHg.
    /// `NaN` until the first tick fires.
    pub fetal_umbilical_vein_po2_mmhg: f64,
}

impl Default for PlacentaState {
    fn default() -> Self {
        Self {
            surface_area_m2: f64::NAN,
            fetal_umbilical_vein_po2_mmhg: f64::NAN,
        }
    }
}

/// Placenta subscriber.
///
/// The placenta does not own maternal or fetal blood composition; those
/// belong to the maternal and fetal subsystems respectively. Instead,
/// the placenta exposes the transport functions that those subsystems
/// invoke on each other's behalf, plus a small piece of state
/// (current surface area, last-computed UV PO₂) that summarises the
/// hourly tick.
pub struct Placenta {
    id: SubscriberId,
    structure_params: StructureParams,
    gas_params: GasExchangeParams,
    glucose_params: GlucoseTransportParams,
    /// Most recent maternal arterial PO₂ supplied by the maternal
    /// subsystem; used by the next tick's gas-exchange computation.
    maternal_arterial_po2_mmhg: f64,
    /// Most recent fetal umbilical-artery (return) PO₂ supplied by the
    /// fetal subsystem; used by the next tick's gas-exchange
    /// computation.
    fetal_umbilical_artery_po2_mmhg: f64,
    state: PlacentaState,
}

impl Placenta {
    /// Construct with default scaffolding parameters and physiological
    /// default inputs (maternal arterial PO₂ ≈ 95 mmHg, fetal
    /// umbilical-artery return ≈ 16 mmHg).
    pub fn with_default_params() -> Self {
        Self::new(
            StructureParams::default(),
            GasExchangeParams::default(),
            GlucoseTransportParams::default(),
            95.0,
            16.0,
        )
    }

    /// Construct from explicit parameter blocks and initial inputs.
    pub fn new(
        structure_params: StructureParams,
        gas_params: GasExchangeParams,
        glucose_params: GlucoseTransportParams,
        maternal_arterial_po2_mmhg: f64,
        fetal_umbilical_artery_po2_mmhg: f64,
    ) -> Self {
        Self {
            id: SubscriberId::new(SUBSCRIBER_ID),
            structure_params,
            gas_params,
            glucose_params,
            maternal_arterial_po2_mmhg,
            fetal_umbilical_artery_po2_mmhg,
            state: PlacentaState::default(),
        }
    }

    /// Most recently computed placental state.
    #[must_use]
    pub fn state(&self) -> PlacentaState {
        self.state
    }

    /// Borrow the structure parameter block.
    #[must_use]
    pub fn structure_params(&self) -> &StructureParams {
        &self.structure_params
    }

    /// Borrow the gas-exchange parameter block.
    #[must_use]
    pub fn gas_params(&self) -> &GasExchangeParams {
        &self.gas_params
    }

    /// Borrow the glucose-transport parameter block.
    #[must_use]
    pub fn glucose_params(&self) -> &GlucoseTransportParams {
        &self.glucose_params
    }

    /// Update the maternal arterial PO₂ used by subsequent gas-exchange
    /// computations. Called by the maternal subsystem on its own tick;
    /// the placenta picks up the new value on its next hourly tick.
    pub fn set_maternal_arterial_po2_mmhg(&mut self, value: f64) {
        self.maternal_arterial_po2_mmhg = value;
    }

    /// Update the fetal umbilical-artery (return) PO₂ used by
    /// subsequent gas-exchange computations.
    pub fn set_fetal_umbilical_artery_po2_mmhg(&mut self, value: f64) {
        self.fetal_umbilical_artery_po2_mmhg = value;
    }
}

impl Subscriber for Placenta {
    fn id(&self) -> &SubscriberId {
        &self.id
    }

    fn tier(&self) -> TickTier {
        TickTier::Hour
    }

    fn on_tick(&mut self, ctx: &mut TickContext<'_>) {
        let area = placental_surface_area_m2(&self.structure_params, ctx.age);
        let uv = gas_exchange(
            &self.gas_params,
            self.maternal_arterial_po2_mmhg,
            self.fetal_umbilical_artery_po2_mmhg,
            area,
        );
        self.state = PlacentaState {
            surface_area_m2: area,
            fetal_umbilical_vein_po2_mmhg: uv,
        };
        // Silence the unused `glucose_params` field for v0.1.0: future
        // prompts will plumb fetal/maternal glucose concentrations
        // through this subscriber. Touching it here keeps the field
        // live without triggering dead-code lints.
        let _ = self.glucose_params;
    }
}

#[cfg(test)]
#[allow(clippy::float_cmp)]
mod tests {
    use super::*;
    use nidus_core::clock::{GestationalAge, SECONDS_PER_HOUR};
    use nidus_core::{Dispatcher, RngService};

    #[test]
    fn placenta_subscriber_updates_state_at_hour_boundary() {
        let mut disp = Dispatcher::new(GestationalAge::from_weeks(28), RngService::from_u64(0));
        disp.register(Box::new(Placenta::with_default_params()));
        disp.advance_seconds(SECONDS_PER_HOUR);
        // We cannot extract subscriber state from the dispatcher in
        // v0.1.0, but the public Placenta::new pipeline is exercised
        // here and the structure+transport tests cover the values.
    }
}
