# ChemLoop Studio — interactive, human- & literature-informed Bayesian optimisation for materials experiments

ChemLoop Studio is a **web-based, interactive** research demo that showcases an *end-to-end* closed-loop workflow for
**AI/ML-driven chemical discovery**:

- **Closed-loop Bayesian optimisation (BO)** with uncertainty-aware experiment suggestion
- **Human-in-the-loop** controls (scientist can override constraints or accept/reject suggestions)
- **Literature-informed priors** (simple RAG-style retrieval using TF‑IDF over a small corpus + automatic range extraction)
- **Multi-objective exploration** (Pareto front visualisation + scalarised optimisation)
- **Robotics/API stub** (FastAPI endpoint to connect to a robot / scheduler)

> This repo is designed as a portfolio-grade demo for roles that require **algorithm development + accessible GUIs + clean software practices**.

---

## Quickstart

### 1) Create environment and install
```bash
python -m venv .venv
# Windows: .venv\Scripts\activate
source .venv/bin/activate

pip install -r requirements.txt
```

### 2) Run the interactive web app (Streamlit)
```bash
streamlit run app/Home.py
```

### 3) (Optional) Run the API stub (FastAPI)
In another terminal:
```bash
uvicorn mds.api:app --reload --port 8000
```

Then open:
- Streamlit UI: http://localhost:8501
- API docs: http://localhost:8000/docs

---

## What you can demo in 2 minutes

1. **Closed-loop BO:** propose a new electrospinning condition → simulate outcome → retrain GP → repeat  
2. **Literature priors:** search a small “papers” corpus → extract suggested voltage/concentration ranges → apply bounds  
3. **Multi-objective trade-offs:** explore a synthetic “porous material” problem → visualise Pareto front  
4. **Robotics bridge:** call `POST /suggest_next` to get the next experiment in JSON

---

## Architecture (high level)

```mermaid
flowchart LR
  U[Scientist] -->|preferences / constraints| GUI[Streamlit UI]
  GUI --> LIT[Literature Retriever]
  GUI --> BO[BO Engine (GP + acquisition)]
  LIT -->|ranges / priors| BO
  BO -->|next experiment| API[FastAPI stub]
  API --> LAB[Robot / Lab Scheduler]
  LAB -->|results| DB[Run history (CSV/JSON)]
  DB --> BO
```

---

## Repo layout

- `app/` — Streamlit UI (multi-page)
- `mds/` — core Python package: BO, simulators, literature, API
- `data/` — tiny example “literature” corpus (JSONL)
- `tests/` — minimal pytest tests
- `.github/workflows/` — CI template

---

## Extending to your own research

This repo is intentionally modular:

- Replace the toy simulator in `mds/simulator.py` with your own experimental model or a call to an instrument/robot queue.
- Replace TF‑IDF in `mds/literature.py` with embeddings + a vector DB (FAISS) and add a real LLM for extraction.
- Swap the BO core in `mds/bo.py` to **BoTorch** (qNEI/EHVI) when you want a publication-grade backend.

---

## Citation

If you build on this repository, please add/modify `CITATION.cff`.

---

## License

MIT — see `LICENSE`.
