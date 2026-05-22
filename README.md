# Nidus

**A curated, citation-backed dataset of human gestational physiology parameters — annotated with explicit confidence tiers, and exportable into the standard mechanistic-modeling formats (SBML, CellML, PhysioCell, COMBINE).**

Nidus is an open dataset of parameter values describing maternal cardiovascular adaptation, placental transport, fetal development, and related physiology across human pregnancy (8–40 weeks gestation, singleton). Every parameter is annotated with:

- a **confidence tier** (A/B/C/D) describing the strength of evidence behind it,
- at least one **peer-reviewed citation** linked by DOI or PMID,
- a **rationale** for the tier assignment,
- a **review status** (`verified` / `unverified` / `contested`) tracking human verification against the source PDF.

It is distributed as a Python package (`pip install nidus`), browsable via an interactive Streamlit dashboard, and exportable into the formats the systems-biology and tissue-modelling communities already use.

## At a glance (v0.4 development snapshot)

- **70 parameters** across **10 subsystems** (maternal cardiovascular / blood / renal / respiratory; placental structure / gas exchange / glucose; fetal circulation / growth / metabolism).
- **33 citations**, each verified against Crossref or PubMed metadata.
- **28 of 70 parameters human-verified** against the source PDF (the rest are `unverified`: the central value is from the literature but a human has not yet eyeballed the source against the dataset entry).
- **11 mechanistic submodels** exportable to SBML L3v2, CellML 2.0 (with 1.1 fallback), and PhysioCell `<user_parameters>`.
- **One composed pregnancy SBML model** wiring all 11 submodels via a shared gestational-time axis.
- **COMBINE archive** (`.omex`) bundling SBML + CellML + PhysioCell + provenance metadata.

See [docs/specs/v0.4/00-overview.md](docs/specs/v0.4/00-overview.md) for the design and [docs/specs/v0.4/02-parameter-expansion-roadmap.md](docs/specs/v0.4/02-parameter-expansion-roadmap.md) for the planned expansion path to ~200 parameters.

## What nidus is

- A **JSON dataset** under [dataset/](dataset/), schema-validated and machine-readable.
- A **Python package** that loads, filters, queries, and exports the dataset.
- A **Streamlit dashboard** for non-coders to browse parameters, citations, and trajectories.
- A **suite of mechanistic-modeling exports** (SBML / CellML / PhysioCell / COMBINE) so the dataset can be consumed directly inside the simulators researchers already use.
- A **citable artifact** — every release gets a Zenodo DOI.

## What nidus is NOT

- **Not a clinical decision-support tool.** Not validated for any decision affecting a real patient.
- **Not a mechanistic simulator.** Nidus exports parameters *into* the simulators ([CellML](https://www.cellml.org/), [COPASI](http://copasi.org/), [PhysioCell](http://physicell.org/), [tellurium](https://tellurium.analogmachine.org/)). It does not integrate ODEs itself.
- **Not an automated medical researcher.** Humans verify every parameter and every citation. LLMs help but do not promote `unverified` to `verified` on their own authority.
- **Not exhaustive (yet).** v0.4 ships 70 parameters; the realistic ceiling for the declared scope is ~200. See the [parameter expansion roadmap](docs/specs/v0.4/02-parameter-expansion-roadmap.md) for what is planned, and what is explicitly out of scope.

## Quick start

```bash
pip install nidus                 # core: dataset + loader + CLI
pip install 'nidus[export]'       # adds python-libsbml + libcellml for SBML/CellML
pip install 'nidus[plot]'         # adds matplotlib for built-in trajectory plotting
```

### Load and query the dataset

```python
import nidus

ds = nidus.load()

co = ds["maternal_cardiovascular.baseline_cardiac_output_l_per_min"]
print(co.value)                      # Value(central=4.5, low=4.0, high=5.0, units='L/min', ...)
print(co.tier)                       # "B"
print(co.primary_citation.doi)       # the DOI of the canonical source
print(co.extraction.review_status)   # "verified" or "unverified"
print(co.extraction.tier_rationale)  # the explicit reason the tier was assigned

# Filter
b_tier_renal = [p for p in ds if p.tier == "B" and p.subsystem == "maternal_renal"]
```

### Mechanistic-modeling exports

```bash
# One SBML file per submodel
nidus export --format sbml --output exports/sbml

# CellML 2.0 (or 1.1 fallback for legacy tools)
nidus export --format cellml --output exports/cellml
nidus export --format cellml --cellml-version 1.1 --output exports/cellml_1_1

# PhysioCell <user_parameters> drop-in
nidus export --format physiocell --output exports/physicell

# Single composed SBML model wiring all 11 submodels together
nidus export --format composed --output exports/composed

# COMBINE archive bundling everything (.omex)
nidus export --format omex --output exports/nidus.omex
```

### Browse the dashboard

```bash
streamlit run dashboard/app.py
```

Or use the hosted Streamlit Community Cloud deployment linked from the repo description.

## The 11 exportable submodels

| Submodel id                            | Equation                                                     | Tier driver                |
| -------------------------------------- | ------------------------------------------------------------ | -------------------------- |
| `placental_villous_growth`             | Logistic surface-area expansion                              | placental_structure        |
| `o2hb_dissociation_adult`              | Severinghaus 1979 algebraic saturation                       | maternal_blood             |
| `o2hb_dissociation_fetal`              | Hill-form fetal HbF (Bauer 1969, P50≈19.5 mmHg)              | fetal_metabolism           |
| `placental_glucose_glut1`              | Michaelis–Menten (lower-affinity, higher-Vmax isoform)       | placental_glucose          |
| `placental_glucose_glut3`              | Michaelis–Menten (higher-affinity isoform)                   | placental_glucose          |
| `maternal_cardiac_output_trajectory`   | Gaussian bump (Mahendru 2014 longitudinal fit)               | maternal_cardiovascular    |
| `maternal_map_trajectory`              | Gaussian nadir mid-pregnancy                                 | maternal_cardiovascular    |
| `uterine_artery_flow_logistic`         | Logistic growth, inflection at 24 weeks (Thaler 1990)        | maternal_cardiovascular    |
| `placental_o2_equilibrator`            | Algebraic intervillous → umbilical-vein PO₂ equilibrium      | placental_gas_exchange     |
| `plasma_volume_expansion`              | Sigmoidal (Bernstein 2001 + de Haas 2017 anchors)            | maternal_blood             |
| `hadlock_fetal_weight`                 | Hadlock 1991 four-parameter biometry regression              | fetal_growth               |

Each submodel ships with a pure-NumPy reference kernel in [`python/nidus/export/reference.py`](python/nidus/export/reference.py) that the SBML/CellML exports are round-trip validated against.

## Confidence tiers

| Tier  | Meaning                                                                                                |
| ----- | ------------------------------------------------------------------------------------------------------ |
| A     | Well-established. ≥3 independent studies, overlapping CIs, mechanism understood, multiple populations. |
| B     | Supported. 1–2 longitudinal studies (n≥100), plausible mechanism, no strong contradicting evidence.    |
| C     | Provisional. Single study, or cross-sectional only, or small n; mechanism speculative.                 |
| D     | Unknown. Hypothesised channel; no quantitative literature; listed for research-question purposes.      |

When a submodel combines parameters of different tiers, **the worst input tier wins** (the submodel inherits the tier of its weakest input). Exported SBML / CellML / PhysioCell models carry this propagated tier as a `nidus:confidenceTier` RDF annotation.

## How to cite

Cite the dataset by its Zenodo concept DOI (added on first formal release). See [CITATION.cff](CITATION.cff) for machine-readable metadata. Every parameter also has its own underlying citation accessible via `parameter.primary_citation.doi` — when you use a single parameter, cite the dataset AND the primary source.

## Read more

- **[Essay — Confidence tiers for pregnancy physiology](docs/about/essay.md).** A ~2,500-word walkthrough of the design philosophy with the Mahendru-2014 cardiac-output parameter as a worked example. The clearest single explanation of what the dataset is and why the tier system is the load-bearing piece.
- **[v0.3 design spec](docs/specs/v0.3/00-overview.md)** — the dataset-and-dashboard rationale.
- **[v0.4 design spec](docs/specs/v0.4/00-overview.md)** — the mechanistic-modeling interop direction.
- **[v0.4 mechanistic interop spec](docs/specs/v0.4/01-mechanistic-modeling-interop.md)** — per-format model design, annotations, validation strategy.
- **[v0.4 parameter expansion roadmap](docs/specs/v0.4/02-parameter-expansion-roadmap.md)** — what's planned next; what's explicitly out of scope.
- **[v0.4 submodel expansion catalog](docs/specs/v0.4/03-submodel-expansion-catalog.md)** — additional mechanistic submodels that could ship in future releases.
- **[`docs/about/history.md`](docs/about/history.md)** — how the project got here (the project began as a Rust prototype, preserved at the `v0.2-archive` tag).
- **[PhysioCell tissue example](docs/examples/physicell_placental_villous/)** — a 2D placental-villous slice showing the canonical nidus→PhysiCell parameter pattern.

## Licence

- **Code:** MIT. See [LICENSE](LICENSE).
- **Dataset:** CC-BY-4.0. See [LICENSE-DATASET](LICENSE-DATASET). Each parameter entry is data; attribution required, no other restrictions.

## Contributing

The most valuable contributions are verified parameters drawn from published empirical work. See [CONTRIBUTING.md](CONTRIBUTING.md) for the tier system, the review checklist, the citation-verification workflow, and the parameter-addition issue template.

The single highest-leverage contribution today is promoting `unverified` parameters to `verified` by reading the source PDF and confirming (or correcting) the dataset entry. 42 such promotions remain available.
