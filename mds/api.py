from __future__ import annotations

from typing import List

import numpy as np
from fastapi import FastAPI
from pydantic import BaseModel, Field

from mds.bo import fit_gp, suggest_next


app = FastAPI(title="ChemLoop Studio API", version="0.1.0")


class SuggestNextRequest(BaseModel):
    X: List[List[float]] = Field(..., description="Previous experiment inputs (n x d)")
    y: List[float] = Field(..., description="Observed objective values (n)")
    bounds: List[List[float]] = Field(..., description="Bounds (d x 2)")
    xi: float = Field(0.01, description="EI exploration parameter")
    n_candidates: int = Field(2000, description="Number of random candidates")


class SuggestNextResponse(BaseModel):
    x_next: List[float]
    predicted_mean: float
    predicted_std: float
    notes: str


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/suggest_next", response_model=SuggestNextResponse)
def suggest_next_endpoint(req: SuggestNextRequest):
    X = np.asarray(req.X, dtype=float)
    y = np.asarray(req.y, dtype=float)
    bounds = np.asarray(req.bounds, dtype=float)

    gp = fit_gp(X, y)
    y_best = float(np.min(y))
    x_next, meta = suggest_next(bounds, gp, y_best=y_best, xi=float(req.xi), n_candidates=int(req.n_candidates), random_state=0)

    return SuggestNextResponse(
        x_next=[float(v) for v in x_next],
        predicted_mean=float(meta["predicted_mean"]),
        predicted_std=float(meta["predicted_std"]),
        notes="Use this JSON in your robot scheduler as the next experiment.",
    )
