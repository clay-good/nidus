# Tutorials

The reference tutorials are Jupyter notebooks under [`notebooks/`](https://github.com/claygood/nidus/tree/main/notebooks). Each one exercises a chunk of the API and runs end-to-end in CI via `nbmake`, so they cannot drift out of sync with the package.

GitHub renders `.ipynb` files inline — click any title below to open the notebook directly. Or clone and run them locally:

```bash
pip install -e python/[dev]
jupyter notebook notebooks/
```

---

## 01 — [Parameter Explorer](https://github.com/claygood/nidus/blob/main/notebooks/01_parameter_explorer.ipynb)

The canonical "first contact" notebook. Loads the dataset, inspects a single parameter, filters by subsystem / tier / combinations, and plots basic statistics (tier distribution, per-subsystem values).

Use this if you are new to the package.

---

## 02 — [Tier Walkthrough](https://github.com/claygood/nidus/blob/main/notebooks/02_tier_walkthrough.ipynb)

What the A/B/C/D tiers mean, with the criteria for each and concrete examples drawn from the dataset. Explains how tiers propagate through derived quantities, and the two degradation rules (out-of-range and out-of-population).

Use this to understand what the tiers are claiming.

---

## 03 — [Uncertainty Propagation](https://github.com/claygood/nidus/blob/main/notebooks/03_uncertainty_propagation.ipynb)

A worked example: estimate peak gestational cardiac output (baseline + peak excess) with a Monte Carlo over both inputs' Gaussian distributions. Demonstrates uncertainty composition, propagated tier, and honest caveats about the independence assumption across cohorts.

Use this when you want to compose nidus parameters into a derived quantity for your own model.

---

## 04 — [Citation Provenance](https://github.com/claygood/nidus/blob/main/notebooks/04_citation_provenance.ipynb)

Citation graph: most load-bearing papers, per-citation drill-down, the small set of identifier-less older book references, and a BibTeX exporter for the full bibliography.

Use this to chase provenance, audit citation rot, or pull a BibTeX file for your own paper.

---

## essay_figures

The [`essay_figures.ipynb`](https://github.com/claygood/nidus/blob/main/notebooks/essay_figures.ipynb) notebook generates the three figures used in the [outreach blog essay](https://github.com/claygood/nidus/blob/main/docs/specs/v0.3/03-outreach-and-essay.md). Seeded numpy, deterministic output.

Not strictly a tutorial — it is a build script for the blog post. Listed here for completeness.

---

## Maintenance

The notebooks are generated artifacts. Their source-of-truth is [`scripts/build_notebooks.py`](https://github.com/claygood/nidus/blob/main/scripts/build_notebooks.py); cell ids are deterministic SHA-256 hashes so diffs stay clean when content is unchanged. To edit a notebook, edit the build script and re-run:

```bash
python scripts/build_notebooks.py
```
