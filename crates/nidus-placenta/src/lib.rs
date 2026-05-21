//! Placental interface.
//!
//! The placenta is modelled as five interacting components
//! (SPEC.md §7): transport, structural development, endocrine
//! production, barrier function, and unknown channels. Version 0.1.0
//! ships the structural-development and transport components needed to
//! couple the maternal and fetal subsystems; the endocrine, barrier,
//! and unknown-channel components are deferred to later prompts.
//!
//! ### Structural development
//!
//! [`structure::placental_surface_area_m2`] returns the effective
//! exchange surface area as a function of gestational age. The
//! trajectory is a sigmoidal rise from a small initial value through
//! mid-gestation to a near-term plateau, consistent with the textbook
//! description of villous-tree development.
//!
//! ### Transport
//!
//! [`transport::gas_exchange`] returns the fetal umbilical-vein
//! partial pressure of oxygen given maternal arterial PO₂, fetal
//! umbilical-artery (return) PO₂, and the placenta's current surface
//! area. The functional form is a single equilibration coefficient
//! that rises monotonically with surface area; it is the simplest
//! model that produces a fetal umbilical-vein PO₂ inside the published
//! physiological range, and it is the entry point that later prompts
//! will refine.
//!
//! [`transport::glucose_flux_mmol_per_min`] applies Michaelis–Menten
//! kinetics to facilitated diffusion through GLUT1/GLUT3-class
//! transporters, returning the net maternal-to-fetal glucose flux per
//! minute as a function of concentrations on both sides, surface area,
//! and transporter `(Vmax, Km)`.
//!
//! All trajectory and transport constants below are scaffolding
//! pending integration with the parameter database (SPEC.md §9); the
//! values they take are textbook-consistent but must be replaced with
//! citation-bearing entries before publication. See CONTRIBUTING.md.

#![cfg_attr(not(test), warn(missing_docs))]

pub mod structure;
pub mod subscriber;
pub mod transport;

pub use structure::{placental_surface_area_m2, StructureParams};
pub use subscriber::{Placenta, PlacentaState, SUBSCRIBER_ID};
pub use transport::{
    gas_exchange, glucose_flux_mmol_per_min, GasExchangeParams, GlucoseTransportParams,
};
