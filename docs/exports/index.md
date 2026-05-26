# Mechanistic-modelling exports

Nidus ships every mechanistic submodel — 41 of them, all derived from
parameters already curated in the dataset — in the three exchange
formats the computational-physiology community already uses. The
dataset stays the source of truth; the exports are presentation
layers, regenerated from the JSON on demand.

| Format       | Audience                                          | Detail page                      |
| ------------ | ------------------------------------------------- | -------------------------------- |
| **SBML L3v2** | BioModels Database, COPASI, tellurium, libSBML    | [SBML](sbml.md)                  |
| **CellML 2.0** (+ 1.1 fallback) | Physiome Model Repository, OpenCOR, libcellml   | [CellML](cellml.md)              |
| **PhysioCell `user_parameters`** | PhysioCell tissue / multicellular modelers       | [PhysioCell](physicell.md)       |
| **COMBINE archive (`.omex`)**    | Anyone reproducing a full simulation experiment | bundled by `nidus export --format omex` |

Every exported model carries [MIRIAM citation + nidus-tier
annotations](annotations.md) so the citation chain and confidence-tier
discipline survive the export.

## CLI

The `nidus` console script exposes one entrypoint:

```bash
nidus export --format {sbml,cellml,physiocell,composed,omex} \
             --output exports/ \
             [--cellml-version {2.0,1.1}]
```

| Flag                      | What it does                                                                                                       |
| ------------------------- | ------------------------------------------------------------------------------------------------------------------ |
| `--format sbml`           | One SBML L3v2 file per submodel + one top-level composed pregnancy model.                                          |
| `--format cellml`         | One CellML file per submodel. Pair with `--cellml-version 1.1` for the legacy-OpenCOR fallback.                    |
| `--format physiocell`     | A single `nidus-parameters.xml` with every nidus parameter as a `<param>` entry, citation key + tier in comments. |
| `--format composed`       | Just the top-level SBML composed pregnancy model.                                                                  |
| `--format omex`           | A COMBINE `.omex` bundle: SBML + CellML (both versions) + PhysioCell + SED-ML descriptors + provenance metadata.  |

## Python API

```python
import nidus
from nidus import export

ds = nidus.load()

# Inspect what's exportable
for submodel in export.list_submodels():
    print(submodel["id"], submodel["sbo_term"], submodel["n_parameters"])

# Build a single SBML document in memory
sbml_xml = export.build_sbml(ds, "placental_villous_growth")

# Or write all formats to disk
export.write_sbml(ds, "exports/sbml/")
export.write_cellml(ds, "exports/cellml/")             # CellML 2.0
export.write_cellml(ds, "exports/cellml-1.1/", version="1.1")
export.write_physiocell(ds, "exports/physiocell/")
export.write_combine_archive(ds, "exports/nidus.omex")
```

The [API reference](../api.md) covers every public helper, including
`equation_latex`, `polynomial_fit_coefficients`, `build_sedml`, and the
`sweep` sensitivity-analysis utility.

## Submission status

The exchange-format submissions sit downstream of the engineering
work. As of nidus v0.4:

| Target                            | Status                                                                                                     |
| --------------------------------- | ---------------------------------------------------------------------------------------------------------- |
| BioModels Database (SBML)         | Submission **pending** for the v0.4.0 cut. COMBINE archive is the submission unit.                          |
| Physiome Model Repository (CellML)| Workspace creation **pending** for the v0.4.0 cut.                                                          |
| PhysioCell tutorials              | PR to `MathCancer/PhysiCell-tutorials` **pending** for the v0.4.0 cut. A worked example already ships in [`docs/examples/physicell_placental_villous/`](https://github.com/clay-good/nidus/tree/main/docs/examples/physicell_placental_villous). |

These are submission/social steps that run on the external curators'
timelines; the code paths they depend on are in place and covered by
50+ tests.

## See also

- [Spec 00 — v0.4 direction](https://github.com/clay-good/nidus/blob/main/docs/specs/v0.4/00-overview.md)
- [Spec 01 — mechanistic-modeling interop](https://github.com/clay-good/nidus/blob/main/docs/specs/v0.4/01-mechanistic-modeling-interop.md)
- [Annotation reference](annotations.md)
