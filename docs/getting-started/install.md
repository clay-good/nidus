# Install

```bash
pip install nidus
```

Requires **Python 3.10 or newer**. Pure Python; no compiled extensions, no system dependencies.

## Optional extras

- `pip install "nidus[plot]"` — adds matplotlib for plotting helpers.

## Verify the install

From Python:

```python
import nidus

ds = nidus.load()
print(ds)
# <nidus.Dataset: 243 parameters, 66 citations>

nidus.validate()  # raises ValidationError on any schema mismatch
```

Or from the shell — the package ships a `nidus` console script:

```bash
nidus version
nidus validate
nidus info
nidus info --subsystem maternal_cardiovascular
```

## Run the dashboard locally

```bash
pip install streamlit
streamlit run https://raw.githubusercontent.com/clay-good/nidus/main/dashboard/app.py
```

Or clone the repo and run it from source:

```bash
git clone https://github.com/clay-good/nidus
cd nidus
streamlit run dashboard/app.py
```

## Development install

```bash
git clone https://github.com/clay-good/nidus
cd nidus
pip install -e python/[dev]
```

That single command pulls in everything CI uses: `pytest`, `mypy`, `ruff`, `nbmake`, `streamlit`, `matplotlib`, `jupyter`, `types-jsonschema`, `build`. After it, the full CI sweep runs locally:

```bash
ruff check python/ dashboard/ scripts/
ruff format --check python/ dashboard/ scripts/
mypy python/nidus
pytest python/tests/
pytest --nbmake notebooks/
```
