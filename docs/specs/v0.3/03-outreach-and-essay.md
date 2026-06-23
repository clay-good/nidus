# Spec 03 — Outreach: Essay in the Repository

**Status:** Active. Essay text + figures shipped to `main` (`docs/about/essay.md`, `docs/assets/essay/`). The outreach channel announcements remain deferred until v0.3.0 is tagged.
**Depends on:** Spec 01 complete; Zenodo DOI minted; dashboard live.

---

## 1. Goal

Get researchers' eyes on the nidus repository. Drive discovery via
Google + GitHub + word of mouth, not via journal gatekeepers.

The vehicle is a **markdown essay published in the repository itself**
at [`docs/about/essay.md`](../../about/essay.md), embedded into the
mkdocs-material site. The essay:

- Explains the confidence-tier framework in plain language.
- Uses human gestational physiology as the worked example.
- Points to the dataset (Zenodo DOI), Python package (PyPI),
  dashboard (Streamlit URL), and GitHub repository.
- Is indexable by Google within days, not 12–18 months.

Earlier iterations of this spec discussed publishing the essay on a
personal blog. The simpler decision is to publish it in the
repository: the essay is already adjacent to the artefact it
describes, GitHub Pages serves it, and it can be moved to any other
venue later without invalidating the canonical version.

## 2. What we are doing (clear and plain)

1. **Write the essay** as
   [`docs/about/essay.md`](../../about/essay.md), ~2500 words.
2. **Generate the three figures** via
   [`notebooks/essay_figures.ipynb`](https://github.com/clay-good/nidus/blob/main/notebooks/essay_figures.ipynb)
   (seeded, deterministic) and commit them to
   [`docs/assets/essay/`](https://github.com/clay-good/nidus/tree/main/docs/assets/essay)
   so they ship as part of the mkdocs site and the repository.
3. **Deposit the dataset** on Zenodo with a permanent DOI (already
   covered by Spec 01).
4. **Announce** on Twitter / Mastodon / Bluesky / relevant Slack
   channels.
5. **Cross-link** from the repository README and the docs index.

That is the entire outreach plan. Ship it.

## 3. What we are NOT doing

| Rejected approach                                | Why                                                                                                            |
| ------------------------------------------------ | -------------------------------------------------------------------------------------------------------------- |
| Personal blog publication                        | The repository is the canonical home; a blog mirror can be added later without breaking the canonical URL.    |
| Methods paper in PLOS Comp Bio / JTB / Bioinformatics | 12–18 months calendar, peer review iteration, ~marginal upside over a freely-indexable essay. |
| Recruiting academic co-authors                   | Slow, political, optional. Skip.                                                                               |
| F1000Research / JOSS submission                  | Still optional in the future, but not the primary plan.                                                        |
| Conference talks                                 | Out of scope unless invited.                                                                                   |
| Press / journalism                               | Out of scope.                                                                                                  |
| Paid promotion                                   | Out of scope.                                                                                                  |

## 4. Essay outline (as shipped)

The essay lives at [`docs/about/essay.md`](../../about/essay.md) and
follows the structure below. Final section lengths are approximate.

| Section                          | Approx. words | What it covers                                                                                       |
| -------------------------------- | ------------- | ---------------------------------------------------------------------------------------------------- |
| Opening / hook                   | 250           | Why uncertainty in physiological modelling is structural.                                            |
| The tier idea                    | 450           | A/B/C/D tiers, criteria, why four levels, propagation rules.                                         |
| Worked example                   | 400           | Mahendru 2014 maternal cardiac output as a Tier-B case.                                              |
| Tier distribution in practice    | 200           | The 14/25/15/0 mix and what it says about the field.                                                 |
| Citations under the surface      | 400           | The bibliographic-audit finding (22 wrong identifiers) and how it was fixed.                         |
| What this is and isn't           | 350           | Honest scope. Not clinical. Not a simulator. A dataset.                                              |
| How to use it                    | 350           | `pip install nidus`. Dashboard. CLI. Three code examples.                                            |
| What's missing / open questions  | 350           | Tier D entries; non-Tier-D gaps; invitation to contribute.                                           |
| Citation / how to cite           | 100           | Zenodo DOI, BibTeX, MIT/CC-BY-4.0 licensing.                                                          |

## 5. Figures

Three figures, generated deterministically by
[`notebooks/essay_figures.ipynb`](https://github.com/clay-good/nidus/blob/main/notebooks/essay_figures.ipynb)
and committed to
[`docs/assets/essay/`](https://github.com/clay-good/nidus/tree/main/docs/assets/essay):

1. `fig1_tier_distribution.png` — stacked bar of tier mix across subsystems.
2. `fig2_worked_example_timeline.png` — Mahendru 2014 → parameter
   extraction → tier B → dataset.
3. `fig3_citation_usage_histogram.png` — citation usage distribution,
   showing the load-bearing top of the curve.

All generated by a seeded notebook so re-runs produce byte-identical
output.

## 6. Outreach checklist (after the essay is in the repo)

Status as of the current commit on `main`:

- [x] Essay written and pushed to `main` (`docs/about/essay.md`); three figures committed under `docs/assets/essay/`.
- [x] Mkdocs nav exposes the essay under About → "Essay — confidence tiers".
- [ ] GitHub Pages serving — *pending the maintainer-side Pages source flip; once enabled, the essay is live without further work.*
- [ ] Post link on Twitter / Mastodon / Bluesky with a short summary — deferred until v0.3.0 actually ships.
- [ ] Post to relevant subreddits if appropriate: r/Bioinformatics, r/datasets — deferred until v0.3.0 ships.
- [ ] Email 5–10 perinatal researchers whose work is cited in the dataset. Short, no-strings-attached: "I built this; you might find it useful; it cites your paper at parameter X." — deferred until v0.3.0 ships and DOI is minted.
- [ ] Submit to Hacker News (Show HN) — deferred.
- [ ] Submit to relevant newsletters: Data Is Plural, etc. — deferred.
- [ ] Update GitHub repository's About / topics / pinned status to point at the essay — deferred until v0.3.0 ships.

The outreach-channel checklist is intentionally on hold until v0.3.0
is tagged and the dataset has a permanent Zenodo DOI. The essay itself
is shipped and discoverable to anyone browsing the repo.

## 7. Optional: parallel preprint

If trivially low-friction (≤2 hours total), post a reformatted
version to **bioRxiv** or **OSF Preprints**. Gets a citable DOI
distinct from the Zenodo dataset DOI. Not necessary; defer if it
becomes friction.

## 8. Success criteria

The repo-buildable items are done; the rest are maintainer-side release/outreach
actions that an agent cannot perform (deploy, social posting, inbound interest).

- [x] Essay built into the docs site at `about/essay/` (renders under `mkdocs build`); **live-serving pending the maintainer-side GitHub Pages flip.**
- [x] Essay links to: repository, dashboard URL, Zenodo DOI (concept-DOI placeholder until minted), and PyPI page.
- [ ] Repository `About` and pinned status point to the essay — *maintainer-side GitHub setting; not buildable by the repo.*
- [ ] Outreach checklist (Section 6) completed — *maintainer-side; deferred until v0.3.0 ships.*
- [ ] At least one of: a GitHub star from someone unknown, an issue, an external installer, an inbound email about the dataset — *outcome metric; depends on the world, not on code.*

## 9. Realistic expectations

- The essay will get modest traffic. Hundreds of views in the first week is a good outcome; thousands would be unusual.
- The audience for nidus is small (perinatal researchers, ~hundreds globally). The essay reaches that audience indirectly — most readers will not be the target audience.
- Adoption from the essay alone is unlikely to be large. The essay's job is to seed Google's index and create a discoverable artefact that can be linked from other places over time.
- Realistic ceiling at 12 months: 2–5 GitHub stars from real researchers, 1–2 emails, ~zero downstream citations (citations take years). That is success at this stage.
