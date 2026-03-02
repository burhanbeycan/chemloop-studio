import numpy as np
import pandas as pd
import streamlit as st

from mds.bo import fit_gp, suggest_next
from mds.simulator import electrospinning_fiber_diameter
from mds.data import init_runhistory, append_run
from mds.plotting import plot_gp_surface, plot_history

st.title("1) Closed-loop Bayesian Optimisation (toy electrospinning)")

st.write(
    """
This page simulates a closed-loop workflow:

1. Start with a few random experiments  
2. Fit a Gaussian Process surrogate model  
3. Use Expected Improvement to suggest the next condition  
4. (Optional) **Human override**: adjust the suggested point  
5. Run the simulated experiment and repeat

The "experiment" here is a toy function that mimics an electrospinning response surface with noise.
"""
)

colA, colB, colC = st.columns(3)

with colA:
    conc_min, conc_max = st.slider("Polymer concentration (wt%) bounds", 2.0, 25.0, (6.0, 16.0), step=0.5)
with colB:
    volt_min, volt_max = st.slider("Voltage (kV) bounds", 5.0, 30.0, (12.0, 24.0), step=0.5)
with colC:
    noise = st.slider("Simulation noise (std)", 0.0, 5.0, 1.0, step=0.1)

bounds = np.array([[conc_min, conc_max], [volt_min, volt_max]], dtype=float)

if "runs" not in st.session_state:
    st.session_state["runs"] = init_runhistory()

runs: pd.DataFrame = st.session_state["runs"]

st.subheader("Run history")
st.dataframe(runs, use_container_width=True, hide_index=True)

c1, c2, c3, c4 = st.columns(4)
with c1:
    n_init = st.number_input("Initial random points", min_value=2, max_value=25, value=5, step=1)
with c2:
    n_candidates = st.number_input("Candidate samples for EI", min_value=200, max_value=20000, value=2000, step=200)
with c3:
    xi = st.number_input("EI exploration parameter (xi)", min_value=0.0, max_value=1.0, value=0.01, step=0.01)
with c4:
    objective = st.selectbox("Objective", ["Minimise fiber diameter"])

st.divider()

if st.button("Generate initial random experiments", type="secondary"):
    st.session_state["runs"] = init_runhistory()
    runs = st.session_state["runs"]

    rng = np.random.default_rng(0)
    X0 = rng.uniform(bounds[:, 0], bounds[:, 1], size=(int(n_init), 2))
    for x in X0:
        y = electrospinning_fiber_diameter(x[0], x[1], noise=noise)
        st.session_state["runs"] = append_run(st.session_state["runs"], x, y)

    st.experimental_rerun()

if len(runs) < 2:
    st.warning("Add some initial experiments first.")
    st.stop()

X = runs[["conc_wt", "voltage_kV"]].to_numpy()
y = runs["fiber_diam_nm"].to_numpy()

gp = fit_gp(X, y)

y_best = float(np.min(y))
x_next, meta = suggest_next(bounds, gp, y_best=y_best, n_candidates=int(n_candidates), xi=float(xi), random_state=1)

st.subheader("Suggested next experiment (Expected Improvement)")

col1, col2 = st.columns(2)
with col1:
    st.metric("Current best (min diameter, nm)", f"{y_best:.2f}")
with col2:
    st.metric("Suggested conc / voltage", f"{x_next[0]:.2f} wt% , {x_next[1]:.2f} kV")

st.caption("Human-in-the-loop: you can override the suggestion before running the next experiment.")

override = st.checkbox("Override suggested point")
if override:
    x1 = st.slider("Override concentration (wt%)", float(bounds[0,0]), float(bounds[0,1]), float(x_next[0]), step=0.1)
    x2 = st.slider("Override voltage (kV)", float(bounds[1,0]), float(bounds[1,1]), float(x_next[1]), step=0.1)
    x_run = np.array([x1, x2], dtype=float)
else:
    x_run = x_next

if st.button("Run next experiment (simulate) ✅", type="primary"):
    y_new = electrospinning_fiber_diameter(x_run[0], x_run[1], noise=noise)
    st.session_state["runs"] = append_run(st.session_state["runs"], x_run, y_new)
    st.success(f"Simulated result: fiber_diam_nm = {y_new:.2f}")
    st.experimental_rerun()

st.divider()
st.subheader("Visualisations")

colL, colR = st.columns(2)
with colL:
    fig1 = plot_history(st.session_state["runs"])
    st.pyplot(fig1, clear_figure=True)

with colR:
    fig2 = plot_gp_surface(bounds, gp, st.session_state["runs"], x_next=x_next)
    st.pyplot(fig2, clear_figure=True)

with st.expander("What to swap for a real lab"):
    st.markdown(
        """
- Replace `electrospinning_fiber_diameter(...)` with a call to your instrument or a robot queue.
- Log metadata (SEM settings, humidity, needle gauge, solvent batch) into the run history.
- Replace GP+EI with BoTorch for batch BO and constraints.
"""
    )
