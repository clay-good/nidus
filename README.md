# Nidus

**A curated, citation-backed dataset of human gestational physiology parameters — annotated with explicit confidence tiers.**

Nidus is an open dataset of parameter values describing maternal cardiovascular adaptation, placental transport, and fetal development across human pregnancy (8–40 weeks gestation). Every parameter is annotated with:

- a **confidence tier** (A/B/C/D) describing the strength of evidence behind it,
- at least one **peer-reviewed citation** linked by DOI or PMID,
- a **rationale** for the tier assignment.

It is distributed as a Python package (`pip install nidus`) and browsable via an interactive Streamlit dashboard.

## What nidus is

- A **JSON dataset** under `dataset/`, schema-validated and machine-readable.
- A **Python package** that loads, filters, and queries the dataset.
- A **Streamlit dashboard** for non-coders to browse parameters, citations, and trajectories.
- A **citable artifact** — every release gets a Zenodo DOI.

## What nidus is NOT

- **Not a clinical decision-support tool.** Not validated for any decision affecting a real patient.
- **Not a mechanistic simulator.** For mechanistic modelling, see [CellML](https://www.cellml.org/), [COPASI](http://copasi.org/), or [PhysioCell](http://physicell.org/).
- **Not an automated medical researcher.** Humans verify every parameter and every citation.

## Quick start

```bash
pip install nidus
```

```python
import nidus

ds = nidus.load()

co = ds["maternal.cardio.cardiac_output.peak_amplitude"]
print(co.value)         # {"central": 1.55, "low": 1.30, "high": 1.80, "units": "L/min"}
print(co.tier)          # "B"
print(co.citations[0].doi)  # "10.1097/HJH.0000000000000090"
```

## Confidence tiers

| Tier  | Meaning                                                                                                |
| ----- | ------------------------------------------------------------------------------------------------------ |
| A     | Well-established. ≥3 independent studies, overlapping CIs, mechanism understood, multiple populations. |
| B     | Supported. 1–2 longitudinal studies (n≥100), plausible mechanism, no strong contradicting evidence.    |
| C     | Provisional. Single study, or cross-sectional only, or small n; mechanism speculative.                 |
| D     | Unknown. Hypothesised channel; no quantitative literature; listed for research-question purposes.      |

## How to cite

Cite the dataset by its Zenodo concept DOI (added on first release). See `CITATION.cff` for machine-readable metadata.

## Read more

- **[Essay — Confidence tiers for pregnancy physiology](docs/about/essay.md).** A ~2,500-word walkthrough of the design philosophy with the Mahendru-2014 cardiac-output parameter as a worked example. The clearest single explanation of what the dataset is and why the tier system is the load-bearing piece.
- **[v0.3 design spec](docs/specs/v0.3/00-overview.md)** — the engineering rationale.
- **[`docs/about/history.md`](docs/about/history.md)** — how the project got here (the project began as a Rust prototype, preserved at the `v0.2-archive` tag).

## Licence

- **Code:** MIT. See [LICENSE](LICENSE).
- **Dataset:** CC-BY-4.0 (each parameter entry is data; attribution required, no other restrictions).

## Contributing

The most valuable contributions are verified parameters drawn from published empirical work. See [CONTRIBUTING.md](CONTRIBUTING.md) for the tier system, the review checklist, and the citation-verification workflow.
