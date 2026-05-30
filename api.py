"""FastAPI app for ChemLoop Studio."""

from __future__ import annotations

from fastapi import FastAPI
from pydantic import BaseModel, Field

from chemloop_studio.corpus import load_corpus
from chemloop_studio.experiment import load_experiments, recommend_next_experiment
from chemloop_studio.retrieval import ChemLoopRetriever

app = FastAPI(
    title="ChemLoop Studio API",
    description="Citation-aware retrieval and experiment planning for polymer/materials R&D.",
    version="0.1.0",
)

_documents = load_corpus()
_retriever = ChemLoopRetriever(_documents)
_experiments = load_experiments()


class AskRequest(BaseModel):
    question: str = Field(..., min_length=5)
    top_k: int = Field(4, ge=1, le=8)


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.post("/ask")
def ask(request: AskRequest) -> dict[str, object]:
    answer = _retriever.answer(request.question, top_k=request.top_k)
    recommendation = recommend_next_experiment(_experiments)

    return {
        "question": answer.question,
        "summary": answer.summary,
        "quality_score": answer.quality_score,
        "uncertainty_flags": list(answer.uncertainty_flags),
        "evidence": [
            {
                "doc_id": item.doc.doc_id,
                "citation": item.doc.citation,
                "score": item.score,
                "snippet": item.snippet,
            }
            for item in answer.evidence
        ],
        "recommendation": {
            "experiment_id": recommendation.experiment_id,
            "predicted_score": recommendation.predicted_score,
            "expected_improvement": recommendation.expected_improvement,
            "uncertainty": recommendation.uncertainty,
            "rationale": recommendation.rationale,
            "variables": recommendation.variables,
        },
    }
