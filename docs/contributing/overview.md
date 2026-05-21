# Contributing

The most valuable contributions to nidus are **verified parameters drawn from published empirical work**.

## What's most useful right now

1. **[Verify an existing citation](verification.md).** Walk an existing parameter, confirm its values match what the cited paper actually reports, and update `extraction.review_status` to `"verified"`. All v0.3 entries are currently marked `unverified`; the tier system only has teeth once verification has happened.

2. **Propose a new Tier-A or Tier-B parameter** from the literature via the [parameter-request issue template](https://github.com/claygood/nidus/issues/new?template=parameter-request.yml). Include the DOI, the extraction method, and the tier you propose; a reviewer cross-checks against the cited paper before the PR lands.

3. **Surface a Tier-D research question** — a hypothesised mechanism worth measuring next — via the [research-question issue template](https://github.com/claygood/nidus/issues/new?template=hypothesis-proposal.yml). See the [tier system page](../dataset/tiers.md) for what makes a good Tier-D candidate.

4. **Improve the docs, tutorials, or dashboard.** PRs welcome; the contribution-friction bar is low.

## Workflow

1. Open an issue first using one of the templates. This lets us catch duplicates, scope problems, or methodological concerns before you spend time on a PR.
2. For parameter / citation work, fork the repo and edit the appropriate JSON file in `dataset/parameters/` or `dataset/citations/`.
3. Run the local CI sweep:
   ```bash
   pip install -e python/[dev]
   ruff check python/ dashboard/ scripts/
   pytest python/tests/
   python -c "import nidus; nidus.validate()"
   ```
4. Open a PR using the [PR template](https://github.com/claygood/nidus/blob/main/.github/PULL_REQUEST_TEMPLATE.md). The structured "Parameter contribution" section requires you to tick the box confirming you have personally consulted the cited paper.

## What we look for in a parameter PR

- A **single citation** linked by DOI or PMID (books accepted without DOI). The citation must be in `dataset/citations/citations.json`; add it if it's new.
- A **schema-valid record** with `id`, `name`, `subsystem`, `value`, `tier`, `tier_rationale`, `citations`, and `extraction.review_status`. Run `nidus.validate()` to confirm.
- A **tier rationale** that references the evidence base — number of studies, cohort size, technique. See examples in the existing dataset.
- **Conservative tier assignment.** When in doubt, drop one level. See the [tier-assignment guide](tier-assignment.md).

## Licence

By contributing, you agree that:

- Your code contributions are MIT-licensed (matching the package).
- Your dataset contributions are CC-BY-4.0 (matching the dataset).
- You hold or have permission to share the data you contribute (no scraped paywalled values, no unauthorised re-publication).

## Code of Conduct

See [CODE_OF_CONDUCT.md](https://github.com/claygood/nidus/blob/main/CODE_OF_CONDUCT.md).

## Getting in touch

File an issue or open a [GitHub Discussion](https://github.com/claygood/nidus/discussions) on the repo.
