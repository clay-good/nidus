# Licence

Nidus uses **two complementary licences**: one for code and tooling, one for the dataset itself.

## Code: MIT

Everything in `python/`, `dashboard/`, `scripts/`, the JSON Schemas in `dataset/schema/`, the test suite, and the build infrastructure is licensed under the [MIT License](https://github.com/claygood/nidus/blob/main/LICENSE).

You may use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the code, subject to the conditions in the licence text.

## Dataset: CC-BY-4.0

The dataset content under `dataset/` — parameter JSON, citation JSON, tier JSON, JSON-LD context — is licensed under the [Creative Commons Attribution 4.0 International License (CC-BY-4.0)](https://github.com/claygood/nidus/blob/main/LICENSE-DATASET).

You are free to:

- **Share** — copy and redistribute the dataset in any medium or format
- **Adapt** — remix, transform, and build upon the dataset for any purpose, even commercially

Under the following terms:

- **Attribution** — You must give appropriate credit by citing the Zenodo DOI for the version you used, provide a link to the licence, and indicate if changes were made.
- **No additional restrictions** — You may not apply legal terms or technological measures that legally restrict others from doing anything the licence permits.

Full text: <https://creativecommons.org/licenses/by/4.0/legalcode>

## Why the split

Code and data have different reuse patterns:

- Code benefits from MIT's permissiveness — anyone integrating the loader into their own tool should be unconstrained.
- Data benefits from CC-BY-4.0's attribution requirement — academic citation conventions match the licence, and citation chains are how datasets accumulate trust over time.

Mixing the two would make either citation harder or relicensing harder. The dual-licence approach is the standard for FAIR research data + open-source tooling.

## How to cite

Cite the dataset by its Zenodo concept DOI (minted on the first release). Machine-readable citation metadata is in [`CITATION.cff`](https://github.com/claygood/nidus/blob/main/CITATION.cff) at the repository root.

A typical academic citation looks like:

> Good, C. (2026). *Nidus: a curated dataset of human gestational physiology parameters* (Version 0.3.0) [Dataset]. Zenodo. https://doi.org/10.5281/zenodo.XXXXXXX

Individual parameters carry their own primary citations; please credit those as well in any paper that builds on specific values.
