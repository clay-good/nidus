//! Nidus command-line interface.
//!
//! Subcommands implemented for v0.1.0:
//!
//! - `run` — execute a scenario (from a TOML file or the built-in
//!   normal-term-pregnancy scaffold) and emit a JSON report on stdout.
//! - `list parameters` — print every parameter in the loaded
//!   parameter database, with id, tier, citation, and value summary.
//! - `list channels` — print every channel in the standard
//!   unknown-channels registry, with id, tier, range, and current mode.
//! - `validate-config` — load a scenario file and report whether it
//!   parses and validates against the schema, without running it.
//!
//! The dashboard, hypothesis-report renderer, and full parameter-query
//! grammar are deferred to later prompts.

use std::path::PathBuf;
use std::process::ExitCode;

use clap::{Parser, Subcommand};

use nidus_data::ParameterDatabase;
use nidus_scenarios::{
    builtin::NORMAL_TERM_PREGNANCY, load_scenario_from_path, load_scenario_from_str,
    ScenarioOrchestrator,
};
use nidus_unknown::ChannelRegistry;

#[derive(Parser, Debug)]
#[command(
    name = "nidus",
    version,
    about = "Nidus research simulator command-line interface",
    long_about = "Command-line entry point to the Nidus gestational-physiology simulator. \
                  Subcommands let you run scenarios, list database contents, and validate \
                  configuration files. See SPEC.md and CONTRIBUTING.md for context."
)]
struct Cli {
    #[command(subcommand)]
    command: Command,
}

#[derive(Subcommand, Debug)]
enum Command {
    /// Run a scenario and write a JSON report to stdout.
    Run {
        /// Path to a scenario TOML file. If omitted, the built-in
        /// `normal-term-pregnancy` scaffold scenario is used.
        #[arg(long, value_name = "PATH")]
        scenario: Option<PathBuf>,
    },
    /// List database contents.
    List {
        #[command(subcommand)]
        what: ListWhat,
    },
    /// Validate a scenario configuration without running it.
    ValidateConfig {
        /// Path to a scenario TOML file.
        scenario: PathBuf,
    },
}

#[derive(Subcommand, Debug)]
enum ListWhat {
    /// List every parameter in the parameter database under `data/`.
    Parameters {
        /// Path to the parameter-database root. Defaults to `./data`.
        #[arg(long, value_name = "PATH", default_value = "data")]
        data_dir: PathBuf,
    },
    /// List every unknown channel in the standard v0.1 registry.
    Channels,
}

fn main() -> ExitCode {
    let cli = Cli::parse();
    match dispatch(cli) {
        Ok(()) => ExitCode::SUCCESS,
        Err(err) => {
            eprintln!("error: {err}");
            ExitCode::FAILURE
        }
    }
}

fn dispatch(cli: Cli) -> Result<(), Box<dyn std::error::Error>> {
    match cli.command {
        Command::Run { scenario } => run_scenario(scenario),
        Command::List { what } => match what {
            ListWhat::Parameters { data_dir } => list_parameters(&data_dir),
            ListWhat::Channels => list_channels(),
        },
        Command::ValidateConfig { scenario } => validate_config(&scenario),
    }
}

fn run_scenario(path: Option<PathBuf>) -> Result<(), Box<dyn std::error::Error>> {
    let spec = match path {
        Some(p) => load_scenario_from_path(&p)?,
        None => load_scenario_from_str(NORMAL_TERM_PREGNANCY)?,
    };
    let orchestrator = ScenarioOrchestrator::new(spec);
    let report = orchestrator.run();
    let json = serde_json::to_string_pretty(&render_report(&report))?;
    println!("{json}");
    Ok(())
}

fn render_report(report: &nidus_scenarios::ScenarioReport) -> serde_json::Value {
    let samples: Vec<_> = report
        .samples
        .iter()
        .map(|s| {
            serde_json::json!({
                "tick_seconds": s.tick_seconds,
                "gestational_week": s.gestational_age.completed_weeks(),
                "gestational_day": s.gestational_age.completed_days() % 7,
                "maternal_cardiac_output_l_per_min": s.maternal_cardiac_output_l_per_min,
                "maternal_map_mmhg": s.maternal_map_mmhg,
                "maternal_uterine_flow_ml_per_min": s.maternal_uterine_flow_ml_per_min,
                "placental_surface_area_m2": s.placental_surface_area_m2,
                "fetal_umbilical_vein_po2_mmhg": s.fetal_umbilical_vein_po2_mmhg,
                "fetal_cerebral_arterial_po2_mmhg": s.fetal_cerebral_arterial_po2_mmhg,
                "fetal_descending_aortic_po2_mmhg": s.fetal_descending_aortic_po2_mmhg,
            })
        })
        .collect();
    serde_json::json!({
        "name": report.name,
        "description": report.description,
        "n_samples": report.samples.len(),
        "samples": samples,
    })
}

fn list_parameters(data_dir: &std::path::Path) -> Result<(), Box<dyn std::error::Error>> {
    let parameters = collect_toml(&data_dir.join("parameters"));
    let citations = collect_toml(&data_dir.join("citations"));
    if citations.is_empty() {
        return Err(format!(
            "no citation files found under {}/citations",
            data_dir.display()
        )
        .into());
    }
    let db = ParameterDatabase::from_paths(&parameters, &citations)?;
    let mut ids: Vec<&str> = db.parameters().map(|p| p.id.as_str()).collect();
    ids.sort_unstable();
    println!("{} parameter(s) in {}:", ids.len(), data_dir.display());
    for id in ids {
        let p = db.parameter(id).expect("present");
        let c = db
            .citation(&p.citation)
            .map_or("<missing citation>", |c| c.id.as_str());
        let value_summary = match &p.value {
            nidus_data::ValueSpec::Point { value, .. } => format!("{value} {}", p.unit),
            nidus_data::ValueSpec::Uniform { low, high } => {
                format!("U[{low}, {high}] {}", p.unit)
            }
            nidus_data::ValueSpec::Normal { mean, sd } => {
                format!("N({mean}, sd={sd}) {}", p.unit)
            }
            nidus_data::ValueSpec::Lognormal { mu, sigma } => {
                format!("logN(mu={mu}, sigma={sigma}) {}", p.unit)
            }
        };
        println!("  [{:?}] {} = {} [cite:{}]", p.tier, p.id, value_summary, c);
    }
    Ok(())
}

#[allow(clippy::unnecessary_wraps)]
fn list_channels() -> Result<(), Box<dyn std::error::Error>> {
    let registry = ChannelRegistry::standard_v0_1();
    println!(
        "{} channel(s) in the standard v0.1 registry:",
        registry.len()
    );
    for ch in registry.channels() {
        let mode = registry.mode(&ch.id).unwrap_or_default();
        println!(
            "  [{:?}] {} (range {:.3}..{:.3} {} mode={:?})",
            ch.tier, ch.id, ch.parameter_range.low, ch.parameter_range.high, ch.units, mode,
        );
        println!("    {}", ch.name);
    }
    Ok(())
}

fn validate_config(path: &std::path::Path) -> Result<(), Box<dyn std::error::Error>> {
    let spec = load_scenario_from_path(path)?;
    println!(
        "ok: scenario `{}` ({} -> {} weeks, seed={}, subscribers={:?})",
        spec.name, spec.start_age_weeks, spec.end_age_weeks, spec.seed, spec.subscribers,
    );
    Ok(())
}

fn collect_toml(dir: &std::path::Path) -> Vec<PathBuf> {
    let mut out = Vec::new();
    if !dir.exists() {
        return out;
    }
    let Ok(entries) = std::fs::read_dir(dir) else {
        return out;
    };
    for entry in entries.flatten() {
        let path = entry.path();
        if path.is_dir() {
            out.extend(collect_toml(&path));
        } else if path.extension().and_then(|s| s.to_str()) == Some("toml") {
            out.push(path);
        }
    }
    out
}
