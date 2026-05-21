//! Confidence tiers.
//!
//! Every modelled quantity in Nidus belongs to one of four tiers. The tier
//! system is structural to the model, not documentation about it: tiers
//! propagate through computations so that any output derived from a less
//! confident input cannot itself be more confident than that input
//! (SPEC.md §3).

use core::cmp::Ordering;
use core::fmt;

/// The four confidence tiers used throughout Nidus.
///
/// The numeric discriminant is meaningful: lower values are more confident.
/// `A < B < C < D` under the derived [`Ord`] implementation, so the
/// less-confident tier (the one a derived value must take) is the
/// [`ConfidenceTier::max`] of its inputs — captured here by
/// [`ConfidenceTier::combine`].
#[derive(Debug, Clone, Copy, PartialEq, Eq, Hash)]
#[cfg_attr(feature = "serde", derive(serde::Serialize, serde::Deserialize))]
#[repr(u8)]
pub enum ConfidenceTier {
    /// Well-characterised mechanism with precise parameters across multiple
    /// independent studies (e.g. oxygen–haemoglobin dissociation,
    /// Fickian gas diffusion across known membranes).
    A = 0,
    /// Understood mechanism with parameter uncertainty by population,
    /// gestational age, individual, or measurement technique (e.g.
    /// placental surface area development).
    B = 1,
    /// Phenomenology without mechanism: observational data without a
    /// first-principles predictive model (e.g. maternal cortisol patterns
    /// on fetal HPA axis development).
    C = 2,
    /// Speculation and unknowns: suspected to be important but not well
    /// characterised (e.g. specific exosomal microRNA cargo effects).
    D = 3,
}

impl ConfidenceTier {
    /// Returns the less-confident of two tiers.
    ///
    /// This is the propagation rule: a value derived from inputs of tiers
    /// `t1` and `t2` has tier `t1.combine(t2)`.
    #[must_use]
    pub const fn combine(self, other: Self) -> Self {
        if (self as u8) >= (other as u8) {
            self
        } else {
            other
        }
    }

    /// Short single-letter label, suitable for compact display.
    #[must_use]
    pub const fn label(self) -> &'static str {
        match self {
            Self::A => "A",
            Self::B => "B",
            Self::C => "C",
            Self::D => "D",
        }
    }
}

impl PartialOrd for ConfidenceTier {
    fn partial_cmp(&self, other: &Self) -> Option<Ordering> {
        Some(self.cmp(other))
    }
}

impl Ord for ConfidenceTier {
    fn cmp(&self, other: &Self) -> Ordering {
        (*self as u8).cmp(&(*other as u8))
    }
}

impl fmt::Display for ConfidenceTier {
    fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {
        f.write_str(self.label())
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn combine_returns_less_confident_tier() {
        assert_eq!(
            ConfidenceTier::A.combine(ConfidenceTier::A),
            ConfidenceTier::A
        );
        assert_eq!(
            ConfidenceTier::A.combine(ConfidenceTier::B),
            ConfidenceTier::B
        );
        assert_eq!(
            ConfidenceTier::C.combine(ConfidenceTier::B),
            ConfidenceTier::C
        );
        assert_eq!(
            ConfidenceTier::D.combine(ConfidenceTier::A),
            ConfidenceTier::D
        );
    }

    #[test]
    fn ordering_matches_confidence() {
        assert!(ConfidenceTier::A < ConfidenceTier::B);
        assert!(ConfidenceTier::B < ConfidenceTier::C);
        assert!(ConfidenceTier::C < ConfidenceTier::D);
    }
}
