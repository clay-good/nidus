//! Tiered values: a generic wrapper that pairs a quantity with its
//! confidence tier and a citation reference, with arithmetic that
//! propagates the less-confident tier to derived values.
//!
//! The tier propagation rule (SPEC.md §3) is the load-bearing invariant
//! here: a value computed from inputs at tiers `t1` and `t2` is published
//! at `t1.combine(t2)`. Arithmetic on `Tiered<T>` enforces this
//! automatically.
//!
//! Citations are tracked as a vector of [`CitationId`] references. When
//! two tiered values combine, the resulting citation set is the union of
//! both inputs — every source that contributed to the derived value
//! remains attached to it. This is what makes simulator output auditable
//! back to original literature.

use core::ops::{Add, Div, Mul, Neg, Sub};

use crate::citation::CitationId;
use crate::tier::ConfidenceTier;

/// A value paired with its confidence tier and contributing citations.
///
/// Arithmetic operators are defined where the underlying type supports
/// them; the resulting [`ConfidenceTier`] is the less-confident of the
/// two inputs, and the citation list is the deduplicated union.
#[derive(Debug, Clone, PartialEq, Eq)]
#[cfg_attr(feature = "serde", derive(serde::Serialize, serde::Deserialize))]
pub struct Tiered<T> {
    /// The underlying value.
    pub value: T,
    /// The confidence tier of this value.
    pub tier: ConfidenceTier,
    /// Citations supporting the value.
    pub citations: Vec<CitationId>,
}

impl<T> Tiered<T> {
    /// Construct a new tiered value with one supporting citation.
    pub fn new(value: T, tier: ConfidenceTier, citation: CitationId) -> Self {
        Self {
            value,
            tier,
            citations: vec![citation],
        }
    }

    /// Construct a tiered value with no citations.
    ///
    /// Useful for intermediate values created inside the engine that have
    /// not yet been associated with a published source. Avoid using this
    /// for published parameters; those must always carry a citation.
    pub fn uncited(value: T, tier: ConfidenceTier) -> Self {
        Self {
            value,
            tier,
            citations: Vec::new(),
        }
    }

    /// Construct a tiered value with an explicit citation list.
    pub fn with_citations(value: T, tier: ConfidenceTier, citations: Vec<CitationId>) -> Self {
        Self {
            value,
            tier,
            citations,
        }
    }

    /// Map the inner value while preserving tier and citations.
    ///
    /// This is the right tool for unary transformations that the type
    /// system cannot express through [`Neg`] or other operator traits.
    pub fn map<U, F: FnOnce(T) -> U>(self, f: F) -> Tiered<U> {
        Tiered {
            value: f(self.value),
            tier: self.tier,
            citations: self.citations,
        }
    }

    /// Borrow the underlying value.
    pub fn value(&self) -> &T {
        &self.value
    }

    /// Tier of this value.
    pub fn tier(&self) -> ConfidenceTier {
        self.tier
    }
}

/// Merge two citation lists preserving order of first appearance.
fn merge_citations(mut a: Vec<CitationId>, b: Vec<CitationId>) -> Vec<CitationId> {
    for c in b {
        if !a.contains(&c) {
            a.push(c);
        }
    }
    a
}

macro_rules! impl_binary_op {
    ($trait:ident, $method:ident) => {
        impl<T, U, O> $trait<Tiered<U>> for Tiered<T>
        where
            T: $trait<U, Output = O>,
        {
            type Output = Tiered<O>;

            fn $method(self, rhs: Tiered<U>) -> Self::Output {
                Tiered {
                    value: self.value.$method(rhs.value),
                    tier: self.tier.combine(rhs.tier),
                    citations: merge_citations(self.citations, rhs.citations),
                }
            }
        }
    };
}

impl_binary_op!(Add, add);
impl_binary_op!(Sub, sub);
impl_binary_op!(Mul, mul);
impl_binary_op!(Div, div);

impl<T: Neg<Output = T>> Neg for Tiered<T> {
    type Output = Self;

    fn neg(self) -> Self::Output {
        self.map(Neg::neg)
    }
}

#[cfg(test)]
#[allow(clippy::float_cmp)]
mod tests {
    use super::*;

    fn cit(id: &str) -> CitationId {
        CitationId::new(id)
    }

    #[test]
    fn arithmetic_propagates_least_confident_tier() {
        let a = Tiered::new(10.0_f64, ConfidenceTier::A, cit("source-a"));
        let c = Tiered::new(2.0_f64, ConfidenceTier::C, cit("source-c"));

        let sum = a.clone() + c.clone();
        assert_eq!(sum.value, 12.0);
        assert_eq!(sum.tier, ConfidenceTier::C);

        let product = a * c;
        assert_eq!(product.value, 20.0);
        assert_eq!(product.tier, ConfidenceTier::C);
    }

    #[test]
    fn citations_are_unioned_without_duplicates() {
        let a = Tiered::new(1.0_f64, ConfidenceTier::A, cit("shared"));
        let b = Tiered::with_citations(
            2.0_f64,
            ConfidenceTier::B,
            vec![cit("shared"), cit("other")],
        );

        let result = a + b;
        assert_eq!(result.tier, ConfidenceTier::B);
        assert_eq!(result.citations, vec![cit("shared"), cit("other")]);
    }

    #[test]
    fn chained_arithmetic_takes_worst_tier_across_chain() {
        let a = Tiered::new(2.0_f64, ConfidenceTier::A, cit("a"));
        let b = Tiered::new(3.0_f64, ConfidenceTier::B, cit("b"));
        let d = Tiered::new(4.0_f64, ConfidenceTier::D, cit("d"));

        let result = a * b + d;
        assert_eq!(result.value, 10.0);
        assert_eq!(result.tier, ConfidenceTier::D);
        assert_eq!(result.citations.len(), 3);
    }

    #[test]
    fn map_preserves_tier_and_citations() {
        let v = Tiered::new(9.0_f64, ConfidenceTier::B, cit("source"));
        let mapped = v.map(f64::sqrt);
        assert_eq!(mapped.value, 3.0);
        assert_eq!(mapped.tier, ConfidenceTier::B);
        assert_eq!(mapped.citations, vec![cit("source")]);
    }
}
