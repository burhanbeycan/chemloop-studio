import streamlit as st

st.set_page_config(
    page_title="ChemLoop Studio",
    page_icon="🧪",
    layout="wide",
)

st.title("🧪 ChemLoop Studio")
st.write(
    """
ChemLoop Studio is a lightweight **interactive web app** that demonstrates:

- **Closed-loop Bayesian optimisation** for experiment suggestion
- **Human-in-the-loop** constraints and preferences
- **Literature-informed** bounds (simple RAG-style retrieval)
- **Multi-objective** exploration and trade-offs
- A **FastAPI stub** to connect the optimiser to a robotic platform

Use the left sidebar to open the demo pages.
"""
)

with st.expander("Why this is useful as a portfolio demo"):
    st.markdown(
        """
Many AI-for-chemistry roles want proof that you can build **end-to-end workflows**:
data → model → decision → (robot/API) → data.

ChemLoop Studio focuses on **clarity**, **reproducibility**, and **interactivity** rather than complex dependencies.
"""
    )

st.info("Tip: start with **Closed-loop BO** then open **Literature priors** to see how constraints change suggestions.")
