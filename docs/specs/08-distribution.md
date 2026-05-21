# Spec 08 — Distribution, Citation, Release Artefacts

## Context

Nidus today builds only from source. A researcher cannot install via
`pip`, cannot download a prebuilt binary, cannot pull a container,
cannot cite the software with a DOI. The audit (items 99–103,
151–155) lists the missing pieces:

- No release workflow.
- No `CITATION.cff`.
- No Zenodo DOI.
- No Dockerfile / Apptainer.
- No conda recipe.
- No PyPI publishing.
- No `SECURITY.md`.

This spec ships them.

## Deliverables

- `.github/workflows/release.yml` building cross-platform binaries
  and wheels on tag.
- Sigstore-signed `SHA256SUMS` per artefact.
- `CITATION.cff` at repo root; `nidus cite` subcommand.
- Zenodo concept DOI minted via GitHub–Zenodo integration; README
  badge.
- `Dockerfile` + `Apptainer.def` for HPC users.
- `conda/meta.yaml` recipe for conda-forge submission.
- `SECURITY.md`.
- A release checklist.

## Dependencies

Requires Spec 04 (wheels), Spec 06 (manifest version field), and Spec
07 (refreshed README that hosts the badges).

## Numbered prompts

### Prompt 08.1 — `CITATION.cff`

File: new [`CITATION.cff`](../CITATION.cff).

Citation File Format 1.2.0. Includes: title, abstract, authors,
keywords, repository URL, version, date-released, license, type
(`software`), preferred-citation block referencing an as-yet-unwritten
JOSS / arXiv paper (placeholder until the paper exists).

Verification: `cffconvert --validate` passes; GitHub's "Cite this
repository" widget renders.

### Prompt 08.2 — `nidus cite` subcommand

File: [`crates/nidus-cli/src/cite.rs`](../crates/nidus-cli/src/cite.rs)
(new).

Prints BibTeX (`@software{nidus, ...}`) keyed by the running
binary's version and git SHA, with the Zenodo per-version DOI when
available. `--format <bibtex|apa|csl-json>` selects format.

Verification: `nidus cite | grep '@software{nidus'` succeeds; the
DOI in the output resolves (after Prompt 08.5).

### Prompt 08.3 — Cross-platform release workflow

File: new [`.github/workflows/release.yml`](../.github/workflows/release.yml).

On a tag `v*`:
1. Build binaries: linux-x86_64, linux-aarch64, macos-arm64,
   macos-x86_64, windows-x86_64 (via `cross` and matrix runners).
2. Build wheels (delegates to the wheels workflow from Spec 04).
3. Build source tarball with `Cargo.lock` and the full `data/` tree.
4. Generate `SHA256SUMS` covering all artefacts.
5. Sign `SHA256SUMS` and each binary with `cosign` (keyless,
   GitHub OIDC).
6. Publish a GitHub Release; body is generated from CHANGELOG.md
   between the last tag and this one.
7. Optionally publish `nidus-cli` to crates.io (gated behind a
   `release-cargo-publish` job).
8. Publish wheels to PyPI via trusted publishing.

Verification: dry-run by tagging on a fork; all artefacts present;
`cosign verify-blob` succeeds against the signed manifest.

### Prompt 08.4 — `SECURITY.md`

File: new [`SECURITY.md`](../SECURITY.md).

States: Nidus is not a clinical tool; security vulnerabilities should
be reported privately via GitHub Security Advisories; expected
response time. Lists supported versions.

### Prompt 08.5 — Zenodo integration

Outside the repo: enable the GitHub–Zenodo integration on the
`anthropics/nidus` repo (or wherever it lives), creating a concept
DOI. Then in the repo:

1. Add the concept DOI badge to `README.md` and `CITATION.cff`.
2. Update `nidus cite` to embed the DOI.

Verification: a fresh release pushes a Zenodo deposit; the DOI
resolves to the deposit page.

### Prompt 08.6 — Dockerfile

File: new [`Dockerfile`](../Dockerfile) plus
[`.dockerignore`](../.dockerignore).

Multi-stage:
- Stage 1: `rust:1.79` builds binaries.
- Stage 2: `python:3.12-slim` + maturin builds wheels.
- Stage 3: `debian:bookworm-slim` runtime; copies binary + wheel,
  pre-installs Python + Nidus, drops to a non-root user.

`docker run --rm ghcr.io/<owner>/nidus:latest doctor` succeeds.

CI publishes the image to `ghcr.io` on tag push.

### Prompt 08.7 — Apptainer / Singularity definition

File: new [`Apptainer.def`](../Apptainer.def).

For HPC users who cannot run Docker. Bootstraps from the docker
image; pins the version.

### Prompt 08.8 — conda-forge recipe

File: new [`conda/meta.yaml`](../conda/meta.yaml).

Recipe for `nidus` Python package + `nidus-cli` binary. Includes a
README in `conda/` explaining how to submit to conda-forge.

Submission to conda-forge is a human follow-up step outside this
repo; document it.

### Prompt 08.9 — Crates.io publication checklist

File: new [`docs/contributing/release-checklist.md`](../docs/contributing/release-checklist.md).

Documents:
- pre-tag steps (CHANGELOG, version bump in `Cargo.toml`,
  `CITATION.cff` date),
- per-crate publication order (`nidus-core` → `nidus-data` →
  observability → ... → `nidus-cli`),
- post-publish smoke tests,
- how to yank a release if needed.

### Prompt 08.10 — Reproducibility verification artefact

File: new [`scripts/verify-release.sh`](../scripts/verify-release.sh).

A shell script that, given a tag, downloads each artefact, verifies
its `cosign` signature against the published `SHA256SUMS`, installs
the wheel into a temporary venv, runs `nidus doctor`, runs a
canonical scenario, and compares the resulting NDJSON to a reference
artefact bundled in the release.

Verification: run against the latest release; exits 0.

### Prompt 08.11 — Package metadata cleanups

Files: every `Cargo.toml` in [`crates/`](../crates/).

Ensure each crate has: `description`, `license`,
`license-file`, `repository`, `homepage`, `documentation`,
`keywords` (≤ 5), `categories`, `readme`. Required for crates.io
publication.

Verification: `cargo publish --dry-run -p nidus-core` succeeds; same
for every crate.

## Acceptance for Spec 08

- [ ] Tagging `v0.2.0` produces signed binaries for all five
  platforms, wheels for the full Python matrix, a source tarball,
  a Docker image, and a GitHub Release.
- [ ] `nidus cite` prints a BibTeX entry with a resolving DOI.
- [ ] README displays Zenodo and CI badges.
- [ ] `Dockerfile`, `Apptainer.def`, and `conda/meta.yaml` all build
  green in CI.
- [ ] `SECURITY.md` and the release checklist exist.
- [ ] `scripts/verify-release.sh` exits 0 against the latest tag.
