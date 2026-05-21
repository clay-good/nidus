//! Nidus command-line interface.
//!
//! Subcommands:
//!
//! - `run` — execute a scenario (from a TOML file or the built-in
//!   normal-term-pregnancy scaffold) and emit a JSON report on stdout.
//! - `list parameters` — print every parameter in the loaded
//!   parameter database, with id, tier, citation, and value summary.
//!   Supports `--tier`, `--search`, and `--json` filters.
//! - `list channels` — print every channel in the standard
//!   unknown-channels registry, with id, tier, range, and current mode.
//! - `validate-config` — load a scenario file and report whether it
//!   parses and validates against the schema, without running it.
//! - `validate` — run the built-in validation suite against the
//!   simulator and emit a JSON or Markdown report.
//! - `hypothesis-report` — run an ensemble + Sobol sensitivity +
//!   experiment-design pipeline on the placental gas-exchange model
//!   and emit ranked structured suggestions.
//!
//! The dashboard described in SPEC.md §13 prompt 15 is the only
//! remaining deferred CLI surface; it is a v0.2 frontend deliverable.

use std::path::PathBuf;
use std::process::ExitCode;

use clap::{Parser, Subcommand, ValueEnum};

use nidus_core::clock::GestationalAge;
use nidus_core::rng::RngService;
use nidus_core::subscriber::SubscriberId;
use nidus_core::tier::ConfidenceTier;
use nidus_data::ParameterDatabase;
use nidus_hypothesis::{
    ExperimentDesignSuggester, ParameterSpec, SamplingStrategy, SensitivityAnalyser,
    SuggesterParameterInfo,
};
use nidus_maternal::cardio::{MaternalCardio, SUBSCRIBER_ID as MATERNAL_CARDIO_ID};
use nidus_scenarios::{
    builtin::NORMAL_TERM_PREGNANCY, load_scenario_from_path, load_scenario_from_str,
    ScenarioOrchestrator,
};
use nidus_unknown::ChannelRegistry;
use nidus_validation::{built_in_cases, ValidationSuite};

#[derive(Parser, Debug)]
#[command(
    name = "nidus",
    version,
    about = "Nidus research simulator command-line interface",
    long_about = "Command-line entry point to the Nidus gestational-physiology simulator. \
                  Subcommands let you run scenarios, list database contents, validate \
                  configuration, run the validation suite, and generate hypothesis-design \
                  reports. See SPEC.md and CONTRIBUTING.md for context."
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
    /// Run the built-in validation suite against the simulator.
    Validate {
        /// Output format.
        #[arg(long, value_enum, default_value_t = ReportFormat::Markdown)]
        format: ReportFormat,
        /// RNG seed used to construct the simulator probes.
        #[arg(long, default_value_t = 123)]
        seed: u64,
    },
    /// Run the hypothesis-generation pipeline on the placental
    /// gas-exchange model.
    ///
    /// Treats placental surface area (Tier B), the gas-exchange
    /// half-saturation surface area (Tier C), and the maximum
    /// equilibration coefficient (Tier C) as uncertain inputs; the
    /// analysed outcome is fetal umbilical-vein PO₂ at term under
    /// fixed maternal-arterial and umbilical-artery PO₂ inputs.
    /// Emits ranked experiment-design suggestions.
    HypothesisReport {
        /// Number of Sobol base samples. Total model evaluations are
        /// `samples · (k + 2)` with `k = 3`.
        #[arg(long, default_value_t = 4_000)]
        samples: usize,
        /// RNG seed.
        #[arg(long, default_value_t = 7)]
        seed: u64,
        /// Output format.
        #[arg(long, value_enum, default_value_t = ReportFormat::Json)]
        format: ReportFormat,
    },
}

#[derive(Subcommand, Debug)]
enum ListWhat {
    /// List every parameter in the parameter database under `data/`.
    Parameters {
        /// Path to the parameter-database root. Defaults to `./data`.
        #[arg(long, value_name = "PATH", default_value = "data")]
        data_dir: PathBuf,
        /// Restrict output to one confidence tier.
        #[arg(long, value_enum)]
        tier: Option<TierArg>,
        /// Case-insensitive substring filter on id, name, and unit.
        #[arg(long)]
        search: Option<String>,
        /// Emit machine-readable JSON instead of the human-readable table.
        #[arg(long)]
        json: bool,
    },
    /// List every unknown channel in the standard v0.1 registry.
    Channels,
}

#[derive(Copy, Clone, Debug, ValueEnum)]
enum TierArg {
    A,
    B,
    C,
    D,
}

impl From<TierArg> for ConfidenceTier {
    fn from(t: TierArg) -> Self {
        match t {
            TierArg::A => Self::A,
            TierArg::B => Self::B,
            TierArg::C => Self::C,
            TierArg::D => Self::D,
        }
    }
}

#[derive(Copy, Clone, Debug, ValueEnum)]
enum ReportFormat {
    Markdown,
    Json,
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
            ListWhat::Parameters {
                data_dir,
                tier,
                search,
                json,
            } => list_parameters(&data_dir, tier.map(Into::into), search.as_deref(), json),
            ListWhat::Channels => list_channels(),
        },
        Command::ValidateConfig { scenario } => validate_config(&scenario),
        Command::Validate { format, seed } => run_validation(format, seed),
        Command::HypothesisReport {
            samples,
            seed,
            format,
        } => run_hypothesis_report(samples, seed, format),
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

fn list_parameters(
    data_dir: &std::path::Path,
    tier: Option<ConfidenceTier>,
    search: Option<&str>,
    as_json: bool,
) -> Result<(), Box<dyn std::error::Error>> {
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

    let needle = search.map(str::to_lowercase);
    let mut ids: Vec<&str> = db
        .parameters()
        .filter(|p| tier.map_or(true, |t| p.tier == t))
        .filter(|p| {
            needle.as_ref().map_or(true, |n| {
                p.id.to_lowercase().contains(n)
                    || p.name.to_lowercase().contains(n)
                    || p.unit.to_lowercase().contains(n)
            })
        })
        .map(|p| p.id.as_str())
        .collect();
    ids.sort_unstable();

    if as_json {
        let entries: Vec<_> = ids
            .iter()
            .map(|id| {
                let p = db.parameter(id).expect("present");
                let c = db.citation(&p.citation);
                serde_json::json!({
                    "id": p.id,
                    "name": p.name,
                    "tier": format!("{:?}", p.tier),
                    "unit": p.unit,
                    "value": value_json(&p.value),
                    "citation": c.map(|c| serde_json::json!({
                        "id": c.id,
                        "authors": c.authors,
                        "title": c.title,
                        "venue": c.venue,
                        "year": c.year,
                        "doi": c.doi,
                        "pmid": c.pmid,
                    })),
                    "population": p.population,
                    "age_range_weeks": [p.age_range.min_weeks, p.age_range.max_weeks],
                })
            })
            .collect();
        let out = serde_json::json!({
            "data_dir": data_dir.display().to_string(),
            "n_parameters": entries.len(),
            "tier_filter": tier.map(|t| format!("{t:?}")),
            "search": search,
            "parameters": entries,
        });
        println!("{}", serde_json::to_string_pretty(&out)?);
        return Ok(());
    }

    println!(
        "{} parameter(s) in {}{}{}:",
        ids.len(),
        data_dir.display(),
        tier.map_or(String::new(), |t| format!(" [tier {t:?}]")),
        search.map_or(String::new(), |s| format!(" [search {s:?}]")),
    );
    for id in ids {
        let p = db.parameter(id).expect("present");
        let c = db
            .citation(&p.citation)
            .map_or("<missing citation>", |c| c.id.as_str());
        println!(
            "  [{:?}] {} = {} [cite:{}]",
            p.tier,
            p.id,
            value_summary(&p.value, &p.unit),
            c
        );
    }
    Ok(())
}

fn value_summary(v: &nidus_data::ValueSpec, unit: &str) -> String {
    match v {
        nidus_data::ValueSpec::Point { value, .. } => format!("{value} {unit}"),
        nidus_data::ValueSpec::Uniform { low, high } => format!("U[{low}, {high}] {unit}"),
        nidus_data::ValueSpec::Normal { mean, sd } => format!("N({mean}, sd={sd}) {unit}"),
        nidus_data::ValueSpec::Lognormal { mu, sigma } => {
            format!("logN(mu={mu}, sigma={sigma}) {unit}")
        }
    }
}

fn value_json(v: &nidus_data::ValueSpec) -> serde_json::Value {
    match v {
        nidus_data::ValueSpec::Point { value, uncertainty } => {
            serde_json::json!({ "kind": "point", "value": value, "uncertainty": uncertainty })
        }
        nidus_data::ValueSpec::Uniform { low, high } => {
            serde_json::json!({ "kind": "uniform", "low": low, "high": high })
        }
        nidus_data::ValueSpec::Normal { mean, sd } => {
            serde_json::json!({ "kind": "normal", "mean": mean, "sd": sd })
        }
        nidus_data::ValueSpec::Lognormal { mu, sigma } => {
            serde_json::json!({ "kind": "lognormal", "mu": mu, "sigma": sigma })
        }
    }
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

#[allow(clippy::cast_possible_truncation, clippy::cast_sign_loss)]
fn run_validation(format: ReportFormat, seed: u64) -> Result<(), Box<dyn std::error::Error>> {
    let mut suite = ValidationSuite::new();
    for case in built_in_cases() {
        suite.push(case);
    }
    let mut svc_rng =
        RngService::from_u64(seed).child_for(&SubscriberId::new(MATERNAL_CARDIO_ID), 0);
    let cardio = MaternalCardio::with_default_params(&mut svc_rng);
    let report = suite.run(|case, week| match case.component.as_str() {
        "nidus-maternal:cardio" => {
            cardio
                .evaluate(GestationalAge::from_weeks(week as u64))
                .cardiac_output_l_per_min
        }
        // Unknown component: emit NaN so the framework records the
        // residual but does not falsely claim agreement. New built-in
        // cases need a probe arm here.
        other => {
            eprintln!("warning: no probe wired for component `{other}`; emitting NaN");
            f64::NAN
        }
    });

    match format {
        ReportFormat::Markdown => print!("{}", report.render_markdown()),
        ReportFormat::Json => {
            let counts = report.summary_counts();
            let results: Vec<_> = report
                .results
                .iter()
                .map(|r| {
                    serde_json::json!({
                        "case_id": r.case_id,
                        "component": r.component,
                        "tier": format!("{:?}", r.tier),
                        "level": format!("{:?}", r.level),
                        "total_points": r.total_points,
                        "points_in_range": r.points_in_range,
                        "rms_residual": r.rms_residual,
                        "residuals": r.residuals,
                        "agreement": r.agreement.label(),
                    })
                })
                .collect();
            let out = serde_json::json!({
                "summary": {
                    "excellent": counts.excellent,
                    "adequate": counts.adequate,
                    "divergent": counts.divergent,
                    "unvalidatable": counts.unvalidatable,
                },
                "results": results,
            });
            println!("{}", serde_json::to_string_pretty(&out)?);
        }
    }
    Ok(())
}

#[allow(clippy::too_many_lines)]
fn run_hypothesis_report(
    samples: usize,
    seed: u64,
    format: ReportFormat,
) -> Result<(), Box<dyn std::error::Error>> {
    let specs = vec![
        ParameterSpec::new(
            "surface_area_m2",
            ConfidenceTier::B,
            SamplingStrategy::Uniform {
                low: 9.0,
                high: 15.0,
            },
        ),
        ParameterSpec::new(
            "half_saturation_area_m2",
            ConfidenceTier::C,
            SamplingStrategy::Uniform {
                low: 1.5,
                high: 4.5,
            },
        ),
        ParameterSpec::new(
            "max_equilibration",
            ConfidenceTier::C,
            SamplingStrategy::Uniform {
                low: 0.20,
                high: 0.40,
            },
        ),
    ];

    let analyser = SensitivityAnalyser::new(specs, samples, seed);
    let sensitivity = analyser.analyse(|sample| {
        let area = sample["surface_area_m2"];
        let half_sat = sample["half_saturation_area_m2"];
        let max_eq = sample["max_equilibration"];
        let eff = max_eq * area / (area + half_sat);
        // Maternal arterial PO₂ ≈ 95 mmHg; fetal-return UA PO₂ ≈ 16 mmHg.
        16.0 + eff * (95.0 - 16.0)
    });

    let suggester = ExperimentDesignSuggester::new()
        .with_info(
            "surface_area_m2",
            SuggesterParameterInfo {
                current_estimate: 12.0,
                current_uncertainty: 3.0,
                outcomes_affected: vec!["fetal-umbilical-vein-PO2".to_owned()],
                available_techniques: vec!["stereological estimation from histology".to_owned()],
            },
        )
        .with_info(
            "half_saturation_area_m2",
            SuggesterParameterInfo {
                current_estimate: 3.0,
                current_uncertainty: 1.5,
                outcomes_affected: vec!["fetal-umbilical-vein-PO2".to_owned()],
                available_techniques: vec![
                    "fit equilibration coefficient against UV PO2 indexed by gestational age"
                        .to_owned(),
                ],
            },
        )
        .with_info(
            "max_equilibration",
            SuggesterParameterInfo {
                current_estimate: 0.28,
                current_uncertainty: 0.10,
                outcomes_affected: vec!["fetal-umbilical-vein-PO2".to_owned()],
                available_techniques: vec![
                    "asymptotic fit of UV PO2 in pregnancies with large placental surface area"
                        .to_owned(),
                ],
            },
        );
    let suggestions = suggester.suggest(&sensitivity);

    match format {
        ReportFormat::Json => {
            let sens_entries: Vec<_> = sensitivity
                .indices
                .iter()
                .map(|(name, idx)| {
                    serde_json::json!({
                        "parameter": name,
                        "tier": format!("{:?}", idx.tier),
                        "first_order": idx.first_order,
                        "total_order": idx.total_order,
                    })
                })
                .collect();
            let sugg_entries: Vec<_> = suggestions
                .iter()
                .map(|s| {
                    serde_json::json!({
                        "parameter": s.parameter_name,
                        "tier": format!("{:?}", s.tier),
                        "total_order_index": s.total_order_index,
                        "first_order_index": s.first_order_index,
                        "expected_information_yield": s.expected_information_yield,
                        "current_estimate": s.current_estimate,
                        "current_uncertainty": s.current_uncertainty,
                        "outcomes_affected": s.outcomes_affected,
                        "available_techniques": s.available_techniques,
                    })
                })
                .collect();
            let out = serde_json::json!({
                "model": "placental-gas-exchange",
                "outcome": "fetal-umbilical-vein-PO2-mmhg-at-term",
                "samples": samples,
                "seed": seed,
                "outcome_variance": sensitivity.variance,
                "sensitivity": sens_entries,
                "suggestions": sugg_entries,
            });
            println!("{}", serde_json::to_string_pretty(&out)?);
        }
        ReportFormat::Markdown => {
            println!("# Hypothesis-design Report");
            println!();
            println!("- Model: placental gas exchange");
            println!("- Outcome: fetal umbilical-vein PO₂ (mmHg) at term");
            println!("- Samples (N): {samples}");
            println!("- Seed: {seed}");
            println!("- Outcome variance: {:.4}", sensitivity.variance);
            println!();
            println!("## Sobol indices");
            println!();
            println!("| Parameter | Tier | S_first | S_total |");
            println!("| --- | --- | --- | --- |");
            for (name, idx) in &sensitivity.indices {
                println!(
                    "| {name} | {} | {:.4} | {:.4} |",
                    idx.tier.label(),
                    idx.first_order,
                    idx.total_order,
                );
            }
            println!();
            println!("## Ranked experiment-design suggestions");
            println!();
            println!("| Rank | Parameter | Tier | Yield | Current estimate | Uncertainty |");
            println!("| --- | --- | --- | --- | --- | --- |");
            for (rank, s) in suggestions.iter().enumerate() {
                println!(
                    "| {} | {} | {} | {:.4} | {} | {} |",
                    rank + 1,
                    s.parameter_name,
                    s.tier.label(),
                    s.expected_information_yield,
                    s.current_estimate,
                    s.current_uncertainty,
                );
            }
        }
    }
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
