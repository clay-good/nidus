<!--
Thank you for contributing to Nidus. Choose the section below that
matches your contribution and delete the others. If your PR is a
parameter or citation update, please follow the structured
"Parameter contribution" section so the review can verify the citation
against its original source. See CONTRIBUTING.md for context.
-->

## Summary

<!-- One or two sentences describing what this PR does and why. -->

---

## Parameter contribution

<!-- Use this section when the PR adds or modifies an entry in
`data/parameters/` or `data/citations/`. Otherwise delete it. -->

- **Parameter id:**
- **Tier (A / B / C / D):**
- **Value:** (point estimate with uncertainty, or distribution)
- **Unit:**
- **Population / cohort:**
- **Gestational-age range:**
- **Measurement technique:**
- **Caveats:**

**Citation:**

- **Authors / Title / Venue / Year / DOI or PMID:**
- **I have personally consulted this source:** yes / no

**Tier rationale:**
<!-- One or two sentences explaining why this tier is the correct
choice. Tier inflation is a more serious error than tier deflation;
when in doubt, choose the more conservative tier. -->

---

## Unknown channel contribution

<!-- Use this section when the PR adds or modifies an entry in
`nidus-unknown::registry`. Otherwise delete it. -->

- **Channel id:**
- **Tier (C / D):**
- **Hypothesised mechanism:**
- **Parameter range and units:**
- **Downstream effects (in subsystem-affected terms):**
- **Supporting citations:**
- **Questioning citations:**

---

## Validation case contribution

<!-- Use this section when the PR adds a case to `nidus-validation`.
Otherwise delete it. -->

- **Component or subsystem under test:**
- **Reference dataset id:**
- **Citation for the dataset:**
- **Level (component / integration / outcome):**
- **Expected agreement bucket:**

---

## Code change

<!-- Use this section for engine, API, or visualisation code changes
that do not fit the structured sections above. Otherwise delete it. -->

### What changed
### Why
### Tests added or updated

---

## Checklist

- [ ] `cargo build --workspace` succeeds with zero warnings
- [ ] `cargo test --workspace` passes
- [ ] `cargo clippy --workspace --all-targets -- -D warnings` passes
- [ ] New public items carry doc comments
- [ ] If this changes confidence-tier behaviour, the change is
      documented in the affected module's top-level docs
- [ ] PROGRESS.md updated if a SPEC.md §13 prompt status changes
