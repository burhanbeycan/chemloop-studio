"""Streamlit demo for ChemLoop Studio."""

from __future__ import annotations

import streamlit as st

from chemloop_studio.corpus import load_corpus
from chemloop_studio.experiment import load_experiments, recommend_next_experiment
from chemloop_studio.retrieval import ChemLoopRetriever


@st.cache_resource
def get_retriever() -> ChemLoopRetriever:
    return ChemLoopRetriever(load_corpus())


@st.cache_data
def get_experiments():
    return load_experiments()


st.set_page_config(page_title="ChemLoop Studio", page_icon="🧪", layout="wide")

st.title("ChemLoop Studio")
st.subheader("Self-auditing RAG + experiment planner for polymer/materials R&D")

st.write(
    "Ask a polymer or materials R&D question. The app retrieves evidence, reports uncertainty, "
    "and recommends a next experiment from the candidate design table."
)

question = st.text_area(
    "Question",
    value="Which electrospinning variables are likely to reduce nanofiber diameter while preserving antimicrobial surface functionality?",
)

top_k = st.slider("Evidence snippets", min_value=2, max_value=8, value=4)

if st.button("Run ChemLoop"):
    retriever = get_retriever()
    answer = retriever.answer(question, top_k=top_k)
    recommendation = recommend_next_experiment(get_experiments())

    st.markdown("### Citation-grounded answer")
    st.write(answer.summary)

    c1, c2, c3 = st.columns(3)
    c1.metric("Evidence quality", answer.quality_score)
    c2.metric("Evidence items", len(answer.evidence))
    c3.metric("Next experiment", recommendation.experiment_id)

    st.markdown("### Uncertainty flags")
    st.write(", ".join(answer.uncertainty_flags))

    st.markdown("### Retrieved evidence")
    for item in answer.evidence:
        st.info(f"**{item.doc.doc_id} — {item.doc.citation}**\n\n{item.snippet}\n\nScore: {item.score:.3f}")

    st.markdown("### Suggested next experiment")
    st.json(
        {
            "experiment_id": recommendation.experiment_id,
            "predicted_score": recommendation.predicted_score,
            "expected_improvement": recommendation.expected_improvement,
            "uncertainty": recommendation.uncertainty,
            "variables": recommendation.variables,
            "rationale": recommendation.rationale,
        }
    )
