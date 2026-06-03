# Project orientation for Claude Code

**Read [docs/specs/v0.3/00-overview.md](docs/specs/v0.3/00-overview.md) first.** It captures the v0.3 design in one page.

## What nidus is

A **curated, citation-backed, confidence-tier-annotated JSON dataset** of human gestational physiology parameters, distributed as a pure-Python package (`pip install nidus`) and browsable via a Streamlit dashboard.

The dataset is the centerpiece. Everything else (Python package, dashboard, optional SBML/CellML export) is a presentation layer.

## Scope decisions (locked in)

- **Pure Python.** No Rust, no PyO3, no compiled extensions. NumPy/SciPy is sufficient for everything the dashboard needs.
- **GitHub + PyPI + Streamlit Cloud are the canonical URLs.** No custom domain.
- **An essay in the repository** is the outreach vehicle. No academic methods paper.
- **Dataset-only scope.** No new mechanistic biology beyond the curated parameters.
- **The earlier Rust prototype is archived,** not deleted: see the `v0.2-archive` git tag.
- **Pre-pivot specs have been deleted.** The original Rust-era specs (`docs/specs/SPEC.md`, `SPEC_V0.2.md`, and twelve numbered work-stream plans) used to live alongside the active v0.3 design as deprecation stubs; once nothing referenced them, they were removed. Recover any from git history.

## Where the work lives

| Path                                          | Status                                                              |
| --------------------------------------------- | ------------------------------------------------------------------- |
| `docs/specs/v0.3/00-overview.md`              | **READ FIRST for v0.3.** Dataset-first design and rationale.        |
| `docs/specs/v0.3/01-dataset-and-dashboard.md` | **Active.** Dataset + Python package + dashboard. Primary work.     |
| `docs/specs/v0.3/03-outreach-and-essay.md`    | **Active.** Essay outreach (in-repo).                               |
| `docs/specs/v0.4/00-overview.md`              | **READ FIRST for v0.4.** Why interop is primary.                    |
| `docs/specs/v0.4/01-mechanistic-modeling-interop.md` | **Active.** SBML + CellML + PhysioCell exports + composed model. |
| `dataset/`                                    | The curated dataset. JSON, schema-validated, FAIR-compliant.        |
| `python/`                                     | The `nidus` package source. Pure Python.                            |
| `dashboard/`                                  | The Streamlit dashboard (scaffolded; pages land incrementally).     |
| `notebooks/`                                  | Reference notebooks (land alongside the dashboard).                 |
| `scripts/`                                    | One-off migration + maintenance scripts.                            |

## Audience and ethos

- Audience: ~hundreds of perinatal researchers globally. Almost all Python/R users.
- Solo maintainer. Scope matches.
- MIT for code, CC-BY-4.0 for the dataset. Forever free. No commercial intent.
- Be honest about scope and limits. Dishonesty about uncertainty turns a useful tool into a misleading one.
- Realistic best case: a handful of researchers cite the dataset; one publishes a hypothesis informed by it. That is success.

## When in doubt

- The dataset is the centerpiece.
- The audience wants something they can use today, not a heroic simulator.
- Honest scope > ambitious scope.

<!-- openlore-decisions-instructions -->
## Architectural decisions

When making a significant design choice, call `record_decision` **before** writing the code.

Significant choices: data structure, library/dependency, API contract, auth strategy,
module boundary, database schema, caching approach, error handling pattern.

```
record_decision({
  title: "Use JWTs for stateless auth",
  rationale: "Avoids session store in infra",
  consequences: "Tokens can't be revoked early",
  affectedFiles: ["src/auth/middleware.ts"],
  supersedes: "a1b2c3d4"  // 8-char ID of prior decision being reversed
})
```

Decisions are consolidated in the background immediately after `record_decision` is called — the pre-commit gate reads the already-consolidated store and adds no LLM latency.

**Performance note**: if you skip `record_decision`, the gate detects unrecorded source changes at commit time and triggers a slow LLM extraction on the *next* commit (~10-30s). Calling `record_decision` proactively keeps every commit instant.

## When git commit is blocked by the decisions gate

If `git commit` fails and the output is JSON with `"gated": true`, do NOT retry silently.
Check the `reason` field and act accordingly:

**`reason: "verified"` — decisions await review:**
Present each decision to the user:
> "The commit is blocked — I found N architectural decision(s) to validate:
> 1. **[id]** Title — rationale
Do you approve? (yes/no)"
For each approval call `approve_decision`, for rejections call `reject_decision`.
Then run `openlore decisions --sync` and retry `git commit`.

**`reason: "approved_not_synced"` — decisions approved but not written to specs:**
Run `openlore decisions --sync` then retry `git commit`. Do not skip this step.

**`reason: "drafts_pending_consolidation"` — drafts were recorded but not yet consolidated:**
Present to the user:
> "N decision draft(s) were recorded but never consolidated. Run consolidation now? (~10-30s)"
If yes: run `openlore decisions --consolidate --gate` and handle the result.
If no: retry with `git commit --no-verify` to skip the gate.

**`reason: "no_decisions_recorded"` — source files staged but nothing recorded:**
Present to the user:
> "Source files are staged but no architectural decisions were recorded. Run fallback extraction to check for undocumented decisions? (~10-30s)"
If yes: run `openlore decisions --consolidate --gate` and handle the result.
If no: retry with `git commit --no-verify` to skip the gate.
<!-- end-openlore-decisions-instructions -->
