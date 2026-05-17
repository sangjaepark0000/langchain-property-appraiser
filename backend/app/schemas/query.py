from pydantic import BaseModel, Field


class QueryRequest(BaseModel):
    question: str = Field(min_length=1)
    limit: int = Field(default=5, ge=1, le=20)
    query_vector: list[float] | None = None


class QueryResponse(BaseModel):
    answer: str
    citations: list[dict]
    data_mode: str
    insufficient_evidence: bool
    insufficient_evidence_reason: str | None = None
    retrieved_count: int
    fallback: bool
    provider: str
