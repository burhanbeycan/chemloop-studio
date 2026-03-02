import numpy as np
import streamlit as st

from mds.literature import LiteratureAssistant

st.title("2) Literature-informed priors (mini RAG demo)")

st.write(
    """
This page demonstrates a **minimal** literature-informed loop:

- Search a small example corpus (JSONL abstracts)
- Retrieve the top-k relevant snippets (TF‑IDF)
- Extract *suggested* parameter ranges (simple regex-based parser)
- Optionally apply those ranges as **bounds** back in the optimiser
"""
)

la = LiteratureAssistant.from_jsonl("data/literature_corpus.jsonl")

query = st.text_input("Search query", value="gelatin polyurethane electrospinning voltage concentration")
k = st.slider("Top-k results", 1, 5, 3)

if st.button("Search"):
    results = la.search(query, top_k=int(k))

    if not results:
        st.warning("No results.")
        st.stop()

    st.subheader("Top matches")
    for i, r in enumerate(results, 1):
        st.markdown(f"### {i}. {r['title']}")
        st.write(r["text"])
        if r.get("meta"):
            st.caption(f"Meta: {r['meta']}")
        extracted = la.extract_ranges(r["text"])
        st.code(extracted, language="json")

    st.subheader("Aggregated suggested ranges")
    agg = la.aggregate_ranges([la.extract_ranges(r["text"]) for r in results])
    st.json(agg)

    st.info(
        """
To *use* these ranges in optimisation, copy them into the bounds sliders on the **Closed-loop BO** page.

In a full system, this step would be automatic and would track provenance:
which snippet produced which constraint and with what confidence.
"""
    )

with st.expander("Upgrade path (research-ready)"):
    st.markdown(
        """
Ideas to turn this into a research contribution:
- Replace TF‑IDF with embedding search (FAISS) for better semantic recall.
- Use an LLM (with citations) to extract structured constraints + uncertainty.
- Treat extracted ranges as **probabilistic priors** instead of hard bounds.
- Learn when literature priors help vs hurt (misleading or out-of-domain snippets).
"""
    )
