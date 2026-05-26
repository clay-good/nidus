# Spec 01 — Dataset, Python Package, and Dashboard

**Status:** Active — primary v0.3 work; the dataset, package, notebooks, dashboard scaffold, CI, and essay are all built and pushed to `main`. The remaining gates to a tagged `v0.3.0` release are external (PyPI Trusted Publishing config, GitHub Pages source flip, Streamlit Cloud deploy, Zenodo integration enable) — those are maintainer-side one-time actions.
**Target release:** `v0.3.0`.
**Depends on:** [`00-overview.md`](00-overview.md) (read first).

---

## 1. Goal

Convert nidus from a Rust simulator into a **curated, citation-backed, confidence-tier-annotated open dataset of human gestational physiology parameters**, with a pure-Python package and a Streamlit dashboard layered on top.

The dataset is the centerpiece. Everything else is a presentation layer.

## 2. What we are doing (clear and plain)

1. **Delete all Rust code.** Remove `crates/`, `Cargo.toml`, `Cargo.lock`, `target/`. Git history preserves it; no archive branch is created.
2. **Extract curated TOML parameters into JSON** under `dataset/parameters/`.
3. **Extract the citation index into JSON** under `dataset/citations/`.
4. **Define JSON Schemas** (draft 2020-12) for parameters, citations, tiers.
5. **Add a JSON-LD context** so the dataset is FAIR-compliant linked data.
6. **Write a Python package** `nidus` (pure Python) that loads, filters, and queries the dataset. Publish to PyPI.
7. **Write a Streamlit dashboard** that browses the dataset. Host free on Streamlit Community Cloud.
8. **Write 4–5 reference Jupyter notebooks** as canonical tutorials. Execute end-to-end in CI.
9. **Deposit on Zenodo** for a permanent DOI on every release. Update `CITATION.cff`.

## 3. What we are NOT doing

| Not doing                                          | Why                                                                                  |
| -------------------------------------------------- | ------------------------------------------------------------------------------------ |
| Keeping the Rust engine in any form                | Wrong language for the audience. Adds compile complexity. Wrong signal.              |
| PyO3 kernel for sensitivity widgets                | NumPy/SciPy is sufficient. ~30 lines of Python.                                      |
| `engine-rs/` subdirectory or any retained crate    | Git history is the archive.                                                          |
| Archive branch                                     | Main only. Clean.                                                                    |
| Custom domain                                      | GitHub + PyPI + Streamlit Cloud are the canonical URLs.                              |
| New biology beyond what is already curated         | Dataset-only scope. No new subsystems.                                               |
| Twin / multiple pregnancies                        | Out of scope.                                                                        |
| Embryonic period (<8 weeks)                        | Out of scope.                                                                        |
| Labour and delivery                                | Out of scope.                                                                        |
| Clinical decision support                          | Out of scope forever.                                                                |
| Automated parameter extraction by LLMs             | Humans verify.                                                                       |

## 4. Repo layout

```
nidus/
├── dataset/                         # PRIMARY: the curated dataset
│   ├── parameters/                  # one JSON file per subsystem group
│   │   ├── maternal_cardiovascular.json
│   │   ├── maternal_respiratory.json
│   │   ├── maternal_renal.json
│   │   ├── placental_structure.json
│   │   ├── placental_gas_exchange.json
│   │   ├── placental_glucose.json
│   │   ├── fetal_circulation.json
│   │   ├── fetal_growth.json
│   │   └── fetal_metabolism.json
│   ├── citations/
│   │   └── citations.json
│   ├── tiers/
│   │   └── tiers.json
│   ├── schema/                      # JSON Schema (draft 2020-12)
│   │   ├── parameter.schema.json
│   │   ├── citation.schema.json
│   │   └── tier.schema.json
│   ├── jsonld/
│   │   ├── context.jsonld
│   │   └── ontology.ttl
│   ├── DATASET.md
│   └── CHANGELOG.md                 # dataset semver, independent
│
├── python/                          # PRIMARY: pip-installable package
│   ├── pyproject.toml
│   ├── nidus/
│   │   ├── __init__.py
│   │   ├── load.py
│   │   ├── filter.py
│   │   ├── citations.py
│   │   ├── tiers.py
│   │   ├── trajectories.py          # parametric forms (gaussian, logistic, polynomial) in NumPy
│   │   └── validate.py
│   └── tests/
│
├── dashboard/                       # PRIMARY: Streamlit app
│   ├── app.py
│   ├── pages/
│   └── requirements.txt
│
├── notebooks/                       # PRIMARY: reference notebooks
│   ├── 01_parameter_explorer.ipynb
│   ├── 02_tier_walkthrough.ipynb
│   ├── 03_sensitivity_example.ipynb
│   ├── 04_citation_provenance.ipynb
│   └── essay_figures.ipynb          # generates figures for the blog essay (Spec 03)
│
├── docs/                            # mkdocs-material site
├── .github/workflows/
├── pyproject.toml                   # monorepo tooling
├── README.md
├── LICENSE                          # MIT (code)
├── LICENSE-DATASET                  # CC-BY-4.0 (dataset)
└── CITATION.cff
```

There is **no** `crates/`, no `Cargo.toml`, no `Cargo.lock`, no `target/`, no `engine-rs/`, no `archive/` branch. Removed entirely.

## 5. Pivot execution order

1. Tag the prior state as `v0.2-archive` (annotated tag, no branch) so git history points to the Rust prototype under a memorable label. Push the tag.
2. Delete `crates/`, `Cargo.toml`, `Cargo.lock`, `target/`, `scenarios/`, `examples/` (simulator-era), old TOML in `data/`. One commit.
3. Create `dataset/` skeleton + JSON Schemas. One commit.
4. Convert curated TOML parameters to JSON, one subsystem per commit. Schema-validate each.
5. Convert citation index to JSON. Schema-validate.
6. Create `python/nidus/` skeleton with `load()` and minimal filter API. Tests pass.
7. Reserve `nidus` on PyPI (confirmed available). Publish `v0.3.0a1` as a dry run.
8. Build Streamlit dashboard: Home, Parameter Explorer, Trajectory Viewer.
9. Add remaining dashboard pages.
10. Write 4 reference notebooks. Wire `nbmake` in CI.
11. Rewrite `docs/` for the new form factor using `mkdocs-material`.
12. Deploy dashboard to Streamlit Community Cloud.
13. Cut `v0.3.0`. GitHub release. Zenodo auto-deposits, mints DOI. Update `CITATION.cff`.
14. Trigger Spec 03 (blog essay) within the same week.

## 6. Dataset specification

### 6.1 Parameter JSON Schema

```json
{
  "id": "maternal.cardio.cardiac_output.peak_amplitude",
  "name": "Cardiac output peak amplitude (rise above non-pregnant baseline)",
  "subsystem": "maternal_cardiovascular",
  "category": "hemodynamics",
  "value": {
    "central": 1.55,
    "low": 1.30,
    "high": 1.80,
    "units": "L/min",
    "distribution": "normal",
    "ci": 0.95
  },
  "trajectory": {
    "type": "gaussian",
    "params": {"peak_week": 30, "fwhm_weeks": 12, "baseline_L_per_min": 5.0},
    "valid_range_weeks": [8, 40]
  },
  "tier": "B",
  "tier_rationale": "Multiple longitudinal cohort studies (n>200 each); CIs overlap across cohorts; mechanism well understood.",
  "citations": ["mahendru2014", "sanghavi2014", "hunter1992"],
  "primary_citation": "mahendru2014",
  "extraction": {
    "method": "table_2_column_3",
    "by": "claygood",
    "date": "2026-04-15",
    "review_status": "verified"
  },
  "applicability": {
    "population": "healthy_singleton",
    "excludes": ["twins", "chronic_hypertension", "preexisting_diabetes"]
  },
  "notes": "Polynomial fit, not mechanistic. Do not extrapolate outside 8–40 weeks."
}
```

Required fields: `id`, `name`, `subsystem`, `value`, `tier`, `tier_rationale`, `citations`, `extraction.review_status`.
Optional: `trajectory`, `applicability`, `notes`, `category`.

### 6.2 Citation JSON Schema

```json
{
  "key": "mahendru2014",
  "type": "journal-article",
  "title": "A longitudinal study of maternal cardiovascular function from preconception to the postpartum period",
  "authors": ["Mahendru, A. A.", "Everett, T. R.", "Wilkinson, I. B.", "Lees, C. C.", "McEniery, C. M."],
  "year": 2014,
  "journal": "Journal of Hypertension",
  "doi": "10.1097/HJH.0000000000000090",
  "pmid": "24406777",
  "open_access": false
}
```

Required: `key`, `type`, `title`, `authors`, `year`, plus at least one of {`doi`, `pmid`, `url`}.

### 6.3 Tier definitions

Canonical file `dataset/tiers/tiers.json`:

```json
{
  "A": {"label": "Well-established", "criteria": ["≥3 independent studies", "CIs overlap", "mechanism grounded", "validated in ≥2 populations"]},
  "B": {"label": "Supported", "criteria": ["1–2 longitudinal studies (n≥100)", "plausible mechanism", "no strong contradicting evidence"]},
  "C": {"label": "Provisional", "criteria": ["single study OR cross-sectional only OR small n", "mechanism speculative"]},
  "D": {"label": "Unknown", "criteria": ["no quantitative data", "hypothesised channel", "for research-question purposes only"]}
}
```

### 6.4 JSON-LD context

`dataset/jsonld/context.jsonld` maps:
- `schema:ScholarlyArticle` for citations,
- `schema:PropertyValue` for parameters,
- `nidus:confidenceTier` (custom predicate) for tier annotation,
- DOI / PMID via `identifiers.org` URIs.

`dataset/jsonld/ontology.ttl` defines the `nidus:` vocabulary in Turtle.

### 6.5 Versioning + DOI

- Dataset uses semver in `dataset/CHANGELOG.md`, independent of code semver.
- GitHub Releases auto-trigger Zenodo deposit via the GitHub-Zenodo integration.
- `CITATION.cff` updated on each release; references the Zenodo concept DOI (always resolves to latest).

## 7. Python package (`nidus` on PyPI)

### 7.1 Distribution

- Package name: `nidus`. (Confirmed available on PyPI.)
- Min Python: 3.10.
- **Pure Python.** No compiled extensions. One platform-independent wheel.
- Dependencies: `pydantic>=2`, `jsonschema`, `numpy`, `requests` (citation resolution).
- Optional: `nidus[plot]` adds `matplotlib`.

### 7.2 Public API

```python
import nidus

ds = nidus.load()                                # bundled dataset
ds = nidus.load(version="0.3.1")                 # pinned
ds = nidus.load(path="path/to/dataset/")         # custom

maternal = ds.filter(subsystem="maternal_cardiovascular", tier=["A", "B"])
unknowns = ds.filter(tier="D")

co = ds["maternal.cardio.cardiac_output.peak_amplitude"]
co.value.central
co.tier
co.citations
co.at(week=24)                                   # evaluate trajectory

cite = ds.citations["mahendru2014"]
cite.doi

nidus.validate(path="path/to/dataset/")          # JSON Schema validation
```

### 7.3 Quality bars

- `mypy --strict` clean.
- ≥90% line coverage.
- `ruff` clean.
- Public API stable from v0.3.0 forward (additive changes only until v0.4).

## 8. Dashboard

**Framework:** Streamlit. **Hosting:** Streamlit Community Cloud (free, auto-deploys from `main`).

Why Streamlit: Python-native, matches audience, zero deployment cost, trivial to run locally (`streamlit run dashboard/app.py`).

Pages:

1. **Home** — what nidus is, how to cite (DOI), tier system, link to dataset and blog essay.
2. **Parameter Explorer** — searchable, filterable table; row click → detail view.
3. **Subsystem Deep-Dive** — one page per subsystem; tier distribution, citation density.
4. **Trajectory Viewer** — pick a mechanistic submodel → plot its trajectory over its natural domain (gestational age 8–40 weeks for time trajectories; PO2 mmHg / substrate mmol/L / cortisol μg/dL / fetal weight g for algebraic submodels). Tier badge for the worst-tier input; per-parameter detail with citations. Backed by `nidus.export.evaluate_submodel` + `submodel_domain`, which bind 36 of the 41 registered submodels (the five Hadlock biometry / EFW fits use a list-of-anchors kernel signature and are listed without a plot).
5. **Sensitivity Sandbox** — pick a submodel + an input parameter, sweep it ±X%, plot the trajectory family. Same kernel binding; uses `evaluate_submodel(..., overrides=...)` so the sweep is one-line.
6. **Citation Provenance** — citation → list of supported parameters, and inverse.
7. **Unknowns Registry** — Tier D entries as structured research questions.
8. **Download** — full dataset (ZIP), per-subsystem subsets, BibTeX, COMBINE archive (if/when Spec 02 ships).

## 9. Notebooks

Five reference notebooks in `notebooks/`. Heavily annotated. Executed end-to-end in CI via `nbmake`.

1. `01_parameter_explorer.ipynb` — loading, filtering, plotting.
2. `02_tier_walkthrough.ipynb` — tier meanings, assignment, propagation.
3. `03_sensitivity_example.ipynb` — vary a Tier-B parameter; observe downstream.
4. `04_citation_provenance.ipynb` — citation graph; BibTeX export.
5. `essay_figures.ipynb` — generates figures for the Spec 03 blog essay. Seeded, deterministic.

## 10. Testing & CI

GitHub Actions on every PR:

- **Dataset validation** — JSON Schema for every parameter, citation, tier.
- **Citation cross-reference** — every `citations[]` in a parameter resolves to a real citation key.
- **Citation reachability** — weekly cron: HEAD-request every DOI; warn on 404. Non-blocking on PR.
- **Python:** `pytest`, `mypy --strict`, `ruff`.
- **Notebooks:** `nbmake` runs every notebook.
- **Dashboard smoke test:** headless Streamlit boot; assert no exception in first 10s.

Release pipeline (on tag push `v*.*.*`):
- Build Python wheel, publish to PyPI.
- GitHub Release.
- Zenodo auto-deposits, mints DOI.
- Update `CITATION.cff`.

## 11. Documentation

`docs/` rewritten as `mkdocs-material` site:

- `index.md` — same as root README.
- `getting-started/` — install, quickstart, dashboard tour.
- `dataset/` — schema reference, tier definitions, subsystem coverage.
- `tutorials/` — extracted from notebooks.
- `contributing/` — add a parameter, verify a citation, assign a tier.
- `methodology/` — links to the Spec 03 blog essay.

Deployed via GitHub Pages on tag.

## 12. Success criteria for `v0.3.0`

Status as of the current commit on `main`:

- [x] All Rust code removed from working tree.
- [x] All 54 parameters in JSON, schema-valid.
- [x] All citations in JSON with DOI or PMID where available (30/32; the 2 without identifiers are pre-DOI books).
- [x] `pip install nidus` works (CI builds + smoke-tests the wheel in a clean venv on every push).
- [ ] Dashboard live at a public Streamlit Cloud URL — *pending external Streamlit Cloud connection step (maintainer-side).*
- [x] All 5 reference notebooks execute end-to-end in CI.
- [ ] First Zenodo DOI minted; `CITATION.cff` references it — *pending v0.3.0 tag release.*
- [x] README rewritten; simulator-era framing removed.
- [x] Old specs deleted (deprecation stubs removed once nothing referenced them; original content preserved in git history and at the `v0.2-archive` tag).
- [x] Essay (Spec 03) drafted and shipped in the repository at `docs/about/essay.md` with three committed figures.

Bonus (beyond the original v0.3 spec):

- [x] **Citation metadata audit + repair tooling**: 22 wrong DOI/PMID identifiers in the v0.2 corpus traced back to the correct papers via Crossref title-search; 23 additional PMIDs resolved via NCBI IdConverter and added.
- [x] **14 of 54 parameters promoted to `extraction.review_status: "verified"`** via PMC full-text reads (5 parameters) and triangulation across publisher records + multiple secondary references (9 parameters). 1 parameter promoted to `contested` (`maternal_cardiovascular.baseline_uterine_flow_ml_per_min`); see [`docs/dataset/verified-examples.md`](../../dataset/verified-examples.md) for the gold-standard provenance exemplars.
- [x] **All 31 placeholder `tier_rationale` fields rewritten** with substantive evidence from the verified citation abstracts / PMC full text / multi-source triangulation.
- [x] **`nidus` CLI shipped** with `version`, `validate`, `info`, and `export --format {bibtex,csv}` subcommands.
- [x] **Coverage 95.45%** across the package; `nidus.validate` at 100%.

## 13. Timeline (realistic — solo dev, evenings/weekends)

| Week  | Milestone                                                                 |
| ----- | ------------------------------------------------------------------------- |
| 1     | Delete Rust. Create `dataset/` skeleton. Write JSON Schemas.              |
| 2     | Convert TOML → JSON for all parameters. Validation passes in CI.          |
| 3     | Convert citations to JSON. DOI reachability check passes.                 |
| 4     | Python package skeleton: `load`, `filter`, basic tests. Reserve PyPI.     |
| 5     | Dashboard scaffold: Home, Parameter Explorer, Trajectory Viewer.          |
| 6     | Dashboard: remaining pages. Streamlit Cloud deploy.                       |
| 7     | Notebooks 01–04.                                                          |
| 8     | Docs rewrite (mkdocs-material).                                           |
| 9     | CI hardening; release rehearsal.                                          |
| 10    | Cut `v0.3.0`. PyPI + Zenodo + dashboard live. Publish blog essay (Spec 03). |

Realistic calendar: 3–5 months end to end. Solo dev pace.

## 14. Risks & mitigations

| ID  | Risk                                                              | Mitigation                                                                    |
| --- | ----------------------------------------------------------------- | ----------------------------------------------------------------------------- |
| R1  | Dataset feels small (54 params)                                   | Be honest in README; tier D entries explain gaps; not a coverage claim.       |
| R2  | Zero adoption                                                     | Blog essay (Spec 03) drives discovery. Realistic ceiling is small audience.   |
| R3  | Streamlit Cloud changes free tier                                 | Dashboard runs locally; HuggingFace Spaces documented as fallback.            |
| R4  | Citation DOIs rot                                                 | Weekly CI check; tier-degradation policy (primary citation 404 → drop a tier).|
| R5  | Schema churn breaks downstream consumers                          | Public API frozen from v0.3.0; breaking changes require major version bump.   |
| R6  | Solo maintainer burnout                                           | Scope is bounded; no biology expansion; docs make handoff possible.           |
| R7  | Researcher requests pull scope outward                            | Defer all such requests to v0.4+; v0.3 establishes form factor only.          |

## 15. Open questions

1. Final license file naming: `LICENSE` (MIT, code) + `LICENSE-DATASET` (CC-BY-4.0)? Or a single `LICENSE` with both? — Recommendation: two files for clarity.
2. Streamlit Cloud URL — `nidus.streamlit.app` if available; otherwise `nidus-pregnancy.streamlit.app`.
3. PyPI name confirmed available: `nidus`. Reserve immediately.
