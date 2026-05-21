# Contributing to Nidus

Thank you for considering a contribution. Nidus is built to invite
participation from the scientific community, and the contribution model
is structured around the principle that the most valuable contributions
are parameter updates derived from published empirical work. The full
specification is in [docs/specs/SPEC.md](docs/specs/SPEC.md); this guide
focuses on the practical mechanics of contributing.

## Filing an issue

Three structured issue templates are wired into GitHub
([`.github/ISSUE_TEMPLATE/`](.github/ISSUE_TEMPLATE/)):

- **Parameter request** — a new entry under `data/parameters/`, or a
  revision of an existing one. Walks you through the citation,
  population, gestational-age range, and tier rationale.
- **Bug report** — a reproducible defect in the simulator, CLI,
  validation suite, or docs.
- **Hypothesis proposal** — a candidate mechanism, unknown channel, or
  experiment-design target.

Open-ended discussion belongs in GitHub Discussions, not Issues.

## The confidence tier system

Every modelled quantity in Nidus belongs to one of four confidence tiers.
The tier system is structural to the model, not documentation about it:
tiers propagate through computations, so any output derived from a less
confident input cannot itself be more confident than that input. The
tiers are:

- **Tier A — Well-characterised mechanism.** The underlying physics or
  chemistry is understood, parameters are measured with good precision
  across multiple independent studies, and the model is essentially a
  careful encoding of accepted equations. Examples: the
  oxygen–haemoglobin dissociation relationship, Fickian diffusion of
  gases across known membranes, the fluid mechanics of umbilical blood
  flow.
- **Tier B — Understood mechanism with parameter uncertainty.** The form
  of the governing equations is settled, but the constants vary
  meaningfully by population, gestational age, individual, or
  measurement technique. Examples: placental surface area development
  across gestation, fetal cardiac output as a function of gestational
  age, amniotic fluid turnover dynamics.
- **Tier C — Phenomenology without mechanism.** Observational data shows
  that something happens, often with reasonable statistical correlation,
  but no mechanistic model lets us predict outcomes from first
  principles. Examples: the influence of maternal cortisol patterns on
  fetal HPA axis development, the dynamics of cellular microchimerism,
  many aspects of placental hormonal signalling.
- **Tier D — Speculation and unknowns.** The phenomenon is suspected to
  be important based on indirect evidence but is not well characterised.
  Examples: the developmental significance of specific maternal
  exosomal microRNA cargo, the functional role of placental hormones
  whose receptors have been detected but whose downstream effects are
  not mapped.

When in doubt, prefer a more conservative (less confident) tier
assignment. The tier system exists to be honest about uncertainty, and an
over-confident tier assignment is a more serious error than a
conservative one. Tier upgrades are easy when new evidence arrives;
silent tier inflation is hard to detect once it has propagated through
the model.

## Parameter contributions

The contribution path that exercises the most of the project's
infrastructure is a parameter update. A parameter update pull request
must include:

1. The parameter value, expressed either as a point estimate with
   uncertainty or as a full distribution, in the schema used by
   `data/parameters/` (forthcoming).
2. A complete citation block for the source: authors, title, venue,
   year, and a DOI or PubMed identifier when one exists.
3. A tier assignment, with a one- or two-sentence rationale.
4. The population or cohort the value was derived from, with enough
   detail that a reader can assess applicability.
5. The gestational age range over which the value is documented.
6. Any caveats about extrapolation outside the studied range.

Contributors are expected to cite parameters from sources they have
personally consulted. The review process will verify citations against
their originals; citations that cannot be verified will not be merged.
This is what protects the scientific integrity of the simulator.

## Other contributions

- **Unknown channel additions.** If you have identified a Tier C or D
  channel the registry does not yet represent, propose it as a new entry
  in `nidus-unknown` with a hypothesised mechanism, supporting and
  questioning citations, and parameter ranges.
- **Validation test additions.** Published reference data that the
  validation suite does not currently use is welcome. Include the data
  source, the model component it tests, and an honest assessment of how
  closely the current model agrees with it.
- **Module implementations.** Extensions that model a system or
  pathology not currently covered can be proposed as new crates
  following the architectural patterns of the existing modules.

## Pull request expectations

- The workspace must build with zero warnings and `cargo test` must
  pass.
- New code is formatted with `cargo fmt` and clippy-clean
  (`cargo clippy --workspace --all-targets`).
- Public items carry doc comments. Comments in the body of code should
  be reserved for the non-obvious *why* of a decision; do not paraphrase
  code in prose.
- The forbid-unsafe-code directive is in force across core crates and
  is not to be relaxed.

## Code of conduct

By participating in this project you agree to follow our
[Code of Conduct](CODE_OF_CONDUCT.md), which emphasises scientific
honesty, respectful engagement, and the project's stated commitment to
reducing maternal and fetal suffering. Contributions that would obscure
rather than surface uncertainty will be declined regardless of their
technical sophistication.
