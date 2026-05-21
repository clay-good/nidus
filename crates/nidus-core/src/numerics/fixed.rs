//! Q32.32 signed fixed-point arithmetic.
//!
//! The representation is a single `i64` whose lower 32 bits are the
//! fractional part. The numeric range is therefore approximately
//! ±2.147 × 10⁹ with a resolution of 2⁻³² ≈ 2.33 × 10⁻¹⁰. This is
//! comfortably more than the dynamic range required by any of the
//! biological quantities Nidus models (a few orders of magnitude for
//! pressures, masses, volumes, and concentrations; well under ten
//! orders of magnitude including their characteristic resolutions).
//!
//! All operations use checked integer arithmetic with arithmetic-shift
//! rounding (truncation toward negative infinity). They are bit-exact
//! across architectures and compilation modes, which is the property
//! the engine's reproducibility contract depends on.

use core::fmt;
use core::ops::Neg;

/// Number of fractional bits in the Q32.32 representation.
pub const FRAC_BITS: u32 = 32;
const SCALE: i64 = 1 << FRAC_BITS;

/// Returned when an operation would produce a value outside the
/// representable range of [`Fixed`], or when a conversion from
/// floating-point receives a non-finite input.
#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub struct OverflowError;

impl fmt::Display for OverflowError {
    fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {
        f.write_str("fixed-point overflow")
    }
}

impl core::error::Error for OverflowError {}

/// Signed 64-bit Q32.32 fixed-point number.
///
/// The raw representation is exposed only via [`Fixed::raw`] and
/// [`Fixed::from_raw`] so that storage formats and unit wrappers can
/// pass through the underlying bits without paying conversion cost.
/// Internal arithmetic uses checked operations exclusively.
#[derive(Debug, Clone, Copy, PartialEq, Eq, PartialOrd, Ord, Hash)]
#[cfg_attr(feature = "serde", derive(serde::Serialize, serde::Deserialize))]
pub struct Fixed {
    raw: i64,
}

impl Fixed {
    /// The additive identity.
    pub const ZERO: Self = Self { raw: 0 };
    /// One unit (1.0 in the represented quantity's natural unit).
    pub const ONE: Self = Self { raw: SCALE };
    /// Most negative representable value.
    pub const MIN: Self = Self { raw: i64::MIN };
    /// Most positive representable value.
    pub const MAX: Self = Self { raw: i64::MAX };

    /// Wrap a raw Q32.32 integer.
    #[must_use]
    pub const fn from_raw(raw: i64) -> Self {
        Self { raw }
    }

    /// Borrow the underlying Q32.32 integer.
    #[must_use]
    pub const fn raw(self) -> i64 {
        self.raw
    }

    /// Construct from an integer (no rounding needed).
    #[must_use]
    pub const fn from_int(value: i32) -> Self {
        Self {
            raw: (value as i64) << FRAC_BITS,
        }
    }

    /// Construct from an `f64`, rounding to the nearest representable
    /// value with ties toward positive infinity (the behaviour of
    /// `f64::round`). Returns [`OverflowError`] for non-finite inputs
    /// and for inputs outside the representable range.
    #[allow(clippy::cast_possible_truncation, clippy::cast_precision_loss)]
    pub fn from_f64(value: f64) -> Result<Self, OverflowError> {
        if !value.is_finite() {
            return Err(OverflowError);
        }
        // Convert to scaled f64 in the i64 range, then range-check.
        let scaled = (value * SCALE as f64).round();
        // i64::MIN/MAX as f64 lose precision; comparing against them
        // directly is the cleanest range check at this precision.
        if scaled < i64::MIN as f64 || scaled > i64::MAX as f64 {
            return Err(OverflowError);
        }
        Ok(Self { raw: scaled as i64 })
    }

    /// Convert to `f64`. This is lossless for values whose magnitude is
    /// below 2⁵³ in raw form (well above the biological range) and
    /// gracefully degrades for extreme values.
    #[must_use]
    #[allow(clippy::cast_precision_loss)]
    pub fn to_f64(self) -> f64 {
        (self.raw as f64) / (SCALE as f64)
    }

    /// Checked addition; returns [`OverflowError`] on overflow.
    pub fn checked_add(self, rhs: Self) -> Result<Self, OverflowError> {
        self.raw
            .checked_add(rhs.raw)
            .map(|raw| Self { raw })
            .ok_or(OverflowError)
    }

    /// Checked subtraction; returns [`OverflowError`] on overflow.
    pub fn checked_sub(self, rhs: Self) -> Result<Self, OverflowError> {
        self.raw
            .checked_sub(rhs.raw)
            .map(|raw| Self { raw })
            .ok_or(OverflowError)
    }

    /// Checked multiplication of two fixed-point values.
    ///
    /// The intermediate product is computed in `i128`, then shifted
    /// right by [`FRAC_BITS`] with arithmetic shift (truncation toward
    /// negative infinity). If the truncated result does not fit in
    /// `i64`, returns [`OverflowError`].
    pub fn checked_mul(self, rhs: Self) -> Result<Self, OverflowError> {
        let product = i128::from(self.raw) * i128::from(rhs.raw);
        let shifted = product >> FRAC_BITS;
        i64::try_from(shifted)
            .map(|raw| Self { raw })
            .map_err(|_| OverflowError)
    }

    /// Checked division.
    ///
    /// Returns [`OverflowError`] if `rhs` is zero or if the quotient
    /// would not fit in `i64`. The numerator is pre-scaled in `i128`
    /// to preserve the Q32.32 result.
    pub fn checked_div(self, rhs: Self) -> Result<Self, OverflowError> {
        if rhs.raw == 0 {
            return Err(OverflowError);
        }
        let numerator = i128::from(self.raw) << FRAC_BITS;
        let quotient = numerator / i128::from(rhs.raw);
        i64::try_from(quotient)
            .map(|raw| Self { raw })
            .map_err(|_| OverflowError)
    }

    /// Absolute value (saturating: `MIN.abs()` returns `MAX`).
    #[must_use]
    pub const fn abs(self) -> Self {
        Self {
            raw: self.raw.saturating_abs(),
        }
    }
}

impl Neg for Fixed {
    type Output = Self;
    fn neg(self) -> Self {
        Self {
            raw: self.raw.saturating_neg(),
        }
    }
}

impl fmt::Display for Fixed {
    fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {
        write!(f, "{}", self.to_f64())
    }
}

#[cfg(test)]
#[allow(clippy::float_cmp)]
mod tests {
    use super::*;

    #[test]
    fn round_trip_through_f64_preserves_simple_decimals() {
        for x in [0.0, 1.0, -1.0, 0.5, -0.25, 7.125, 1234.5678] {
            let f = Fixed::from_f64(x).unwrap();
            let back = f.to_f64();
            assert!((back - x).abs() < 1e-9, "x={x} back={back}");
        }
    }

    #[test]
    fn from_f64_rejects_non_finite() {
        assert!(Fixed::from_f64(f64::NAN).is_err());
        assert!(Fixed::from_f64(f64::INFINITY).is_err());
        assert!(Fixed::from_f64(f64::NEG_INFINITY).is_err());
    }

    #[test]
    fn from_f64_rejects_out_of_range() {
        assert!(Fixed::from_f64(1e20).is_err());
        assert!(Fixed::from_f64(-1e20).is_err());
    }

    #[test]
    fn checked_add_detects_overflow() {
        assert_eq!(Fixed::MAX.checked_add(Fixed::ONE), Err(OverflowError));
        assert_eq!(Fixed::MIN.checked_sub(Fixed::ONE), Err(OverflowError));
    }

    #[test]
    fn checked_mul_is_bit_stable() {
        let a = Fixed::from_f64(2.5).unwrap();
        let b = Fixed::from_f64(4.0).unwrap();
        let product = a.checked_mul(b).unwrap();
        assert_eq!(product.to_f64(), 10.0);
    }

    #[test]
    fn checked_mul_detects_overflow() {
        // sqrt(i64::MAX / 2^32) ≈ 46_340, so squaring values below
        // that fits and above that does not.
        let safe = Fixed::from_f64(30_000.0).unwrap();
        assert!(safe.checked_mul(safe).is_ok());
        let too_big = Fixed::from_f64(100_000.0).unwrap();
        assert_eq!(too_big.checked_mul(too_big), Err(OverflowError));
    }

    #[test]
    fn checked_div_detects_zero_and_overflow() {
        assert_eq!(Fixed::ONE.checked_div(Fixed::ZERO), Err(OverflowError));
        let tiny = Fixed::from_raw(1);
        assert_eq!(Fixed::MAX.checked_div(tiny), Err(OverflowError));
    }

    #[test]
    fn integer_arithmetic_is_exact() {
        let a = Fixed::from_int(3);
        let b = Fixed::from_int(7);
        let sum = a.checked_add(b).unwrap();
        let product = a.checked_mul(b).unwrap();
        assert_eq!(sum.to_f64(), 10.0);
        assert_eq!(product.to_f64(), 21.0);
    }

    #[test]
    fn neg_handles_min_via_saturation() {
        // i64::MIN cannot be negated without overflow; saturating-neg
        // returns i64::MAX, which is the documented behaviour.
        let m = Fixed::MIN;
        assert_eq!((-m).raw(), i64::MAX);
    }
}
