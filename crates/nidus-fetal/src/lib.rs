//! Fetal subsystem.
//!
//! Version 0.1.0 ships the cardiovascular special-circulation
//! component — the part of fetal physiology with no postnatal
//! analogue, and the part most consequential for downstream gas and
//! substrate distribution (SPEC.md §7). Metabolism, organ maturation,
//! and neurological development are deferred to later prompts.
//!
//! ### Special circulation
//!
//! Fetal cardiovascular anatomy includes three shunts that have no
//! postnatal analogue: the ductus venosus, the foramen ovale, and the
//! ductus arteriosus. Together they route the most oxygenated blood
//! from the umbilical vein preferentially to the fetal brain, while
//! the less oxygenated systemic venous return is preferentially
//! directed through the pulmonary artery and ductus arteriosus to the
//! descending aorta, bypassing the unventilated fetal lungs.
//!
//! [`special_circulation::FetalSpecialCirculation`] is the v0.1.0
//! model of this routing. It is a small algebraic model — weighted
//! averages over a streamline-preference parameter — and it produces
//! the qualitative pattern required by SPEC.md §13 prompt 8:
//! cerebral arterial oxygen tension is consistently higher than
//! descending aortic oxygen tension, with the umbilical-artery
//! (return) oxygen tension below both.

#![cfg_attr(not(test), warn(missing_docs))]

pub mod special_circulation;
pub mod subscriber;

pub use special_circulation::{
    FetalCirculationParams, FetalCirculationState, FetalSpecialCirculation,
};
pub use subscriber::{Fetal, SUBSCRIBER_ID};
