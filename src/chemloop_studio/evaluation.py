"""Evaluation helpers for evidence and retrieval quality."""

from __future__ import annotations

import math

from .models import Evidence


def evidence_quality_score(evidence: tuple[Evidence, ...] | list[Evidence]) -> float:
    """Return a 0-1 evidence quality score.

    The score rewards high relevance, multiple sources, and source diversity.
    It is not a truth score; it is a reviewer-friendly diagnostic.
    """

    if not evidence:
        return 0.0

    scores = [max(0.0, item.score) for item in evidence]
    mean_relevance = sum(scores) / len(scores)
    unique_sources = len({item.doc.source for item in evidence})
    source_diversity = min(1.0, unique_sources / max(1, len(evidence)))
    nonzero_fraction = sum(score > 0.01 for score in scores) / len(scores)

    quality = 0.55 * min(1.0, mean_relevance * 3.0) + 0.30 * source_diversity + 0.15 * nonzero_fraction
    return round(float(quality), 3)


def uncertainty_flags(evidence: tuple[Evidence, ...] | list[Evidence]) -> list[str]:
    """Return human-readable uncertainty flags for an answer."""

    flags: list[str] = []
    if len(evidence) < 3:
        flags.append("few_retrieved_sources")

    if evidence:
        sources = {item.doc.source for item in evidence}
        if len(sources) == 1:
            flags.append("single_source_family")

        scores = [item.score for item in evidence]
        if max(scores) < 0.08:
            flags.append("weak_query_match")
        if len(scores) > 1 and _std(scores) > 0.20:
            flags.append("score_dispersion")

    flags.append("requires_experimental_validation")
    return flags


def retrieval_hit_rate(retrieved_doc_ids: list[str], expected_doc_ids: set[str]) -> float:
    """Compute the fraction of expected document IDs appearing in retrieved results."""

    if not expected_doc_ids:
        raise ValueError("expected_doc_ids cannot be empty.")
    retrieved = set(retrieved_doc_ids)
    return len(retrieved & expected_doc_ids) / len(expected_doc_ids)


def _std(values: list[float]) -> float:
    mean = sum(values) / len(values)
    return math.sqrt(sum((value - mean) ** 2 for value in values) / len(values))
