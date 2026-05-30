# Contributing

ChemLoop Studio is a portfolio-first scientific AI project. Contributions should keep the project reproducible, well-documented, and transparent.

## Development setup

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e ".[dev,app]"
pytest -q
```

## Contribution priorities

- Better sample datasets with clear provenance.
- Retrieval evaluation cases.
- Additional active-learning acquisition functions.
- Optional embedding and LLM adapters.
- Better Streamlit visualizations.
- Documentation that helps both AI and scientific reviewers.
