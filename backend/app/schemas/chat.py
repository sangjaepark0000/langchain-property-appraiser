from pydantic import BaseModel, Field


class ChatRequest(BaseModel):
    question: str = Field(min_length=1)
    conversation_id: int | None = None
    query_vector: list[float] | None = None
    rewrite_query_vector: list[float] | None = None
    max_rewrite_attempts: int = Field(default=1, ge=0, le=3)


class ChatResponse(BaseModel):
    conversation_id: int
    message_id: int
    answer: str
    citations: list[dict]
    data_mode: str
    insufficient_evidence: bool
    insufficient_evidence_reason: str | None = None
    retrieval_trace: dict
    fallback: bool
    provider: str
