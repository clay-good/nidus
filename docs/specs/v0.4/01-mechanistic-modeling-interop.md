# Spec 01 — Mechanistic-Modeling Interop: SBML, CellML, PhysioCell

**Status:** Active — primary v0.4 work.
**Target release:** `v0.4.0`.
**Supersedes:** [`v0.3/02-sbml-cellml-export.md`](../v0.3/02-sbml-cellml-export.md).
**Depends on:** v0.3.0 shipped (dataset stable, schemas frozen).

---

## 1. Goal

Make the nidus dataset directly consumable in the three platforms the
computational-physiology community already uses to build mechanistic
models of gestational physiology:

1. **SBML** (Systems Biology Markup Language) — submitted to the
   **BioModels Database** at EMBL-EBI.
2. **CellML 2.0** — submitted to the **Physiome Model Repository** at
   the Auckland Bioengineering Institute.
3. **PhysioCell** — distributed as a drop-in `parameters.xml` plus a
   worked example, with announcement on the PhysioCell community
   channels.

Each platform's audience is small. Each is the right place to reach
the researchers who actually do mechanistic gestational modelling.

## 2. Why this is the right move now

The earlier conditional-spec for SBML/CellML was conservative about
maintenance load. The project owner has clarified that **maintenance
is not the binding constraint; community adoption is**. Under that
constraint, integrating with the platforms researchers already use is
strictly better than waiting for them to discover the Python API.

The dataset stays the centerpiece. The exported models are presentation
layers — the same dataset, projected into the formats each community
consumes natively.

## 3. Scope: what gets exported

For each exportable submodel, we ship one SBML file, one CellML file,
one PhysioCell-parameters entry, and one combined COMBINE archive
(for SBML/CellML). Each exported model is annotated with MIRIAM
references back to the cited primary literature plus custom RDF
predicates for the nidus confidence tier.

### 3.1 The submodels

Ten submodels derived directly from current dataset records:

| # | Submodel                                | Mathematical form                                          | Tier | Source parameters                                                                       |
| - | --------------------------------------- | ---------------------------------------------------------- | ---- | --------------------------------------------------------------------------------------- |
| 1 | Placental villous surface-area growth   | Logistic ODE: `dA/dt = r·A·(1 − A/K)`                     | B    | `placental_structure.{initial_area_m2, term_area_m2, growth_rate_per_week, midpoint_week}` |
| 2 | Maternal cardiac output trajectory      | Algebraic Gaussian: `CO(t) = base + A·exp(−((t−μ)/σ)²)`   | B    | `maternal_cardiovascular.{baseline_cardiac_output_l_per_min, peak_excess_cardiac_output_l_per_min, cardiac_output_peak_week, cardiac_output_spread_weeks}` |
| 3 | Maternal MAP trajectory                 | Algebraic Gaussian (nadir form)                            | B    | `maternal_cardiovascular.{baseline_map_mmhg, map_nadir_drop_mmhg, map_nadir_week, map_spread_weeks}` |
| 4 | Uterine artery flow growth              | Logistic: `Q(t) = baseline + (term − baseline)·logistic(k(t−t₀))` | C    | `maternal_cardiovascular.{baseline_uterine_flow_ml_per_min, term_uterine_flow_ml_per_min, uterine_flow_growth_rate_per_week}` |
| 5 | Placental glucose transport (GLUT1)     | Michaelis-Menten: `V = V_max·[S] / (K_m + [S])`            | B    | `placental_glucose.{glucose_glut1_km_mmol_per_l, glucose_glut1_vmax_per_area_mmol_per_min_per_m2}` |
| 6 | Placental glucose transport (GLUT3)     | Michaelis-Menten (high-affinity isoform)                   | B/C  | `placental_glucose.{glucose_glut3_km_mmol_per_l, glucose_glut3_vmax_per_area_mmol_per_min_per_m2}` |
| 7 | Venous-equilibrator O₂ exchange         | Algebraic equilibrium between umbilical-vein and intervillous-space PO₂ | C | `placental_gas_exchange.{gas_half_saturation_area_m2, gas_max_equilibration}` |
| 8 | O₂-Hb dissociation (Severinghaus form)  | Algebraic: `S = ((PO₂³ + 150·PO₂)⁻¹·23400 + 1)⁻¹`         | A    | `maternal_blood.{o2_hb_p50_maternal, o2_hb_hill_coefficient_maternal, oxyhb_bohr_coefficient}` |
| 9 | Maternal plasma-volume expansion        | Algebraic over gestational age (per de Haas 2017 meta)     | B    | `maternal_blood.{plasma_volume_l, plasma_volume_early_l}` |
| 10| Hadlock fetal-weight standard           | Log-regression algebraic: `log₁₀(W) = a + b·BPD + c·AC + d·FL` | A | `fetal_growth.{hadlock_coefficient, efw_*_g}` |

The selection criterion: each submodel is **mechanistic enough** to
express as either a true ODE or a published algebraic relationship.
Pure tabular records (e.g. specific EFW at a specific week) appear as
parameter values inside the relevant model, not as standalone models.

### 3.2 What does NOT get exported

Stated explicitly to anchor the scope:

- **The dataset itself.** SBML/CellML are not data interchange
  formats; downstream users still pull the JSON dataset for raw
  parameter values + uncertainty bounds.
- **Tier D entries.** By definition there is no quantitative model
  to export.
- **Discrete decision logic** (e.g. fetal shunt routing as a
  decision tree). SBML and CellML cannot express discrete state
  machines without overstatement.
- **Multi-cohort or multi-population stratifications.** Each
  exported model uses the dataset's central + sigma; race/ethnicity
  stratifications stay in the JSON dataset.

## 4. Per-platform deliverables

### 4.1 SBML L3v2 + `comp` package → BioModels Database

**Format**: SBML Level 3 Version 2 (current standard). The `comp`
(hierarchical model composition) package allows assembling
submodels into a top-level model when downstream users want to
compose them.

**Files produced** (under `exports/sbml/`):

- `placental_villous_growth.xml` — submodel 1
- `maternal_cardiac_output.xml` — submodel 2
- `maternal_map.xml` — submodel 3
- `uterine_flow.xml` — submodel 4
- `placental_glucose_glut1.xml` — submodel 5
- `placental_glucose_glut3.xml` — submodel 6
- `placental_o2_exchange.xml` — submodel 7
- `o2hb_dissociation.xml` — submodel 8
- `plasma_volume_expansion.xml` — submodel 9
- `hadlock_fetal_weight.xml` — submodel 10
- `nidus_pregnancy_v04.combine.omex` — bundled COMBINE archive
  containing all of the above plus per-model SED-ML descriptions for
  the canonical simulation experiments.

**Submission**: BioModels Database submission portal
(<https://www.ebi.ac.uk/biomodels/submit>). Each model gets a
`BIOMD0000000XXX` accession after curator review (4–8 weeks). The
COMBINE archive is the recommended submission unit.

**Annotations**: see §5.

### 4.2 CellML 2.0 → Physiome Model Repository

**Format**: CellML 2.0 (current standard, libcellml-compatible).
CellML's component model is a closer match for nidus's submodel
structure than SBML's reaction-network bias.

**Files produced** (under `exports/cellml/`):

- One `.cellml` file per submodel (same ten).
- `nidus_pregnancy.cellml` — top-level composition importing the
  per-submodel components.
- `nidus_pregnancy.sed-ml` — SED-ML simulation experiments.
- `nidus_pregnancy_cellml.omex` — COMBINE archive.

**Submission**: Physiome Model Repository workspace at
<https://models.physiomeproject.org/>. Workflow:

1. Create a `nidus-pregnancy-physiology` workspace via Mercurial
   push.
2. Add files; commit; push.
3. Create an "exposure" (publishable view) with metadata.
4. Request curator review for upgrade to "official" status.

Self-publishing the workspace gives an immediately-citable URL; the
official-curation upgrade is optional polish.

**Annotations**: see §5.

### 4.3 PhysioCell parameters + worked example

**Format**: PhysioCell consumes parameters via two XML files in its
config tree:

- `PhysiCell_settings.xml` for simulation-level constants (custom
  `user_parameters`).
- `cell_definitions.xml` for per-cell-type parameters (rates, sizes,
  motility).

For nidus, the natural surface is `user_parameters`: scalar values a
PhysioCell-based pregnancy-tissue model would consume.

**Files produced** (under `exports/physiocell/`):

- `nidus-parameters.xml` — a `<user_parameters>` block containing
  every nidus parameter as `<param name="..." type="double"
  units="..." description="...">central</param>`. Comments contain
  citation key + tier.
- `example_placental_tissue.xml` — a complete PhysioCell config
  demonstrating consumption: a minimal tissue domain importing
  glucose Km/Vmax, surface area, etc.
- `notebooks/physiocell_integration.ipynb` — a tutorial notebook
  showing how to load `nidus-parameters.xml` into a PhysioCell run
  and how to update parameters when the dataset is re-released.

**Distribution**: PhysioCell does not have a central model repository.
Announcement via:

- PhysioCell GitHub Discussions (<https://github.com/MathCancer/PhysiCell/discussions>).
- PhysioCell community Slack (the `#physicell-help` channel).
- PhysioCell-tutorials repository (PR to add a `pregnancy` example).
- Mention in the v0.4 outreach essay.

## 5. Annotation strategy (cross-format)

Every exported model carries three layers of annotation that preserve
the citation chain and the nidus tier system into the exchange format.

### 5.1 MIRIAM `bqbiol:isDescribedBy`

For every parameter that originates in a literature citation, add a
MIRIAM RDF triple linking that parameter (or species, or reaction) to
its citation's DOI and PMID via `identifiers.org` URIs.

Example (SBML annotation block):

```xml
<parameter id="cardiac_output_peak" value="1.55" units="L_per_min">
  <annotation>
    <rdf:RDF xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#"
             xmlns:bqbiol="http://biomodels.net/biology-qualifiers/"
             xmlns:nidus="https://github.com/clay-good/nidus/ontology#">
      <rdf:Description rdf:about="#cardiac_output_peak">
        <bqbiol:isDescribedBy rdf:resource="https://identifiers.org/doi/10.1097/hjh.0000000000000090"/>
        <bqbiol:isDescribedBy rdf:resource="https://identifiers.org/pubmed/24406777"/>
        <nidus:confidenceTier>B</nidus:confidenceTier>
        <nidus:tierRationale>Tier B from Mahendru et al. 2014: prospective longitudinal cohort of 54 healthy nulliparous women...</nidus:tierRationale>
        <nidus:datasetParameterId>maternal_cardiovascular.peak_excess_cardiac_output_l_per_min</nidus:datasetParameterId>
        <nidus:datasetVersion>0.4.0</nidus:datasetVersion>
        <nidus:reviewStatus>verified</nidus:reviewStatus>
      </rdf:Description>
    </rdf:RDF>
  </annotation>
</parameter>
```

CellML uses the same RDF syntax, embedded differently (in a `cmeta:id`
target).

### 5.2 SBO (Systems Biology Ontology) terms

Where the modelled relationship has a canonical SBO term, add it:

- Logistic growth → SBO:0000295 (logistic equation)
- Michaelis-Menten kinetics → SBO:0000028 (irreversible
  Michaelis-Menten) or SBO:0000326 (reversible)
- Hill equation → SBO:0000192 (Hill function)
- Algebraic rule (no kinetic interpretation) → SBO:0000412 (boundary
  condition) where applicable

### 5.3 Custom `nidus:` predicates

Predicates under namespace
`https://github.com/clay-good/nidus/ontology#`:

| Predicate                       | Object type                          | Used on                                |
| ------------------------------- | ------------------------------------ | -------------------------------------- |
| `nidus:confidenceTier`          | Literal: `"A"` / `"B"` / `"C"` / `"D"` | Every annotated parameter            |
| `nidus:tierRationale`           | Literal string                       | Every annotated parameter              |
| `nidus:datasetParameterId`      | Literal string (dotted id)           | Round-trip identifier                  |
| `nidus:datasetVersion`          | Literal string (semver)              | Top-level model annotation             |
| `nidus:reviewStatus`            | Literal: `"unverified"` / `"verified"` / `"contested"` | Per parameter |
| `nidus:applicabilityPopulation` | Literal string                       | Where applicable                       |
| `nidus:trajectoryValidRangeWeeks` | List of two numbers                | On parameters with bounded gestational windows |

The full ontology lives at `dataset/jsonld/ontology.ttl` and is
already loosely defined there. v0.4 hardens it into a versioned OWL
2 ontology submitted to BioPortal as a supporting artefact (a
secondary follow-up; not blocking the model exports).

## 6. Validation

Every exported model passes three layers of validation before
submission to a repository.

### 6.1 Static schema validation

- **SBML**: `libSBML.SBMLDocument.checkConsistency()` returns zero
  errors (warnings logged but not blocking).
- **CellML**: `libcellml.Validator.validateModel()` returns zero
  issues.
- **PhysioCell**: XSD validation against the PhysioCell config
  schema where available; otherwise structural lint.

### 6.2 Round-trip simulation

For each algebraic or kinetic submodel:

1. Load the SBML/CellML export with the standard tooling
   (`tellurium` for SBML; `OpenCOR`/`libcellml` for CellML).
2. Simulate the canonical experiment defined in the bundled SED-ML.
3. Compare output against a pure-NumPy reference implementation
   shipped under `python/nidus/_reference_kernels.py`.
4. Assert agreement: 1e-6 relative error for algebraic submodels,
   1e-4 for ODE submodels (loose tolerance on time-integration
   methods).

The reference kernels are *not* a new mechanistic engine — they are
unit-testable Python evaluations of the same algebraic relationships
the exported models encode, used solely to detect export errors.

### 6.3 MIRIAM compliance

Every `bqbiol:isDescribedBy` URI resolves to identifiers.org. Every
SBO term resolves to a real SBO accession. Custom `nidus:` predicates
match the published ontology.

## 7. Generation pipeline

```
dataset/parameters/*.json
        │
        ▼
python/nidus/export/
├── sbml.py          (libSBML)        — one module per submodel
├── cellml.py        (libcellml)
├── physiocell.py    (plain XML)
├── annotate.py      (MIRIAM, SBO, nidus predicates — shared)
├── sedml.py         (SED-ML simulation descriptions)
├── combine.py       (.omex archive packaging)
└── reference.py     (the NumPy kernels for round-trip validation)
        │
        ▼
exports/{sbml,cellml,physiocell}/*.*
exports/combine/*.omex
```

CLI entry points extend the existing `nidus` console script:

```bash
nidus export --format sbml --output exports/sbml/
nidus export --format cellml --output exports/cellml/
nidus export --format physiocell --output exports/physiocell/
nidus export --format combine --output exports/combine/
```

CI regenerates all exports on every change to `dataset/`. The generated
files are committed to the repo (under `exports/`) so consumers can
fetch them directly without rebuilding.

## 8. Submission workflow

### 8.1 BioModels Database (SBML)

1. Build the COMBINE archive locally with `nidus export --format combine`.
2. Submit via the BioModels submission portal.
3. Pair with a citation: either the Zenodo dataset DOI or, ideally,
   the v0.4 outreach blog post once published.
4. Iterate with the BioModels curator on annotation completeness and
   biological plausibility (typical 4–8 weeks).
5. Receive `BIOMD0000000XXX` accession; cite back in nidus's docs.

### 8.2 Physiome Model Repository (CellML)

1. Create a workspace via Mercurial: `hg clone https://models.physiomeproject.org/workspace/...`
2. Add CellML + SED-ML + metadata.
3. Push; the workspace becomes immediately citable via its
   persistent URL.
4. (Optional) Create an "exposure" — a curated, versioned view of
   the workspace — and submit for "official" curation status.

### 8.3 PhysioCell community channels

1. PR to `MathCancer/PhysiCell-tutorials` adding a `pregnancy/`
   example built on `nidus-parameters.xml`.
2. Announcement in PhysioCell GitHub Discussions and the community
   Slack.
3. Mention in the v0.4 outreach essay (which gets a new section).

## 9. Maintenance pattern

The exports are **generated artefacts**. The source of truth is
always the JSON dataset. When the dataset changes (a new parameter,
a corrected value, a promotion to verified status), the exports
regenerate automatically:

1. GitHub Actions `ci.yml` adds a `regenerate-exports` job that runs
   `nidus export --format sbml/cellml/physiocell/combine` on every
   push to `main` after dataset validation passes.
2. The regenerated exports are committed back (via a bot account
   or a manual maintainer PR; bot is cleaner).
3. The Zenodo deposit on each tagged release includes the regenerated
   exports alongside the dataset.

Versioning: each exported model carries the nidus dataset version in
its `nidus:datasetVersion` annotation. Consumers of the SBML/CellML
models can pin to a specific dataset version if they need
reproducibility against a particular submodel.

## 10. Tooling and dependencies

Added to `python/pyproject.toml` under a new `[export]` optional
extra:

```toml
[project.optional-dependencies]
export = [
    "python-libsbml >= 5.20",
    "libcellml >= 0.5",
    "pyomexmeta >= 1.2",       # for the MIRIAM RDF construction
    "tellurium >= 2.2",        # for round-trip simulation validation
    "lxml >= 5.0",             # for PhysioCell XML generation
]
```

All Python. No new languages introduced. The `[export]` extra is
opt-in; the core `pip install nidus` install stays minimal.

## 11. Testing

New test files under `python/tests/`:

- `test_export_sbml.py` — every submodel exports, validates, round-trips
- `test_export_cellml.py` — same
- `test_export_physiocell.py` — XML schema validation, parameter
  coverage check (every nidus parameter appears in the export)
- `test_export_annotations.py` — every parameter in every export has
  the expected MIRIAM and nidus predicates
- `test_export_combine.py` — `.omex` archives validate against the
  COMBINE archive spec

CI's existing test job runs these alongside the unit tests. CI
coverage stays above the 85% floor.

## 12. Documentation

- `docs/exports/index.md` — landing page describing the four export
  formats and their target communities.
- `docs/exports/sbml.md` — SBML detail, BioModels submission status.
- `docs/exports/cellml.md` — CellML detail, Physiome submission
  status.
- `docs/exports/physiocell.md` — PhysioCell detail, tutorial link.
- `docs/exports/annotations.md` — the MIRIAM + nidus annotation
  reference.

These get added to the mkdocs nav under a new "Exports" tab.

The outreach essay (`docs/about/essay.md`) gains a section
"Reaching the modelling communities" pointing to the three exports.

## 13. Risks and honest mitigations

| Risk | Mitigation |
| ---- | ---------- |
| BioModels curator rejects the submission for being "too small" (10 disconnected submodels rather than one integrated pregnancy model). | Submit as a "Curated submodels of human gestational physiology" entry, not as "A model of pregnancy". Be modest in the framing. Reference the v0.3 dataset DOI as the integrated artefact. |
| Physiome curator requests an integrated top-level model that composes the submodels. | The CellML `comp`-style top-level model is included from the start (`nidus_pregnancy.cellml`); curator demand is anticipated. |
| PhysioCell community doesn't engage. | This is the lowest-investment integration (a single XML file + tutorial). Cost of failure is small. |
| Tier annotations get stripped by downstream tools that don't recognise custom RDF predicates. | The MIRIAM `bqbiol:isDescribedBy` links remain valid even if `nidus:confidenceTier` is dropped — the citation chain is the durable layer. Tier survives in the JSON-LD `ontology.ttl`. |
| The tier-degradation rules ("inherit lowest tier in derived quantities") don't translate cleanly into SBML/CellML semantics. | Document the rule in the per-export documentation. The annotations carry source-parameter tier; downstream simulators can re-derive degradation manually. (Future work: a formal annotation predicate that *encodes* the propagation rule.) |
| Adoption stays at the realistic lower bound (single-digit users). | This is still a real outcome — the dataset is now accessible through three distinct community channels. The work is bounded; the exports regenerate automatically; the maintenance cost is real but small. |
| Tooling rot (libSBML/libcellml major version changes) breaks the generators. | CI pins versions and re-runs nightly; breakage is detected on the day it happens. |
| BioModels submission requires a peer-reviewed paper. | The v0.4 outreach essay (in the repo + on bioRxiv if desired) plays this role. Alternative: submit the dataset paper to JOSS for a citable software-paper alongside. |

## 14. Timeline

Estimates assume single-maintainer work with the new "maintenance not
a constraint" guidance. Calendar elapsed time, not hours.

| Phase | Work | Calendar |
| ----- | ---- | -------- |
| 1     | `python/nidus/export/sbml.py` — all 10 SBML submodels, libSBML, MIRIAM + nidus annotations, round-trip validation against NumPy reference. | 1–2 weeks |
| 2     | `python/nidus/export/cellml.py` — CellML equivalents. | 1 week |
| 3     | `python/nidus/export/physiocell.py` + example config + tutorial notebook. | 3–5 days |
| 4     | `nidus export` CLI extensions + CI integration + docs site exports pages. | 3 days |
| 5     | BioModels Database submission + curator iteration. | 6–10 weeks (mostly waiting) |
| 6     | Physiome Model Repository workspace + exposure. | 1–3 weeks |
| 7     | PhysioCell community announcement + tutorial PR. | 1 week |
| 8     | Outreach essay update + bioRxiv companion (optional). | 1 week |

Total local development: ~4 weeks of evenings/weekends.
Total external (curator review): variable, can run in parallel.

## 15. Success criteria for `v0.4.0`

- [ ] All 10 SBML files produced; pass `libSBML.checkConsistency()`.
- [ ] All 10 CellML files produced; pass `libcellml.Validator`.
- [ ] PhysioCell `nidus-parameters.xml` produced; XSD-validates.
- [ ] COMBINE archives bundled and validated.
- [ ] Round-trip simulation passes for every algebraic and ODE submodel.
- [ ] Every exported parameter carries MIRIAM citation + nidus tier
      annotation.
- [ ] `nidus export` CLI shipped with `--format sbml|cellml|physiocell|combine`.
- [ ] CI regenerates exports automatically on dataset changes.
- [ ] BioModels Database submission **submitted** (accession not
      required at release — curator review is on their timeline).
- [ ] Physiome Model Repository workspace **created and exposed**.
- [ ] PhysioCell tutorial PR **opened** to `MathCancer/PhysiCell-tutorials`.
- [ ] Docs site has the Exports section live.
- [ ] Outreach essay updated to mention the three integrations.
- [ ] First Zenodo deposit at v0.4.0 includes the exports as
      supplementary files.

## 16. Open questions for the maintainer

1. **Top-level "pregnancy model" assembly.** Should the SBML/CellML
   bundles include a top-level model that *composes* all 10
   submodels into a maximally-integrated pregnancy simulation? This
   would be effortful to build correctly (defining coupling between
   subsystems is exactly the simulator problem we deliberately said
   "no" to), and could be seen as overreaching. Default
   recommendation: ship the submodels separately; do not provide a
   coupled top-level. Curators can be told this is intentional.
2. **PhysioCell sample tissue model.** Should the worked example be
   a *real* multicellular tissue simulation, or a minimal placeholder
   that just demonstrates parameter consumption? Real example is
   more useful but is much more work. Default: minimal placeholder
   for v0.4; consider full example in v0.5.
3. **Ontology submission to BioPortal.** Is the `nidus:` ontology
   worth submitting as a standalone OWL artefact? Probably yes, but
   it can land after v0.4 release; not blocking.
4. **JOSS software paper.** Worth pursuing alongside BioModels
   submission for an additional citable artefact? Probably yes —
   JOSS turnaround is fast and reviewer demands are bounded. Defer
   the decision to v0.4 mid-cycle.
5. **CellML 2.0 vs. 1.1.** Physiome accepts both. Default to 2.0
   (current standard); fall back to 1.1 only if curator requests it.
