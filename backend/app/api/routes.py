from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.session import get_db_session
from app.graph.conversation import run_conversation_graph
from app.models.message import Message
from app.models.retrieval_trace import RetrievalTrace
from app.rag.query import answer_question
from app.schemas.chat import ChatRequest, ChatResponse
from app.schemas.query import QueryRequest, QueryResponse

router = APIRouter()


def _latest_trace_summary(db: Session, conversation_id: int) -> dict:
    trace = (
        db.query(RetrievalTrace)
        .filter(RetrievalTrace.conversation_id == conversation_id)
        .order_by(RetrievalTrace.id.desc())
        .first()
    )
    if trace is None:
        return {}
    return {
        "id": trace.id,
        "relevance_result": trace.relevance_result,
        "retrieved_chunk_ids": trace.retrieved_chunk_ids,
        "rewritten_retrieved_chunk_ids": trace.rewritten_retrieved_chunk_ids,
        "insufficient_evidence_reason": trace.insufficient_evidence_reason,
        "rewrite_status": trace.summary.get("rewrite_status"),
        "rewrite_fallback": trace.summary.get("rewrite_fallback"),
        "rewrite_attempts": trace.summary.get("rewrite_attempts"),
        "summary": trace.summary,
    }


def _latest_user_message_id(db: Session, conversation_id: int) -> int:
    message = (
        db.query(Message)
        .filter(Message.conversation_id == conversation_id, Message.role == "user")
        .order_by(Message.id.desc())
        .first()
    )
    if message is None:
        raise RuntimeError("user message was not persisted")
    return message.id


@router.post("/query", response_model=QueryResponse, tags=["rag"])
def query(request: QueryRequest, db: Session = Depends(get_db_session)) -> QueryResponse:
    result = answer_question(db, request.question, query_vector=request.query_vector, limit=request.limit)
    return QueryResponse(
        answer=result.answer.answer,
        citations=result.answer.citations,
        data_mode=result.answer.data_mode,
        insufficient_evidence=result.insufficient_evidence,
        insufficient_evidence_reason=result.insufficient_evidence_reason,
        retrieved_count=result.retrieved_count,
        fallback=result.answer.fallback,
        provider=result.answer.provider,
    )


@router.post("/chat", response_model=ChatResponse, tags=["chat"])
def chat(request: ChatRequest, db: Session = Depends(get_db_session)) -> ChatResponse:
    result = run_conversation_graph(
        db,
        question=request.question,
        conversation_id=request.conversation_id,
        query_vector=request.query_vector,
        rewrite_query_vector=request.rewrite_query_vector,
        max_rewrite_attempts=request.max_rewrite_attempts,
    )
    return ChatResponse(
        conversation_id=result.conversation_id,
        message_id=_latest_user_message_id(db, result.conversation_id),
        answer=result.answer.answer,
        citations=result.answer.citations,
        data_mode=result.answer.data_mode,
        insufficient_evidence=result.insufficient_evidence,
        insufficient_evidence_reason=result.insufficient_evidence_reason,
        retrieval_trace=_latest_trace_summary(db, result.conversation_id),
        fallback=result.answer.fallback,
        provider=result.answer.provider,
    )
