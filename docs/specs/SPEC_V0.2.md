# SPEC_V0.2.md — Filling the Remaining Blanks

**Goal:** take Nidus from its current v0.1.0 state (engine + scaffolding,
17 prompts landed) to a state where a working science researcher — not a
Rust engineer — can clone the repository, install it, run a credible
simulation, inspect uncertainty, and contribute back parameters and
hypotheses without having to read the source tree first.

This document is a sibling to [SPEC.md](SPEC.md). SPEC.md defined the
v0.1.0 design and prompts 1–17; this document defines the v0.2.0
"researcher-ready" milestone as a numbered sequence of Claude Code
prompts. Each prompt is self-contained, references the artefacts it
must produce, and ends with a verification step. Work them in order;
later prompts depend on earlier ones.

The shape of every prompt below is:

> **Prompt N — short title.**
> Context: why this exists, what it unblocks.
> Task: concrete deliverables, listed.
> Acceptance: how to know it is done.

Mark each finished prompt in [PROGRESS.md](PROGRESS.md) under a new
"v0.2.0" section.

---

## Stream A — Make the parameter database real

The v0.1.0 database loads a scaffold. A researcher will not trust output
that says "Tier C — scaffold value, not verified." These prompts replace
that with verified, cited entries.

### Prompt A1 — Citation index population

Context: every Tier A/B parameter must point at a real reviewed source.
The scaffolding `index.toml` only has two entries, one of them a
placeholder.

Task:
1. Replace `data/citations/index.toml` with verified entries covering the
   sources named in SPEC.md §13 Prompt 5: Severinghaus 1979 (O₂–Hb), a
   modern revision (Dash & Bassingthwaighte 2010 or equivalent), Carter
   2009 / Mayhew 2014 for placental morphometry, Illsley 2000 for
   GLUT1, Baumann 2002 / Brown 2011 for GLUT3, Hytten & Chamberlain or
   Bernstein & Ziegler for maternal blood volume expansion, and the
   NICHD Fetal Growth Studies (Buck Louis 2015, Grewal 2018).
2. Each entry must carry `id`, `authors`, `title`, `venue`, `year`, a
   stable identifier (`pmid` or `doi`), and a `notes` field stating
   which parameters depend on it.
3. Remove the `scaffold-template-source` placeholder once nothing depends
   on it.
4. Add a `data/citations/README.md` explaining the verification workflow:
   reviewer must obtain the PDF, confirm the numeric values, initial
   the PR.

Acceptance: `cargo test -p nidus-data` still passes; every citation id
referenced by a parameter file resolves; no entry has `notes` containing
the word "scaffold" or "placeholder".

### Prompt A2 — Maternal parameter coverage

Context: `data/parameters/maternal/blood.toml` is the only maternal file.
Maternal cardio uses hard-coded `MaternalCardioParams` defaults flagged
as scaffolding.

Task:
1. Author `data/parameters/maternal/cardio.toml` with gestational-age
   trajectories for cardiac output, stroke volume, heart rate, MAP,
   and uterine artery flow. Use `ValueSpec::normal` with population mean
   and SD from cited sources; supply `AgeRange` blocks per trimester.
2. Extend `blood.toml` with plasma volume, red cell mass, haematocrit,
   plasma oncotic pressure, and fibrinogen across gestation.
3. Add `data/parameters/maternal/respiratory.toml` (minute ventilation,
   PaCO₂, PaO₂, oxyhaemoglobin P50 shift) and
   `data/parameters/maternal/renal.toml` (GFR, plasma creatinine).
4. Update [`crates/nidus-maternal/src/cardio.rs`](crates/nidus-maternal/src/cardio.rs)
   so `MaternalCardioParams::from_database(&ParameterDatabase)` is the
   primary constructor; the hard-coded defaults become a fallback only
   used in unit tests, gated behind `#[cfg(test)]`.

Acceptance: `nidus list parameters --tier A` returns at least twenty
entries; running the normal-term scenario logs zero parameters with the
"scaffold" notes string.

### Prompt A3 — Placental and fetal parameter coverage

Context: the placental gas exchange and fetal circulation models also
fall back to coded defaults.

Task:
1. Author `data/parameters/placenta/structure.toml` (villous surface
   area, membrane thickness, intervillous volume) and
   `data/parameters/placenta/transport.toml` (O₂ and CO₂ diffusion
   capacities, GLUT1/GLUT3 Vmax/Km, amino-acid system A/L capacities).
2. Author `data/parameters/fetal/circulation.toml`,
   `data/parameters/fetal/growth.toml` (NICHD biometric percentiles),
   and `data/parameters/fetal/metabolism.toml`.
3. Wire each subsystem's `Params` struct to load from the database the
   same way as Prompt A2.
4. Add an integration test in [`crates/nidus-scenarios/`](crates/nidus-scenarios/)
   that runs the normal-term scenario fully from database-derived
   parameters and asserts the third-trimester O₂ delivery is within
   the literature range cited in `placenta/transport.toml`.

Acceptance: the integration test passes; `cargo run -p nidus-cli --
list parameters --tier A` shows coverage across maternal, placental,
and fetal categories.

---

## Stream B — Validation against published data

A research tool earns trust by reproducing measurements it was not
fitted to. Prompt 14 only shipped a scaffold case.

### Prompt B1 — Reference dataset adapters

Task:
1. Create `crates/nidus-validation/src/datasets/` with one Rust file per
   reference dataset: `nichd_growth.rs`, `placental_doppler.rs`,
   `fetal_cardiac.rs`.
2. Each adapter exposes a `Dataset` struct with: source citation id,
   the measured quantity, the age range, and per-age `(mean, sd,
   percentiles)` rows.
3. Source data lives under `data/validation/` as TOML so it is reviewable
   in PRs. Adapters parse it at load time and are cached.

Acceptance: `cargo test -p nidus-validation` covers loader round-trips
for each dataset; every dataset row points at a citation id that resolves.

### Prompt B2 — Validation cases

Task:
1. For each adapter from B1, add a `ValidationCase` that runs the
   normal-term scenario, extracts the matching simulator output via
   the telemetry bus, and compares against the dataset using the
   tier-aware tolerances from SPEC.md §10.
2. Wire all cases into `nidus_validation::builtin::suite()`.
3. The `nidus validate` CLI subcommand already exists; extend its
   Markdown report to render a per-case pass/fail table grouped by
   subsystem.

Acceptance: `nidus validate --format markdown` produces a report with
at least the three new cases listed; passing/failing both render
readably; the JSON form is schema-stable (document the schema in
`docs/validation/report-schema.md`).

### Prompt B3 — Validation documentation

Task: populate the empty [`docs/validation/`](docs/validation/) directory
with: `overview.md` (what the suite covers and why), one
`case-<name>.md` per case (datasets, tolerance choice, current status),
and `extending.md` (how to add a new case).

Acceptance: the docs tree links from [`docs/README.md`](docs/README.md);
every case file references the same citation id used in TOML.

---

## Stream C — Python interface

A researcher will reach for Python before Rust. `nidus-py` is currently
an empty placeholder.

### Prompt C1 — PyO3 bindings

Task:
1. Replace [`crates/nidus-py/`](crates/nidus-py/) with a PyO3 + maturin
   project. Use `abi3` for forward-compatibility.
2. Expose, at minimum: `Scenario.load_builtin(name)`,
   `Scenario.from_toml(path)`, `Scenario.run() -> RunResult`,
   `RunResult.telemetry() -> pandas.DataFrame`, `RunResult.to_ndjson(path)`,
   `ParameterDatabase.load(path)` and `.list(tier=None, search=None)`.
3. Determinism and tier propagation must round-trip through Python: a
   `Tiered` Python class shows `.value`, `.tier`, `.citations`.
4. Build wheels for cp39+ on Linux/macOS/Windows in CI.

Acceptance: `pip install -e crates/nidus-py` in a fresh venv, then
`python -c "import nidus; print(nidus.Scenario.load_builtin('normal_term').run().telemetry().head())"`
prints a dataframe.

### Prompt C2 — Jupyter quickstart notebook

Task: add `examples/quickstart.ipynb` (also exported as
`examples/quickstart.py` for diff-ability) that walks a researcher
through: install, load normal-term scenario, run, plot maternal cardiac
output and fetal weight against gestational age with tier-coloured
confidence bands, then perturb a single parameter and re-plot.

Acceptance: notebook executes top-to-bottom with `jupyter nbconvert
--execute`; outputs are committed; figures use matplotlib only (no
extra deps).

### Prompt C3 — Hypothesis & sensitivity in Python

Task: extend the Python API so the workflow from
`crates/nidus-hypothesis/examples/sensitivity_placental_gas_exchange.rs`
is reachable as `nidus.hypothesis.sensitivity(model, params, n=1024)`
returning a dataframe of Sobol indices, and add `examples/hypothesis.ipynb`
demonstrating it end-to-end with a ranked experiment-design table.

Acceptance: notebook reproduces, within Monte Carlo error, the ranking
from the Rust example.

---

## Stream D — Researcher-facing UX

### Prompt D1 — Interactive dashboard (deferred from Prompt 15)

Task:
1. Create `dashboard/` at the repo root: a Vite + React + TypeScript
   single-page app that streams NDJSON telemetry from
   `nidus run --emit ndjson -` over a local websocket (`nidus serve`).
2. Views: maternal vital trajectories, placental transport,
   fetal-growth percentiles overlaid on NICHD curves, an
   unknown-channels panel listing currently-active uncertainty
   sources, and a scenario diff view.
3. Every plotted line carries its tier as a colour, and clicking a
   point opens the citation list for that quantity.
4. `cargo run -p nidus-cli -- serve` starts the websocket; `npm run
   dev` inside `dashboard/` starts the frontend.

Acceptance: a researcher running `nidus serve` and opening
`http://localhost:5173` sees live plots for the normal-term scenario
within ten seconds; killing `nidus serve` produces a visible
disconnected state, not a silent freeze.

### Prompt D2 — End-to-end researcher tutorials

Task: expand [`docs/tutorials/`](docs/tutorials/) with:
1. `installing.md` — three install paths (cargo, pip, prebuilt
   binaries from a GitHub Release).
2. `running_first_scenario.md` — CLI + Python paths in parallel
   columns.
3. `interpreting_tiers.md` — worked example reading a tier-D output
   and deciding whether to trust it.
4. `designing_an_experiment.md` — from hypothesis-report output to a
   pre-registered experiment outline.

Acceptance: each tutorial has been executed end-to-end on a clean
machine; commands shown work verbatim.

### Prompt D3 — CLI polish

Task:
1. Add `nidus run <scenario> [--out dir]` as the single high-level
   command; it writes NDJSON telemetry, a Markdown summary, and a
   reproducibility manifest (seed, git sha, parameter database hash)
   to `out/`.
2. Add `nidus doctor` that prints the toolchain versions, the loaded
   parameter database hash, and the count of Tier A/B/C/D parameters.
3. Add `--seed` and `--age-range` as top-level flags so a researcher
   can sweep without editing TOML.

Acceptance: `nidus doctor` on a clean clone reports zero errors and
matches the numbers in [README.md](README.md).

---

## Stream E — Distribution, citation, reproducibility

### Prompt E1 — Release artefacts

Task:
1. GitHub Actions release workflow (`.github/workflows/release.yml`)
   that, on a tag `v*`, builds:
   - Rust binaries for linux-x86_64, linux-aarch64, macos-arm64,
     windows-x86_64;
   - Python wheels via `maturin`;
   - A source tarball with `Cargo.lock` and the full `data/` tree.
2. Each artefact ships with `SHA256SUMS` signed via Sigstore (`cosign`).
3. The release notes are generated from [CHANGELOG.md](CHANGELOG.md).

Acceptance: a dry-run tag against a fork produces all artefacts and
they install on a clean VM.

### Prompt E2 — Software citation

Task:
1. Add `CITATION.cff` (Citation File Format 1.2.0) at repo root.
2. Mint a Zenodo DOI via the GitHub–Zenodo integration; record the
   concept DOI and per-version DOI in README.md and CITATION.cff.
3. Add a `cite` subcommand: `nidus cite` prints the BibTeX entry
   matching the running binary's version.

Acceptance: `nidus cite | grep '@software{nidus'` succeeds; the DOI in
the output resolves.

### Prompt E3 — Reproducibility manifest

Task: define the manifest schema written by `nidus run` (Prompt D3):
git SHA, parameter-database SHA-256, scenario TOML SHA-256, RNG seed,
Rust toolchain version, host OS, total tick count. Add a verifier:
`nidus reproduce <manifest.json>` re-runs and asserts byte-identical
NDJSON output. Document at `docs/reproducibility.md`.

Acceptance: `nidus reproduce` against a manifest produced an hour ago
on the same machine returns exit code 0; mutating one byte of the
parameter DB causes a clear mismatch report.

---

## Stream F — Project hygiene

### Prompt F1 — Examples directory

Context: [`examples/`](examples/) is empty.

Task: add at least
- `examples/scenarios_normal_term.sh` — shell driver that produces
  the canonical plots,
- `examples/python_quickstart.py` — mirror of the notebook,
- `examples/parameter_sweep.py` — sweeps maternal MAP and emits a
  CSV of fetal weight at term,
- `examples/README.md` indexing them.

Acceptance: each example runs from a clean clone; the README explains
prerequisites.

### Prompt F2 — Contributor onboarding

Task: refresh [CONTRIBUTING.md](CONTRIBUTING.md) with: how to run the
full validation suite locally, how to submit a parameter PR end-to-end
(with the PR template fields already in
`.github/PULL_REQUEST_TEMPLATE.md`), and the tier-promotion review
criteria. Add `.github/ISSUE_TEMPLATE/parameter-request.yml`,
`bug-report.yml`, and `hypothesis-proposal.yml`.

Acceptance: opening a new issue on GitHub presents the three templates;
the contributing doc references them.

### Prompt F3 — CI completeness

Task: ensure the GitHub Actions matrix runs, on every PR:
`cargo build --workspace`, `cargo test --workspace`, `cargo clippy
--workspace --all-targets -- -D warnings`, `cargo fmt --check`,
`maturin build` for the Python crate, and the validation suite via
`nidus validate --format json` with a failing exit code on any
regression. Cache the toolchain and target directory.

Acceptance: a green CI badge in [README.md](README.md); average PR
build under ten minutes.

### Prompt F4 — Final PROGRESS update

Task: append a `## v0.2.0` section to [PROGRESS.md](PROGRESS.md) with
one checkbox per prompt above; tick them as they land. Update
[CHANGELOG.md](CHANGELOG.md) under a new `## [0.2.0]` heading.

Acceptance: every prompt in this file has a corresponding checkbox; the
checkboxes match reality.

---

## Suggested ordering

Stream A is the unblock — until the parameter database is real,
Streams B/C/D will be demoing scaffold values. Run A1 → A2 → A3 first.

Then either:
- **Engineer-led path:** B → C → D → E → F.
- **Researcher-led path** (faster perceived progress): C1 + C2 → D2
  → B → D1 → E → F.

A reasonable team of two contributors plus an LLM assistant can land
v0.2.0 in roughly six focused weeks; a single contributor with the
assistant should plan on twelve.

---

## Definition of "100% complete for a researcher"

When all prompts above are checked, a researcher can:

1. Install Nidus from `pip` or a prebuilt binary in under five minutes.
2. Run a published scenario and reproduce the figures shown in
   `docs/tutorials/`.
3. Identify, for any plotted quantity, the citation list and the
   confidence tier.
4. Perturb a parameter from Python, re-run, and compare.
5. Generate a ranked experiment-design list against the current
   parameter database.
6. Cite Nidus with a DOI.
7. Submit a verified parameter PR using the existing review checklist.
8. Re-run a colleague's manifest and obtain byte-identical output.

That is the bar for v0.2.0.
