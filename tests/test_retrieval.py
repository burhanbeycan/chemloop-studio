import pytest

from chemloop_studio.corpus import load_corpus
from chemloop_studio.retrieval import ChemLoopRetriever


def test_retrieval_returns_evidence_for_electrospinning_question():
    retriever = ChemLoopRetriever(load_corpus())
    evidence = retriever.search("electrospinning nanofiber antimicrobial PEI", top_k=3)
    assert len(evidence) == 3
    assert evidence[0].score >= evidence[-1].score
    assert any("electrospinning" in item.snippet.lower() for item in evidence)


def test_answer_contains_quality_and_uncertainty_flags():
    retriever = ChemLoopRetriever(load_corpus())
    answer = retriever.answer("Which variables control nanofiber diameter?", top_k=3)
    assert answer.quality_score > 0
    assert answer.evidence
    assert "requires_experimental_validation" in answer.uncertainty_flags


def test_empty_query_is_rejected():
    retriever = ChemLoopRetriever(load_corpus())
    with pytest.raises(ValueError):
        retriever.search("   ")
