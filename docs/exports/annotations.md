# Annotation reference

Every exported model carries three layers of annotation. The goal is
that the **citation chain** and the **nidus confidence-tier
discipline** survive the export so downstream consumers can trace any
value back to the primary literature and reason about its evidence
strength.

## Layer 1 — MIRIAM `bqbiol:isDescribedBy`

For every parameter that originates in a literature citation, an RDF
triple links the parameter to its citation's DOI and PMID via
[identifiers.org](https://identifiers.org) URIs.

```xml
<parameter id="cardiac_output_peak" value="1.55" units="L_per_min">
  <annotation>
    <rdf:RDF xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#"
             xmlns:bqbiol="http://biomodels.net/biology-qualifiers/">
      <rdf:Description rdf:about="#cardiac_output_peak">
        <bqbiol:isDescribedBy rdf:resource="https://identifiers.org/doi/10.1097/hjh.0000000000000090"/>
        <bqbiol:isDescribedBy rdf:resource="https://identifiers.org/pubmed/24406777"/>
      </rdf:Description>
    </rdf:RDF>
  </annotation>
</parameter>
```

These links remain valid even if downstream tools strip the
nidus-specific predicates below. The citation chain is the durable
layer.

## Layer 2 — Systems Biology Ontology (SBO)

Each submodel is tagged with the SBO term that names its kinetic
form, so a downstream tool can recognise the equation type without
having to parse the MathML:

| Submodel family                                  | SBO term                                                              |
| ------------------------------------------------ | --------------------------------------------------------------------- |
| Logistic growth                                  | [SBO:0000295](https://www.ebi.ac.uk/sbo/main/SBO:0000295) — logistic equation |
| Michaelis–Menten kinetics                        | [SBO:0000028](https://www.ebi.ac.uk/sbo/main/SBO:0000028)             |
| Hill function (e.g. O₂-Hb dissociation)          | [SBO:0000192](https://www.ebi.ac.uk/sbo/main/SBO:0000192)             |
| Algebraic / boundary-condition relationships     | [SBO:0000412](https://www.ebi.ac.uk/sbo/main/SBO:0000412)             |

## Layer 3 — `nidus:` predicates

Predicates under the namespace
`https://github.com/clay-good/nidus/ontology#` capture nidus-specific
semantics that SBO + MIRIAM cannot express on their own.

| Predicate                          | Object type                                              | Used on                                                |
| ---------------------------------- | -------------------------------------------------------- | ------------------------------------------------------ |
| `nidus:confidenceTier`             | Literal: `"A"` / `"B"` / `"C"` / `"D"`                   | Every annotated parameter                              |
| `nidus:tierRationale`              | Literal string                                           | Every annotated parameter                              |
| `nidus:datasetParameterId`         | Literal string (dotted id)                               | Round-trip identifier back to the JSON dataset         |
| `nidus:datasetVersion`             | Literal string (semver)                                  | Top-level model annotation                             |
| `nidus:reviewStatus`               | Literal: `"unverified"` / `"verified"` / `"contested"` / `"hypothesis-only"` | Per parameter                              |
| `nidus:applicabilityPopulation`    | Literal string                                           | Where the dataset specifies an applicability block      |
| `nidus:trajectoryValidRangeWeeks`  | List of two numbers                                      | On parameters with bounded gestational windows         |
| `nidus:couplingType`               | Literal: `"mechanistic"` / `"empirical"` / `"sequential"` | Edges in the top-level composed pregnancy model        |
| `nidus:couplingNotes`              | Literal string                                           | Prose justification for non-trivial composed couplings |

The vocabulary is defined in Turtle at
[`dataset/jsonld/ontology.ttl`](https://github.com/clay-good/nidus/blob/main/dataset/jsonld/ontology.ttl).
A formal OWL 2 release for BioPortal is deferred to post-v0.4.

## Hypothesis-only submodels

Phase C entries (currently four: maternal–fetal IgG transfer,
placental cortisol gradient, maternal microchimerism trajectory, fetal
pulmonary fluid trajectory) carry:

- `nidus:reviewStatus = "hypothesis-only"`,
- a "DO NOT USE FOR PREDICTION" string in the SBML/CellML `<notes>`
  block,
- the canonical citation that motivates the open question.

The export is for *research-question* purposes — it makes the open
question explicit rather than promising quantitative output.

## Tier propagation

In a composed model, the downstream observable's tier is the **minimum
tier of its inputs**, further degraded when an edge is `"empirical"`
or `"sequential"` rather than `"mechanistic"`. This rule is documented
on the composed model's top-level annotation; downstream simulators
can re-derive the propagation manually from the per-parameter tier
annotations.

A formal annotation predicate that *encodes* the propagation rule is
deferred to a future spec.
