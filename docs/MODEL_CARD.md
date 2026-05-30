# Model Card

## Model components

ChemLoop Studio currently uses two transparent components:

1. TF-IDF retriever for literature-style evidence retrieval.
2. Random forest surrogate for candidate experiment ranking.

## Intended purpose

The models are intended for reproducible portfolio demonstration and early-stage R&D decision-support prototyping.

## Inputs

- Natural-language scientific question.
- JSONL corpus of literature-style documents.
- CSV table of observed and candidate experiments.

## Outputs

- Retrieved evidence snippets.
- Evidence quality score and uncertainty flags.
- Suggested next experiment.

## Limitations

- TF-IDF does not understand deep scientific semantics.
- The sample corpus is small.
- The random forest surrogate is trained on a demonstration table.
- Recommendations require expert review and experimental validation.

## Ethical and safety considerations

The tool should support research reasoning, not replace scientific judgment. It should not be used to recommend unsafe experiments or unvalidated medical, biological, or hazardous protocols.
