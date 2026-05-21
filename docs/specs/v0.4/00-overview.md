# Spec 00 — v0.4 Direction: Mechanistic-Modeling Interop

## Status

**Implementation in progress.** First four submodels (logistic
placental growth, Severinghaus adult O2-Hb, fetal HbF dissociation,
Michaelis-Menten GLUT1) ship to all three formats — SBML L3v2,
CellML 2.0 with 1.1 fallback, PhysioCell `parameters.xml`. The
`nidus export --format {sbml,cellml,physiocell}` CLI is live, covered
by 26 tests, with libSBML consistency-check pass and round-trip
numerical validation against pure-NumPy reference kernels.

Remaining for v0.4.0 release: the other ~6 submodels, top-level
composed pregnancy model (SBML `comp` + CellML imports), COMBINE
archive bundling, BioModels submission, Physiome workspace creation,
PhysioCell real tissue-simulation example, PR to
`MathCancer/PhysiCell-tutorials`, outreach essay update.

## TL;DR

v0.3 ships nidus as a Python-and-dashboard dataset. v0.4 ships nidus
*through the three platforms the computational-physiology community
already uses*: **SBML / BioModels Database**, **CellML / Physiome
Model Repository**, and **PhysioCell**.

The dataset remains the centerpiece. v0.4 adds presentation layers
targeted at the existing user communities for mechanistic gestational
modelling.

## Why this reshuffles priorities

The earlier `v0.3/02-sbml-cellml-export.md` made these exports
conditional on a v0.3 adoption signal, on the theory that maintaining
multiple format outputs would overload a single maintainer. That
constraint has been explicitly relaxed by the project owner:
maintenance load is *not* the binding constraint; **scientific-
community adoption is.**

Under the new constraint, the right move is to meet the existing
modelling communities in their native formats rather than waiting for
them to come to ours. Each platform's audience is small, but each is
*the* place the relevant researchers already work.

## What v0.4 ships

| Target              | Form                                                  | Audience size               |
| ------------------- | ----------------------------------------------------- | --------------------------- |
| **SBML L3v2**       | One SBML file per exportable submodel (~10); bundled COMBINE archive; submitted to BioModels Database. | ~hundreds of computational systems biologists |
| **CellML 2.0**      | One CellML file per submodel; submitted to Physiome Model Repository as a curated workspace. | ~hundreds of computational physiologists |
| **PhysioCell**      | A drop-in `nidus-parameters.xml`, an example PhysioCell `XML config` showing how to consume it, and a tutorial notebook. | ~dozens of multicellular-tissue modellers |
| **Tooling**         | `nidus export --format {sbml,cellml,physiocell}` extensions + `scripts/build_models.py` generator + CI that regenerates exports on every dataset change. | maintainer + contributors |

See [`01-mechanistic-modeling-interop.md`](01-mechanistic-modeling-interop.md)
for the implementation spec.

## What v0.4 is NOT

- A new simulator. The three target platforms ARE the simulators;
  nidus feeds them parameter values, it does not compute trajectories
  itself.
- A replacement for `nidus.load()`. The Python API remains the
  primary access path for researchers who use Python directly.
- A claim of mechanistic insight beyond what the dataset's tier
  system already says. Tier degradation rules apply to derived
  quantities in any of the exported models.
- A clinical tool, in any format.

## Honest expectations

The realistic ceiling at 12 months after v0.4 ships:

- **Physiome Model Repository**: 5–20 researchers download or
  reference the CellML models. 1–3 cite nidus in a paper that uses
  a derivative model.
- **BioModels Database**: 1–2 entries accepted into the curated
  catalogue. Few-dozen downloads. Citation flux smaller than
  Physiome's.
- **PhysioCell community**: <5 users who actively consume nidus
  parameters in their simulations. Of these, maybe one uses it for a
  paper.

These numbers are small. They are also realistic for a niche field.
What v0.4 produces is *positioning*: nidus becomes the cited parameter
source for whoever does gestational-physiology mechanistic modelling
in the next five years. The audience grows slowly; the citation
chain is durable.

## Order of operations

1. Spec 01 (this directory) — implementation plan for all three
   formats; supersedes the earlier `v0.3/02-sbml-cellml-export.md`.
2. Implementation, in priority order: CellML first (highest-leverage
   audience), then SBML, then PhysioCell.
3. Submission: Physiome workspace first (self-publishing path),
   BioModels next (curated path), PhysioCell channel announcement
   last.
4. Update the outreach essay and the methods paragraph in the
   dashboard to reflect the interop capability.

## What stays the same

- The dataset (`dataset/`) is unchanged in scope or schema.
- The Python package (`nidus`) gains the export CLI but no API
  changes.
- The Streamlit dashboard gains a "Download as model" section but
  the existing pages stay.
- The verification standard (`docs/contributing/verification.md`)
  is unchanged: humans verify against PDFs; the tier system
  propagates into the exported models via MIRIAM annotations.

## How to read the rest of this directory

| File                                       | What it covers                                                          |
| ------------------------------------------ | ----------------------------------------------------------------------- |
| `01-mechanistic-modeling-interop.md`       | The full implementation plan: per-format model design, annotations, submission, validation, maintenance pattern. |
| (further specs)                            | Reserved for follow-on work as v0.4 progresses.                         |

The earlier `v0.3/02-sbml-cellml-export.md` is superseded by Spec 01
in this directory and is marked accordingly.
