# Project Brief

ChemLoop Studio is an end-to-end AI-for-science portfolio project for polymer and materials experiment planning.

## Core idea

A scientist starts with experimental goals and constraints. The system retrieves relevant literature-style evidence, converts the evidence into suggested parameter bounds, fits a surrogate model to previous experiments, and proposes the next experiment using Bayesian optimisation.

## Why this is a strong GitHub project

The project is stronger than a single ML notebook because it demonstrates a full applied-AI workflow:

- data ingestion,
- literature-informed retrieval,
- surrogate modelling,
- uncertainty-aware optimisation,
- human-in-the-loop interaction,
- web interface,
- API handoff to a lab scheduler or robot,
- tests and reproducibility.

## Target career signal

This project positions the author for applied AI, scientific machine learning, materials informatics, R&D automation, and research software roles.

## MVP scope

- Streamlit multipage interface.
- Gaussian-process Bayesian optimisation.
- Expected-improvement acquisition function.
- Simple retrieval over a demonstration scientific corpus.
- Range extraction for literature-informed priors.
- FastAPI endpoint for next-experiment suggestion.
- Unit tests and CI.

## Scientific scope

The current use case is electrospinning/materials optimisation, but the framework is designed so the same logic can be extended to battery materials, polymer formulations, coatings, porous materials, or other R&D datasets.
