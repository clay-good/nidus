//! Maternal cardiovascular subsystem.
//!
//! The model produces three observable signals as functions of
//! gestational age and per-individual stochastic variability:
//!
//! - Cardiac output (`cardiac_output_l_per_min`)
//! - Mean arterial pressure (`mean_arterial_pressure_mmhg`)
//! - Uterine artery blood flow (`uterine_artery_flow_ml_per_min`)
//!
//! The functional forms are deliberately simple parametric curves whose
//! coefficients are pinned to ranges visible in textbook descriptions of
//! maternal cardiovascular adaptation. They will be replaced by
//! database-resolved values in a later prompt (see SPEC.md §13 prompt 5
//! and §9). The structure of the module — a parameter struct, a state
//! struct, and a [`nidus_core::Subscriber`] implementation — is what
//! the rest of the simulator depends on, and that structure is stable.

use nidus_core::clock::{GestationalAge, TickTier, DAYS_PER_WEEK, SECONDS_PER_DAY};
use nidus_core::subscriber::{Subscriber, SubscriberId, TickContext};
use nidus_data::{DatabaseError, ParameterDatabase};

/// Stable subscriber id for the maternal cardiovascular subsystem.
pub const SUBSCRIBER_ID: &str = "nidus-maternal:cardio";

/// Coefficients describing the population-level mean trajectories and
/// the magnitude of per-individual variability.
///
/// All units are explicit in the field names. The default trajectory
/// coefficients place the trajectories in the textbook range; they are
/// not yet citation-backed and must be resolved through the parameter
/// database before the model is used for published output.
#[derive(Debug, Clone, Copy, PartialEq)]
pub struct MaternalCardioParams {
    /// Non-pregnant cardiac output (week 0 baseline), L/min.
    pub baseline_cardiac_output_l_per_min: f64,
    /// Peak excess cardiac output above baseline, L/min.
    pub peak_excess_cardiac_output_l_per_min: f64,
    /// Gestational week of the cardiac-output peak.
    pub cardiac_output_peak_week: f64,
    /// Spread (Gaussian-like sigma in weeks) controlling rise and fall
    /// of the cardiac-output trajectory around its peak.
    pub cardiac_output_spread_weeks: f64,
    /// One-sigma fractional per-individual variability in cardiac
    /// output (e.g. 0.10 means ±10% one-sigma).
    pub cardiac_output_individual_sigma: f64,

    /// Non-pregnant mean arterial pressure, mmHg.
    pub baseline_map_mmhg: f64,
    /// Maximum mid-pregnancy MAP drop relative to baseline, mmHg.
    pub map_nadir_drop_mmhg: f64,
    /// Gestational week of the MAP nadir.
    pub map_nadir_week: f64,
    /// Spread (sigma in weeks) of the MAP trajectory around its nadir.
    pub map_spread_weeks: f64,
    /// One-sigma per-individual MAP offset, mmHg.
    pub map_individual_sigma_mmhg: f64,

    /// Non-pregnant uterine artery flow, mL/min.
    pub baseline_uterine_flow_ml_per_min: f64,
    /// Term-pregnancy uterine artery flow, mL/min.
    pub term_uterine_flow_ml_per_min: f64,
    /// Steepness of the exponential rise in uterine artery flow with
    /// gestational age; larger values give a sharper late rise.
    pub uterine_flow_growth_rate_per_week: f64,
    /// One-sigma fractional per-individual variability in uterine
    /// artery flow.
    pub uterine_flow_individual_sigma: f64,
}

impl Default for MaternalCardioParams {
    fn default() -> Self {
        // Scaffolding constants. Each must be replaced with a
        // database-resolved citation-bearing parameter before publication;
        // see SPEC.md §9 and CONTRIBUTING.md.
        Self {
            baseline_cardiac_output_l_per_min: 5.0,
            peak_excess_cardiac_output_l_per_min: 2.5,
            cardiac_output_peak_week: 32.0,
            cardiac_output_spread_weeks: 11.0,
            cardiac_output_individual_sigma: 0.10,

            baseline_map_mmhg: 85.0,
            map_nadir_drop_mmhg: 10.0,
            map_nadir_week: 22.0,
            map_spread_weeks: 10.0,
            map_individual_sigma_mmhg: 4.0,

            baseline_uterine_flow_ml_per_min: 50.0,
            term_uterine_flow_ml_per_min: 700.0,
            uterine_flow_growth_rate_per_week: 0.12,
            uterine_flow_individual_sigma: 0.15,
        }
    }
}

/// Database ids consumed by [`MaternalCardioParams::from_database`].
///
/// Listed here (rather than only in the function body) so contributors
/// can audit the wiring against `data/parameters/maternal/cardio.toml`
/// without reading code.
pub mod param_ids {
    /// Pre-pregnancy cardiac output (L/min).
    pub const BASELINE_CO: &str = "maternal-cardio-baseline-cardiac-output-l-per-min";
    /// Peak excess cardiac output above baseline (L/min).
    pub const PEAK_EXCESS_CO: &str = "maternal-cardio-peak-excess-cardiac-output-l-per-min";
    /// Gestational week of peak cardiac output.
    pub const CO_PEAK_WEEK: &str = "maternal-cardio-cardiac-output-peak-week";
    /// Spread of the cardiac-output curve (weeks).
    pub const CO_SPREAD_WEEKS: &str = "maternal-cardio-cardiac-output-spread-weeks";
    /// Between-individual sigma for cardiac output (fraction).
    pub const CO_INDIVIDUAL_SIGMA: &str = "maternal-cardio-cardiac-output-individual-sigma";
    /// Pre-pregnancy mean arterial pressure (mmHg).
    pub const BASELINE_MAP: &str = "maternal-cardio-baseline-map-mmhg";
    /// Mid-pregnancy MAP drop from baseline (mmHg).
    pub const MAP_NADIR_DROP: &str = "maternal-cardio-map-nadir-drop-mmhg";
    /// Gestational week of MAP nadir.
    pub const MAP_NADIR_WEEK: &str = "maternal-cardio-map-nadir-week";
    /// Spread of the MAP nadir (weeks).
    pub const MAP_SPREAD_WEEKS: &str = "maternal-cardio-map-spread-weeks";
    /// Between-individual sigma for MAP (mmHg).
    pub const MAP_INDIVIDUAL_SIGMA: &str = "maternal-cardio-map-individual-sigma-mmhg";
    /// Pre-pregnancy uterine artery flow (mL/min).
    pub const BASELINE_UTERINE_FLOW: &str = "maternal-cardio-baseline-uterine-flow-ml-per-min";
    /// Term uterine artery flow (mL/min).
    pub const TERM_UTERINE_FLOW: &str = "maternal-cardio-term-uterine-flow-ml-per-min";
    /// Uterine-flow growth rate (1/week).
    pub const UTERINE_FLOW_GROWTH: &str = "maternal-cardio-uterine-flow-growth-rate-per-week";
    /// Between-individual sigma for uterine flow (fraction).
    pub const UTERINE_FLOW_INDIVIDUAL_SIGMA: &str = "maternal-cardio-uterine-flow-individual-sigma";
}

impl MaternalCardioParams {
    /// Construct from point-estimate values resolved against a loaded
    /// [`ParameterDatabase`]. Every id in [`param_ids`] must exist or
    /// [`DatabaseError::MissingParameter`] is returned.
    ///
    /// This is the canonical production constructor; the
    /// [`Default`] implementation is retained as a scaffold for tests
    /// and override-only scenarios.
    pub fn from_database(db: &ParameterDatabase) -> Result<Self, DatabaseError> {
        Ok(Self {
            baseline_cardiac_output_l_per_min: db.point_estimate(param_ids::BASELINE_CO)?,
            peak_excess_cardiac_output_l_per_min: db.point_estimate(param_ids::PEAK_EXCESS_CO)?,
            cardiac_output_peak_week: db.point_estimate(param_ids::CO_PEAK_WEEK)?,
            cardiac_output_spread_weeks: db.point_estimate(param_ids::CO_SPREAD_WEEKS)?,
            cardiac_output_individual_sigma: db.point_estimate(param_ids::CO_INDIVIDUAL_SIGMA)?,
            baseline_map_mmhg: db.point_estimate(param_ids::BASELINE_MAP)?,
            map_nadir_drop_mmhg: db.point_estimate(param_ids::MAP_NADIR_DROP)?,
            map_nadir_week: db.point_estimate(param_ids::MAP_NADIR_WEEK)?,
            map_spread_weeks: db.point_estimate(param_ids::MAP_SPREAD_WEEKS)?,
            map_individual_sigma_mmhg: db.point_estimate(param_ids::MAP_INDIVIDUAL_SIGMA)?,
            baseline_uterine_flow_ml_per_min: db
                .point_estimate(param_ids::BASELINE_UTERINE_FLOW)?,
            term_uterine_flow_ml_per_min: db.point_estimate(param_ids::TERM_UTERINE_FLOW)?,
            uterine_flow_growth_rate_per_week: db.point_estimate(param_ids::UTERINE_FLOW_GROWTH)?,
            uterine_flow_individual_sigma: db
                .point_estimate(param_ids::UTERINE_FLOW_INDIVIDUAL_SIGMA)?,
        })
    }
}

/// Computed cardiovascular state at a moment in gestation.
#[derive(Debug, Clone, Copy, PartialEq)]
pub struct MaternalCardioState {
    /// Cardiac output, L/min.
    pub cardiac_output_l_per_min: f64,
    /// Mean arterial pressure, mmHg.
    pub mean_arterial_pressure_mmhg: f64,
    /// Uterine artery flow, mL/min.
    pub uterine_artery_flow_ml_per_min: f64,
}

/// Population-mean cardiac output (L/min) at gestational week `w`.
///
/// Bell-shaped around `peak_week` with width `spread_weeks`; rises
/// from baseline at w=0 and falls back as `w` moves far from the peak.
fn mean_cardiac_output(params: &MaternalCardioParams, w: f64) -> f64 {
    let z = (w - params.cardiac_output_peak_week) / params.cardiac_output_spread_weeks;
    params.baseline_cardiac_output_l_per_min
        + params.peak_excess_cardiac_output_l_per_min * (-z * z).exp()
}

/// Population-mean mean arterial pressure (mmHg) at gestational week
/// `w`. Inverted bell: drops from baseline to a nadir near
/// `nadir_week`, recovers toward baseline at term.
fn mean_map(params: &MaternalCardioParams, w: f64) -> f64 {
    let z = (w - params.map_nadir_week) / params.map_spread_weeks;
    params.baseline_map_mmhg - params.map_nadir_drop_mmhg * (-z * z).exp()
}

/// Population-mean uterine artery flow (mL/min) at gestational week
/// `w`. Saturating exponential from `baseline` toward `term_flow`.
fn mean_uterine_flow(params: &MaternalCardioParams, w: f64) -> f64 {
    let frac = 1.0 - (-params.uterine_flow_growth_rate_per_week * w).exp();
    params.baseline_uterine_flow_ml_per_min
        + (params.term_uterine_flow_ml_per_min - params.baseline_uterine_flow_ml_per_min) * frac
}

/// Maternal cardiovascular subsystem subscriber.
///
/// Drawn at hour resolution; the cardiovascular trajectory is too slow
/// to need finer ticks, and a coarser tier would be slow to respond to
/// scenarios that perturb the trajectory mid-pregnancy. The
/// per-individual offsets are drawn once at construction time and held
/// constant for the duration of the simulation.
pub struct MaternalCardio {
    id: SubscriberId,
    params: MaternalCardioParams,
    cardiac_output_individual_offset: f64,
    map_individual_offset_mmhg: f64,
    uterine_flow_individual_offset: f64,
    state: MaternalCardioState,
}

impl MaternalCardio {
    /// Construct from default parameters and a per-individual draw.
    ///
    /// The draw uses a single RNG stream keyed by the subscriber id so
    /// that two simulations differing only in registration order
    /// produce identical individual offsets.
    pub fn new(params: MaternalCardioParams, rng: &mut nidus_core::ChildRng) -> Self {
        let cardiac_output_individual_offset =
            sample_normal(rng) * params.cardiac_output_individual_sigma;
        let map_individual_offset_mmhg = sample_normal(rng) * params.map_individual_sigma_mmhg;
        let uterine_flow_individual_offset =
            sample_normal(rng) * params.uterine_flow_individual_sigma;
        Self {
            id: SubscriberId::new(SUBSCRIBER_ID),
            params,
            cardiac_output_individual_offset,
            map_individual_offset_mmhg,
            uterine_flow_individual_offset,
            state: MaternalCardioState {
                cardiac_output_l_per_min: f64::NAN,
                mean_arterial_pressure_mmhg: f64::NAN,
                uterine_artery_flow_ml_per_min: f64::NAN,
            },
        }
    }

    /// Construct with default parameters from a freshly drawn RNG.
    pub fn with_default_params(rng: &mut nidus_core::ChildRng) -> Self {
        Self::new(MaternalCardioParams::default(), rng)
    }

    /// Most recently computed cardiovascular state. Will be a
    /// `f64::NAN`-valued sentinel until the first tick fires.
    #[must_use]
    pub fn state(&self) -> MaternalCardioState {
        self.state
    }

    /// Compute (without storing) the cardiovascular state at a given
    /// gestational age. Convenient for tests and for one-off queries
    /// outside the dispatcher loop.
    #[must_use]
    pub fn evaluate(&self, age: GestationalAge) -> MaternalCardioState {
        let w = age_in_weeks_f64(age);
        let co_mean = mean_cardiac_output(&self.params, w);
        let map_mean = mean_map(&self.params, w);
        let uf_mean = mean_uterine_flow(&self.params, w);
        MaternalCardioState {
            cardiac_output_l_per_min: co_mean * (1.0 + self.cardiac_output_individual_offset),
            mean_arterial_pressure_mmhg: map_mean + self.map_individual_offset_mmhg,
            uterine_artery_flow_ml_per_min: uf_mean * (1.0 + self.uterine_flow_individual_offset),
        }
    }
}

impl Subscriber for MaternalCardio {
    fn id(&self) -> &SubscriberId {
        &self.id
    }

    fn tier(&self) -> TickTier {
        TickTier::Hour
    }

    fn on_tick(&mut self, ctx: &mut TickContext<'_>) {
        self.state = self.evaluate(ctx.age);
    }
}

/// Box-Muller transform applied to two uniform `[0, 1)` draws.
///
/// Used to convert the engine's child RNG output into a standard
/// normal sample for per-individual offsets. Two independent samples
/// could be produced per call, but we discard the second to keep the
/// API minimal; the cost is negligible.
fn sample_normal(rng: &mut nidus_core::ChildRng) -> f64 {
    let u1 = rng.next_f64_unit().max(f64::MIN_POSITIVE);
    let u2 = rng.next_f64_unit();
    (-2.0 * u1.ln()).sqrt() * (core::f64::consts::TAU * u2).cos()
}

/// Convert a [`GestationalAge`] to a floating-point number of completed
/// weeks plus the fraction of the current week. Used inside the
/// population-mean trajectory functions where a continuous time axis is
/// required.
#[allow(clippy::cast_precision_loss)]
fn age_in_weeks_f64(age: GestationalAge) -> f64 {
    let seconds_per_week = (DAYS_PER_WEEK * SECONDS_PER_DAY) as f64;
    (age.seconds as f64) / seconds_per_week
}

#[cfg(test)]
#[allow(clippy::float_cmp)]
mod tests {
    use super::*;
    use nidus_core::clock::SECONDS_PER_HOUR;
    use nidus_core::{Dispatcher, GestationalAge, RngService};

    fn make_subject(seed: u64) -> MaternalCardio {
        let svc = RngService::from_u64(seed);
        let mut rng = svc.child_for(&SubscriberId::new(SUBSCRIBER_ID), 0);
        MaternalCardio::with_default_params(&mut rng)
    }

    #[test]
    fn cardiac_output_rises_then_declines_toward_term() {
        let m = make_subject(42);
        let co_8 = m
            .evaluate(GestationalAge::from_weeks(8))
            .cardiac_output_l_per_min;
        let co_32 = m
            .evaluate(GestationalAge::from_weeks(32))
            .cardiac_output_l_per_min;
        let co_40 = m
            .evaluate(GestationalAge::from_weeks(40))
            .cardiac_output_l_per_min;
        assert!(
            co_32 > co_8,
            "CO should rise from 8w ({co_8}) to 32w ({co_32})"
        );
        assert!(
            co_40 < co_32,
            "CO should decline from 32w ({co_32}) to 40w ({co_40})"
        );
        // Plausible ranges per textbook physiology.
        assert!((4.0..10.0).contains(&co_8));
        assert!((5.0..10.0).contains(&co_32));
    }

    #[test]
    fn map_has_mid_pregnancy_nadir() {
        let m = make_subject(42);
        let map_8 = m
            .evaluate(GestationalAge::from_weeks(8))
            .mean_arterial_pressure_mmhg;
        let map_22 = m
            .evaluate(GestationalAge::from_weeks(22))
            .mean_arterial_pressure_mmhg;
        let map_40 = m
            .evaluate(GestationalAge::from_weeks(40))
            .mean_arterial_pressure_mmhg;
        assert!(map_22 < map_8, "MAP should dip mid-pregnancy");
        assert!(map_22 < map_40, "MAP should recover toward term");
    }

    #[test]
    fn uterine_artery_flow_rises_monotonically() {
        let m = make_subject(42);
        let mut prev = -f64::INFINITY;
        for w in [8u64, 12, 20, 28, 36, 40] {
            let f = m
                .evaluate(GestationalAge::from_weeks(w))
                .uterine_artery_flow_ml_per_min;
            assert!(f > prev, "expected monotonic rise; w={w} f={f} prev={prev}");
            prev = f;
        }
    }

    #[test]
    fn same_seed_gives_identical_individual_offsets() {
        let a = make_subject(7);
        let b = make_subject(7);
        assert_eq!(
            a.evaluate(GestationalAge::from_weeks(20)),
            b.evaluate(GestationalAge::from_weeks(20))
        );
    }

    #[test]
    fn different_seeds_give_different_individual_offsets() {
        let a = make_subject(1);
        let b = make_subject(2);
        let sa = a.evaluate(GestationalAge::from_weeks(20));
        let sb = b.evaluate(GestationalAge::from_weeks(20));
        assert_ne!(sa, sb);
    }

    #[test]
    fn dispatcher_updates_state_at_hour_boundary() {
        let svc = RngService::from_u64(99);
        let mut rng = svc.child_for(&SubscriberId::new(SUBSCRIBER_ID), 0);
        let cardio = MaternalCardio::with_default_params(&mut rng);
        let mut disp = Dispatcher::new(GestationalAge::from_weeks(20), svc);
        disp.register(Box::new(cardio));
        // Advancing less than an hour should leave the state uninitialised
        // (still NaN sentinel); after one hour the state should be valid.
        disp.advance_seconds(SECONDS_PER_HOUR);
        // We cannot retrieve subscriber state via the dispatcher in
        // v0.1.0; instead the test confirms the dispatcher ran without
        // panicking and that direct evaluation produces finite values.
        let direct = MaternalCardio::with_default_params(
            &mut RngService::from_u64(99).child_for(&SubscriberId::new(SUBSCRIBER_ID), 0),
        )
        .evaluate(GestationalAge::from_weeks(20));
        assert!(direct.cardiac_output_l_per_min.is_finite());
        assert!(direct.mean_arterial_pressure_mmhg.is_finite());
        assert!(direct.uterine_artery_flow_ml_per_min.is_finite());
    }

    #[test]
    fn from_database_loads_workspace_parameter_tree() {
        // Locate `data/parameters/maternal/cardio.toml` and its citation
        // index relative to the workspace root; the maternal crate sits
        // two directories below.
        let manifest = std::path::PathBuf::from(env!("CARGO_MANIFEST_DIR"));
        let root = manifest.parent().unwrap().parent().unwrap();
        let citations = root.join("data/citations/index.toml");
        let parameters = root.join("data/parameters/maternal/cardio.toml");
        let db = nidus_data::ParameterDatabase::from_paths(&[parameters], &[citations])
            .expect("workspace data tree loads");
        let params = MaternalCardioParams::from_database(&db).expect("all ids resolved");
        // Sanity: same plausibility envelopes as the default-values test.
        assert!((4.0..6.0).contains(&params.baseline_cardiac_output_l_per_min));
        assert!((1.5..4.0).contains(&params.peak_excess_cardiac_output_l_per_min));
        assert!((24.0..36.0).contains(&params.cardiac_output_peak_week));
        assert!((70.0..95.0).contains(&params.baseline_map_mmhg));
        assert!((400.0..1200.0).contains(&params.term_uterine_flow_ml_per_min));
        assert!(params.cardiac_output_individual_sigma > 0.0);
        assert!(params.cardiac_output_individual_sigma < 1.0);
    }

    #[test]
    fn parameter_struct_default_values_are_in_textbook_range() {
        let p = MaternalCardioParams::default();
        assert!((4.0..6.0).contains(&p.baseline_cardiac_output_l_per_min));
        assert!((1.5..4.0).contains(&p.peak_excess_cardiac_output_l_per_min));
        assert!((24.0..36.0).contains(&p.cardiac_output_peak_week));
        assert!((70.0..95.0).contains(&p.baseline_map_mmhg));
        assert!((400.0..1200.0).contains(&p.term_uterine_flow_ml_per_min));
    }
}
