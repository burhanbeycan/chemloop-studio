"""Retrieval and evidence-grounded answer building."""

from __future__ import annotations

import re
from collections import Counter

import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

from .evaluation import evidence_quality_score, uncertainty_flags
from .models import Answer, Document, Evidence


_SENTENCE_RE = re.compile(r"(?<=[.!?])\s+")
_KEYWORD_RE = re.compile(r"[A-Za-z][A-Za-z0-9\-]{2,}")


class ChemLoopRetriever:
    """Simple, transparent TF-IDF retriever for scientific portfolio demos.

    The implementation intentionally avoids external APIs so the repository is reproducible.
    It can later be replaced with sentence-transformer embeddings or a hybrid GraphRAG store.
    """

    def __init__(self, documents: list[Document]) -> None:
        if not documents:
            raise ValueError("ChemLoopRetriever requires at least one document.")
        self.documents = documents
        self.vectorizer = TfidfVectorizer(stop_words="english", ngram_range=(1, 2))
        self.matrix = self.vectorizer.fit_transform([doc.text for doc in documents])

    def search(self, query: str, top_k: int = 4) -> list[Evidence]:
        """Return top-k evidence snippets for a query."""

        if not query.strip():
            raise ValueError("Query cannot be empty.")
        if top_k <= 0:
            raise ValueError("top_k must be positive.")

        query_vector = self.vectorizer.transform([query])
        scores = cosine_similarity(query_vector, self.matrix).ravel()
        order = np.argsort(scores)[::-1][:top_k]

        evidence: list[Evidence] = []
        for index in order:
            doc = self.documents[int(index)]
            score = float(scores[int(index)])
            evidence.append(Evidence(doc=doc, score=score, snippet=self._best_snippet(query, doc.text)))
        return evidence

    def answer(self, question: str, top_k: int = 4) -> Answer:
        """Build a compact extractive answer with citations and uncertainty flags."""

        evidence = tuple(self.search(question, top_k=top_k))
        summary = build_summary(question, evidence)
        quality = evidence_quality_score(evidence)
        flags = uncertainty_flags(evidence)
        next_step = propose_next_step(question, evidence)
        return Answer(
            question=question,
            summary=summary,
            evidence=evidence,
            quality_score=quality,
            uncertainty_flags=tuple(flags),
            suggested_next_step=next_step,
        )

    def _best_snippet(self, query: str, text: str) -> str:
        query_terms = {term.lower() for term in _KEYWORD_RE.findall(query)}
        sentences = _SENTENCE_RE.split(text.strip())
        if not sentences:
            return text[:280]

        def sentence_score(sentence: str) -> int:
            terms = {term.lower() for term in _KEYWORD_RE.findall(sentence)}
            return len(query_terms & terms)

        best = max(sentences, key=sentence_score)
        return best[:360].strip()


def build_summary(question: str, evidence: tuple[Evidence, ...]) -> str:
    """Create a citation-grounded extractive summary from evidence."""

    if not evidence:
        return "No evidence was retrieved."

    terms = Counter()
    for item in evidence:
        terms.update(term.lower() for term in _KEYWORD_RE.findall(item.snippet))

    high_signal_terms = [term for term, _ in terms.most_common(8)]
    cited_points = []
    for item in evidence[:3]:
        cited_points.append(f"{item.snippet} [{item.doc.doc_id}]")

    return (
        f"For the question '{question}', the retrieved evidence emphasizes "
        f"{', '.join(high_signal_terms[:5])}. Key evidence: "
        + " ".join(cited_points)
    )


def propose_next_step(question: str, evidence: tuple[Evidence, ...]) -> str:
    """Generate a conservative next-step recommendation from retrieved evidence."""

    joined = " ".join(item.snippet.lower() for item in evidence)
    if "electrospinning" in joined or "nanofiber" in joined:
        return (
            "Run a small design-of-experiments sweep around polymer concentration, voltage, "
            "and flow rate; keep one antimicrobial additive constant and validate morphology "
            "before increasing formulation complexity."
        )
    if "battery" in joined or "cathode" in joined:
        return (
            "Prioritize a controlled comparison of active-material loading, conductive additive, "
            "and binder fraction before moving to complex electrolyte or cycling protocols."
        )
    return (
        "Start with a small, well-documented candidate set, measure one primary response, "
        "and update the surrogate model before expanding the search space."
    )
