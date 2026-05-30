"""Minimal ChemLoop Studio example."""

from chemloop_studio.corpus import load_corpus
from chemloop_studio.experiment import load_experiments, recommend_next_experiment
from chemloop_studio.retrieval import ChemLoopRetriever

question = "How can electrospinning parameters reduce fiber diameter and preserve antimicrobial function?"

retriever = ChemLoopRetriever(load_corpus())
answer = retriever.answer(question)
recommendation = recommend_next_experiment(load_experiments())

print(answer.summary)
print("Quality:", answer.quality_score)
print("Next experiment:", recommendation.experiment_id, recommendation.variables)
