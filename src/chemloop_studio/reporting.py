"""Markdown reporting utilities."""

from __future__ import annotations

from .models import Answer, ExperimentRecommendation


def build_markdown_report(answer: Answer, recommendation: ExperimentRecommendation) -> str:
    """Create a reviewer-friendly Markdown report."""

    evidence_lines = []
    for item in answer.evidence:
        evidence_lines.append(
            f"- **{item.doc.doc_id}** — {item.doc.citation}, score={item.score:.3f}: "
            f"{item.snippet}"
        )

    variable_lines = [f"- `{key}`: {value}" for key, value in recommendation.variables.items()]

    return f"""# ChemLoop Studio Report

## Question

{answer.question}

## Citation-grounded answer

{answer.summary}

## Evidence quality

- Quality score: `{answer.quality_score}`
- Uncertainty flags: `{", ".join(answer.uncertainty_flags)}`

## Retrieved evidence

{chr(10).join(evidence_lines)}

## Suggested next experiment

- Experiment ID: `{recommendation.experiment_id}`
- Predicted score: `{recommendation.predicted_score}`
- Expected improvement: `{recommendation.expected_improvement}`
- Model uncertainty: `{recommendation.uncertainty}`

### Variables

{chr(10).join(variable_lines)}

### Rationale

{recommendation.rationale}

## Scientific caution

This report is generated from a small demonstration corpus and a lightweight surrogate model.
It should be treated as a reproducible AI workflow example, not as validated experimental advice.
"""
