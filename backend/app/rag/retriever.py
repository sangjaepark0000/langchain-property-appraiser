from __future__ import annotations

import math
from dataclasses import dataclass

from sqlalchemy.orm import Session

from app.models.chunk import Chunk
from app.models.document import Document  # noqa: F401 - ensure relationship registration
from app.rag.embeddings import EmbeddingProvider, get_embedding_provider


@dataclass(frozen=True)
class RetrievalResult:
    chunk_id: int
    document_id: int
    text: str
    score: float
    relevance: str


def cosine_similarity(left: list[float], right: list[float]) -> float:
    if not left or not right or len(left) != len(right):
        return 0.0
    dot = sum(a * b for a, b in zip(left, right, strict=True))
    left_norm = math.sqrt(sum(a * a for a in left))
    right_norm = math.sqrt(sum(b * b for b in right))
    if left_norm == 0 or right_norm == 0:
        return 0.0
    return round(dot / (left_norm * right_norm), 6)


def relevance_label(score: float) -> str:
    if score >= 0.8:
        return "high"
    if score >= 0.4:
        return "medium"
    return "low"


class VectorRetriever:
    def __init__(self, session: Session, *, embedding_provider: EmbeddingProvider | None = None) -> None:
        self.session = session
        self.embedding_provider = embedding_provider or get_embedding_provider()

    def search(
        self,
        query: str,
        *,
        query_vector: list[float] | None = None,
        limit: int = 5,
        min_score: float = 0.0,
    ) -> list[RetrievalResult]:
        if limit <= 0:
            return []
        resolved_query_vector = query_vector
        if resolved_query_vector is None:
            embedding = self.embedding_provider.embed_text(query)
            if embedding.status != "success" or not embedding.vector:
                return []
            resolved_query_vector = embedding.vector

        candidates: list[RetrievalResult] = []
        for chunk in self.session.query(Chunk).all():
            stored_embedding = chunk.metadata_.get("embedding") if chunk.metadata_ else None
            if not isinstance(stored_embedding, list):
                continue
            try:
                vector = [float(value) for value in stored_embedding]
            except (TypeError, ValueError):
                continue
            score = cosine_similarity(resolved_query_vector, vector)
            if score < min_score:
                continue
            candidates.append(
                RetrievalResult(
                    chunk_id=chunk.id,
                    document_id=chunk.document_id,
                    text=chunk.text,
                    score=score,
                    relevance=relevance_label(score),
                )
            )
        candidates.sort(key=lambda result: result.score, reverse=True)
        return candidates[:limit]
