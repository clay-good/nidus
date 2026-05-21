# Spec 07 — Examples, Tutorials, and Module Documentation

## Context

The documentation has the right skeleton but holes a researcher will
trip over:

- [`docs/modules/`](../docs/modules/) directory is empty even though
  [`docs/README.md`](../docs/README.md) says it contains "one short
  page per crate" describing implementations.
- [`docs/validation/`](../docs/validation/) is empty (Spec 03 fills
  it).
- Tutorials exist but predate the v0.2 features they would showcase:
  [`docs/tutorials/README.md`](../docs/tutorials/README.md) lists
  several as "planned"; existing pages reference deferred features.
- [`examples/`](../examples/) directory at repo root is empty; the
  only worked Rust example is
  [`crates/nidus-hypothesis/examples/sensitivity_placental_gas_exchange.rs`](../crates/nidus-hypothesis/examples/sensitivity_placental_gas_exchange.rs).
- No CLI reference document.
- No "installation" page covering pip / cargo / binary paths.
- `README.md:55-65` lists crates as "(planned)" that are now shipped
  (audit item 156).

## Deliverables

- One module page per crate under `docs/modules/`.
- Four researcher-facing tutorials covering install, first scenario,
  tier interpretation, experiment design.
- A complete CLI reference.
- Rust examples under `crates/<crate>/examples/`; Python examples and
  shell drivers under `examples/`.
- A refreshed top-level `README.md` reflecting v0.2 reality.
- An out-of-date label sweep across all docs.

## Dependencies

Specs 01–06 must be substantially complete before final docs are
written; the install page (Prompt 07.5) depends on Spec 08
(release artefacts). Draft docs can land alongside their feature
specs.

## Numbered prompts

### Prompt 07.1 — Module documentation pages

Files: new files under [`docs/modules/`](../docs/modules/):
- `nidus-core.md`, `nidus-data.md`, `nidus-maternal.md`,
  `nidus-placenta.md`, `nidus-fetal.md`, `nidus-unknown.md`,
  `nidus-validation.md`, `nidus-scenarios.md`,
  `nidus-hypothesis.md`, `nidus-observability.md`,
  `nidus-cli.md`, `nidus-py.md`.

Each page covers, in two pages or less: purpose, public API surface,
the main `Subscriber`/`Params` types, the parameters it reads from
the database (link to id list), tier landscape, known limitations,
references to extended docs.

Verification: every page is linked from
[`docs/README.md`](../docs/README.md); every crate in
[`Cargo.toml`](../Cargo.toml) has a corresponding module page.

### Prompt 07.2 — Refresh `docs/architecture/overview.md`

File: [`docs/architecture/overview.md`](../docs/architecture/overview.md).

Remove "(planned: web dashboard, Jupyter)" and any other "planned"
references whose features have shipped. Add a section on the
manifest format (linking Spec 06).

### Prompt 07.3 — Tutorial: Installing Nidus

File: new [`docs/tutorials/installing.md`](../docs/tutorials/installing.md).

Three paths in parallel columns:
1. Researcher path: `pip install nidus`, then run a one-liner.
2. CLI-only path: download a prebuilt binary from the latest release
   (links to Spec 08 artefacts), or `cargo install nidus-cli`.
3. Developer path: clone, `cargo build --workspace`, `maturin
   develop`.

Document each platform's quirks (Apple Silicon, Windows Defender,
HPC modules). Test by running the commands on a fresh machine.

### Prompt 07.4 — Tutorial: Running your first scenario

File: new [`docs/tutorials/running_first_scenario.md`](../docs/tutorials/running_first_scenario.md).

Parallel CLI / Python columns. Loads `normal_term`, runs, points the
reader at the four output files, walks the Markdown summary, then
plots one quantity in Python.

### Prompt 07.5 — Tutorial: Interpreting confidence tiers

File: new [`docs/tutorials/interpreting_tiers.md`](../docs/tutorials/interpreting_tiers.md).

Worked example reading a tier-D output (fetal endocrine, say),
clicking through to the citation list, looking at the underlying
unknown channel, and deciding whether to trust the number. Ends with
a short rubric for researchers communicating Nidus output to
collaborators.

### Prompt 07.6 — Tutorial: Designing an experiment

File: new [`docs/tutorials/designing_an_experiment.md`](../docs/tutorials/designing_an_experiment.md).

Walks from `nidus hypothesis-report` output to a pre-registered
experiment outline (PICO format, expected effect size, sample-size
estimate). Encourages users to file the resulting design as a GitHub
issue using the `hypothesis-proposal.yml` template (Spec 09).

### Prompt 07.7 — Refresh existing tutorials

Files: existing tutorials in
[`docs/tutorials/`](../docs/tutorials/).

Update [`unknown_channels.md`](../docs/tutorials/unknown_channels.md),
[`hypothesis_workflow.md`](../docs/tutorials/hypothesis_workflow.md),
[`contributing_parameter.md`](../docs/tutorials/contributing_parameter.md)
to reflect: the now-populated parameter database (Spec 01), the
v0.2 hypothesis pipeline (Spec 11), the new validation cases (Spec
03), and the Python API (Spec 04).

Verification: every command shown in the tutorials runs verbatim on
a fresh clone.

### Prompt 07.8 — CLI reference document

File: new [`docs/cli-reference.md`](../docs/cli-reference.md).

Generated mostly from clap's `--help` output (`clap-mangen` or a
custom dump), then hand-edited to add examples and link to relevant
tutorials. Documents exit-code semantics, environment variables,
config-file locations.

### Prompt 07.9 — Rust examples under each crate

Files:
- new [`crates/nidus-maternal/examples/cardio_trajectory.rs`](../crates/nidus-maternal/examples/cardio_trajectory.rs)
- new [`crates/nidus-placenta/examples/glucose_flux_sweep.rs`](../crates/nidus-placenta/examples/glucose_flux_sweep.rs)
- new [`crates/nidus-fetal/examples/growth_vs_nichd.rs`](../crates/nidus-fetal/examples/growth_vs_nichd.rs)
- new [`crates/nidus-unknown/examples/custom_channel.rs`](../crates/nidus-unknown/examples/custom_channel.rs)
  (closes audit item 150)
- new [`crates/nidus-validation/examples/custom_case.rs`](../crates/nidus-validation/examples/custom_case.rs)
  (closes audit item 148)
- new [`crates/nidus-scenarios/examples/scenario_with_overrides.rs`](../crates/nidus-scenarios/examples/scenario_with_overrides.rs)

Each example is runnable via `cargo run -p <crate> --example
<name>`, prints meaningful output, and is referenced from the
corresponding `docs/modules/` page.

### Prompt 07.10 — Top-level `examples/` directory

Files: new in [`examples/`](../examples/):
- `README.md` indexing every example.
- `scenarios_normal_term.sh` — shell driver that runs the canonical
  workflow end-to-end.
- `parameter_sweep.py` — sweeps maternal MAP, emits CSV.
- `validation_local.sh` — runs the suite, opens the report.
- `python_quickstart.py` — mirror of the notebook (Spec 04).
- `unknown_channel_ensemble.py` — runs the channel registry across
  modes.

Each example tested on a clean clone.

### Prompt 07.11 — Refresh top-level `README.md`

File: [`README.md`](../README.md).

Updates (audit item 156):
- Lines 55–65: remove "(planned)" labels from shipped crates.
- Quickstart section: add the three install paths.
- "What Nidus is" section: add a sentence on the dashboard.
- Add the Zenodo DOI badge once Spec 08 mints it.
- Add CI badge.
- Add a "Cite Nidus" footer pointing at `CITATION.cff` and `nidus
  cite`.

### Prompt 07.12 — Glossary

File: new [`docs/glossary.md`](../docs/glossary.md).

Defines: confidence tier, unknown channel, subscriber, tick tier,
scenario, manifest, ensemble, Sobol index, NICHD percentile band.
Linked from every tutorial.

### Prompt 07.13 — Stale-label sweep

Cross-cutting cleanup: grep for "TBD", "coming soon", "planned",
"placeholder", "scaffold", "TODO" across all `.md` files. For each
hit, either delete the line (feature shipped) or move it to
[`PROGRESS.md`](../PROGRESS.md) under a `## v0.3+ roadmap` section.

Verification: `grep -rni "placeholder\|scaffold\|TBD\|coming soon"
docs/ README.md CONTRIBUTING.md CODE_OF_CONDUCT.md` returns no
hits.

## Acceptance for Spec 07

- [ ] One module page exists per crate.
- [ ] Six tutorials present: installing, first scenario, tiers,
  experiment design, unknown channels (refreshed), hypothesis
  workflow (refreshed), contributing parameter (refreshed).
- [ ] CLI reference exists and is up to date with `--help` output.
- [ ] `examples/` indexed; every script runs on a clean clone.
- [ ] `README.md` reflects v0.2 reality (no "planned" labels for
  shipped crates).
- [ ] No stale "scaffold/placeholder/TBD" strings in docs.
