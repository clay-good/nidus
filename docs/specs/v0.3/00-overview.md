# Spec 00 — v0.3 Design: Dataset-first Form Factor

## TL;DR

Nidus is a citation-verified, tier-annotated parameter dataset for
human gestational physiology, distributed as a Python package and a
Streamlit dashboard. v0.3 is the first release in this form.

Earlier work (preserved at the `v0.2-archive` git tag) prototyped a
coupled maternal-placental-fetal physiology engine in Rust. That
exploration surfaced two things:

1. The **durable contribution** is the curated parameter set plus the
   confidence-tier discipline — both presentation-layer-agnostic.
2. The **right form factor for the audience** (biomedical researchers,
   ~all Python/R users) is a pip-installable dataset, not a compiled
   simulator competing with mature physiological-modelling platforms
   like CellML, COPASI, and PhysioCell.

v0.3 reframes the project around the durable contribution in the
right form factor.

## What v0.3 ships

| Component             | Form                                            | Why                                                |
| --------------------- | ----------------------------------------------- | -------------------------------------------------- |
| Dataset               | JSON + JSON Schema + JSON-LD under `dataset/`   | Portable, FAIR-compliant, machine-readable.        |
| Python package        | `pip install nidus`, pure Python                | Meets researchers where they work.                 |
| Interactive dashboard | Streamlit, hosted free on Streamlit Cloud       | Zero-install browse for non-coders.                |
| Reference notebooks   | 4–5 Jupyter notebooks, executed in CI            | Canonical tutorials that double as documentation. |
| Citation / DOI        | Zenodo deposit on every release                  | Permanent, citable, machine-findable.              |
| Outreach              | Essay in the repository                       | SEO + visibility, no academic gatekeeping.         |

The **dataset is the centerpiece**; everything else is a presentation
layer.

## Out of scope (with reasoning)

| Excluded                                          | Reasoning                                                                                                            |
| ------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------- |
| Rust kernel of any kind                           | NumPy/SciPy handles the trajectories and sensitivity widgets to identical precision. A second language is friction, not value. |
| PyO3 bindings                                     | Same — no compute-bound paths in the v0.3 dashboard.                                                                |
| Custom domain (.org/.com)                         | GitHub + PyPI + Streamlit Cloud are the canonical URLs and don't need renewing.                                     |
| Methods paper in PLOS Comp Bio / JTB / similar    | 12–18 months for marginal upside over a blog essay. The audience finds tools via Google + GitHub, not journal TOCs. |
| Mechanistic competition with CellML / COPASI      | The community standard for mechanistic gestational modelling already lives there. Spec 02 documents an interop path.|
| Subsystem expansion (immune, respiratory, etc.)   | Out of scope for v0.3. Curate what we already have first.                                                            |
| Twin / higher-order pregnancies                   | Out of scope.                                                                                                        |
| Embryonic period (<8 weeks)                       | Out of scope.                                                                                                        |
| Labour and delivery                               | Out of scope.                                                                                                        |
| Clinical decision support                         | Out of scope forever.                                                                                                |
| Personalised pregnancy prediction                 | Out of scope forever.                                                                                                |
| Automated parameter extraction by LLM             | Humans verify every parameter against the original paper. LLMs do not.                                              |
| Commercial / paid features                       | Forever free. MIT code, CC-BY-4.0 dataset.                                                                          |

## Order of operations

1. **Spec 01** — Dataset + Python package + Streamlit dashboard +
   Zenodo. Ship `v0.3.0`.
2. **Spec 03** — Essay in the repository. Same week as Spec 01
   release.
3. **Spec 02** — *Conditional.* SBML/CellML export, executed only if
   Spec 01 sees adoption (issues, stars, citations, external installs,
   emails) within ~3 months. Otherwise indefinitely deferred — silence
   is also a successful outcome.

## Audience and ethos

- **Audience:** ~hundreds of perinatal researchers globally. Almost
  all Python/R users. Small field — every adoption matters.
- **Solo maintainer.** Scope must match steady-state capacity. No
  expansion beyond what one person can sustain on evenings and
  weekends.
- **Licence:** MIT for code, CC-BY-4.0 for the dataset. Forever free.
  No commercial intent.
- **Honesty about scope.** The README states what nidus is *and isn't*,
  plainly. Dishonesty about uncertainty turns a useful tool into a
  misleading one.
- **Realistic ceiling.** Best case at 12 months: a handful of
  researchers cite the dataset; one publishes a hypothesis informed by
  it. That is success. Anything more is a bonus.

## How to read the rest of this directory

| File                                  | What it covers                                                            |
| ------------------------------------- | ------------------------------------------------------------------------- |
| `01-dataset-and-dashboard.md`         | The primary work: how to ship the v0.3.0 release.                         |
| `02-sbml-cellml-export.md`            | Conditional interop with CellML/SBML, executed only on adoption signal.   |
| `03-outreach-and-essay.md`            | Blog essay strategy on the repository essay + Zenodo deposit.                     |

Specs superseded by this design are listed in [`../README.md`](../README.md).
