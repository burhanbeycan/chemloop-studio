"""Shared data models for ChemLoop Studio."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass(frozen=True)
class Document:
    """A literature-style document chunk used for retrieval."""

    doc_id: str
    title: str
    source: str
    year: int
    text: str
    tags: tuple[str, ...] = field(default_factory=tuple)
    metadata: dict[str, Any] = field(default_factory=dict)

    @property
    def citation(self) -> str:
        return f"{self.title} ({self.year})"


@dataclass(frozen=True)
class Evidence:
    """Retrieved evidence snippet with a relevance score."""

    doc: Document
    score: float
    snippet: str


@dataclass(frozen=True)
class Answer:
    """Citation-grounded answer produced from retrieved evidence."""

    question: str
    summary: str
    evidence: tuple[Evidence, ...]
    quality_score: float
    uncertainty_flags: tuple[str, ...]
    suggested_next_step: str


@dataclass(frozen=True)
class ExperimentRecommendation:
    """Recommendation returned by the experiment planner."""

    experiment_id: str
    expected_improvement: float
    predicted_score: float
    uncertainty: float
    rationale: str
    variables: dict[str, Any]
