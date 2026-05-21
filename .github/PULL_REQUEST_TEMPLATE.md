<!--
Thank you for contributing to nidus. Pick the section below that fits
your change and delete the others. For parameter and citation updates
the structured section is required so reviewers can verify every value
against its source.
-->

## Summary

<!-- One or two sentences describing what this PR does and why. -->

---

## Parameter contribution

<!-- Use this section when the PR adds or modifies an entry in
`dataset/parameters/` or `dataset/citations/`. Otherwise delete it. -->

- **Parameter id:** (dotted, snake_case — e.g. `placental_glucose.glut1_km`)
- **Subsystem:**
- **Tier (A / B / C / D):**
- **Value:** central + low/high + units, matching the schema's `value` object
- **Population / cohort:**
- **Gestational-age range:**
- **Extraction method:** (table, figure, digitised, etc.)

**Citation:**

- **Authors / Title / Venue / Year / DOI or PMID:**
- [ ] I have personally consulted this source (not just an abstract or downstream review).
- [ ] Cohort, gestational window, and units in the source match this entry.

**Tier rationale:**

<!-- One or two sentences explaining why this tier is the correct choice.
Tier inflation is a worse error than tier deflation; when in doubt,
choose the more conservative tier. -->

---

## Tier-D entry (research question)

<!-- Use this section when the PR adds a hypothesised mechanism that
lacks quantitative literature. Otherwise delete it. -->

- **Channel id:**
- **Hypothesised mechanism:**
- **Subsystem affected:**
- **What measurement would promote this from Tier D:**
- **Supporting citations:**
- **Questioning citations:**

---

## Code / dashboard / docs change

<!-- Use this section for changes to the Python package, dashboard,
notebooks, or documentation that don't fit the structured sections
above. Otherwise delete it. -->

### What changed
### Why
### Tests added or updated

---

## Checklist

- [ ] `pytest python/tests/` passes
- [ ] `ruff check python/` and `ruff format --check python/` pass
- [ ] `mypy python/nidus` passes
- [ ] `python -c "import nidus; nidus.validate()"` passes
- [ ] If this changes the schema, the relevant JSON Schema file is updated
- [ ] If this is a parameter/citation change, the verification box above is ticked
- [ ] `CHANGELOG.md` or `dataset/CHANGELOG.md` updated under `## [Unreleased]`
