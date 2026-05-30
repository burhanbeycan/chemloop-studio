# ChemLoop Studio

**ChemLoop Studio** is a publishable AI-for-science portfolio project: a self-auditing retrieval and experiment-planning workbench for polymer and materials R&D.

It is designed to show a broad applied-AI skill set while using polymer chemistry and materials science as a domain advantage. The project combines:

- citation-aware scientific retrieval,
- transparent evidence cards,
- uncertainty/risk flags,
- lightweight active-learning style experiment selection,
- a FastAPI service,
- a Streamlit demo,
- tests and CI.

> Portfolio positioning: **Applied AI / Machine Learning Researcher with PhD-level scientific R&D expertise**.

## Why this project is novel enough for your GitHub

Most portfolio RAG demos only answer questions. ChemLoop Studio goes further by connecting literature-style retrieval to an R&D decision loop:

1. Retrieve relevant polymer/materials evidence.
2. Build an answer with explicit source snippets.
3. Score evidence quality and uncertainty.
4. Recommend the next experiment using a surrogate model and expected-improvement logic.
5. Produce a reproducible project report that can be reviewed by both AI and science audiences.

The first release uses transparent classical ML and extractive retrieval so the project is reproducible without paid LLM APIs. The architecture is ready for optional LLM, embedding, and lab-automation integrations later.

## Demo use case

Question:

```text
Which electrospinning variables are likely to reduce nanofiber diameter while preserving antimicrobial surface functionality?
```

The system retrieves evidence from the included sample corpus, generates citation-grounded notes, estimates uncertainty, and suggests the next experiment from a candidate design table.

## Repository structure

```text
chemloop-studio/
├── src/chemloop_studio/
│   ├── cli.py                  # Command-line interface
│   ├── corpus.py               # Corpus loading and document models
│   ├── evaluation.py           # Retrieval and evidence quality metrics
│   ├── experiment.py           # Active-learning style experiment planner
│   ├── models.py               # Shared dataclasses
│   ├── retrieval.py            # TF-IDF retriever and answer builder
│   └── reporting.py            # Markdown report generation
├── app.py                      # Streamlit demo
├── api.py                      # FastAPI service
├── data/
│   ├── sample_papers.jsonl     # Small literature-style sample corpus
│   └── sample_experiments.csv  # Candidate experiment table
├── examples/
│   └── quickstart.py           # Minimal Python example
├── tests/                      # Unit tests
├── docs/                       # Project brief, data card, roadmap
└── .github/workflows/ci.yml    # GitHub Actions CI
```

## Quick start

```bash
git clone https://github.com/burhanbeycan/chemloop-studio.git
cd chemloop-studio
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -e ".[dev,app]"
```

Run the retrieval + planning demo:

```bash
chemloop ask "How can electrospinning parameters reduce fiber diameter and improve antimicrobial fabric performance?"
```

Create a Markdown report:

```bash
chemloop report \
  --question "Which formulation should be tried next for thin antimicrobial nanofibers?" \
  --output reports/demo-report.md
```

Run the API:

```bash
uvicorn api:app --reload
```

Run the Streamlit app:

```bash
streamlit run app.py
```

Run tests:

```bash
pytest -q
```

## What reviewers should look for

This repository is meant to demonstrate:

- clean Python packaging,
- retrieval systems and evidence ranking,
- evaluation mindset,
- API and UI deployment readiness,
- experiment-design reasoning,
- scientific communication and limitations.

## Example CLI output

```text
Answer summary
- Lower polymer concentration, optimized voltage, and controlled flow rate are repeatedly linked to thinner fibers.
- PEI or cationic additives can support antimicrobial behavior, but cytocompatibility must be checked.
- The next experiment should explore a moderate voltage and low flow rate region with a formulation that preserves film integrity.

Evidence quality: medium-high
Uncertainty flags: limited sample corpus, no wet-lab validation, extrapolation risk
```

## Limitations

The included data are small demonstration datasets. They are not a substitute for a systematic literature review, validated material database, or wet-lab confirmation. The project is intentionally built so stronger datasets, embeddings, and LLMs can be added later.

## Roadmap

See [`docs/ROADMAP.md`](docs/ROADMAP.md).

## Citation

If you reuse this project structure, cite it using [`CITATION.cff`](CITATION.cff).

## License

MIT License.
