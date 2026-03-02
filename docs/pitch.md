# 1-page pitch: why ChemLoop Studio matters (AI/ML-driven chemical discovery)

ChemLoop Studio is a demonstration of an end-to-end workflow for AI-driven discovery:

- **Decision layer:** Bayesian optimisation (active learning) with uncertainty
- **Knowledge layer:** literature-informed constraints (minimal RAG)
- **Human layer:** scientist overrides and preferences
- **Execution layer:** API stub that can connect to a robot scheduler
- **Reproducibility:** exportable run logs, tests, CI workflow template

This mirrors typical autonomous lab stacks at modern materials discovery centres.

## What makes it research-relevant
- The same UI can be connected to *real* experiments (electrospinning, polymer synthesis, porous materials screening).
- The literature module can be upgraded to RAG + LLM extraction while retaining provenance.
- The optimiser can be upgraded to BoTorch for batch, constrained, and multi-objective BO.

## What you can claim in an application
- You can design **accessible GUIs** for optimisation.
- You can implement the core optimisation loop and expose it through an API.
- You can integrate literature/human knowledge into experiment selection.
- You can write code that is documented, tested, and CI-ready.

