//! Placental transport: gas exchange and facilitated glucose diffusion.
//!
//! The two functions in this module compose with the structural
//! surface-area trajectory ([`crate::structure`]) to couple the
//! maternal and fetal subsystems.
//!
//! `gas_exchange` produces a fetal umbilical-vein PO₂ by interpolating
//! between the fetal umbilical-artery (return) PO₂ and the maternal
//! arterial PO₂ with an equilibration coefficient that grows with
//! exchange surface area. The coefficient saturates at a documented
//! maximum below 1.0, reflecting the venous-equilibrator regime of the
//! human placenta — fetal umbilical-vein PO₂ never reaches maternal
//! arterial PO₂.
//!
//! `glucose_flux_mmol_per_min` applies Michaelis–Menten kinetics to a
//! net facilitated-diffusion model: GLUT1- and GLUT3-class transporters
//! move glucose down the concentration gradient between maternal and
//! fetal sides, with the rate determined by the difference of
//! `[s] / (Km + [s])` on the two sides scaled by `Vmax` and surface
//! area.
//!
//! Like every other quantity in this crate, the default parameters are
//! scaffolding values pending citation-bearing entries in the parameter
//! database (SPEC.md §9).

use nidus_data::{DatabaseError, ParameterDatabase};

/// Database ids consumed by [`GasExchangeParams::from_database`] and
/// [`GlucoseTransportParams::from_database`].
pub mod param_ids {
    /// Half-saturation surface area (m²) of the saturable equilibrator.
    pub const GAS_HALF_SAT_AREA: &str = "placenta-gas-half-saturation-area-m2";
    /// Maximum venous-equilibrator fraction (dimensionless).
    pub const GAS_MAX_EQUILIBRATION: &str = "placenta-gas-max-equilibration";
    /// GLUT1 Km (mmol/L).
    pub const GLUT1_KM: &str = "placenta-glucose-glut1-km-mmol-per-l";
    /// GLUT1 Vmax per unit area (mmol/min/m²).
    pub const GLUT1_VMAX_PER_AREA: &str =
        "placenta-glucose-glut1-vmax-per-area-mmol-per-min-per-m2";
    /// GLUT3 Km (mmol/L).
    pub const GLUT3_KM: &str = "placenta-glucose-glut3-km-mmol-per-l";
    /// GLUT3 Vmax per unit area (mmol/min/m²).
    pub const GLUT3_VMAX_PER_AREA: &str =
        "placenta-glucose-glut3-vmax-per-area-mmol-per-min-per-m2";
}

/// Coefficients for the placental gas-exchange model.
#[derive(Debug, Clone, Copy, PartialEq)]
pub struct GasExchangeParams {
    /// Half-saturation surface area (m²) at which the equilibration
    /// coefficient reaches half its asymptotic maximum.
    pub half_saturation_area_m2: f64,
    /// Maximum equilibration coefficient (dimensionless, `[0, 1)`).
    /// The placenta is a venous equilibrator, so this is bounded
    /// strictly below 1.
    pub max_equilibration: f64,
}

impl Default for GasExchangeParams {
    fn default() -> Self {
        // Scaffolding constants. Each must be replaced with a
        // database-resolved citation-bearing parameter before
        // publication; see SPEC.md §9 and CONTRIBUTING.md.
        Self {
            half_saturation_area_m2: 3.0,
            max_equilibration: 0.28,
        }
    }
}

impl GasExchangeParams {
    /// Construct from point-estimate values resolved against a loaded
    /// [`ParameterDatabase`].
    pub fn from_database(db: &ParameterDatabase) -> Result<Self, DatabaseError> {
        Ok(Self {
            half_saturation_area_m2: db.point_estimate(param_ids::GAS_HALF_SAT_AREA)?,
            max_equilibration: db.point_estimate(param_ids::GAS_MAX_EQUILIBRATION)?,
        })
    }
}

/// Compute fetal umbilical-vein PO₂ from the surrounding conditions.
///
/// All pressures are in mmHg. `surface_area_m2` is the current
/// placental exchange surface area; pass the output of
/// [`crate::structure::placental_surface_area_m2`].
///
/// The model:
///
/// ```text
/// eff = max_equilibration * area / (area + half_saturation_area)
/// UV_PO2 = umbilical_artery_PO2 + eff * (maternal_arterial_PO2 - umbilical_artery_PO2)
/// ```
///
/// At small surface areas (early gestation, severe placental
/// insufficiency) the equilibration coefficient is small and the fetal
/// umbilical-vein PO₂ stays near the fetal umbilical-artery return
/// PO₂. At larger surface areas the coefficient saturates at
/// `max_equilibration`, never reaching unity — fetal blood does not
/// fully equilibrate with maternal arterial PO₂.
#[must_use]
pub fn gas_exchange(
    params: &GasExchangeParams,
    maternal_arterial_po2_mmhg: f64,
    umbilical_artery_po2_mmhg: f64,
    surface_area_m2: f64,
) -> f64 {
    let area = surface_area_m2.max(0.0);
    let eff = params.max_equilibration * area / (area + params.half_saturation_area_m2);
    umbilical_artery_po2_mmhg + eff * (maternal_arterial_po2_mmhg - umbilical_artery_po2_mmhg)
}

/// Coefficients for the placental glucose transport model.
#[derive(Debug, Clone, Copy, PartialEq)]
pub struct GlucoseTransportParams {
    /// Michaelis constant of the placental glucose transporters,
    /// mmol/L. GLUT1 is dominant on the maternal-facing membrane and
    /// has a Km in the low-millimolar range.
    pub km_mmol_per_l: f64,
    /// Maximum velocity per unit surface area, mmol/(min · m²).
    pub vmax_per_area_mmol_per_min_per_m2: f64,
}

impl Default for GlucoseTransportParams {
    fn default() -> Self {
        // Scaffolding constants. Each must be replaced with a
        // database-resolved citation-bearing parameter before
        // publication; see SPEC.md §9 and CONTRIBUTING.md.
        Self {
            km_mmol_per_l: 5.0,
            vmax_per_area_mmol_per_min_per_m2: 0.5,
        }
    }
}

impl GlucoseTransportParams {
    /// Construct from point-estimate values resolved against a loaded
    /// [`ParameterDatabase`].
    ///
    /// The single-pool model collapses GLUT1 (maternal microvillous,
    /// dominant) and GLUT3 (basal) into one Michaelis–Menten kinetic.
    /// `Km` is taken from GLUT1 (the rate-limiting transporter for
    /// maternal-to-fetal flux); `Vmax` is the sum of the two per-area
    /// rates, since the transporters act in parallel.
    pub fn from_database(db: &ParameterDatabase) -> Result<Self, DatabaseError> {
        let vmax_glut1 = db.point_estimate(param_ids::GLUT1_VMAX_PER_AREA)?;
        let vmax_glut3 = db.point_estimate(param_ids::GLUT3_VMAX_PER_AREA)?;
        Ok(Self {
            km_mmol_per_l: db.point_estimate(param_ids::GLUT1_KM)?,
            vmax_per_area_mmol_per_min_per_m2: vmax_glut1 + vmax_glut3,
        })
    }
}

/// Net maternal-to-fetal glucose flux, mmol/min.
///
/// Positive values indicate net transfer from maternal to fetal side.
/// The function is symmetric under swap of maternal and fetal
/// concentrations (with a sign change), so it correctly returns
/// negative flux for the unusual case of higher fetal than maternal
/// glucose.
#[must_use]
pub fn glucose_flux_mmol_per_min(
    params: &GlucoseTransportParams,
    maternal_glucose_mmol_per_l: f64,
    fetal_glucose_mmol_per_l: f64,
    surface_area_m2: f64,
) -> f64 {
    let mat_term =
        maternal_glucose_mmol_per_l / (params.km_mmol_per_l + maternal_glucose_mmol_per_l);
    let fet_term = fetal_glucose_mmol_per_l / (params.km_mmol_per_l + fetal_glucose_mmol_per_l);
    params.vmax_per_area_mmol_per_min_per_m2 * surface_area_m2 * (mat_term - fet_term)
}

#[cfg(test)]
#[allow(clippy::float_cmp)]
mod tests {
    use super::*;
    use crate::structure::{placental_surface_area_m2, StructureParams};
    use nidus_core::clock::GestationalAge;

    #[test]
    fn fetal_umbilical_vein_po2_within_published_range_at_term() {
        let gas = GasExchangeParams::default();
        let area =
            placental_surface_area_m2(&StructureParams::default(), GestationalAge::from_weeks(40));
        // Standard maternal arterial PO2 ~95 mmHg; fetal umbilical
        // artery return ~16 mmHg.
        let uv = gas_exchange(&gas, 95.0, 16.0, area);
        // Published umbilical-vein PO2 at term is roughly 25–40 mmHg.
        assert!((25.0..40.0).contains(&uv), "UV PO2 out of range: {uv}");
    }

    #[test]
    fn smaller_surface_area_produces_growth_restriction_pattern() {
        let gas = GasExchangeParams::default();
        let term_area =
            placental_surface_area_m2(&StructureParams::default(), GestationalAge::from_weeks(40));
        let healthy_uv = gas_exchange(&gas, 95.0, 16.0, term_area);
        let insufficient_uv = gas_exchange(&gas, 95.0, 16.0, term_area * 0.4);
        assert!(
            insufficient_uv < healthy_uv,
            "expected reduced UV PO2 under placental insufficiency: \
             healthy={healthy_uv} insufficient={insufficient_uv}"
        );
    }

    #[test]
    fn gas_exchange_never_reaches_maternal_arterial_po2() {
        let gas = GasExchangeParams::default();
        let absurd_area = 1000.0;
        let uv = gas_exchange(&gas, 95.0, 16.0, absurd_area);
        assert!(
            uv < 95.0,
            "venous-equilibrator model must bound UV below maternal"
        );
    }

    #[test]
    fn glucose_flux_is_positive_when_maternal_exceeds_fetal() {
        let p = GlucoseTransportParams::default();
        let flux = glucose_flux_mmol_per_min(&p, 5.0, 3.5, 10.0);
        assert!(flux > 0.0, "expected positive net flux to fetus: {flux}");
    }

    #[test]
    fn glucose_flux_reverses_sign_with_gradient() {
        let p = GlucoseTransportParams::default();
        let forward = glucose_flux_mmol_per_min(&p, 5.0, 3.5, 10.0);
        let reverse = glucose_flux_mmol_per_min(&p, 3.5, 5.0, 10.0);
        assert!(forward > 0.0);
        assert!(reverse < 0.0);
        assert!((forward + reverse).abs() < 1e-12);
    }

    #[test]
    fn glucose_flux_saturates_at_high_concentration() {
        let p = GlucoseTransportParams::default();
        let low = glucose_flux_mmol_per_min(&p, 5.0, 0.0, 10.0);
        let high = glucose_flux_mmol_per_min(&p, 500.0, 0.0, 10.0);
        // Saturated Michaelis-Menten kinetics cap the flux at Vmax * area,
        // so the high-concentration flux must not exceed that cap.
        let cap = p.vmax_per_area_mmol_per_min_per_m2 * 10.0;
        assert!(high <= cap + 1e-9);
        assert!(high > low);
    }
}
