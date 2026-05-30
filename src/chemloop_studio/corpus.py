"""Corpus loading utilities."""

from __future__ import annotations

import json
from pathlib import Path

from .models import Document


DEFAULT_CORPUS_PATH = Path(__file__).resolve().parents[2] / "data" / "sample_papers.jsonl"


def load_corpus(path: str | Path = DEFAULT_CORPUS_PATH) -> list[Document]:
    """Load a JSONL corpus into Document objects.

    Each JSON line must contain: doc_id, title, source, year, text, and optionally tags.
    """

    corpus_path = Path(path)
    if not corpus_path.exists():
        raise FileNotFoundError(f"Corpus file not found: {corpus_path}")

    documents: list[Document] = []
    with corpus_path.open("r", encoding="utf-8") as handle:
        for line_number, line in enumerate(handle, start=1):
            if not line.strip():
                continue
            payload = json.loads(line)
            try:
                documents.append(
                    Document(
                        doc_id=str(payload["doc_id"]),
                        title=str(payload["title"]),
                        source=str(payload.get("source", "unknown")),
                        year=int(payload.get("year", 0)),
                        text=str(payload["text"]),
                        tags=tuple(payload.get("tags", [])),
                        metadata=dict(payload.get("metadata", {})),
                    )
                )
            except KeyError as exc:
                raise ValueError(f"Missing required field {exc} on line {line_number}") from exc

    if not documents:
        raise ValueError(f"Corpus is empty: {corpus_path}")

    return documents
