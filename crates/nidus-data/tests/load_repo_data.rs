//! Integration test: the parameter and citation TOML files committed to
//! the repository's `data/` tree load without error and pass reference
//! validation. This is what catches a malformed scaffold entry before it
//! reaches a downstream model crate.

use std::path::{Path, PathBuf};

use nidus_data::ParameterDatabase;

fn repo_data_dir() -> PathBuf {
    // CARGO_MANIFEST_DIR points at crates/nidus-data; the data tree is
    // two directories up.
    let manifest = PathBuf::from(env!("CARGO_MANIFEST_DIR"));
    manifest.parent().unwrap().parent().unwrap().join("data")
}

fn collect_toml(dir: &Path) -> Vec<PathBuf> {
    let mut out = Vec::new();
    if !dir.exists() {
        return out;
    }
    for entry in std::fs::read_dir(dir).unwrap() {
        let entry = entry.unwrap();
        let path = entry.path();
        if path.is_dir() {
            out.extend(collect_toml(&path));
        } else if path.extension().and_then(|s| s.to_str()) == Some("toml") {
            out.push(path);
        }
    }
    out
}

#[test]
fn repository_data_loads_and_validates() {
    let data = repo_data_dir();
    let parameter_files = collect_toml(&data.join("parameters"));
    let citation_files = collect_toml(&data.join("citations"));
    assert!(
        !citation_files.is_empty(),
        "expected at least one citation file under data/citations"
    );
    let db = ParameterDatabase::from_paths(&parameter_files, &citation_files)
        .expect("repository data files should load and validate");
    // The scaffold ships at least the Severinghaus 1979 entries; if that
    // changes, update the count and the assertion.
    assert!(
        !db.is_empty(),
        "expected at least one parameter in the scaffold data"
    );
}
