//! Worked example: sensitivity analysis on the placental gas-exchange
//! model.
//!
//! Treats placental surface area, the half-saturation surface area in
//! the gas-exchange equilibration coefficient, and the maximum
//! equilibration coefficient as the inputs; the analysed outcome is
//! fetal umbilical-vein PO₂ at term under default maternal-arterial
//! and umbilical-artery PO₂ inputs.
//!
//! Run with:
//!
//! ```sh
//! cargo run --release -p nidus-hypothesis --example sensitivity_placental_gas_exchange
//! ```

use nidus_core::tier::ConfidenceTier;
use nidus_hypothesis::{
    ExperimentDesignSuggester, ParameterSpec, SamplingStrategy, SensitivityAnalyser,
    SuggesterParameterInfo,
};

fn main() {
    let specs = vec![
        ParameterSpec::new(
            "surface_area_m2",
            ConfidenceTier::B,
            // Range spans ~25% above and below the scaffold term value
            // of 12 m², capturing the placental-insufficiency regime.
            SamplingStrategy::Uniform {
                low: 9.0,
                high: 15.0,
            },
        ),
        ParameterSpec::new(
            "half_saturation_area_m2",
            ConfidenceTier::C,
            SamplingStrategy::Uniform {
                low: 1.5,
                high: 4.5,
            },
        ),
        ParameterSpec::new(
            "max_equilibration",
            ConfidenceTier::C,
            SamplingStrategy::Uniform {
                low: 0.20,
                high: 0.40,
            },
        ),
    ];

    // Fetal umbilical-vein PO₂ as a function of the three parameters,
    // holding maternal arterial PO₂ = 95 and umbilical-artery (fetal
    // return) PO₂ = 16 fixed.
    let analyser = SensitivityAnalyser::new(specs, 4_000, 7);
    let sensitivity = analyser.analyse(|sample| {
        let area = sample["surface_area_m2"];
        let half_sat = sample["half_saturation_area_m2"];
        let max_eq = sample["max_equilibration"];
        let eff = max_eq * area / (area + half_sat);
        16.0 + eff * (95.0 - 16.0)
    });

    println!("Outcome variance: {:.4}", sensitivity.variance);
    println!(
        "{:32}  {:>5}  {:>9}  {:>9}",
        "parameter", "tier", "S_first", "S_total"
    );
    for (name, idx) in &sensitivity.indices {
        println!(
            "{:32}  {:>5}  {:>9.4}  {:>9.4}",
            name,
            idx.tier.label(),
            idx.first_order,
            idx.total_order
        );
    }

    let suggester = ExperimentDesignSuggester::new()
        .with_info(
            "surface_area_m2",
            SuggesterParameterInfo {
                current_estimate: 12.0,
                current_uncertainty: 3.0,
                outcomes_affected: vec!["fetal-umbilical-vein-PO2".to_owned()],
                available_techniques: vec!["stereological estimation from histology".to_owned()],
            },
        )
        .with_info(
            "half_saturation_area_m2",
            SuggesterParameterInfo {
                current_estimate: 3.0,
                current_uncertainty: 1.5,
                outcomes_affected: vec!["fetal-umbilical-vein-PO2".to_owned()],
                available_techniques: vec![
                    "fit equilibration coefficient against series of cohort UV PO2 \
                     measurements indexed by gestational age"
                        .to_owned(),
                ],
            },
        )
        .with_info(
            "max_equilibration",
            SuggesterParameterInfo {
                current_estimate: 0.28,
                current_uncertainty: 0.10,
                outcomes_affected: vec!["fetal-umbilical-vein-PO2".to_owned()],
                available_techniques: vec!["asymptotic fit of UV PO2 in pregnancies with large \
                     placental surface area"
                    .to_owned()],
            },
        );
    let suggestions = suggester.suggest(&sensitivity);

    println!();
    println!("Ranked experiment-design suggestions:");
    for (rank, s) in suggestions.iter().enumerate() {
        println!(
            "  {}. {} [tier {}] yield={:.4} current={}±{}",
            rank + 1,
            s.parameter_name,
            s.tier.label(),
            s.expected_information_yield,
            s.current_estimate,
            s.current_uncertainty,
        );
    }
}
