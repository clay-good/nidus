//! TOML schema for scenarios.

use std::path::Path;

use serde::{Deserialize, Serialize};
use thiserror::Error;

/// Scenario file (top-level structure).
#[derive(Debug, Clone, Serialize, Deserialize, PartialEq)]
#[serde(deny_unknown_fields)]
pub struct ScenarioSpec {
    /// Free-form name for display.
    pub name: String,
    /// One-line description of what the scenario represents.
    pub description: String,
    /// Gestational age at simulation start, in completed weeks.
    pub start_age_weeks: u64,
    /// Gestational age at simulation end, in completed weeks.
    pub end_age_weeks: u64,
    /// Master RNG seed.
    pub seed: u64,
    /// Cadence (in engine seconds) at which the orchestrator records
    /// snapshots of subscriber state into the
    /// [`crate::orchestrator::ScenarioReport`]. Default one day, which
    /// keeps reports compact while preserving day-scale resolution.
    #[serde(default = "default_record_every_seconds")]
    pub record_every_seconds: u64,
    /// Subscribers to register, in order. Each entry is a kebab-case
    /// component identifier. Recognised values for v0.1.0 are
    /// `"maternal-cardio"`, `"placenta"`, and `"fetal"`. Unknown values
    /// are rejected at orchestration time.
    #[serde(default = "default_subscribers")]
    pub subscribers: Vec<String>,
    /// Per-component parameter overrides applied on top of the default
    /// scaffold values. Used to express pathological scenarios as
    /// perturbations of the normal trajectory without forking the
    /// underlying model code. Each override field is `Option<f64>`;
    /// `None` (the default) means "use the model's default".
    #[serde(default)]
    pub overrides: Overrides,
}

/// Container for per-component parameter overrides.
#[derive(Debug, Clone, Default, Serialize, Deserialize, PartialEq)]
#[serde(deny_unknown_fields, default)]
pub struct Overrides {
    /// Overrides for the maternal cardiovascular subsystem.
    pub maternal_cardio: MaternalCardioOverrides,
    /// Overrides for placental structural development.
    pub placenta_structure: PlacentaStructureOverrides,
    /// Overrides for placental gas exchange.
    pub placenta_gas: PlacentaGasOverrides,
    /// Overrides for the fetal special circulation.
    pub fetal_circulation: FetalCirculationOverrides,
}

/// Optional overrides for [`nidus_maternal::MaternalCardioParams`].
///
/// Field names mirror the parameter struct so the override is
/// self-documenting. Any field set to `Some(value)` replaces the
/// default; `None` leaves it untouched.
#[derive(Debug, Clone, Copy, Default, Serialize, Deserialize, PartialEq)]
#[serde(deny_unknown_fields, default)]
#[allow(missing_docs)]
pub struct MaternalCardioOverrides {
    pub baseline_cardiac_output_l_per_min: Option<f64>,
    pub peak_excess_cardiac_output_l_per_min: Option<f64>,
    pub cardiac_output_peak_week: Option<f64>,
    pub cardiac_output_spread_weeks: Option<f64>,
    pub cardiac_output_individual_sigma: Option<f64>,
    pub baseline_map_mmhg: Option<f64>,
    pub map_nadir_drop_mmhg: Option<f64>,
    pub map_nadir_week: Option<f64>,
    pub map_spread_weeks: Option<f64>,
    pub map_individual_sigma_mmhg: Option<f64>,
    pub baseline_uterine_flow_ml_per_min: Option<f64>,
    pub term_uterine_flow_ml_per_min: Option<f64>,
    pub uterine_flow_growth_rate_per_week: Option<f64>,
    pub uterine_flow_individual_sigma: Option<f64>,
}

/// Optional overrides for [`nidus_placenta::StructureParams`].
#[derive(Debug, Clone, Copy, Default, Serialize, Deserialize, PartialEq)]
#[serde(deny_unknown_fields, default)]
#[allow(missing_docs)]
pub struct PlacentaStructureOverrides {
    pub initial_area_m2: Option<f64>,
    pub term_area_m2: Option<f64>,
    pub midpoint_week: Option<f64>,
    pub growth_rate_per_week: Option<f64>,
}

/// Optional overrides for [`nidus_placenta::GasExchangeParams`].
#[derive(Debug, Clone, Copy, Default, Serialize, Deserialize, PartialEq)]
#[serde(deny_unknown_fields, default)]
#[allow(missing_docs)]
pub struct PlacentaGasOverrides {
    pub half_saturation_area_m2: Option<f64>,
    pub max_equilibration: Option<f64>,
}

/// Optional overrides for [`nidus_fetal::FetalCirculationParams`].
#[derive(Debug, Clone, Copy, Default, Serialize, Deserialize, PartialEq)]
#[serde(deny_unknown_fields, default)]
#[allow(missing_docs)]
pub struct FetalCirculationOverrides {
    pub foramen_ovale_streamline_preference: Option<f64>,
    pub ductus_arteriosus_share: Option<f64>,
    pub systemic_venous_return_po2_mmhg: Option<f64>,
}

const fn default_record_every_seconds() -> u64 {
    nidus_core::clock::SECONDS_PER_DAY
}

fn default_subscribers() -> Vec<String> {
    vec![
        "maternal-cardio".to_owned(),
        "placenta".to_owned(),
        "fetal".to_owned(),
    ]
}

/// Errors raised by the scenario loader.
#[derive(Debug, Error)]
pub enum ScenarioError {
    /// I/O error reading the scenario file.
    #[error("failed to read scenario file: {0}")]
    Io(#[from] std::io::Error),
    /// TOML parse error.
    #[error("failed to parse scenario TOML: {0}")]
    Parse(#[from] toml::de::Error),
    /// Schema-level validation error (e.g. end before start).
    #[error("invalid scenario: {0}")]
    Invalid(String),
    /// Subscriber identifier did not match any known component.
    #[error("unknown subscriber `{0}` in scenario")]
    UnknownSubscriber(String),
}

/// Parse and validate a scenario from a TOML string.
pub fn load_scenario_from_str(text: &str) -> Result<ScenarioSpec, ScenarioError> {
    let spec: ScenarioSpec = toml::from_str(text)?;
    validate(&spec)?;
    Ok(spec)
}

/// Read a scenario from a file and validate it.
pub fn load_scenario_from_path(path: &Path) -> Result<ScenarioSpec, ScenarioError> {
    let text = std::fs::read_to_string(path)?;
    load_scenario_from_str(&text)
}

fn validate(spec: &ScenarioSpec) -> Result<(), ScenarioError> {
    if spec.start_age_weeks < 8 {
        return Err(ScenarioError::Invalid(format!(
            "start_age_weeks ({}) is below the simulator's supported lower bound of 8 weeks",
            spec.start_age_weeks
        )));
    }
    if spec.end_age_weeks > 40 {
        return Err(ScenarioError::Invalid(format!(
            "end_age_weeks ({}) is above the simulator's supported upper bound of 40 weeks",
            spec.end_age_weeks
        )));
    }
    if spec.end_age_weeks <= spec.start_age_weeks {
        return Err(ScenarioError::Invalid(format!(
            "end_age_weeks ({}) must exceed start_age_weeks ({})",
            spec.end_age_weeks, spec.start_age_weeks
        )));
    }
    if spec.record_every_seconds == 0 {
        return Err(ScenarioError::Invalid(
            "record_every_seconds must be positive".to_owned(),
        ));
    }
    for sub in &spec.subscribers {
        if !is_known_subscriber(sub) {
            return Err(ScenarioError::UnknownSubscriber(sub.clone()));
        }
    }
    Ok(())
}

fn is_known_subscriber(id: &str) -> bool {
    matches!(id, "maternal-cardio" | "placenta" | "fetal")
}

#[cfg(test)]
mod tests {
    use super::*;

    const NORMAL: &str = r#"
name = "Normal term pregnancy"
description = "Default scaffold scenario."
start_age_weeks = 8
end_age_weeks = 40
seed = 0
"#;

    #[test]
    fn loads_with_default_subscribers() {
        let spec = load_scenario_from_str(NORMAL).unwrap();
        assert_eq!(spec.subscribers.len(), 3);
        assert_eq!(
            spec.record_every_seconds,
            nidus_core::clock::SECONDS_PER_DAY
        );
    }

    #[test]
    fn rejects_start_age_below_8_weeks() {
        let s = NORMAL.replace("start_age_weeks = 8", "start_age_weeks = 4");
        assert!(matches!(
            load_scenario_from_str(&s),
            Err(ScenarioError::Invalid(_))
        ));
    }

    #[test]
    fn rejects_end_before_start() {
        let s = NORMAL.replace("end_age_weeks = 40", "end_age_weeks = 8");
        assert!(matches!(
            load_scenario_from_str(&s),
            Err(ScenarioError::Invalid(_))
        ));
    }

    #[test]
    fn rejects_unknown_subscriber() {
        let s = format!("{NORMAL}\nsubscribers = [\"not-a-subscriber\"]\n");
        assert!(matches!(
            load_scenario_from_str(&s),
            Err(ScenarioError::UnknownSubscriber(_))
        ));
    }

    #[test]
    fn rejects_unknown_fields() {
        let s = format!("{NORMAL}\nextra = \"oops\"\n");
        assert!(matches!(
            load_scenario_from_str(&s),
            Err(ScenarioError::Parse(_))
        ));
    }
}
