from __future__ import annotations

import json
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, List

import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


@dataclass
class Doc:
    title: str
    text: str
    meta: Dict


class LiteratureAssistant:
    """Minimal retrieval + range extraction to mimic literature-informed priors."""

    def __init__(self, docs: List[Doc]):
        self.docs = docs
        self.vectorizer = TfidfVectorizer(stop_words="english", ngram_range=(1, 2))
        self._X = self.vectorizer.fit_transform([d.text for d in docs])

    @classmethod
    def from_jsonl(cls, path: str) -> "LiteratureAssistant":
        docs: List[Doc] = []
        p = Path(path)
        for line in p.read_text(encoding="utf-8").splitlines():
            if not line.strip():
                continue
            obj = json.loads(line)
            docs.append(Doc(title=obj["title"], text=obj["text"], meta=obj.get("meta", {})))
        return cls(docs)

    def search(self, query: str, top_k: int = 3) -> List[Dict]:
        q = self.vectorizer.transform([query])
        sims = cosine_similarity(q, self._X).ravel()
        idx = np.argsort(-sims)[: int(top_k)]
        out = []
        for i in idx:
            d = self.docs[int(i)]
            out.append({"title": d.title, "text": d.text, "score": float(sims[int(i)]), "meta": d.meta})
        return out

    def extract_ranges(self, text: str) -> Dict:
        """Extract parameter ranges for voltage (kV) and concentration (wt%) if present.

        This is a toy regex-based extractor.
        A research-grade system would use LLM extraction + citations + uncertainty.
        """
        out: Dict = {"conc_wt_range": None, "voltage_kV_range": None, "single_values": {}}

        # Range patterns
        conc_rng = re.search(r"(\d+(?:\.\d+)?)\s*[-–]\s*(\d+(?:\.\d+)?)\s*wt\s*%?", text, flags=re.I)
        volt_rng = re.search(r"(\d+(?:\.\d+)?)\s*[-–]\s*(\d+(?:\.\d+)?)\s*kV", text, flags=re.I)

        if conc_rng:
            out["conc_wt_range"] = [float(conc_rng.group(1)), float(conc_rng.group(2))]
        if volt_rng:
            out["voltage_kV_range"] = [float(volt_rng.group(1)), float(volt_rng.group(2))]

        # Single values (e.g., "at 18 kV")
        volt_single = re.search(r"\b(?:at|around|approx\.?|≈)\s*(\d+(?:\.\d+)?)\s*kV\b", text, flags=re.I)
        conc_single = re.search(r"\b(?:at|around|approx\.?|≈)\s*(\d+(?:\.\d+)?)\s*wt\s*%?", text, flags=re.I)

        if volt_single:
            out["single_values"]["voltage_kV"] = float(volt_single.group(1))
        if conc_single:
            out["single_values"]["conc_wt"] = float(conc_single.group(1))

        return out

    def aggregate_ranges(self, extracted: List[Dict]) -> Dict:
        """Aggregate multiple extracted snippets into a single suggested range (intersection when possible)."""
        conc_ranges = [e["conc_wt_range"] for e in extracted if e.get("conc_wt_range")]
        volt_ranges = [e["voltage_kV_range"] for e in extracted if e.get("voltage_kV_range")]

        def intersect(ranges):
            if not ranges:
                return None
            lo = max(r[0] for r in ranges)
            hi = min(r[1] for r in ranges)
            if lo <= hi:
                return [float(lo), float(hi)]
            # If no intersection, return the union to avoid over-constraining
            lo = min(r[0] for r in ranges)
            hi = max(r[1] for r in ranges)
            return [float(lo), float(hi)]

        return {"conc_wt_suggested": intersect(conc_ranges), "voltage_kV_suggested": intersect(volt_ranges)}
