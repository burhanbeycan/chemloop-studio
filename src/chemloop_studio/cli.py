"""Command-line interface for ChemLoop Studio."""

from __future__ import annotations

from pathlib import Path
from typing import Optional

import typer
from rich.console import Console
from rich.panel import Panel
from rich.table import Table

from .corpus import load_corpus
from .experiment import load_experiments, recommend_next_experiment
from .reporting import build_markdown_report
from .retrieval import ChemLoopRetriever

app = typer.Typer(help="ChemLoop Studio: RAG + experiment planner for polymer/materials R&D.")
console = Console()


@app.command()
def ask(
    question: str = typer.Argument(..., help="Scientific/R&D question to ask."),
    top_k: int = typer.Option(4, help="Number of evidence snippets to retrieve."),
    corpus_path: Optional[Path] = typer.Option(None, help="Optional JSONL corpus path."),
    experiments_path: Optional[Path] = typer.Option(None, help="Optional experiment CSV path."),
) -> None:
    """Ask a question and recommend a next experiment."""

    documents = load_corpus(corpus_path) if corpus_path else load_corpus()
    retriever = ChemLoopRetriever(documents)
    answer = retriever.answer(question, top_k=top_k)

    frame = load_experiments(experiments_path) if experiments_path else load_experiments()
    recommendation = recommend_next_experiment(frame)

    console.print(Panel(answer.summary, title="Citation-grounded answer"))
    console.print(f"[bold]Evidence quality:[/bold] {answer.quality_score}")
    console.print(f"[bold]Uncertainty flags:[/bold] {', '.join(answer.uncertainty_flags)}")

    table = Table(title="Retrieved evidence")
    table.add_column("ID")
    table.add_column("Score")
    table.add_column("Snippet")
    for item in answer.evidence:
        table.add_row(item.doc.doc_id, f"{item.score:.3f}", item.snippet)
    console.print(table)

    console.print(
        Panel(
            (
                f"Next experiment: {recommendation.experiment_id}\n"
                f"Predicted score: {recommendation.predicted_score}\n"
                f"Expected improvement: {recommendation.expected_improvement}\n"
                f"Rationale: {recommendation.rationale}"
            ),
            title="Experiment planner",
        )
    )


@app.command()
def report(
    question: str = typer.Option(..., help="Scientific/R&D question to ask."),
    output: Path = typer.Option(Path("reports/demo-report.md"), help="Markdown output path."),
    top_k: int = typer.Option(4, help="Number of evidence snippets to retrieve."),
) -> None:
    """Generate a Markdown report."""

    documents = load_corpus()
    retriever = ChemLoopRetriever(documents)
    answer = retriever.answer(question, top_k=top_k)

    recommendation = recommend_next_experiment(load_experiments())
    markdown = build_markdown_report(answer, recommendation)

    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(markdown, encoding="utf-8")
    console.print(f"[green]Report written to {output}[/green]")


if __name__ == "__main__":
    app()
