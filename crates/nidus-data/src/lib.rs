//! Parameter database and citation index for Nidus.
//!
//! The parameter database stores every numerical quantity used by the
//! simulator as structured data rather than code constants
//! (SPEC.md §9). Each parameter is paired with a citation, a confidence
//! tier, the population the value was derived from, and the gestational
//! age range over which it is documented. Citations are stored
//! separately in a citation index so that one source can be referenced
//! by many parameters without duplication.
//!
//! Parameters and citations are written in TOML. This crate loads them
//! into in-memory representations, validates that every parameter's
//! `citation` field references a citation that exists, and exposes a
//! small query API.
//!
//! ### What this crate does not do
//!
//! The crate does not verify citations against their original sources;
//! that verification is a human-review step in the pull-request workflow
//! described in CONTRIBUTING.md. The schema loader will accept any
//! plausibly-shaped citation entry, so a malformed real-world
//! bibliography is detected by reviewers rather than by the type system.

#![cfg_attr(not(test), warn(missing_docs))]

pub mod database;
pub mod schema;

pub use database::{DatabaseError, ParameterDatabase};
pub use schema::{
    AgeRange, CitationEntry, CitationIndexFile, ParameterEntry, ParameterFile, ValueSpec,
};
