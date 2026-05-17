from __future__ import annotations

from dataclasses import dataclass

from sqlalchemy.orm import Session

from app.rag.answer import AnswerResult, compose_answer
from app.rag.citations import hydrate_retrieval_results
from app.rag.grading import RetrievalGrade, grade_retrieval_results
from app.rag.retriever import VectorRetriever
from app.rag.rewrite import QueryRewriteResult, rewrite_query
from app.services.retrieval_trace_service import create_retrieval_trace


@dataclass(frozen=True)
class RAGQueryResult:
    question: str
    answer: AnswerResult
    retrieved_count: int
    results: list[dict]
    grading: RetrievalGrade
    rewrite: QueryRewriteResult


def _empty_rewrite(question: str) -> QueryRewriteResult:
    return QueryRewriteResult(original_query=question, rewritten_query=None, status="not_needed", fallback=False, attempts=0)


def answer_question(
    session: Session,
    question: str,
    *,
    query_vector: list[float] | None = None,
    rewrite_query_vector: list[float] | None = None,
    history_texts: list[str] | None = None,
    limit: int = 5,
    min_retrieval_score: float = 0.0,
    max_rewrite_attempts: int = 1,
    conversation_id: int | None = None,
    message_id: int | None = None,
) -> RAGQueryResult:
    retriever = VectorRetriever(session)
    raw_results = retriever.search(
        question,
        query_vector=query_vector,
        limit=limit,
        min_score=min_retrieval_score,
    )
    initial_grading = grade_retrieval_results(raw_results)
    grading = initial_grading
    rewrite = _empty_rewrite(question)
    rewritten_results = None

    if initial_grading.status in {"weak", "irrelevant"} and max_rewrite_attempts > 0:
        rewrite = rewrite_query(question, history=history_texts or [])
        if rewrite.status == "rewritten" and rewrite.rewritten_query:
            rewritten_results = retriever.search(
                rewrite.rewritten_query,
                query_vector=rewrite_query_vector,
                limit=limit,
                min_score=min_retrieval_score,
            )
            rewritten_grading = grade_retrieval_results(rewritten_results)
            if rewritten_grading.max_score >= initial_grading.max_score:
                raw_results = rewritten_results
                grading = rewritten_grading

    hydrated = hydrate_retrieval_results(session, raw_results) if grading.status == "sufficient" else []
    insufficient_reason = None if grading.status == "sufficient" else grading.reason or grading.status
    answer = compose_answer(question, hydrated)
    create_retrieval_trace(
        session,
        original_query=question,
        rewritten_query=rewrite.rewritten_query,
        retrieved_chunk_ids=[result.chunk_id for result in raw_results],
        rewritten_retrieved_chunk_ids=[result.chunk_id for result in rewritten_results] if rewritten_results is not None else None,
        relevance_result=grading.status,
        conversation_id=conversation_id,
        message_id=message_id,
        insufficient_evidence_reason=insufficient_reason,
        extra_summary={
            "max_score": grading.max_score,
            "initial_grading_status": initial_grading.status,
            "grading_status": grading.status,
            "rewrite_status": rewrite.status,
            "rewrite_fallback": rewrite.fallback,
            "rewrite_attempts": min(rewrite.attempts, max_rewrite_attempts),
        },
    )
    return RAGQueryResult(
        question=question,
        answer=answer,
        retrieved_count=len(hydrated),
        results=hydrated,
        grading=grading,
        rewrite=rewrite,
    )
