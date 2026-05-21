"""MIRIAM and nidus annotation helpers for exported models.

Builds the RDF blocks that link an exported model's parameters back to
the cited primary literature (via `bqbiol:isDescribedBy` and
`identifiers.org` URIs) and to the nidus confidence-tier system (via
custom `nidus:` predicates).

The same RDF is embedded in SBML, CellML, and (where supported)
PhysioCell exports.
"""

from __future__ import annotations

from nidus.models import Citation, Parameter

NIDUS_ONTOLOGY = "https://github.com/clay-good/nidus/ontology#"
BQBIOL = "http://biomodels.net/biology-qualifiers/"
RDF_NS = "http://www.w3.org/1999/02/22-rdf-syntax-ns#"

# Lowest-tier propagation across multiple input parameters.
TIER_ORDER = {"A": 0, "B": 1, "C": 2, "D": 3}


def worst_tier(*tiers: str) -> str:
    """Return the worst (highest-letter) tier; the propagation rule."""
    return max(tiers, key=lambda t: TIER_ORDER.get(t, 99))


def identifiers_org_uri(citation: Citation) -> str | None:
    """Build the canonical identifiers.org URI for a citation."""
    if citation.doi:
        return f"https://identifiers.org/doi/{citation.doi}"
    if citation.pmid:
        return f"https://identifiers.org/pubmed/{citation.pmid}"
    if citation.url:
        return citation.url
    return None


def parameter_miriam_block(param: Parameter, indent: str = "    ") -> str:
    """RDF block for a single parameter, suitable for SBML <annotation>.

    Emits one `bqbiol:isDescribedBy` per resolvable citation, plus the
    full nidus tier / rationale / provenance predicate set.
    """
    citation_uris: list[str] = []
    for c in param.citations:
        uri = identifiers_org_uri(c)
        if uri:
            citation_uris.append(uri)

    rdf_lines = [
        f'{indent}<rdf:RDF xmlns:rdf="{RDF_NS}"',
        f'{indent}         xmlns:bqbiol="{BQBIOL}"',
        f'{indent}         xmlns:nidus="{NIDUS_ONTOLOGY}">',
        f'{indent}  <rdf:Description rdf:about="#{param.id.replace(".", "_")}">',
    ]
    for uri in citation_uris:
        rdf_lines.append(f'{indent}    <bqbiol:isDescribedBy rdf:resource="{uri}"/>')
    rdf_lines.append(f"{indent}    <nidus:confidenceTier>{param.tier}</nidus:confidenceTier>")
    rdf_lines.append(
        f"{indent}    <nidus:reviewStatus>{param.extraction.review_status}</nidus:reviewStatus>"
    )
    rdf_lines.append(f"{indent}    <nidus:datasetParameterId>{param.id}</nidus:datasetParameterId>")
    if param.tier_rationale:
        # Escape XML-special characters in the rationale text.
        esc = param.tier_rationale.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
        rdf_lines.append(f"{indent}    <nidus:tierRationale>{esc}</nidus:tierRationale>")
    if param.applicability and param.applicability.population:
        esc = (
            param.applicability.population.replace("&", "&amp;")
            .replace("<", "&lt;")
            .replace(">", "&gt;")
        )
        rdf_lines.append(
            f"{indent}    <nidus:applicabilityPopulation>{esc}</nidus:applicabilityPopulation>"
        )
    rdf_lines.append(f"{indent}  </rdf:Description>")
    rdf_lines.append(f"{indent}</rdf:RDF>")
    return "\n".join(rdf_lines)


def parameter_id_to_sbml(param_id: str) -> str:
    """SBML/CellML identifiers must start with a letter and use only
    [A-Za-z0-9_]. Map nidus dotted ids accordingly."""
    return param_id.replace(".", "_").replace("-", "_")
