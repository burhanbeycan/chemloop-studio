import numpy as np
import pandas as pd
import streamlit as st

from mds.simulator import porous_material_sim
from mds.pareto import pareto_front
from mds.plotting import plot_pareto

st.title("3) Multi-objective exploration (toy porous materials)")

st.write(
    """
A common discovery setting is **multi-objective**:
e.g., maximise surface area while maintaining yield (or stability, cost, etc.).

This page samples a toy design space and visualises an approximate Pareto front.
"""
)

colA, colB, colC = st.columns(3)
with colA:
    n = st.slider("Number of samples", 50, 2000, 400, step=50)
with colB:
    noise = st.slider("Simulation noise", 0.0, 5.0, 0.5, step=0.1)
with colC:
    seed = st.number_input("Random seed", 0, 9999, 7, step=1)

bounds = np.array([[0.0, 1.0], [0.0, 1.0]], dtype=float)  # x1,x2 in [0,1]

if st.button("Sample design space"):
    rng = np.random.default_rng(int(seed))
    X = rng.uniform(0, 1, size=(int(n), 2))

    y1 = []  # surface area (maximize)
    y2 = []  # yield (maximize)
    for x in X:
        sa, yld = porous_material_sim(x[0], x[1], noise=float(noise))
        y1.append(sa)
        y2.append(yld)

    df = pd.DataFrame({"x1": X[:,0], "x2": X[:,1], "surface_area": y1, "yield": y2})

    st.session_state["mo_df"] = df
    st.experimental_rerun()

df = st.session_state.get("mo_df")
if df is None:
    st.info("Click **Sample design space** to generate data.")
    st.stop()

st.dataframe(df.head(20), use_container_width=True, hide_index=True)

F = df[["surface_area", "yield"]].to_numpy()
mask = pareto_front(F, maximize=True)

st.subheader("Pareto front (approx.)")
fig = plot_pareto(df, mask)
st.pyplot(fig, clear_figure=True)

with st.expander("How to turn this into BO"):
    st.markdown(
        """
For a research-grade multi-objective optimiser, you can:
- Use **scalarisation** (weighted sum / Chebyshev) + BO
- Or use BoTorch's **qEHVI** for direct hypervolume improvement
- Add **constraints** (e.g., gel fraction, viscosity, stability windows)
"""
    )
