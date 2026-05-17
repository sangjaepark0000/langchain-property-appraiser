from __future__ import annotations

import hashlib

from sqlalchemy.orm import Session

from app.models.retrieval_trace import RetrievalTrace

MAX_QUERY_PREVIEW_CHARS = 80


def query_preview(query: str) -> str:
    normalized = " ".join(query.split())
    if len(normalized) <= MAX_QUERY_PREVIEW_CHARS:
        return normalized
    return normalized[:MAX_QUERY_PREVIEW_CHARS] + "…"


def query_hash(query: str) -> str:
    return hashlib.sha256(query.encode("utf-8")).hexdigest()


def create_retrieval_trace(
    session: Session,
    *,
    original_query: str,
    retrieved_chunk_ids: list[int],
    relevance_result: str,
    conversation_id: int | None = None,
    message_id: int | None = None,
    rewritten_query: str | None = None,
    rewritten_retrieved_chunk_ids: list[int] | None = None,
    insufficient_evidence_reason: str | None = None,
) -> RetrievalTrace:
    summary = {
        "retrieved_count": len(retrieved_chunk_ids),
        "rewritten_retrieved_count": len(rewritten_retrieved_chunk_ids or []),
        "has_rewrite": rewritten_query is not None,
        "relevance_result": relevance_result,
        "has_insufficient_evidence_reason": insufficient_evidence_reason is not None,
    }
    trace = RetrievalTrace(
        conversation_id=conversation_id,
        message_id=message_id,
        query_preview=query_preview(original_query),
        query_hash=query_hash(original_query),
        rewritten_query_preview=query_preview(rewritten_query) if rewritten_query is not None else None,
        rewritten_query_hash=query_hash(rewritten_query) if rewritten_query is not None else None,
        retrieved_chunk_ids=retrieved_chunk_ids,
        rewritten_retrieved_chunk_ids=rewritten_retrieved_chunk_ids,
        relevance_result=relevance_result,
        insufficient_evidence_reason=insufficient_evidence_reason,
        summary=summary,
    )
    session.add(trace)
    session.commit()
    session.refresh(trace)
    return trace
