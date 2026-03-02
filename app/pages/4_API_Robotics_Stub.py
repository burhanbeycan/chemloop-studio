import json
import streamlit as st

st.title("4) API + robotics integration stub")

st.write(
    """
Many autonomous labs separate:

- a **decision layer** (optimiser / planner) and  
- an **execution layer** (robotics, instruments, scheduling)

This repo includes a small **FastAPI** server (`mds/api.py`) that exposes a `suggest_next` endpoint.
"""
)

st.subheader("Run the API locally")
st.code("uvicorn mds.api:app --reload --port 8000", language="bash")

st.subheader("Example request (curl)")
example = {
    "X": [[10.0, 18.0], [12.0, 20.0], [14.0, 16.0]],
    "y": [420.0, 350.0, 510.0],
    "bounds": [[6.0, 16.0], [12.0, 24.0]],
    "xi": 0.01,
    "n_candidates": 2000,
}
st.code(
    "curl -X POST http://localhost:8000/suggest_next \
"
    "  -H 'Content-Type: application/json' \
"
    f"  -d '{json.dumps(example)}'",
    language="bash",
)

st.subheader("What the endpoint returns")
st.json(
    {
        "x_next": [11.3, 19.1],
        "predicted_mean": 380.2,
        "predicted_std": 22.8,
        "notes": "Use this JSON in your robot scheduler as the next experiment."
    }
)

with st.expander("Research idea: experiment failure + safety constraints"):
    st.markdown(
        """
A real autonomous lab must handle:
- failed runs / missing measurements
- safety envelopes (pressure, voltage, solvent compatibility)
- temporal drift (humidity, batch effects)
- multi-fidelity data (cheap proxies vs expensive measurements)

A publishable direction is to build a *robust* decision layer that reasons under these realities.
"""
    )
