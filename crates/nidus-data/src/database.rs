//! In-memory parameter database.
//!
//! A [`ParameterDatabase`] holds a set of parameter entries indexed by
//! id, plus the citation index they reference. The database is built
//! from one or more parameter TOML files and one or more citation TOML
//! files; the loader validates the schema, rejects duplicate ids, and
//! checks that every parameter's `citation` field resolves to a
//! citation that exists.

use std::collections::HashMap;
use std::path::{Path, PathBuf};

use thiserror::Error;

use nidus_core::tier::ConfidenceTier;

use crate::schema::{CitationEntry, CitationIndexFile, ParameterEntry, ParameterFile};

/// Errors that can arise while building or querying the database.
#[derive(Debug, Error)]
pub enum DatabaseError {
    /// Could not read a TOML file from disk.
    #[error("failed to read {path}: {source}")]
    Io {
        /// Path that could not be read.
        path: PathBuf,
        /// Underlying I/O error.
        #[source]
        source: std::io::Error,
    },
    /// File contents did not match the expected TOML schema.
    #[error("failed to parse {path}: {source}")]
    Parse {
        /// Path that failed to parse.
        path: PathBuf,
        /// Underlying TOML decode error.
        #[source]
        source: toml::de::Error,
    },
    /// Two parameter entries declared the same `id`.
    #[error("duplicate parameter id `{id}` (first seen in {first}, again in {second})")]
    DuplicateParameter {
        /// The conflicting id.
        id: String,
        /// File the first entry was declared in.
        first: PathBuf,
        /// File the conflicting entry was declared in.
        second: PathBuf,
    },
    /// Two citation entries declared the same `id`.
    #[error("duplicate citation id `{id}`")]
    DuplicateCitation {
        /// The conflicting id.
        id: String,
    },
    /// A parameter referenced a citation id that no citation file
    /// declares.
    #[error("parameter `{parameter}` references unknown citation `{citation}`")]
    UnknownCitation {
        /// Parameter whose `citation` field was unresolved.
        parameter: String,
        /// Unresolved citation id.
        citation: String,
    },
    /// `min_weeks > max_weeks`, or some other schema constraint.
    #[error("parameter `{parameter}` has invalid age range: {detail}")]
    InvalidAgeRange {
        /// Parameter whose age range is invalid.
        parameter: String,
        /// Human-readable detail.
        detail: String,
    },
}

/// Parameter database: parameter entries plus the citations they cite.
#[derive(Debug, Default, Clone)]
pub struct ParameterDatabase {
    parameters: HashMap<String, ParameterEntry>,
    parameter_sources: HashMap<String, PathBuf>,
    citations: HashMap<String, CitationEntry>,
}

impl ParameterDatabase {
    /// Construct an empty database.
    #[must_use]
    pub fn new() -> Self {
        Self::default()
    }

    /// Build a database from a set of parameter files and a set of
    /// citation files. Order of files within each set is not significant
    /// — duplicate-id detection runs against the accumulating set.
    pub fn from_paths(
        parameter_files: &[impl AsRef<Path>],
        citation_files: &[impl AsRef<Path>],
    ) -> Result<Self, DatabaseError> {
        let mut db = Self::new();
        for path in citation_files {
            db.load_citation_file(path.as_ref())?;
        }
        for path in parameter_files {
            db.load_parameter_file(path.as_ref())?;
        }
        db.validate_references()?;
        Ok(db)
    }

    /// Load and merge a single citation file.
    pub fn load_citation_file(&mut self, path: &Path) -> Result<(), DatabaseError> {
        let text = std::fs::read_to_string(path).map_err(|source| DatabaseError::Io {
            path: path.to_path_buf(),
            source,
        })?;
        let parsed: CitationIndexFile =
            toml::from_str(&text).map_err(|source| DatabaseError::Parse {
                path: path.to_path_buf(),
                source,
            })?;
        for entry in parsed.citation {
            if self.citations.contains_key(&entry.id) {
                return Err(DatabaseError::DuplicateCitation { id: entry.id });
            }
            self.citations.insert(entry.id.clone(), entry);
        }
        Ok(())
    }

    /// Load and merge a single parameter file.
    pub fn load_parameter_file(&mut self, path: &Path) -> Result<(), DatabaseError> {
        let text = std::fs::read_to_string(path).map_err(|source| DatabaseError::Io {
            path: path.to_path_buf(),
            source,
        })?;
        let parsed: ParameterFile =
            toml::from_str(&text).map_err(|source| DatabaseError::Parse {
                path: path.to_path_buf(),
                source,
            })?;
        for entry in parsed.parameter {
            if let Some(first) = self.parameter_sources.get(&entry.id) {
                return Err(DatabaseError::DuplicateParameter {
                    id: entry.id,
                    first: first.clone(),
                    second: path.to_path_buf(),
                });
            }
            if !entry.age_range.is_valid() {
                return Err(DatabaseError::InvalidAgeRange {
                    parameter: entry.id,
                    detail: format!(
                        "min_weeks ({}) > max_weeks ({})",
                        entry.age_range.min_weeks, entry.age_range.max_weeks
                    ),
                });
            }
            self.parameter_sources
                .insert(entry.id.clone(), path.to_path_buf());
            self.parameters.insert(entry.id.clone(), entry);
        }
        Ok(())
    }

    /// Confirm that every parameter's `citation` field resolves.
    pub fn validate_references(&self) -> Result<(), DatabaseError> {
        for entry in self.parameters.values() {
            if !self.citations.contains_key(&entry.citation) {
                return Err(DatabaseError::UnknownCitation {
                    parameter: entry.id.clone(),
                    citation: entry.citation.clone(),
                });
            }
        }
        Ok(())
    }

    /// Look up a parameter by id.
    #[must_use]
    pub fn parameter(&self, id: &str) -> Option<&ParameterEntry> {
        self.parameters.get(id)
    }

    /// Look up a citation by id.
    #[must_use]
    pub fn citation(&self, id: &str) -> Option<&CitationEntry> {
        self.citations.get(id)
    }

    /// Resolve the citation backing a parameter, if both exist.
    #[must_use]
    pub fn citation_for(&self, parameter_id: &str) -> Option<&CitationEntry> {
        self.parameters
            .get(parameter_id)
            .and_then(|p| self.citations.get(&p.citation))
    }

    /// Iterate over all parameters, in arbitrary but stable order
    /// determined by the underlying `HashMap` (for deterministic order
    /// across queries, collect and sort by id at the call site).
    pub fn parameters(&self) -> impl Iterator<Item = &ParameterEntry> {
        self.parameters.values()
    }

    /// Iterate over parameters whose tier matches the predicate.
    pub fn parameters_at_tier(
        &self,
        tier: ConfidenceTier,
    ) -> impl Iterator<Item = &ParameterEntry> {
        self.parameters.values().filter(move |p| p.tier == tier)
    }

    /// Number of parameter entries.
    #[must_use]
    pub fn len(&self) -> usize {
        self.parameters.len()
    }

    /// `true` iff the database contains no parameters.
    #[must_use]
    pub fn is_empty(&self) -> bool {
        self.parameters.is_empty()
    }
}

#[cfg(test)]
mod tests {
    use super::*;
    use std::io::Write;

    fn write_tmp(name: &str, contents: &str) -> PathBuf {
        let dir = std::env::temp_dir().join("nidus-data-tests");
        std::fs::create_dir_all(&dir).unwrap();
        let path = dir.join(name);
        let mut f = std::fs::File::create(&path).unwrap();
        f.write_all(contents.as_bytes()).unwrap();
        path
    }

    const CITATIONS: &str = r#"
[[citation]]
id = "demo-source"
authors = "Demonstration Author"
title = "A reference for tests"
venue = "Journal of Tests"
year = 2024
"#;

    const PARAMETERS: &str = r#"
[[parameter]]
id = "demo-parameter"
name = "Demo parameter"
description = "Demonstrates the schema loader."
tier = "B"
unit = "mmHg"
value = { kind = "point", value = 100.0, uncertainty = 5.0 }
citation = "demo-source"
population = "Test cohort"
age_range = { min_weeks = 8, max_weeks = 40 }
"#;

    #[test]
    fn loads_and_resolves_references() {
        let cit = write_tmp("citations_ok.toml", CITATIONS);
        let par = write_tmp("parameters_ok.toml", PARAMETERS);
        let db = ParameterDatabase::from_paths(&[par], &[cit]).unwrap();
        assert_eq!(db.len(), 1);
        let p = db.parameter("demo-parameter").unwrap();
        assert_eq!(p.tier, ConfidenceTier::B);
        let c = db.citation_for("demo-parameter").unwrap();
        assert_eq!(c.year, 2024);
    }

    #[test]
    fn rejects_unknown_citation() {
        let par = write_tmp(
            "parameters_dangling.toml",
            r#"
[[parameter]]
id = "p1"
name = "p"
description = "d"
tier = "C"
unit = "x"
value = { kind = "point", value = 1.0 }
citation = "no-such-source"
population = "pop"
age_range = { min_weeks = 8, max_weeks = 40 }
"#,
        );
        let cit = write_tmp("citations_empty.toml", "");
        let err = ParameterDatabase::from_paths(&[par], &[cit]).unwrap_err();
        match err {
            DatabaseError::UnknownCitation {
                parameter,
                citation,
            } => {
                assert_eq!(parameter, "p1");
                assert_eq!(citation, "no-such-source");
            }
            other => panic!("unexpected error: {other:?}"),
        }
    }

    #[test]
    fn rejects_invalid_age_range() {
        let par = write_tmp(
            "parameters_bad_age.toml",
            r#"
[[parameter]]
id = "p1"
name = "p"
description = "d"
tier = "A"
unit = "x"
value = { kind = "point", value = 1.0 }
citation = "demo-source"
population = "pop"
age_range = { min_weeks = 40, max_weeks = 8 }
"#,
        );
        let cit = write_tmp("citations_for_bad_age.toml", CITATIONS);
        let err = ParameterDatabase::from_paths(&[par], &[cit]).unwrap_err();
        assert!(matches!(err, DatabaseError::InvalidAgeRange { .. }));
    }

    #[test]
    fn rejects_duplicate_parameter_id() {
        let p1 = write_tmp("dup_a.toml", PARAMETERS);
        let p2 = write_tmp("dup_b.toml", PARAMETERS);
        let cit = write_tmp("citations_for_dup.toml", CITATIONS);
        let err = ParameterDatabase::from_paths(&[p1, p2], &[cit]).unwrap_err();
        assert!(matches!(err, DatabaseError::DuplicateParameter { .. }));
    }

    #[test]
    fn parameters_at_tier_filters_correctly() {
        let cit = write_tmp("citations_tier.toml", CITATIONS);
        let par = write_tmp(
            "parameters_tiers.toml",
            r#"
[[parameter]]
id = "a-tier-a"
name = "A"
description = "d"
tier = "A"
unit = "x"
value = { kind = "point", value = 1.0 }
citation = "demo-source"
population = "p"
age_range = { min_weeks = 8, max_weeks = 40 }

[[parameter]]
id = "b-tier-c"
name = "B"
description = "d"
tier = "C"
unit = "x"
value = { kind = "uniform", low = 0.0, high = 1.0 }
citation = "demo-source"
population = "p"
age_range = { min_weeks = 8, max_weeks = 40 }
"#,
        );
        let db = ParameterDatabase::from_paths(&[par], &[cit]).unwrap();
        let a_ids: Vec<_> = db
            .parameters_at_tier(ConfidenceTier::A)
            .map(|p| p.id.clone())
            .collect();
        assert_eq!(a_ids, vec!["a-tier-a".to_owned()]);
        let c_ids: Vec<_> = db
            .parameters_at_tier(ConfidenceTier::C)
            .map(|p| p.id.clone())
            .collect();
        assert_eq!(c_ids, vec!["b-tier-c".to_owned()]);
    }

    #[test]
    fn rejects_unknown_fields() {
        let par = write_tmp(
            "parameters_extra.toml",
            r#"
[[parameter]]
id = "p1"
name = "p"
description = "d"
tier = "A"
unit = "x"
value = { kind = "point", value = 1.0 }
citation = "demo-source"
population = "pop"
age_range = { min_weeks = 8, max_weeks = 40 }
unexpected_field = "should fail"
"#,
        );
        let cit = write_tmp("citations_for_extra.toml", CITATIONS);
        let err = ParameterDatabase::from_paths(&[par], &[cit]).unwrap_err();
        assert!(matches!(err, DatabaseError::Parse { .. }));
    }
}
