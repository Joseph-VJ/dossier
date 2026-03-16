from __future__ import annotations

import re

from dossier.contracts import RankedInsight
from dossier.db import SqliteRepository

_STOP_WORDS = {
    "a",
    "an",
    "and",
    "are",
    "as",
    "at",
    "be",
    "by",
    "did",
    "do",
    "does",
    "for",
    "from",
    "how",
    "in",
    "is",
    "it",
    "next",
    "of",
    "on",
    "or",
    "q1",
    "q2",
    "q3",
    "q4",
    "should",
    "that",
    "the",
    "this",
    "to",
    "we",
    "what",
    "why",
    "will",
    "with",
}


class CaseMemoryManager:
    def __init__(self, repository: SqliteRepository) -> None:
        self.repository = repository

    def warm_start(self, question: str) -> list[str]:
        keywords = self._extract_keywords(question)
        matches = self.repository.search_case_memory(keywords, limit=5)
        if not matches:
            return ["No prior case memory found."]
        return [
            f"[{match['motif_type']}] {match['content']} (score: {float(match['score']):.2f})"
            for match in matches
        ]

    def writeback(self, case_id: str, insights: list[RankedInsight]) -> int:
        stored = 0
        for insight in insights:
            total = insight.score.total or 0.0
            if total < 0.62:
                continue
            self.repository.store_case_memory(
                case_id=case_id,
                motif_type="mechanism_pattern",
                content=f"{insight.mechanism.name}: {insight.mechanism.description}",
                score=total,
            )
            self.repository.store_case_memory(
                case_id=case_id,
                motif_type="hypothesis_template",
                content=f"{insight.title}: {insight.summary}",
                score=total,
            )
            stored += 2
        return stored

    def _extract_keywords(self, question: str) -> list[str]:
        tokens = re.findall(r"[a-z0-9]+", question.lower())
        unique_tokens: list[str] = []
        seen: set[str] = set()
        for token in sorted(tokens, key=lambda value: (-len(value), value)):
            if len(token) < 3 or token in _STOP_WORDS or token in seen:
                continue
            seen.add(token)
            unique_tokens.append(token)
            if len(unique_tokens) >= 5:
                break
        return unique_tokens
