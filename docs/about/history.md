# History

Nidus began as a Rust prototype exploring coupled maternal-placental-fetal physiology simulation. The prototype is preserved at the `v0.2-archive` git tag and remains recoverable with:

```bash
git checkout v0.2-archive
```

## What that phase produced

- Twelve Rust crates totalling ~9,000 lines of engine and infrastructure: deterministic RNG, fixed-point numerics, tick hierarchy, telemetry bus, hypothesis pipeline (Sobol sensitivity, divergence detection), and three subsystem modules (maternal cardiovascular, placental transport, fetal circulation).
- The TOML-based parameter database that became the source for the v0.3 JSON dataset.
- The confidence-tier framework as a first-class engine concept.
- One shipped validation case (maternal cardiac output against Mahendru 2014).

## What that phase surfaced

Two things became clear during the prototype:

1. The **durable contribution** was the curated parameter set plus the confidence-tier discipline — both presentation-layer-agnostic.
2. The **right form factor for the audience** (biomedical researchers, almost all Python/R users) was a pip-installable dataset, not a compiled simulator competing with mature physiological-modelling platforms like CellML, COPASI, and PhysioCell.

## What v0.3 keeps

- The curated parameters (migrated to schema-valid JSON).
- The citation index (also migrated).
- The confidence-tier framework (now central, not decorative).
- The honest scope statement: not a clinical tool; not a mechanistic simulator competitor.

## What v0.3 drops

- The Rust engine itself. NumPy/SciPy handles everything the dashboard needs, and a second language was friction without value for the audience.
- The simulator-as-product framing. The dataset is the product; the simulator was the prototype that surfaced it.
- The aspiration to compete with CellML/COPASI on mechanistic modelling. Interop via optional SBML/CellML export is the right relationship.

## Why this matters

A common mistake in research tooling is to over-engineer the substrate (a more flexible simulator, a richer DSL, a more elegant runtime) instead of curating the artefact that researchers actually need (a dataset, a benchmark, a reference table). v0.3 corrects that mistake.

The git history (and the `v0.2-archive` tag) preserves the full prototype work for anyone who wants to see where it ended up before the reframe.
