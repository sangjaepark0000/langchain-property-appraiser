from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.session import get_db_session
from app.rag.query import answer_question
from app.schemas.query import QueryRequest, QueryResponse

router = APIRouter()


@router.post("/query", response_model=QueryResponse, tags=["rag"])
def query(request: QueryRequest, db: Session = Depends(get_db_session)) -> QueryResponse:
    result = answer_question(db, request.question, query_vector=request.query_vector, limit=request.limit)
    return QueryResponse(
        answer=result.answer.answer,
        citations=result.answer.citations,
        data_mode=result.answer.data_mode,
        insufficient_evidence=result.answer.status == "insufficient_evidence",
        retrieved_count=result.retrieved_count,
        fallback=result.answer.fallback,
        provider=result.answer.provider,
    )
