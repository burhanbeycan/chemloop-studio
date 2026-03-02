# Roadmap: research directions for ChemLoop Studio

This file is intentionally written like a mini research plan.
You can copy/paste parts into a cover letter or "future work" section.

## R1 — Human-in-the-loop BO with preference learning
**Idea:** go beyond hard bounds. Let the scientist express *pairwise preferences* (A better than B) or soft constraints.
Learn a utility function and optimise it.

**Why it’s novel:** preferences are common in chemistry ("looks stable", "good morphology") but rarely quantified.

**Implementation in this repo:**
- Add a UI widget: choose between two candidate experiments (or their predicted outcomes)
- Train a Bradley–Terry / GP preference model
- Optimise an acquisition function under preference uncertainty

## R2 — Literature priors as probabilistic constraints (not hard bounds)
**Idea:** extracted ranges are noisy. Treat them as priors with confidence, then learn when to trust them.

**Why it’s novel:** reduces failure modes where the literature is out-of-domain.

**Implementation:**
- Store per-snippet provenance + a confidence score
- Use a mixture model: `p(feasible|x) = alpha * p_lit(feasible|x) + (1-alpha)*p_data(...)`
- Learn `alpha` online

## R3 — Vision-in-the-loop optimisation (SEM/optical)
**Idea:** the objective is not a scalar; it is a distribution (fiber diameters, bead fraction, pore size distribution).

**Implementation:**
- Add an upload widget for images + an analysis pipeline (e.g., segmentation or diameter estimation)
- Define objectives from distributions: mean, variance, tail probability
- Add active learning for **where to image next** (measurement planning)

## R4 — Multi-fidelity BO for materials workflows
**Idea:** combine cheap proxy measurements (viscosity, conductivity, UV-Vis) with expensive SEM/XPS.

**Implementation:**
- Extend data schema with a fidelity level
- Train a multi-fidelity surrogate and select either:
  - the next condition, or
  - the next measurement type
- Visualise the value of information from each measurement

## R5 — Robust BO under failures + safety envelopes
**Idea:** in real autonomous labs, some suggested experiments fail or produce missing outcomes.

**Implementation:**
- Add a `run_status` column (success/fail)
- Model failure probability with a classifier
- Constrain BO to keep risk below a threshold
- Log full decision traces to support reproducibility

## R6 — Agentic workflows (planner + tools)
**Idea:** add a lightweight “agent” that can:
- retrieve snippets
- propose constraints
- propose experiments
- explain trade-offs

**Implementation:**
- Keep it modular: retrieval tool, extraction tool, optimisation tool
- Add a “reasoning trace” panel in the UI that records each tool call (for transparency)
