from __future__ import annotations

from dataclasses import dataclass

from app.rag.retriever import RetrievalResult


@dataclass(frozen=True)
class RetrievalGrade:
    status: str
    max_score: float
    retrieved_count: int
    reason: str | None = None


def grade_retrieval_results(
    results: list[RetrievalResult],
    *,
    sufficient_threshold: float = 0.8,
    weak_threshold: float = 0.4,
) -> RetrievalGrade:
    if not results:
        return RetrievalGrade(status="irrelevant", max_score=0.0, retrieved_count=0, reason="no results")
    max_score = max(result.score for result in results)
    if max_score >= sufficient_threshold:
        return RetrievalGrade(status="sufficient", max_score=max_score, retrieved_count=len(results))
    if max_score >= weak_threshold:
        return RetrievalGrade(status="weak", max_score=max_score, retrieved_count=len(results), reason="low relevance")
    return RetrievalGrade(status="irrelevant", max_score=max_score, retrieved_count=len(results), reason="irrelevant results")
