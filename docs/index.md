# Nidus

**A curated, citation-backed dataset of human gestational physiology parameters, annotated with explicit confidence tiers.**

Nidus is an open dataset of parameter values describing maternal cardiovascular adaptation, placental transport, and fetal development across human pregnancy (8–40 weeks gestation). Every parameter is annotated with:

- a **confidence tier** (A/B/C/D) describing the strength of evidence behind it,
- at least one **peer-reviewed citation** linked by DOI or PMID,
- a **rationale** for the tier assignment.

It is distributed as a Python package ([`pip install nidus`](getting-started/install.md)) and browsable via an interactive Streamlit dashboard.

## What nidus is

- A JSON dataset, schema-validated against [JSON Schema draft 2020-12](dataset/schema.md), FAIR-compliant.
- A pure-Python package with a [stable, typed API](api.md).
- An [interactive dashboard](https://nidus.streamlit.app) (placeholder URL pending deploy).
- Citable via a [Zenodo DOI](about/license.md) minted on every release.
- **MIT** on the code, **CC-BY-4.0** on the dataset.

## What nidus is not

- **Not a clinical decision-support tool.** Not validated for any decision affecting a real patient.
- **Not a mechanistic simulator.** For mechanistic modelling, see [CellML](https://www.cellml.org/), [COPASI](http://copasi.org/), or [PhysioCell](http://physicell.org/).
- **Not an automated medical researcher.** Humans verify every parameter and every citation.

## Quick start

```python
import nidus

ds = nidus.load()
co = ds["maternal_cardiovascular.baseline_cardiac_output_l_per_min"]
print(co.value.central, co.value.units)   # 4.6 L/min
print(co.tier)                             # B
print(co.primary_citation.doi)             # 10.1097/hjh.0000000000000090
```

See the [quickstart](getting-started/quickstart.md) for the full walkthrough.

## Where to go from here

- [Install](getting-started/install.md)
- [Quickstart](getting-started/quickstart.md)
- [Dataset overview](dataset/overview.md)
- [Tutorials](tutorials/index.md) (Jupyter notebooks)
- [API reference](api.md)
- [Contributing](contributing/overview.md)
- [Design rationale](about/design.md)
