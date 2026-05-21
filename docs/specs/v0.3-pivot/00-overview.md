# Spec 00 — Overview: Why We Pivoted, What We Are Doing

## TL;DR

Nidus was originally built as a Rust simulator of coupled maternal-placental-fetal physiology. After honest reality-testing against (a) the actual research landscape — CellML, COPASI, PhysioCell, Physiome Model Repository — and (b) the actual audience — perinatal researchers globally, almost all Python/R users — the simulator-first direction was rejected.

The pivot lifts the **durable value** out of the simulator and presents it in a form researchers can actually use today.

## What we are doing (clear and plain)

| Component             | Form                                            | Why                                              |
| --------------------- | ----------------------------------------------- | ------------------------------------------------ |
| Dataset               | JSON + JSON Schema + JSON-LD under `dataset/`   | Portable, FAIR-compliant, machine-readable.      |
| Python package        | `pip install nidus`, pure Python                | Meets researchers where they are.                |
| Interactive dashboard | Streamlit, hosted free on Streamlit Cloud       | Zero-install browse for non-coders.              |
| Reference notebooks   | 4–5 Jupyter notebooks, executed in CI            | Canonical tutorials.                             |
| Citation / DOI        | Zenodo deposit on every release                  | Permanent, citable, machine-findable.            |
| Outreach              | Blog essay on claygood.com                       | SEO + visibility, no academic gatekeeping.       |

The **dataset is the centerpiece.** Everything else is a presentation layer.

## What we are NOT doing (locked-in decisions)

| Rejected approach                                | Why                                                                                                            |
| ------------------------------------------------ | -------------------------------------------------------------------------------------------------------------- |
| Rust simulator (`crates/`, `Cargo.*`)            | Wrong language for the audience. Compile step is friction. Signals "engineering project" not "research dataset." Being **deleted** in pivot step 1. |
| PyO3 kernel / `engine-rs/` subdirectory          | NumPy/SciPy compute the same trajectories to identical precision for everything the dashboard needs.           |
| Archive branch for the deleted Rust code         | Git history is the archive. No long-lived parallel branches.                                                   |
| Custom domain (.org/.com)                        | GitHub + PyPI + Streamlit Cloud are the canonical URLs. No domain to renew, no DNS to break.                   |
| Methods paper in PLOS Comp Bio / JTB / similar   | 12–18 months for marginal upside over a blog essay. Audience finds tools via Google + GitHub, not journal TOCs. |
| Mechanistic competition with CellML / COPASI     | Out of scope. Solo maintainer cannot sustain. Optional SBML interop (Spec 02) only if adoption warrants.       |
| Subsystem expansion (immune, respiratory, etc.)  | Out of scope this cycle. Curate what we already have. No new biology.                                          |
| Twin / higher-order pregnancies                  | Out of scope.                                                                                                  |
| Embryonic period (<8 weeks)                      | Out of scope.                                                                                                  |
| Labour and delivery                              | Out of scope.                                                                                                  |
| Clinical decision support, in any form           | Out of scope forever.                                                                                          |
| Personalised pregnancy prediction                | Out of scope forever.                                                                                          |
| Automated parameter extraction by LLM            | Humans verify every parameter and every citation. LLMs do not.                                                 |
| Commercial / paid features                       | Forever free. MIT code, CC-BY-4.0 data.                                                                        |

## Order of operations

1. **Spec 01** — Execute the pivot. Delete Rust. Extract dataset. Build Python package + Streamlit dashboard. Ship `v0.3.0`. Deposit on Zenodo.
2. **Spec 03** — Publish blog essay on claygood.com pointing to repo + DOI. Done same week as Spec 01 release.
3. **Spec 02** — *Conditional.* Only execute if Spec 01 sees adoption signal (issues, stars, citations, external installs, emails) within ~3 months. Otherwise indefinitely deferred.

## Audience and ethos

- **Audience:** ~hundreds of perinatal researchers globally. Almost all Python/R users. Small field — every adoption matters.
- **Solo maintainer.** Scope must match the steady-state capacity of one person doing this on evenings/weekends.
- **Licence:** MIT for code, CC-BY-4.0 for the dataset. Forever free. No commercial intent.
- **Honesty about scope.** Dishonesty about uncertainty turns a useful tool into a misleading one. The README states what nidus is *and isn't*, plainly.
- **Realistic best case:** a handful of researchers cite the dataset; one publishes a hypothesis informed by it. That is success. Anything more is a bonus.

## How to read the rest of this directory

| File                                  | What it covers                                                       |
| ------------------------------------- | -------------------------------------------------------------------- |
| `01-dataset-and-dashboard.md`         | The actual work: how to execute the pivot.                           |
| `02-sbml-cellml-export.md`            | Conditional follow-up: interop with CellML/SBML if adoption warrants. |
| `03-outreach-and-essay.md`            | Blog essay strategy on claygood.com + Zenodo deposit.                |

Specs deprecated by this pivot are listed in [`../README.md`](../README.md).
