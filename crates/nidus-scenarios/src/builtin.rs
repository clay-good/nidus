//! Built-in scenario TOML strings.
//!
//! These are compiled-in for convenience so the CLI can offer a smoke
//! test (`nidus run`) without depending on the on-disk `scenarios/`
//! directory. The on-disk versions of the same scenarios live under
//! `scenarios/` in the repository root for users to copy and edit.

/// A scaffold "normal singleton pregnancy" scenario: 8 → 40 weeks,
/// seed 0, all v0.1.0 subscribers active, daily recording cadence.
pub const NORMAL_TERM_PREGNANCY: &str = r#"
name = "Normal term pregnancy"
description = "Default scaffold scenario: singleton pregnancy from 8 to 40 weeks, all v0.1.0 subscribers active. Constants throughout are scaffolding values pending parameter-database integration (see CONTRIBUTING.md)."
start_age_weeks = 8
end_age_weeks = 40
seed = 0
subscribers = ["maternal-cardio", "placenta", "fetal"]
"#;

/// Placental insufficiency: term placental surface area reduced from
/// the scaffold default. Reproduces the qualitative pattern of reduced
/// fetal umbilical-vein PO₂ and depressed cerebral PO₂ associated with
/// growth restriction. Scaffold values; pending parameter-database
/// integration.
pub const PLACENTAL_INSUFFICIENCY: &str = r#"
name = "Placental insufficiency"
description = "Placental insufficiency modelled as a reduction in effective term placental exchange surface area (scaffold values; pending parameter-database integration)."
start_age_weeks = 8
end_age_weeks = 40
seed = 0
subscribers = ["maternal-cardio", "placenta", "fetal"]

[overrides.placenta_structure]
term_area_m2 = 6.0
"#;

/// Mild preeclampsia: elevated maternal MAP baseline with attenuated
/// mid-pregnancy nadir, plus a moderate reduction in placental surface
/// area. Scaffold values; pending parameter-database integration.
pub const MILD_PREECLAMPSIA: &str = r#"
name = "Mild preeclampsia"
description = "Mild preeclampsia modelled as elevated maternal MAP plus moderately reduced placental surface area (scaffold values; pending parameter-database integration)."
start_age_weeks = 8
end_age_weeks = 40
seed = 0
subscribers = ["maternal-cardio", "placenta", "fetal"]

[overrides.maternal_cardio]
baseline_map_mmhg = 100.0
map_nadir_drop_mmhg = 4.0

[overrides.placenta_structure]
term_area_m2 = 9.0
"#;

#[cfg(test)]
mod tests {
    use super::*;
    use crate::spec::load_scenario_from_str;

    #[test]
    fn builtin_normal_term_pregnancy_parses() {
        let spec = load_scenario_from_str(NORMAL_TERM_PREGNANCY).unwrap();
        assert_eq!(spec.start_age_weeks, 8);
        assert_eq!(spec.end_age_weeks, 40);
    }

    #[test]
    fn builtin_placental_insufficiency_parses_and_overrides_area() {
        let spec = load_scenario_from_str(PLACENTAL_INSUFFICIENCY).unwrap();
        assert_eq!(spec.overrides.placenta_structure.term_area_m2, Some(6.0));
    }

    #[test]
    fn builtin_mild_preeclampsia_parses_and_overrides_map() {
        let spec = load_scenario_from_str(MILD_PREECLAMPSIA).unwrap();
        assert_eq!(
            spec.overrides.maternal_cardio.baseline_map_mmhg,
            Some(100.0)
        );
        assert_eq!(spec.overrides.placenta_structure.term_area_m2, Some(9.0));
    }
}
