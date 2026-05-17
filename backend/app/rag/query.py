from __future__ import annotations

from dataclasses import dataclass

from sqlalchemy.orm import Session

from app.rag.answer import AnswerResult, compose_answer
from app.rag.citations import hydrate_retrieval_results
from app.rag.retriever import VectorRetriever


@dataclass(frozen=True)
class RAGQueryResult:
    question: str
    answer: AnswerResult
    retrieved_count: int
    results: list[dict]


def answer_question(
    session: Session,
    question: str,
    *,
    query_vector: list[float] | None = None,
    limit: int = 5,
) -> RAGQueryResult:
    raw_results = VectorRetriever(session).search(question, query_vector=query_vector, limit=limit)
    hydrated = hydrate_retrieval_results(session, raw_results)
    answer = compose_answer(question, hydrated)
    return RAGQueryResult(
        question=question,
        answer=answer,
        retrieved_count=len(hydrated),
        results=hydrated,
    )
