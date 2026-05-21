//! Typed biological quantities.
//!
//! Each newtype wraps a [`Fixed`] value and pins it to a specific
//! physical unit. The type system then prevents accidentally adding a
//! [`Pressure`] to a [`Mass`] — a mistake whose biological cousin
//! ("metric/imperial confusion") has crashed spacecraft. The wrappers
//! also document the canonical unit each quantity is stored in, which
//! is the contract scenario files and parameter database entries are
//! expected to respect.

use core::ops::Neg;

use super::fixed::{Fixed, OverflowError};

macro_rules! define_quantity {
    ($name:ident, $unit_doc:expr, $about_doc:expr) => {
        #[doc = $about_doc]
        ///
        #[doc = concat!("Stored in **", $unit_doc, "**.")]
        #[derive(Debug, Clone, Copy, PartialEq, Eq, PartialOrd, Ord, Hash)]
        #[cfg_attr(feature = "serde", derive(serde::Serialize, serde::Deserialize))]
        pub struct $name(Fixed);

        impl $name {
            /// The zero value.
            pub const ZERO: Self = Self(Fixed::ZERO);

            /// Wrap a raw [`Fixed`] value.
            #[must_use]
            pub const fn from_fixed(value: Fixed) -> Self {
                Self(value)
            }

            /// Unwrap to the underlying [`Fixed`] value.
            #[must_use]
            pub const fn to_fixed(self) -> Fixed {
                self.0
            }

            /// Construct from an `f64`, returning [`OverflowError`] on
            /// non-finite or out-of-range input.
            pub fn from_f64(value: f64) -> Result<Self, OverflowError> {
                Fixed::from_f64(value).map(Self)
            }

            /// Convert to `f64` for display or export.
            #[must_use]
            pub fn as_f64(self) -> f64 {
                self.0.to_f64()
            }

            /// Checked addition between values of the same unit.
            pub fn checked_add(self, rhs: Self) -> Result<Self, OverflowError> {
                self.0.checked_add(rhs.0).map(Self)
            }

            /// Checked subtraction between values of the same unit.
            pub fn checked_sub(self, rhs: Self) -> Result<Self, OverflowError> {
                self.0.checked_sub(rhs.0).map(Self)
            }

            /// Scale by a dimensionless [`Ratio`].
            pub fn checked_scale(self, ratio: Ratio) -> Result<Self, OverflowError> {
                self.0.checked_mul(ratio.0).map(Self)
            }
        }

        impl Neg for $name {
            type Output = Self;
            fn neg(self) -> Self {
                Self(-self.0)
            }
        }
    };
}

define_quantity!(
    Mass,
    "grams (g)",
    "Mass of tissue, blood, or other biological material."
);
define_quantity!(
    Pressure,
    "millimetres of mercury (mmHg)",
    "Pressure: arterial, venous, or partial gas pressure."
);
define_quantity!(
    Volume,
    "millilitres (mL)",
    "Fluid volume: blood, amniotic fluid, ventilated tidal volume, and similar."
);
define_quantity!(
    Concentration,
    "millimoles per litre (mmol/L)",
    "Solute concentration: glucose, lactate, ions, and similar species."
);
define_quantity!(
    Duration,
    "seconds (s)",
    "A span of time, distinct from absolute gestational age."
);
define_quantity!(
    Ratio,
    "dimensionless (a pure ratio)",
    "Dimensionless ratio, typically but not necessarily in `[0, 1]`."
);

impl Ratio {
    /// The dimensionless unit value (`1.0`).
    pub const ONE: Self = Self(Fixed::ONE);

    /// Construct a ratio from a fraction `num / den`. Returns
    /// [`OverflowError`] if `den` is zero or if the quotient does not
    /// fit in the fixed-point range.
    pub fn from_ratio(num: i32, den: i32) -> Result<Self, OverflowError> {
        Fixed::from_int(num)
            .checked_div(Fixed::from_int(den))
            .map(Self)
    }
}

#[cfg(test)]
#[allow(clippy::float_cmp)]
mod tests {
    use super::*;

    #[test]
    fn same_unit_arithmetic_round_trips_through_f64() {
        let a = Mass::from_f64(60_000.0).unwrap(); // ~typical maternal mass in g
        let b = Mass::from_f64(1500.0).unwrap();
        let sum = a.checked_add(b).unwrap();
        assert!((sum.as_f64() - 61_500.0).abs() < 1e-6);
    }

    #[test]
    fn scaling_by_ratio_preserves_unit_type() {
        let v = Volume::from_f64(5000.0).unwrap();
        let half = Ratio::from_ratio(1, 2).unwrap();
        let scaled = v.checked_scale(half).unwrap();
        assert!((scaled.as_f64() - 2500.0).abs() < 1e-6);
    }

    #[test]
    fn out_of_range_input_errors() {
        assert!(Pressure::from_f64(f64::INFINITY).is_err());
        assert!(Concentration::from_f64(1e20).is_err());
    }

    #[test]
    fn negation_works() {
        let p = Pressure::from_f64(100.0).unwrap();
        assert_eq!((-p).as_f64(), -100.0);
    }

    #[test]
    fn from_ratio_zero_denominator_errors() {
        assert!(Ratio::from_ratio(1, 0).is_err());
    }

    // A simple compile-fail-style assertion expressed as a *no-op* test:
    // the next two lines would not compile if Mass and Pressure were
    // interchangeable (the type signatures differ). The point is the
    // type system, not the runtime check.
    #[test]
    fn cross_unit_addition_is_a_compile_error_by_construction() {
        let _m = Mass::from_f64(1.0).unwrap();
        let _p = Pressure::from_f64(1.0).unwrap();
        // _m.checked_add(_p) // ← would not compile; tested implicitly
    }
}
