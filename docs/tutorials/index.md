# Tutorials

The reference tutorials are Jupyter notebooks living under
[`notebooks/`](https://github.com/claygood/nidus/tree/main/notebooks).
Each one exercises a chunk of the API and runs end-to-end in CI via
`nbmake`, so they cannot drift out of sync with the package.

The notebooks are embedded as pages on this site (see the navigation
on the left). You can also open them on GitHub for inline rendering, or
clone and run them locally:

```bash
pip install -e python/[dev]
jupyter notebook notebooks/
```

## What each notebook covers

| # | Notebook | Topic |
| - | -------- | ----- |
| 01 | [Parameter Explorer](../notebooks/01_parameter_explorer.ipynb) | Loading, inspecting, filtering, and plotting basic statistics. The canonical "first contact" notebook. |
| 02 | [Tier Walkthrough](../notebooks/02_tier_walkthrough.ipynb) | What the A/B/C/D tiers mean, with examples from the dataset; propagation rules. |
| 03 | [Uncertainty Propagation](../notebooks/03_uncertainty_propagation.ipynb) | A worked Monte Carlo composition of two Tier-B parameters with propagated tier. |
| 04 | [Citation Provenance](../notebooks/04_citation_provenance.ipynb) | Load-bearing citations, the citation graph, and BibTeX export. |

A fifth notebook, `essay_figures.ipynb`, generates the three figures
for the outreach blog essay (Spec 03). It's a build script for the
post, not a tutorial — it isn't embedded as a tutorial page but is
listed for completeness.

## Maintenance

The notebooks are generated artefacts; their source-of-truth is
[`scripts/build_notebooks.py`](https://github.com/claygood/nidus/blob/main/scripts/build_notebooks.py).
Cell ids are deterministic SHA-256 hashes so re-generations produce
stable diffs.

To edit a notebook, edit the build script and re-run:

```bash
python scripts/build_notebooks.py
```
