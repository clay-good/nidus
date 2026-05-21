# Researcher-Ready Spec Set

This directory holds the detailed implementation plan for taking Nidus
from its current v0.1.0 state (scaffolded engine, 17 prompts landed) to
a state where a working scientific researcher — not a Rust engineer —
can clone, install, run, trust, cite, and extend the simulator.

The high-level overview lives in [`../SPEC_V0.2.md`](../SPEC_V0.2.md).
This directory expands that overview into twelve focused specs, one per
work stream, with concrete Claude Code prompts, file paths, and
acceptance tests drawn from a 157-item gap audit of the repository.

## Reading order

Specs build on each other. The intended order is:

| # | Spec | Why this position |
|---|------|------------------|
| 01 | [Parameter database](01-parameter-database.md) | Unblocks everything else — all subsystem parameters currently scaffold. |
| 02 | [Subsystem completion](02-subsystem-completion.md) | Implements the maternal/placental/fetal modules that SPEC.md §§5–8 promised but v0.1 left out. |
| 03 | [Validation suite](03-validation-suite.md) | Without real validation cases, no researcher can trust output. Depends on 01. |
| 04 | [Python bindings & notebooks](04-python-bindings.md) | Researchers reach for Python first. Depends on a stable Rust API (01–02). |
| 05 | [Interactive dashboard](05-dashboard.md) | Visual interpretation surface. Depends on observability NDJSON (already shipped). |
| 06 | [CLI, reproducibility, manifest](06-cli-and-reproducibility.md) | `nidus run`, `nidus doctor`, `nidus reproduce`. Depends on 01–02. |
| 07 | [Examples, tutorials, module docs](07-examples-and-tutorials.md) | The on-ramp. Depends on 01–06 having stable APIs. |
| 08 | [Distribution & citation](08-distribution.md) | Releases, CITATION.cff, Zenodo DOI, Docker, conda. Last because it ships the result. |
| 09 | [Testing & CI](09-testing-and-ci.md) | Cross-cutting; can be worked in parallel with 01–08. |
| 10 | [Population modelling](10-population-modeling.md) | Cohort sampling, individual heterogeneity from real distributions. Depends on 01. |
| 11 | [Hypothesis generalization](11-hypothesis-generalization.md) | Broadens the v0.1 placental-gas-exchange-only pipeline. Depends on 02. |
| 12 | [Code hygiene & error handling](12-code-hygiene.md) | Remove panics, update stale README labels, polish. Last polish pass. |

A two-person team plus an LLM assistant should plan on **eight to
twelve focused weeks** to clear specs 01–08. Specs 09–12 are
cross-cutting polish that can interleave throughout.

## How each spec is structured

Every spec in this directory follows the same shape:

1. **Context.** Where the current code stands and what gap this spec
   closes. Quotes the audit when useful.
2. **Deliverables.** A bullet list of concrete artefacts (files,
   functions, doc pages, CI jobs).
3. **Numbered prompts.** Each prompt is a self-contained Claude Code
   instruction with:
   - the file(s) to touch,
   - the specific change,
   - the verification command.
4. **Acceptance.** The end-state checklist for the whole spec.
5. **Dependencies.** Which earlier specs (or human-only tasks) must be
   complete first.

Numbered prompts in this directory should be referenced as
`Spec NN, Prompt M` (e.g. `Spec 01, Prompt 3`) in PRs, commit messages,
and [PROGRESS.md](../PROGRESS.md).

## What "100% ready for a researcher" means

When every spec in this directory is complete, a researcher can:

1. Install in under five minutes (`pip install nidus` or
   `cargo install nidus-cli` or a prebuilt binary).
2. Run a published scenario and reproduce the figures shown in
   `docs/tutorials/running_first_scenario.md`.
3. Inspect, for any plotted quantity, the citation list and the
   confidence tier.
4. Perturb a parameter from Python, re-run, compare, and plot the
   difference with tier-aware uncertainty bands.
5. Generate a ranked experiment-design list against the current
   parameter database for any modelled subsystem.
6. Cite Nidus with a permanent DOI; cite individual parameters by
   their original sources.
7. Submit a verified parameter PR using the templates in
   `.github/`; CI checks the citation and tier; reviewers follow a
   documented checklist.
8. Re-run a colleague's manifest and obtain byte-identical output
   across machines.
9. Validate any simulator output against the bundled reference
   datasets (NICHD Fetal Growth Studies, Doppler flow ranges, fetal
   cardiovascular development) and see exactly which checks pass and
   which fail.
10. Read a one-page module doc for any crate before touching its
    source.

That is the v0.2.0 bar.

## Out of scope for v0.2.0

The following are explicitly **not** targets of this spec set — they
remain v0.3+ work, called out so reviewers know what to push back on:

- Embryonic period (< 8 weeks gestational age).
- Labour and delivery.
- Twin and higher-order pregnancies.
- Clinical decision support, in any form.
- Automated parameter-from-literature extraction (humans verify; LLMs
  do not).
- A general-purpose hosted "Nidus cloud."

Anything else absent from this spec set is an oversight — please file
an issue.

## Cross-cutting principles for every spec

Apply these to every prompt unless a spec explicitly overrides them:

- **Determinism is sacred.** Any change that breaks bit-identical
  reproducibility for a fixed seed must be called out in the PR and
  in [`CHANGELOG.md`](../CHANGELOG.md), with reasoning.
- **Tiers propagate.** Any new computed quantity must carry its
  tier and citation list through `Tiered<T>`. Hard-coded numbers
  outside of `#[cfg(test)]` are an audit failure.
- **Citations are non-negotiable.** Every Tier A/B parameter must
  link to a `Citation` record that a human has personally verified.
- **No silent failure.** Replace `panic!` paths with typed errors;
  CLI exit codes must be non-zero on any unhandled failure.
- **Tests follow code.** Every prompt's verification step ends with
  a runnable command. CI must enforce them.
