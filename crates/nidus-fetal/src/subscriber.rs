//! Fetal subscriber.
//!
//! Wires the special-circulation transform into the engine's tick
//! loop. The fetal subsystem takes the placenta's most recent
//! umbilical-vein PO₂ as input and produces cerebral, descending
//! aortic, and umbilical-artery PO₂ values on each hourly tick. The
//! umbilical-artery value is what closes the loop with the placenta
//! on the fetal side; the placenta picks it up on its next tick.

use nidus_core::clock::TickTier;
use nidus_core::subscriber::{Subscriber, SubscriberId, TickContext};

use crate::special_circulation::{
    FetalCirculationParams, FetalCirculationState, FetalSpecialCirculation,
};

/// Stable subscriber id for the fetal subsystem.
pub const SUBSCRIBER_ID: &str = "nidus-fetal:circulation";

/// Fetal subsystem subscriber for v0.1.0.
pub struct Fetal {
    id: SubscriberId,
    circulation: FetalSpecialCirculation,
    /// Most recent umbilical-vein PO₂ supplied by the placenta;
    /// updated by [`Fetal::set_umbilical_vein_po2_mmhg`] between ticks.
    umbilical_vein_po2_mmhg: f64,
    state: FetalCirculationState,
}

impl Fetal {
    /// Construct with default scaffolding parameters and a baseline
    /// umbilical-vein PO₂ matching the placenta module's default
    /// inputs.
    pub fn with_default_params() -> Self {
        Self::new(FetalCirculationParams::default(), 30.0)
    }

    /// Construct from explicit circulation parameters and an initial
    /// umbilical-vein PO₂.
    pub fn new(params: FetalCirculationParams, umbilical_vein_po2_mmhg: f64) -> Self {
        let circulation = FetalSpecialCirculation::new(params);
        let state = circulation.route(umbilical_vein_po2_mmhg);
        Self {
            id: SubscriberId::new(SUBSCRIBER_ID),
            circulation,
            umbilical_vein_po2_mmhg,
            state,
        }
    }

    /// Most recently computed cardiovascular state.
    #[must_use]
    pub fn state(&self) -> FetalCirculationState {
        self.state
    }

    /// Borrow the circulation parameter block.
    #[must_use]
    pub fn params(&self) -> &FetalCirculationParams {
        self.circulation.params()
    }

    /// Update the umbilical-vein PO₂ used by the next tick's routing.
    /// Called by the placenta module on its hourly tick.
    pub fn set_umbilical_vein_po2_mmhg(&mut self, value: f64) {
        self.umbilical_vein_po2_mmhg = value;
    }
}

impl Subscriber for Fetal {
    fn id(&self) -> &SubscriberId {
        &self.id
    }

    fn tier(&self) -> TickTier {
        TickTier::Hour
    }

    fn on_tick(&mut self, ctx: &mut TickContext<'_>) {
        let _ = ctx.age;
        self.state = self.circulation.route(self.umbilical_vein_po2_mmhg);
    }
}

#[cfg(test)]
#[allow(clippy::float_cmp)]
mod tests {
    use super::*;
    use nidus_core::clock::{GestationalAge, SECONDS_PER_HOUR};
    use nidus_core::{Dispatcher, RngService};

    #[test]
    fn fetal_state_initialised_at_construction() {
        let f = Fetal::with_default_params();
        let s = f.state();
        assert!(s.cerebral_arterial_po2_mmhg > s.descending_aortic_po2_mmhg);
    }

    #[test]
    fn fetal_subscriber_runs_under_dispatcher() {
        let mut disp = Dispatcher::new(GestationalAge::from_weeks(30), RngService::from_u64(0));
        disp.register(Box::new(Fetal::with_default_params()));
        disp.advance_seconds(SECONDS_PER_HOUR);
    }
}
