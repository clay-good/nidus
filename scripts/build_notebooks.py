#!/usr/bin/env python3
"""Build the reference notebooks from their Python source.

The .ipynb files in ``notebooks/`` are generated artifacts; this script
is the source of truth. Re-run after editing notebook content:

    python scripts/build_notebooks.py

The committed .ipynb files have empty outputs; ``nbmake`` (in CI and
locally) executes them end-to-end to verify correctness.
"""

from __future__ import annotations

import hashlib
import json
import textwrap
from pathlib import Path

ROOT = Path(__file__).parent.parent
OUT = ROOT / "notebooks"


def _stable_cell_id(notebook: str, index: int, source: str) -> str:
    """Deterministic cell id; stable across runs so diffs stay clean.

    nbformat warns (and will eventually error) on cells without an
    ``id`` field. Using uuid4 would mean a diff on every regeneration;
    hashing instead keeps the ipynb files stable when the source
    doesn't change.
    """
    h = hashlib.sha256(f"{notebook}::{index}::{source}".encode()).hexdigest()
    return h[:12]


# ---- Cell helpers ---------------------------------------------------


def _lines(text: str) -> list[str]:
    """JSON-format notebook cell sources: list of lines, each with trailing \n
    except the last which may omit it. Use splitlines(keepends=True)."""
    if not text:
        return []
    return text.splitlines(keepends=True)


def md(text: str) -> dict:
    return {
        "cell_type": "markdown",
        "metadata": {},
        "source": _lines(textwrap.dedent(text).strip("\n")),
    }


def code(src: str) -> dict:
    return {
        "cell_type": "code",
        "execution_count": None,
        "metadata": {},
        "outputs": [],
        "source": _lines(textwrap.dedent(src).strip("\n")),
    }


def write_notebook(filename: str, cells: list[dict]) -> None:
    # Inject deterministic cell ids so nbformat doesn't warn / error.
    for i, c in enumerate(cells):
        c["id"] = _stable_cell_id(filename, i, "".join(c["source"]))
    nb = {
        "cells": cells,
        "metadata": {
            "kernelspec": {
                "display_name": "Python 3",
                "language": "python",
                "name": "python3",
            },
            "language_info": {
                "name": "python",
                "version": "3.10",
                "mimetype": "text/x-python",
                "file_extension": ".py",
            },
        },
        "nbformat": 4,
        "nbformat_minor": 5,
    }
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / filename).write_text(json.dumps(nb, indent=1) + "\n", encoding="utf-8")
    print(f"  wrote notebooks/{filename}")


# ========== 01 — Parameter Explorer =================================


def build_01() -> None:
    cells = [
        md("""
        # Parameter Explorer

        Loading the nidus dataset, inspecting individual parameters,
        filtering across axes, and rendering basic statistics.

        This is the canonical "first contact" notebook for the nidus
        package. It exercises every public API documented in the README.
        """),
        md("## Setup"),
        code("""
        import nidus
        import matplotlib.pyplot as plt
        from collections import Counter
        """),
        code("""
        ds = nidus.load()
        ds
        """),
        md("## Inspect a single parameter"),
        code("""
        p = ds["maternal_cardiovascular.baseline_cardiac_output_l_per_min"]
        print(f"Name:           {p.name}")
        print(f"Subsystem:      {p.subsystem}")
        print(f"Value:          {p.value.central} {p.value.units}")
        print(f"Range:          {p.value.low}–{p.value.high}")
        print(f"Distribution:   {p.value.distribution} (CI {p.value.ci})")
        print(f"Tier:           {p.tier}")
        print(f"Citations:      {len(p.citations)}")
        print(f"Primary DOI:    {p.primary_citation.doi}")
        print()
        print("Tier rationale:")
        print(p.tier_rationale)
        """),
        md("""
        ## Filter by subsystem

        ``Dataset.filter`` returns a new ``Dataset`` containing the
        matching parameters. All citations and tier definitions are
        carried through unchanged so back-references still resolve.
        """),
        code("""
        cardio = ds.filter(subsystem="maternal_cardiovascular")
        print(f"{len(cardio)} maternal-cardiovascular parameters")
        for p in list(cardio)[:5]:
            print(f"  [{p.tier}] {p.id}")
        """),
        md("## Filter by tier"),
        code("""
        tier_a = ds.filter(tier="A")
        print(f"{len(tier_a)} Tier-A parameters across all subsystems")
        for p in list(tier_a)[:5]:
            print(f"  {p.id}")
        """),
        md("## Combine filters"),
        code("""
        b_or_c = ds.filter(subsystem="placental_glucose", tier=["B", "C"])
        for p in b_or_c:
            print(f"  [{p.tier}] {p.id}  ({p.value.central} {p.value.units})")
        """),
        md("## Tier distribution across the whole dataset"),
        code("""
        tier_counts = Counter(p.tier for p in ds)
        tier_counts
        """),
        code("""
        fig, ax = plt.subplots(figsize=(6, 3))
        tiers = ["A", "B", "C", "D"]
        colors = ["#2ca02c", "#1f77b4", "#ff7f0e", "#d62728"]
        ax.bar(tiers, [tier_counts.get(t, 0) for t in tiers], color=colors)
        ax.set_ylabel("Number of parameters")
        ax.set_title(f"Tier distribution across {len(ds)} parameters")
        plt.tight_layout()
        plt.show()
        """),
        md("## Compare values within one subsystem"),
        code("""
        subset = list(ds.filter(subsystem="fetal_growth"))
        labels = [p.name for p in subset]
        centrals = [p.value.central for p in subset]
        units = [p.value.units for p in subset]
        for label, central, unit in zip(labels, centrals, units):
            print(f"  {central:>8.3g} {unit:<14s}  {label}")
        """),
        md("""
        ## What next

        - **[02_tier_walkthrough.ipynb](02_tier_walkthrough.ipynb)** —
          what the A/B/C/D tiers mean and how they propagate through
          derived quantities.
        - **[03_uncertainty_propagation.ipynb](03_uncertainty_propagation.ipynb)** —
          composing parameters across subsystems with explicit
          uncertainty handling.
        - **[04_citation_provenance.ipynb](04_citation_provenance.ipynb)** —
          citation graph, load-bearing papers, BibTeX export.
        """),
    ]
    write_notebook("01_parameter_explorer.ipynb", cells)


# ========== 02 — Tier Walkthrough ===================================


def build_02() -> None:
    cells = [
        md("""
        # Confidence Tiers — A Walkthrough

        Every parameter in nidus carries one of four confidence tiers
        describing the strength of evidence behind it. This notebook
        explains what each tier means, how to read the
        ``tier_rationale`` field, and how tiers propagate through
        derived quantities.

        The tier system is the most rare and load-bearing thing about
        nidus. Treat it as central, not decorative.
        """),
        md("## Setup"),
        code("""
        import nidus
        from collections import Counter

        ds = nidus.load()
        """),
        md("## The tier definitions"),
        code("""
        for tier_id, tier in ds.tiers.items():
            print(f"Tier {tier_id} — {tier.label}")
            for c in tier.criteria:
                print(f"  · {c}")
            print()
        """),
        md("""
        ## Tier distribution in this dataset

        The mix tells you something about the field: pregnancy
        physiology is data-rich for maternal hemodynamics (mostly
        Tier B), patchy for placental transport (a mix of B and C),
        and almost entirely empty at Tier D (we have not yet started
        cataloguing structured open questions).
        """),
        code("""
        tier_counts = Counter(p.tier for p in ds)
        for t in "ABCD":
            print(f"  Tier {t}: {tier_counts.get(t, 0):>3} parameters")
        """),
        md("""
        ## How to read ``tier_rationale``

        Every parameter carries a free-text rationale explaining why it
        was assigned its tier. The rationale should reference the
        evidence base — number of studies, cohort size, measurement
        technique, known caveats.

        Most rationales in v0.3 are placeholders synthesised from the
        v0.2 TOML curation. Reviewers re-write them when promoting
        parameters from ``unverified`` to ``verified``.
        """),
        code("""
        example_b = next(p for p in ds if p.tier == "B")
        print(f"[Tier B example] {example_b.id}")
        print(example_b.tier_rationale)
        """),
        code("""
        example_c = next(p for p in ds if p.tier == "C")
        print(f"\\n[Tier C example] {example_c.id}")
        print(example_c.tier_rationale)
        """),
        md("""
        ## Tier propagation rules

        When a model derives a quantity from multiple parameters, the
        derived quantity's tier is the **minimum** (lowest) of its
        inputs. The reasoning is conservative:

        * A derived quantity cannot be better-supported than its
          weakest input.
        * A user comparing two derived quantities needs to know the
          worst-case provenance, not the best-case.

        Concretely, if you compute ``F(p1, p2, p3)`` where p1 is
        Tier A, p2 is Tier B, and p3 is Tier C, then the result is
        Tier C.

        Two additional degradations:

        * Tier degrades by one level if a parameter is **extrapolated
          outside its validated range** (e.g. a 8–40 week parameter
          used at week 6).
        * Tier degrades by one level if a parameter is **applied
          outside its applicability population** (e.g. a singleton
          parameter used for twins).

        The next notebook demonstrates propagation in code.
        """),
        md("""
        ## How to assign a tier

        Tier inflation is a worse error than tier deflation. When in
        doubt, choose the more conservative tier.

        For a candidate parameter:

        1. Is there a single citation, or multiple? Single → C or B.
        2. Is the cohort longitudinal with n≥100? If yes → B candidate.
        3. Are there ≥3 independent confirmations with overlapping
           confidence intervals? If yes → A candidate.
        4. Is there no quantitative literature at all? → D.

        See [CONTRIBUTING.md](../CONTRIBUTING.md) for the verification
        standard, and the
        [parameter-request issue template](https://github.com/clay-good/nidus/issues/new?template=parameter-request.yml)
        for the full proposal flow.
        """),
    ]
    write_notebook("02_tier_walkthrough.ipynb", cells)


# ========== 03 — Uncertainty Propagation ============================


def build_03() -> None:
    cells = [
        md("""
        # Uncertainty-aware Composition

        A worked example: estimate the **peak gestational cardiac
        output** (preconception baseline + peak rise) with explicit
        uncertainty propagation, and verify that the derived quantity
        inherits the tier of its weakest input.

        This notebook demonstrates one of the most useful things you
        can do with nidus: combine its citation-backed parameters into
        a derived quantity, while keeping uncertainty and provenance
        intact.
        """),
        md("## Setup"),
        code("""
        import nidus
        import numpy as np
        import matplotlib.pyplot as plt

        rng = np.random.default_rng(seed=20251101)  # deterministic

        ds = nidus.load()
        """),
        md("""
        ## Inputs

        Two parameters describe maternal cardiac output across
        pregnancy. The dataset stores them as separate records, each
        with its own central value, low/high (1σ) bounds, units, tier,
        and citation chain.
        """),
        code("""
        baseline = ds["maternal_cardiovascular.baseline_cardiac_output_l_per_min"]
        peak_excess = ds["maternal_cardiovascular.peak_excess_cardiac_output_l_per_min"]

        for p in (baseline, peak_excess):
            print(f"{p.id}")
            print(f"  value:    {p.value.central} {p.value.units} (low {p.value.low}, high {p.value.high})")
            print(f"  tier:     {p.tier}")
            print(f"  citation: {p.primary_citation.key} (DOI: {p.primary_citation.doi})")
            print()
        """),
        md("""
        ## Point-estimate calculation

        The naïve sum of central values gives a single number with no
        information about uncertainty.
        """),
        code("""
        point_peak = baseline.value.central + peak_excess.value.central
        print(f"Point estimate of peak gestational CO: {point_peak:.2f} L/min")
        """),
        md("""
        ## Monte Carlo from low/high bounds

        Both source records have ``distribution = "normal"`` and store
        their bounds at one standard deviation (``ci = 0.683``). Drawing
        Gaussians with the appropriate mean and σ recovers the original
        distributions; the sum of two independent Gaussians is itself
        Gaussian.
        """),
        code("""
        def sample(p, n):
            assert p.value.distribution == "normal"
            sigma = (p.value.high - p.value.low) / 2  # one-sigma
            return rng.normal(p.value.central, sigma, size=n)

        N = 50_000
        baseline_samples = sample(baseline, N)
        peak_excess_samples = sample(peak_excess, N)
        peak_co = baseline_samples + peak_excess_samples

        print(f"Mean:  {peak_co.mean():.2f} L/min")
        print(f"Std:   {peak_co.std():.2f} L/min")
        q025, q975 = np.quantile(peak_co, [0.025, 0.975])
        print(f"95% CI: {q025:.2f} – {q975:.2f} L/min")
        """),
        md("## Visualise the propagated distribution"),
        code("""
        fig, ax = plt.subplots(figsize=(7, 3.5))
        ax.hist(peak_co, bins=60, alpha=0.7, color="#1f77b4", edgecolor="white")
        ax.axvline(point_peak, color="black", linestyle="--", linewidth=1, label=f"point estimate ({point_peak:.2f})")
        ax.axvline(q025, color="#d62728", linestyle=":", linewidth=1, label="95% CI bounds")
        ax.axvline(q975, color="#d62728", linestyle=":", linewidth=1)
        ax.set_xlabel("Peak gestational cardiac output (L/min)")
        ax.set_ylabel("Samples")
        ax.set_title("Monte Carlo composition: baseline + peak excess")
        ax.legend()
        plt.tight_layout()
        plt.show()
        """),
        md("""
        ## Tier propagation

        Both inputs are Tier B, so the derived quantity is Tier B too.
        The rule is conservative: a derived quantity cannot be
        better-supported than its weakest input.
        """),
        code("""
        TIER_ORDER = ["A", "B", "C", "D"]
        def propagate(*params):
            return max((p.tier for p in params), key=TIER_ORDER.index)

        derived_tier = propagate(baseline, peak_excess)
        print(f"baseline tier:     {baseline.tier}")
        print(f"peak_excess tier:  {peak_excess.tier}")
        print(f"derived tier:      {derived_tier}")
        """),
        md("""
        ## What this means

        - **Both inputs are Tier B.** Mahendru 2014 is the primary
          source; multiple cohort studies confirm the qualitative
          shape, but the framework treats the specific values as
          supported-but-not-confirmed.
        - **Distributions are one-sigma normal.** This matches how the
          source TOML encoded ``(mean, sd)``. A wider 95% CI
          interpretation would use ``± 1.96σ`` instead.
        - **Independence is assumed.** Real CO components are
          correlated (women with higher baselines tend to have larger
          absolute increases). The Monte Carlo assumes independence,
          which slightly overstates the spread.
        - **Mahendru 2014 is one cohort.** Replicating across cohorts
          would promote both inputs (and therefore the derived
          quantity) to Tier A.

        See the [Spec 03 blog essay outline](../docs/specs/v0.3/03-outreach-and-essay.md)
        for the longer narrative that this calculation supports.
        """),
    ]
    write_notebook("03_uncertainty_propagation.ipynb", cells)


# ========== 04 — Citation Provenance ================================


def build_04() -> None:
    cells = [
        md("""
        # Citation Provenance

        nidus exposes citations as first-class objects. This notebook
        explores the citation graph: which papers support which
        parameters, which papers are most load-bearing, and how to
        export the whole bibliography as BibTeX for use in a paper or
        thesis.
        """),
        md("## Setup"),
        code("""
        import nidus
        from collections import Counter

        ds = nidus.load()
        print(f"{len(ds.citations)} citations indexed")
        """),
        md("""
        ## Most load-bearing citations

        How many parameters in the dataset trace back to each paper?
        The top of this list shows which sources the dataset is most
        sensitive to — if any of these were retracted, a large fraction
        of nidus would need re-tiering.
        """),
        code("""
        uses = Counter(c.key for p in ds for c in p.citations)
        for key, n in uses.most_common(8):
            c = ds.citations[key]
            authors = ", ".join(c.authors[:2]) + (" et al." if len(c.authors) > 2 else "")
            print(f"  {n:>2} parameters  ·  {authors} ({c.year}) — {c.title[:70]}")
        """),
        md("## Inspect a single citation"),
        code("""
        c = ds.citations["mahendru-2014-cardiac-output"]
        print(f"Title:    {c.title}")
        print(f"Authors:  {', '.join(c.authors)}")
        print(f"Year:     {c.year}")
        print(f"Journal:  {c.journal}")
        print(f"DOI:      {c.doi}")
        print()
        print("Supports these parameters:")
        for p in ds.citations_for(c.key):
            primary = " (primary)" if p.primary_citation and p.primary_citation.key == c.key else ""
            print(f"  · [{p.tier}] {p.id}{primary}")
        """),
        md("""
        ## Citations without a resolvable identifier

        Most citations have a DOI or PMID. Older book references
        predate DOIs and are kept in the dataset for accuracy. The
        schema accepts them without an identifier; the weekly
        reachability check skips them rather than failing.
        """),
        code("""
        unresolved = [c for c in ds.citations.values() if not (c.doi or c.pmid or c.url)]
        for c in unresolved:
            print(f"  {c.key}  ({c.type})  — {c.title}")
        if not unresolved:
            print("  (none — every citation has at least one of DOI / PMID / URL)")
        """),
        md("## Export the whole bibliography as BibTeX"),
        code("""
        _BIBTEX_TYPE_MAP = {
            "journal-article": "article",
            "book": "book",
            "book-chapter": "incollection",
            "conference-paper": "inproceedings",
            "preprint": "misc",
            "report": "techreport",
            "dataset": "misc",
            "thesis": "phdthesis",
        }

        def to_bibtex(c):
            entry_type = _BIBTEX_TYPE_MAP.get(c.type, "misc")
            fields = []
            def add(name, value):
                if value not in (None, "", []):
                    fields.append(f"  {name} = {{{value}}}")
            add("title", c.title)
            add("author", " and ".join(c.authors))
            add("year", c.year)
            if entry_type == "article":
                add("journal", c.journal)
            else:
                add("publisher", c.publisher or c.journal)
            add("volume", c.volume)
            add("number", c.issue)
            add("pages", c.pages)
            add("doi", c.doi)
            add("pmid", c.pmid)
            add("url", c.url)
            add("isbn", c.isbn)
            return f"@{entry_type}{{{c.key},\\n" + ",\\n".join(fields) + "\\n}}"

        print(to_bibtex(ds.citations["mahendru-2014-cardiac-output"]))
        """),
        code("""
        # Full bibliography (truncated for display):
        bib = "\\n\\n".join(to_bibtex(c) for c in ds.citations.values())
        print(bib[:600] + "\\n...")
        print(f"\\n[full bibliography is {len(bib):,} characters across {len(ds.citations)} entries]")
        """),
        md("""
        The dashboard's Download page exposes the same BibTeX export as
        a single-click download. Both rely on the citation metadata
        encoded in ``dataset/citations/citations.json``.
        """),
    ]
    write_notebook("04_citation_provenance.ipynb", cells)


# ========== essay_figures ============================================


def build_essay_figures() -> None:
    cells = [
        md("""
        # Figures for the blog essay

        Generates the figures called out in the
        [Spec 03 outreach plan](../docs/specs/v0.3/03-outreach-and-essay.md).
        All output is seeded and deterministic; re-running produces
        byte-identical PNGs.

        Output directory: ``notebooks/figures/`` (gitignored). The
        maintainer re-runs this notebook before publishing the essay
        and copies the PNGs into the blog post manually.
        """),
        md("## Setup"),
        code("""
        from pathlib import Path
        from collections import Counter
        import numpy as np
        import matplotlib.pyplot as plt
        import nidus

        rng = np.random.default_rng(seed=20251101)

        FIGURES = Path("figures")
        FIGURES.mkdir(exist_ok=True)

        ds = nidus.load()
        """),
        md("""
        ## Figure 1 — Tier distribution by subsystem

        Stacked bar showing how the four tiers are distributed across
        the ten subsystems. The visual point: data density is uneven,
        and the tier system surfaces where the dataset is well-grounded
        versus where it is provisional.
        """),
        code("""
        SUBSYSTEMS = list(ds.subsystems())
        TIERS = ["A", "B", "C", "D"]
        COLORS = {"A": "#2ca02c", "B": "#1f77b4", "C": "#ff7f0e", "D": "#d62728"}

        counts = {(s, t): 0 for s in SUBSYSTEMS for t in TIERS}
        for p in ds:
            counts[(p.subsystem, p.tier)] += 1

        fig, ax = plt.subplots(figsize=(9, 5))
        bottoms = [0] * len(SUBSYSTEMS)
        for tier in TIERS:
            heights = [counts[(s, tier)] for s in SUBSYSTEMS]
            ax.barh(SUBSYSTEMS, heights, left=bottoms, color=COLORS[tier], label=f"Tier {tier}")
            bottoms = [b + h for b, h in zip(bottoms, heights)]

        ax.set_xlabel("Number of parameters")
        ax.set_title("Tier distribution by subsystem")
        ax.legend(loc="lower right")
        ax.invert_yaxis()
        plt.tight_layout()
        plt.savefig(FIGURES / "fig1_tier_distribution.png", dpi=180, bbox_inches="tight")
        plt.show()
        """),
        md("""
        ## Figure 2 — Worked-example timeline (Mahendru 2014)

        A diagram showing how a single peer-reviewed paper flows
        through nidus: original publication → parameter extraction →
        tier assignment → use in the dataset → exposure to dashboard
        and downstream computations.
        """),
        code("""
        fig, ax = plt.subplots(figsize=(11, 3))
        ax.set_xlim(0, 10)
        ax.set_ylim(0, 3)
        ax.axis("off")

        STAGES = [
            ("Mahendru et al.\\n2014\\n(J. Hypertension)", "#cdd9f0"),
            ("Extracted\\nvalues +\\ncontext", "#cdd9f0"),
            ("Tier B\\nassigned\\n(verified)", "#cde8d2"),
            ("Stored in\\ndataset/\\nparameters/", "#cdd9f0"),
            ("Resolved by\\nnidus.load()\\nfor downstream\\ncomputation", "#f0e3cd"),
        ]
        N = len(STAGES)
        margin = 0.4
        width = (10 - 2 * margin - (N - 1) * 0.4) / N

        for i, (label, color) in enumerate(STAGES):
            x = margin + i * (width + 0.4)
            ax.add_patch(plt.Rectangle((x, 0.8), width, 1.4, facecolor=color, edgecolor="#444"))
            ax.text(x + width / 2, 1.5, label, ha="center", va="center", fontsize=9)
            if i < N - 1:
                arrow_x = x + width + 0.05
                ax.annotate(
                    "", xy=(arrow_x + 0.3, 1.5), xytext=(arrow_x, 1.5),
                    arrowprops=dict(arrowstyle="->", color="#444", lw=1.4),
                )

        ax.text(5, 0.3, "Same model applies to every other Tier-A/B parameter in the dataset.",
                ha="center", fontsize=9, color="#666")
        ax.set_title("From paper to parameter to downstream use", pad=14)
        plt.tight_layout()
        plt.savefig(FIGURES / "fig2_worked_example_timeline.png", dpi=180, bbox_inches="tight")
        plt.show()
        """),
        md("""
        ## Figure 3 — Citation usage histogram

        How many parameters depend on each citation? The shape of this
        distribution tells you how concentrated the dataset's
        provenance is. A few load-bearing papers carry most of the
        weight; a long tail of supporting papers contribute one or two
        parameters each.

        Replaces the Spec-03 "dashboard screenshot" placeholder (the
        screenshot is captured manually from the running dashboard, not
        from this notebook).
        """),
        code("""
        uses = Counter(c.key for p in ds for c in p.citations)
        usage_counts = sorted(uses.values(), reverse=True)

        fig, ax = plt.subplots(figsize=(8, 4))
        ax.bar(range(len(usage_counts)), usage_counts, color="#1f77b4", edgecolor="white")
        ax.set_xlabel("Citation (sorted by usage)")
        ax.set_ylabel("Number of parameters citing this work")
        ax.set_title(f"Citation usage across {len(usage_counts)} cited works")
        ax.axhline(np.mean(usage_counts), color="#444", linestyle="--", linewidth=1,
                   label=f"mean = {np.mean(usage_counts):.1f}")
        ax.legend()
        plt.tight_layout()
        plt.savefig(FIGURES / "fig3_citation_usage_histogram.png", dpi=180, bbox_inches="tight")
        plt.show()
        """),
        md("""
        ## Done

        The three PNGs are now in ``notebooks/figures/`` and can be
        embedded in the blog essay. Re-run this notebook any time the
        dataset changes; the figures will update deterministically.
        """),
    ]
    write_notebook("essay_figures.ipynb", cells)


# ---- main ----------------------------------------------------------


def main() -> int:
    print(f"Writing notebooks to {OUT.relative_to(ROOT)}/")
    build_01()
    build_02()
    build_03()
    build_04()
    build_essay_figures()
    print(f"\nDone. {len(list(OUT.glob('*.ipynb')))} notebooks generated.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
