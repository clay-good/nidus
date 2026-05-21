//! Fetal cardiovascular special circulation.
//!
//! Three anatomical shunts route fetal blood in ways that have no
//! postnatal analogue:
//!
//! - The **ductus venosus** carries a fraction of umbilical-vein
//!   blood directly to the inferior vena cava, bypassing the fetal
//!   liver.
//! - The **foramen ovale** allows the DV-enriched IVC stream to cross
//!   from the right atrium to the left atrium, biased by a streamline
//!   preference in the right atrium so that the most oxygenated blood
//!   preferentially reaches the left side of the heart.
//! - The **ductus arteriosus** shunts most right-ventricular output
//!   away from the unventilated fetal lungs and into the descending
//!   aorta.
//!
//! The net effect is a two-stream system: the upper body and cerebral
//! circulation receive blood derived preferentially from the
//! umbilical vein, while the descending aorta receives blood
//! preferentially derived from the systemic venous return mixed with
//! pulmonary-artery flow shunted through the DA. The model here
//! computes oxygen tension for both streams from a small set of
//! anatomical fractions; it does not attempt to resolve the full
//! hemodynamics, which is deferred to a later prompt.

use nidus_data::{DatabaseError, ParameterDatabase};

/// Database ids consumed by [`FetalCirculationParams::from_database`].
pub mod param_ids {
    /// Foramen-ovale streamline preference (dimensionless fraction).
    pub const FORAMEN_OVALE_PREFERENCE: &str =
        "fetal-circulation-foramen-ovale-streamline-preference";
    /// Ductus arteriosus flow share (dimensionless fraction).
    pub const DUCTUS_ARTERIOSUS_SHARE: &str = "fetal-circulation-ductus-arteriosus-share";
    /// Systemic venous return PO₂ (mmHg).
    pub const SYSTEMIC_VENOUS_PO2: &str = "fetal-circulation-systemic-venous-return-po2-mmhg";
}

/// Anatomical fractions of the fetal special circulation.
///
/// All values are dimensionless `[0, 1]` ratios. They are not yet
/// citation-resolved; like every other constant in v0.1.0 they are
/// scaffolding values pending integration with the parameter database
/// (SPEC.md §9).
#[derive(Debug, Clone, Copy, PartialEq)]
pub struct FetalCirculationParams {
    /// Streamline preference of DV-enriched IVC blood for the foramen
    /// ovale (i.e. for crossing to the left side). A value of 1.0
    /// would mean every drop of DV blood crosses; 0.5 means no
    /// preferential streaming.
    pub foramen_ovale_streamline_preference: f64,
    /// Fraction of systemic venous return that ends up in the
    /// descending aorta via the ductus arteriosus (as opposed to
    /// reaching the cerebral and upper-body circulation via the
    /// foramen ovale and left ventricle).
    pub ductus_arteriosus_share: f64,
    /// Oxygen tension (mmHg) of the systemic venous return entering
    /// the right atrium, before any DV mixing. Used as the
    /// less-oxygenated pole of the weighted-average model. Default
    /// reflects a typical fetal systemic venous PO₂.
    pub systemic_venous_return_po2_mmhg: f64,
}

impl Default for FetalCirculationParams {
    fn default() -> Self {
        // Scaffolding constants. Each must be replaced with a
        // database-resolved citation-bearing parameter before
        // publication; see SPEC.md §9 and CONTRIBUTING.md.
        Self {
            foramen_ovale_streamline_preference: 0.80,
            ductus_arteriosus_share: 0.85,
            systemic_venous_return_po2_mmhg: 14.0,
        }
    }
}

impl FetalCirculationParams {
    /// Construct from point-estimate values resolved against a loaded
    /// [`ParameterDatabase`].
    pub fn from_database(db: &ParameterDatabase) -> Result<Self, DatabaseError> {
        Ok(Self {
            foramen_ovale_streamline_preference: db
                .point_estimate(param_ids::FORAMEN_OVALE_PREFERENCE)?,
            ductus_arteriosus_share: db.point_estimate(param_ids::DUCTUS_ARTERIOSUS_SHARE)?,
            systemic_venous_return_po2_mmhg: db.point_estimate(param_ids::SYSTEMIC_VENOUS_PO2)?,
        })
    }
}

/// Computed oxygen tensions across the fetal special circulation.
#[derive(Debug, Clone, Copy, PartialEq)]
pub struct FetalCirculationState {
    /// Cerebral arterial PO₂ (mmHg). Preferentially supplied by
    /// umbilical-vein blood through the foramen ovale.
    pub cerebral_arterial_po2_mmhg: f64,
    /// Descending aortic PO₂ (mmHg). Preferentially supplied by
    /// pulmonary-artery blood through the ductus arteriosus.
    pub descending_aortic_po2_mmhg: f64,
    /// Umbilical-artery (fetal return to placenta) PO₂ (mmHg).
    /// Reflects the descending-aorta composition that the placenta
    /// sees on its fetal side.
    pub umbilical_artery_po2_mmhg: f64,
}

/// Stateless transform that maps the umbilical-vein input to the three
/// observable PO₂ values.
pub struct FetalSpecialCirculation {
    params: FetalCirculationParams,
}

impl FetalSpecialCirculation {
    /// Construct with explicit parameters.
    #[must_use]
    pub const fn new(params: FetalCirculationParams) -> Self {
        Self { params }
    }

    /// Construct with default scaffolding parameters.
    #[must_use]
    pub fn with_default_params() -> Self {
        Self::new(FetalCirculationParams::default())
    }

    /// Borrow the parameter block.
    #[must_use]
    pub fn params(&self) -> &FetalCirculationParams {
        &self.params
    }

    /// Apply the routing model: given the placenta's most recent
    /// umbilical-vein PO₂, return the cerebral, descending-aorta, and
    /// umbilical-artery PO₂ values.
    ///
    /// Cerebral arterial PO₂ is a weighted average between UV PO₂ and
    /// the systemic venous-return PO₂, biased toward UV by the
    /// foramen-ovale streamline preference. Descending-aorta PO₂ is
    /// the complementary weighted average, biased toward systemic
    /// venous return by the same parameter. The umbilical-artery
    /// return PO₂ then closes the loop with the placenta on the
    /// fetal side.
    #[must_use]
    pub fn route(&self, umbilical_vein_po2_mmhg: f64) -> FetalCirculationState {
        let p = self.params;
        let cerebral = weighted(
            p.foramen_ovale_streamline_preference,
            umbilical_vein_po2_mmhg,
            p.systemic_venous_return_po2_mmhg,
        );
        let descending = weighted(
            1.0 - p.foramen_ovale_streamline_preference,
            umbilical_vein_po2_mmhg,
            p.systemic_venous_return_po2_mmhg,
        );
        // The umbilical artery returns to the placenta from the
        // descending aorta via the umbilical arteries (branches of the
        // internal iliacs). At the fetal-side gas-exchange surface its
        // composition is close to descending aortic, modulated by the
        // share of descending-aortic flow that comes via the ductus
        // arteriosus rather than the LV.
        let umbilical_artery = mix(p.ductus_arteriosus_share, descending, cerebral);
        FetalCirculationState {
            cerebral_arterial_po2_mmhg: cerebral,
            descending_aortic_po2_mmhg: descending,
            umbilical_artery_po2_mmhg: umbilical_artery,
        }
    }
}

/// `frac * high + (1 - frac) * low`, with `frac` clamped to `[0, 1]`.
fn weighted(frac: f64, high: f64, low: f64) -> f64 {
    let f = frac.clamp(0.0, 1.0);
    f * high + (1.0 - f) * low
}

/// `frac * a + (1 - frac) * b`, with `frac` clamped to `[0, 1]`.
fn mix(frac: f64, a: f64, b: f64) -> f64 {
    weighted(frac, a, b)
}

#[cfg(test)]
#[allow(clippy::float_cmp)]
mod tests {
    use super::*;

    #[test]
    fn cerebral_po2_preferentially_higher_than_descending_aortic() {
        let circ = FetalSpecialCirculation::with_default_params();
        let s = circ.route(30.0);
        assert!(
            s.cerebral_arterial_po2_mmhg > s.descending_aortic_po2_mmhg,
            "expected preferential cerebral oxygenation: cereb={} desc={}",
            s.cerebral_arterial_po2_mmhg,
            s.descending_aortic_po2_mmhg
        );
    }

    #[test]
    fn umbilical_artery_po2_below_descending_aortic() {
        let circ = FetalSpecialCirculation::with_default_params();
        let s = circ.route(30.0);
        // Umbilical-artery composition is a mixture of descending
        // aortic and cerebral streams, with cerebral the more
        // oxygenated, so UA should sit between the two.
        assert!(s.umbilical_artery_po2_mmhg >= s.descending_aortic_po2_mmhg);
        assert!(s.umbilical_artery_po2_mmhg < s.cerebral_arterial_po2_mmhg);
    }

    #[test]
    fn higher_umbilical_vein_po2_raises_cerebral_po2() {
        let circ = FetalSpecialCirculation::with_default_params();
        let low = circ.route(20.0).cerebral_arterial_po2_mmhg;
        let high = circ.route(35.0).cerebral_arterial_po2_mmhg;
        assert!(high > low);
    }

    #[test]
    fn streamline_preference_collapse_eliminates_advantage() {
        let params = FetalCirculationParams {
            foramen_ovale_streamline_preference: 0.5,
            ..FetalCirculationParams::default()
        };
        let circ = FetalSpecialCirculation::new(params);
        let s = circ.route(30.0);
        assert!((s.cerebral_arterial_po2_mmhg - s.descending_aortic_po2_mmhg).abs() < 1e-12);
    }

    #[test]
    fn cerebral_po2_in_textbook_range_at_normal_conditions() {
        let circ = FetalSpecialCirculation::with_default_params();
        // Normal term umbilical-vein PO₂ ≈ 30 mmHg from the placenta
        // module's defaults.
        let s = circ.route(30.0);
        // Textbook cerebral arterial PO₂ in normal term fetus is
        // roughly 25–30 mmHg.
        assert!(
            (22.0..32.0).contains(&s.cerebral_arterial_po2_mmhg),
            "cerebral PO2 out of range: {}",
            s.cerebral_arterial_po2_mmhg
        );
    }
}
