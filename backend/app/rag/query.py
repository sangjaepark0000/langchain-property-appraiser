from __future__ import annotations

from dataclasses import dataclass

from sqlalchemy.orm import Session

from app.rag.answer import AnswerResult, compose_answer
from app.rag.citations import hydrate_retrieval_results
from app.rag.grading import RetrievalGrade, grade_retrieval_results
from app.rag.retriever import VectorRetriever
from app.services.retrieval_trace_service import create_retrieval_trace


@dataclass(frozen=True)
class RAGQueryResult:
    question: str
    answer: AnswerResult
    retrieved_count: int
    results: list[dict]
    grading: RetrievalGrade


def answer_question(
    session: Session,
    question: str,
    *,
    query_vector: list[float] | None = None,
    limit: int = 5,
    min_retrieval_score: float = 0.0,
    conversation_id: int | None = None,
    message_id: int | None = None,
) -> RAGQueryResult:
    raw_results = VectorRetriever(session).search(
        question,
        query_vector=query_vector,
        limit=limit,
        min_score=min_retrieval_score,
    )
    grading = grade_retrieval_results(raw_results)
    hydrated = hydrate_retrieval_results(session, raw_results) if grading.status == "sufficient" else []
    insufficient_reason = None if grading.status == "sufficient" else grading.reason or grading.status
    answer = compose_answer(question, hydrated)
    create_retrieval_trace(
        session,
        original_query=question,
        retrieved_chunk_ids=[result.chunk_id for result in raw_results],
        relevance_result=grading.status,
        conversation_id=conversation_id,
        message_id=message_id,
        insufficient_evidence_reason=insufficient_reason,
        extra_summary={"max_score": grading.max_score, "grading_status": grading.status},
    )
    return RAGQueryResult(
        question=question,
        answer=answer,
        retrieved_count=len(hydrated),
        results=hydrated,
        grading=grading,
    )
