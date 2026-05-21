# v0.3 design

Nidus is a citation-verified, tier-annotated parameter dataset for human gestational physiology, distributed as a Python package and a Streamlit dashboard. v0.3 is the first release in this form.

## The two contributions

1. The **curated parameter set** — every value linked to a primary source, every source linked to a DOI/PMID/URL, every entry carrying explicit confidence-tier metadata.
2. The **confidence-tier discipline** — the rare and intellectually honest practice of saying *"this value is Tier B because of these specific studies"* rather than reporting point estimates without provenance.

Both are presentation-layer-agnostic. v0.3 ships them in the form factor that matches the audience: a `pip install` Python package with a browsable dashboard.

## What v0.3 ships

| Component             | Form                                            |
| --------------------- | ----------------------------------------------- |
| Dataset               | JSON + JSON Schema + JSON-LD under `dataset/`   |
| Python package        | `pip install nidus`, pure Python                |
| Interactive dashboard | Streamlit, hosted free on Streamlit Cloud       |
| Reference notebooks   | Five Jupyter notebooks, executed in CI          |
| Citation / DOI        | Zenodo deposit on every release                  |
| Outreach              | Essay in the repository                       |

The **dataset is the centerpiece**; everything else is a presentation layer.

## Out of scope (with reasoning)

| Excluded                                          | Reasoning                                                                                                            |
| ------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------- |
| Rust kernel of any kind                           | NumPy/SciPy handles the trajectories and sensitivity widgets to identical precision. A second language is friction, not value. |
| PyO3 bindings                                     | Same — no compute-bound paths in the v0.3 dashboard.                                                                |
| Custom domain (.org/.com)                         | GitHub + PyPI + Streamlit Cloud are the canonical URLs and don't need renewing.                                     |
| Methods paper in PLOS Comp Bio / JTB / similar    | 12–18 months for marginal upside over a blog essay. The audience finds tools via Google + GitHub, not journal TOCs. |
| Mechanistic competition with CellML / COPASI      | The community standard for mechanistic gestational modelling already lives there. SBML/CellML export from this dataset is a deferred interop play (executed only if v0.3 sees adoption). |
| Subsystem expansion (immune, respiratory, etc.)   | Out of scope for v0.3. Curate what we already have first.                                                            |
| Twin / higher-order pregnancies                   | Out of scope.                                                                                                        |
| Embryonic period (<8 weeks)                       | Out of scope.                                                                                                        |
| Labour and delivery                               | Out of scope.                                                                                                        |
| Clinical decision support                         | Out of scope forever.                                                                                                |
| Personalised pregnancy prediction                 | Out of scope forever.                                                                                                |
| Automated parameter extraction by LLM             | Humans verify every parameter against the original paper. LLMs do not.                                              |
| Commercial / paid features                        | Forever free. MIT code, CC-BY-4.0 dataset.                                                                          |

## Audience and ethos

- **Audience:** ~hundreds of perinatal researchers globally. Almost all Python/R users. Small field — every adoption matters.
- **Solo maintainer.** Scope must match steady-state capacity. No expansion beyond what one person can sustain on evenings and weekends.
- **Licence:** MIT for code, CC-BY-4.0 for the dataset. Forever free. No commercial intent.
- **Honesty about scope.** The README states what nidus is *and isn't*, plainly. Dishonesty about uncertainty turns a useful tool into a misleading one.
- **Realistic ceiling.** Best case at 12 months: a handful of researchers cite the dataset; one publishes a hypothesis informed by it. That is success. Anything more is a bonus.

## The full design specs

The numbered design documents live at [`docs/specs/v0.3/`](https://github.com/clay-good/nidus/tree/main/docs/specs/v0.3/) in the repository:

- [`00-overview.md`](https://github.com/clay-good/nidus/blob/main/docs/specs/v0.3/00-overview.md) — what we are doing and why.
- [`01-dataset-and-dashboard.md`](https://github.com/clay-good/nidus/blob/main/docs/specs/v0.3/01-dataset-and-dashboard.md) — the primary work.
- [`02-sbml-cellml-export.md`](https://github.com/clay-good/nidus/blob/main/docs/specs/v0.3/02-sbml-cellml-export.md) — conditional CellML/SBML interop.
- [`03-outreach-and-essay.md`](https://github.com/clay-good/nidus/blob/main/docs/specs/v0.3/03-outreach-and-essay.md) — blog essay strategy.
