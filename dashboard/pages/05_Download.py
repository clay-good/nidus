"""Download — dataset ZIP, per-subsystem JSON, BibTeX, mechanistic-model exports."""

from __future__ import annotations

import io
import tempfile
import zipfile
from pathlib import Path
from typing import Any

import streamlit as st

from utils import REPO_URL, get_dataset

st.set_page_config(page_title="Download · Nidus", layout="wide")
st.title("Download")

ds = get_dataset()

st.markdown(
    "The dataset is freely redistributable under **CC-BY-4.0**. Code "
    "(this dashboard, the Python package, schemas, tooling) is **MIT**. "
    f"Please cite the Zenodo DOI on the [repository]({REPO_URL}) in any "
    "work that uses the dataset."
)

# Locate the bundled dataset on disk.
from nidus.load import _default_dataset_dir  # noqa: E402

ds_root = _default_dataset_dir()

# ---- Full dataset ZIP ----------------------------------------------


@st.cache_data
def make_dataset_zip() -> bytes:
    buf = io.BytesIO()
    with zipfile.ZipFile(buf, "w", zipfile.ZIP_DEFLATED) as zf:
        for fp in sorted(ds_root.rglob("*")):
            if fp.is_file() and not fp.name.startswith("."):
                zf.write(fp, fp.relative_to(ds_root.parent))
    return buf.getvalue()


st.subheader("Full dataset")
st.download_button(
    label="nidus-dataset.zip",
    data=make_dataset_zip(),
    file_name="nidus-dataset.zip",
    mime="application/zip",
)
st.caption(
    "Contains: parameters/, citations/, tiers/, schema/, jsonld/, "
    "DATASET.md, CHANGELOG.md."
)

# ---- Per-subsystem JSON --------------------------------------------

st.subheader("Per-subsystem JSON")
subsystems = list(ds.subsystems())
cols = st.columns(2)
for i, sub in enumerate(subsystems):
    sub_path = ds_root / "parameters" / f"{sub}.json"
    if sub_path.exists():
        with cols[i % 2]:
            st.download_button(
                label=f"{sub}.json",
                data=sub_path.read_bytes(),
                file_name=f"{sub}.json",
                mime="application/json",
                key=f"dl_{sub}",
            )

# ---- Citations as JSON and BibTeX ----------------------------------

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


def _bibtex_field(name: str, value: Any) -> str:
    if value in (None, "", []):
        return ""
    return f"  {name} = {{{value}}}"


def _to_bibtex(c) -> str:  # noqa: ANN001 — nidus.Citation, kept loose
    entry_type = _BIBTEX_TYPE_MAP.get(c.type, "misc")
    fields = [
        _bibtex_field("title", c.title),
        _bibtex_field("author", " and ".join(c.authors)),
        _bibtex_field("year", c.year),
    ]
    if entry_type == "article":
        fields.append(_bibtex_field("journal", c.journal))
    else:
        fields.append(_bibtex_field("publisher", c.publisher or c.journal))
    for name, attr in [
        ("volume", c.volume),
        ("number", c.issue),
        ("pages", c.pages),
        ("doi", c.doi),
        ("pmid", c.pmid),
        ("url", c.url),
        ("isbn", c.isbn),
    ]:
        fields.append(_bibtex_field(name, attr))
    body = ",\n".join(f for f in fields if f)
    return f"@{entry_type}{{{c.key},\n{body}\n}}"


@st.cache_data
def make_bibtex() -> bytes:
    return ("\n\n".join(_to_bibtex(c) for c in ds.citations.values()) + "\n").encode()


st.subheader("Citations")
c1, c2 = st.columns(2)
with c1:
    st.download_button(
        label="citations.json",
        data=(ds_root / "citations" / "citations.json").read_bytes(),
        file_name="citations.json",
        mime="application/json",
    )
with c2:
    st.download_button(
        label="nidus-citations.bib",
        data=make_bibtex(),
        file_name="nidus-citations.bib",
        mime="text/plain",
    )

# ---- Tier definitions ----------------------------------------------

st.subheader("Tier definitions")
st.download_button(
    label="tiers.json",
    data=(ds_root / "tiers" / "tiers.json").read_bytes(),
    file_name="tiers.json",
    mime="application/json",
)

# ---- Schemas -------------------------------------------------------

st.subheader("JSON Schemas")
schema_cols = st.columns(3)
for i, name in enumerate(["parameter", "citation", "tier"]):
    schema_path = ds_root / "schema" / f"{name}.schema.json"
    if schema_path.exists():
        with schema_cols[i]:
            st.download_button(
                label=f"{name}.schema.json",
                data=schema_path.read_bytes(),
                file_name=f"{name}.schema.json",
                mime="application/json",
                key=f"schema_{name}",
            )

# ---- Mechanistic-modeling exports ----------------------------------
# Spec 00 v0.4: "the Streamlit dashboard gains a 'Download as model'
# section but the existing pages stay."

st.subheader("Download as model")
st.markdown(
    "Nidus parameters are wired into **mechanistic submodels** that "
    "export to the three formats the systems-biology and "
    "physiological-modelling communities already use: **SBML L3v2**, "
    "**CellML 2.0**, and **PhysioCell** `<user_parameters>`. Each "
    "submodel below carries the worst-tier of its inputs as a MIRIAM "
    "annotation so downstream consumers can see the confidence chain."
)

from nidus.export import (  # noqa: E402
    SUBMODELS,
    build_cellml,
    build_sbml,
    build_sedml,
    write_combine_archive,
)


@st.cache_data
def _build_sbml_str(submodel_id: str) -> str:
    return build_sbml(ds, submodel_id)


@st.cache_data
def _build_cellml_str(submodel_id: str) -> str:
    return build_cellml(ds, submodel_id)


@st.cache_data
def _build_sedml_str(submodel_id: str) -> str | None:
    return build_sedml(ds, submodel_id)


@st.cache_data
def _build_combine_archive_bytes() -> bytes:
    with tempfile.TemporaryDirectory() as tmp:
        out = write_combine_archive(ds, Path(tmp) / "nidus.omex")
        return out.read_bytes()


submodel_options = {f"{sm.name} ({sm.id})": sm.id for sm in SUBMODELS}
chosen_label = st.selectbox(
    "Submodel",
    options=list(submodel_options.keys()),
    help="41 mechanistic submodels covering CO trajectory, growth curves, "
    "endocrine kinetics, gas exchange, glucose transport, and more.",
)
chosen_id = submodel_options[chosen_label]
chosen_sm = next(sm for sm in SUBMODELS if sm.id == chosen_id)
st.caption(
    f"Inputs: {len(chosen_sm.parameter_ids)} parameters; "
    f"independent variable: `{chosen_sm.independent_variable or 'algebraic'}`; "
    f"output units: `{chosen_sm.output_units or 'unspecified'}`."
)

c1, c2, c3 = st.columns(3)
with c1:
    st.download_button(
        label="SBML L3v2 (.xml)",
        data=_build_sbml_str(chosen_id).encode(),
        file_name=f"{chosen_id}.xml",
        mime="application/xml",
        key=f"dl_sbml_{chosen_id}",
    )
with c2:
    st.download_button(
        label="CellML 2.0 (.cellml)",
        data=_build_cellml_str(chosen_id).encode(),
        file_name=f"{chosen_id}.cellml",
        mime="application/xml",
        key=f"dl_cellml_{chosen_id}",
    )
with c3:
    sedml_str = _build_sedml_str(chosen_id)
    if sedml_str is not None:
        st.download_button(
            label="SED-ML (.sedml)",
            data=sedml_str.encode(),
            file_name=f"{chosen_id}.sedml",
            mime="application/xml",
            key=f"dl_sedml_{chosen_id}",
        )
    else:
        st.caption(
            "SED-ML: not applicable (algebraic submodel — independent variable is not time)"
        )

st.markdown(
    "**Full bundle.** A single COMBINE archive (`.omex`) packs every submodel as SBML + CellML + SED-ML, the composed pregnancy SBML, the PhysioCell parameters XML, and a provenance metadata RDF."
)
st.download_button(
    label="nidus-models.omex (full COMBINE archive)",
    data=_build_combine_archive_bytes(),
    file_name="nidus-models.omex",
    mime="application/zip",
    key="dl_combine_omex",
)
