# Spec 02 — SBML / CellML Export (CONDITIONAL)

> **Status: CONDITIONAL — DO NOT START YET.**
>
> Only execute this spec if **all three** of the following are true ~3 months after Spec 01 ships:
> 1. The dataset has been downloaded or installed by ≥1 external party (PyPI stats, GitHub clones, issues).
> 2. At least one external user has asked about interop with CellML / SBML / BioModels / Physiome.
> 3. Spec 01 is stable — no major schema churn in the prior month.
>
> If those signals don't appear, this spec stays deferred indefinitely. That is a successful outcome — it means the dataset alone is sufficient.

**Depends on:** Spec 01 complete and `v0.3.0` shipped.
**Target release (if executed):** `v0.4.0`.

---

## 1. Goal

Generate SBML and CellML model files from the nidus dataset for the small set of submodels that are mechanistic enough to express in those formats. Annotate them with citations (MIRIAM) and tier metadata. Submit to BioModels Database and Physiome Model Repository so the curated work is discoverable to physiologists who already use those repositories.

This is interop, not a new feature. The goal is to get the work into the places where physiological modellers already look.

## 2. What we are doing (if triggered)

1. **Write SBML generators** for ~6 submodels in Python using `python-libsbml`.
2. **Write CellML generators** for the same submodels using `libcellml`.
3. **Annotate** each model with MIRIAM `bqbiol:isDescribedBy` links to DOIs and a custom `nidus:confidenceTier` RDF predicate.
4. **Bundle** as COMBINE archives (`.omex`).
5. **Validate** via round-trip simulation (tellurium for SBML, libcellml solver for CellML) against pure-NumPy reference.
6. **Submit** to BioModels Database (SBML) and Physiome Model Repository (CellML).

## 3. What we are NOT doing

| Not doing                                          | Why                                                                |
| -------------------------------------------------- | ------------------------------------------------------------------ |
| New biology to make more models exportable         | Out of scope. Export only what already exists.                     |
| Replacing CellML / COPASI / tellurium tooling      | Out of scope.                                                      |
| Standalone CellML editor / GUI                     | Out of scope. The export pipeline is CLI only.                     |
| Submitting models that misrepresent confidence     | Tier metadata is required on every parameter export.              |

## 4. Honest inventory of exportable submodels

From the nidus dataset:

| Submodel                                | Mathematical form                          | Tier | Notes                                |
| --------------------------------------- | ------------------------------------------ | ---- | ------------------------------------ |
| Placental surface-area growth           | dA/dt = r·A·(1 − A/K)                     | B    | True ODE. Exports cleanly.           |
| Maternal cardiac output trajectory      | CO(t) = baseline + A·exp(−((t−μ)/σ)²)    | B    | Fitted curve. Algebraic rule.        |
| Maternal MAP trajectory                 | Piecewise polynomial                       | B    | Algebraic rule.                      |
| Uterine artery flow trajectory          | Q(t) = baseline · exp(k·t)                | C    | Algebraic rule.                      |
| Placental glucose transport             | V = V_max · [S] / (K_m + [S])             | B    | Genuine kinetic. Exports cleanly.    |
| Venous-equilibrator O₂ exchange         | Algebraic equilibrium                      | C    | Simplified.                          |

**Total: 6 submodels.** Be modest in framing: "Curated submodels of human gestational physiology," not "A model of pregnancy."

Not exportable:
- Fetal shunt routing — discrete logic, not a flow equation.
- The confidence-tier framework itself — described in the Spec 03 blog essay; only *referenced* via SBML annotation.
- Tier D entries — by definition unmodelled.

## 5. Format choices

| Format              | When                                                | Why                                       |
| ------------------- | --------------------------------------------------- | ----------------------------------------- |
| SBML L3v2 + `comp`  | Primary export → BioModels submission.              | Widest support; rich annotation.          |
| CellML 2.0          | Secondary export → Physiome Model Repository.       | Native format for Physiome.               |
| SED-ML              | Wraps simulation experiments alongside each model.  | Required by BioModels for reproducibility.|
| COMBINE archive     | `.omex` bundles SBML + CellML + SED-ML + metadata.  | Single-file distribution.                 |

## 6. Tooling

All Python. No new languages.

- `python-libsbml` — SBML generation + validation.
- `libcellml` Python bindings — CellML 2.0 generation + validation.
- `pyomexmeta` (or equivalent) — MIRIAM RDF annotations.
- `tellurium` — round-trip simulation testing.
- `combine-archive` — `.omex` packaging.

## 7. Pipeline

```
dataset/*.json
        │
        ▼
python/nidus/export/sbml.py     # one function per submodel
python/nidus/export/cellml.py
python/nidus/export/annotate.py
python/nidus/export/sedml.py
python/nidus/export/combine.py
        │
        ▼
exports/sbml/*.xml
exports/cellml/*.cellml
exports/combine/*.omex
```

CLI: `nidus export --format sbml --output exports/sbml/`.

Each generator is a pure function. Outputs are byte-stable for a frozen dataset version (tested in CI).

## 8. Annotation strategy

```xml
<parameter id="cardiac_output_peak" value="1.55" units="L_per_min">
  <annotation>
    <rdf:RDF xmlns:bqbiol="http://biomodels.net/biology-qualifiers/"
             xmlns:nidus="https://github.com/claygood/nidus/ontology#">
      <rdf:Description rdf:about="#cardiac_output_peak">
        <bqbiol:isDescribedBy rdf:resource="https://identifiers.org/doi/10.1097/HJH.0000000000000090"/>
        <bqbiol:isDescribedBy rdf:resource="https://identifiers.org/pubmed/24406777"/>
        <nidus:confidenceTier>B</nidus:confidenceTier>
        <nidus:datasetParameterId>maternal.cardio.cardiac_output.peak_amplitude</nidus:datasetParameterId>
        <nidus:datasetVersion>0.3.0</nidus:datasetVersion>
      </rdf:Description>
    </rdf:RDF>
  </annotation>
</parameter>
```

Custom predicates documented in `dataset/jsonld/ontology.ttl`.

## 9. Validation

Three layers:

1. **Static** — libSBML / libcellml consistency checks; 0 errors required.
2. **Round-trip simulation** — load SBML/CellML, simulate 8–40 weeks, compare against pure-NumPy reference. Tolerance: 1e-6 relative (algebraic), 1e-4 (ODE).
3. **MIRIAM compliance** — all `bqbiol:isDescribedBy` URIs resolve.

## 10. Submission targets

### BioModels Database (EMBL-EBI)
- Submit SBML + COMBINE archive via portal.
- Curator review: 4–8 weeks typical.
- Accession: `BIOMD0000000XXX`.

### Physiome Model Repository (Auckland)
- Self-publish via workspace + exposure.
- 1–4 weeks; optional formal curation later.

Submit to both. Different audiences.

## 11. Deliverables (if triggered)

- `python/nidus/export/` module.
- `exports/sbml/`, `exports/cellml/`, `exports/combine/`, `exports/sedml/`.
- `nidus export` CLI.
- CI regenerates exports on dataset changes; PRs fail if exports stale.
- `docs/exports.md` with submission status and accessions.

## 12. Success criteria (if triggered)

- [ ] All 6 submodels exported to both formats; pass static validation.
- [ ] Round-trip simulation agrees with reference to tolerance.
- [ ] MIRIAM + tier annotations present and validated.
- [ ] COMBINE archives generated.
- [ ] BioModels submission *submitted*.
- [ ] Physiome workspace *created and exposed*.

## 13. Why this is conditional and not active

Most likely outcome of shipping Spec 01 alone is a small, slow-growing audience. Building SBML/CellML exports before there is demand wastes 4–6 weeks of solo-dev time on an artifact that may have zero users. The cost of waiting is small: the dataset format is stable, generation can be done later without breaking anything. The cost of building eagerly is real.

Defer until there is a signal that demand exists.
