from __future__ import annotations

import math
import re
from dataclasses import dataclass
from typing import TYPE_CHECKING

from sqlalchemy import text as sql_text
from sqlalchemy.orm import Session

from app.models.chunk import Chunk
from app.models.document import Document  # noqa: F401 - ensure relationship registration
from app.rag.embeddings import EmbeddingProvider, get_embedding_provider

if TYPE_CHECKING:
    from app.rag.recent_filter import RecentPeriodFilter


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
        recent_filter: "RecentPeriodFilter | None" = None,
    ) -> list[RetrievalResult]:
        if limit <= 0:
            return []
        resolved_query_vector = query_vector
        if resolved_query_vector is None:
            embedding = self.embedding_provider.embed_text(query)
            if embedding.status != "success" or not embedding.vector:
                return []
            resolved_query_vector = embedding.vector

        if self.session.bind is not None and self.session.bind.dialect.name == "postgresql":
            pgvector_results = self._search_pgvector(resolved_query_vector, limit=limit, min_score=min_score)
            pgvector_results = self._merge_lexical_article_results(query, pgvector_results, limit=limit, min_score=min_score)
            if pgvector_results:
                if recent_filter is not None:
                    from app.rag.recent_filter import apply_recent_period_filter

                    return apply_recent_period_filter(self.session, pgvector_results, recent_filter).results
                return pgvector_results

        candidates: list[RetrievalResult] = []
        for chunk in self.session.query(Chunk).all():
            stored_embedding = chunk.embedding or (chunk.metadata_.get("embedding") if chunk.metadata_ else None)
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
        candidates = self._merge_lexical_article_results(query, candidates, limit=limit, min_score=min_score)
        limited = candidates[:limit]
        if recent_filter is not None:
            from app.rag.recent_filter import apply_recent_period_filter

            return apply_recent_period_filter(self.session, limited, recent_filter).results
        return limited

    def _merge_lexical_article_results(
        self, query: str, results: list[RetrievalResult], *, limit: int, min_score: float
    ) -> list[RetrievalResult]:
        article_numbers = set(re.findall(r"제\s*(\d+)\s*조(?:의\s*(\d+))?", query))
        normalized_articles = {
            f"제{number}조" + (f"의{sub}" if sub else "") for number, sub in article_numbers
        }
        if not normalized_articles:
            return results
        result_by_id = {result.chunk_id: result for result in results}
        lexical_results: list[RetrievalResult] = []
        law_hint = _law_hint(query)
        article_chunks = [
            chunk
            for chunk in self.session.query(Chunk).all()
            if (chunk.metadata_ or {}).get("article_number") in normalized_articles
        ]
        if law_hint:
            hinted_chunks = [chunk for chunk in article_chunks if chunk.document is not None and law_hint in chunk.document.source_name]
            if hinted_chunks:
                article_chunks = hinted_chunks
        for chunk in article_chunks:
            document_name = chunk.document.source_name if chunk.document is not None else ""
            score = 1.1 if law_hint and law_hint in document_name else 1.01
            if score < min_score:
                continue
            lexical_result = RetrievalResult(
                chunk_id=chunk.id,
                document_id=chunk.document_id,
                text=chunk.text,
                score=score,
                relevance=relevance_label(score),
            )
            if chunk.id in result_by_id:
                result_by_id[chunk.id] = lexical_result
            else:
                lexical_results.append(lexical_result)
        merged = [*lexical_results, *result_by_id.values()]
        merged.sort(key=lambda result: result.score, reverse=True)
        return merged[:limit]

    def _search_pgvector(self, query_vector: list[float], *, limit: int, min_score: float) -> list[RetrievalResult]:
        vector_literal = "[" + ",".join(str(float(value)) for value in query_vector) + "]"
        rows = self.session.execute(
            sql_text(
                """
                SELECT id, document_id, text, 1 - (embedding <=> CAST(:query_vector AS vector)) AS score
                FROM chunks
                WHERE embedding IS NOT NULL
                ORDER BY embedding <=> CAST(:query_vector AS vector)
                LIMIT :limit
                """
            ),
            {"query_vector": vector_literal, "limit": limit},
        ).mappings()
        results: list[RetrievalResult] = []
        for row in rows:
            score = round(float(row["score"]), 6)
            if score < min_score:
                continue
            results.append(
                RetrievalResult(
                    chunk_id=int(row["id"]),
                    document_id=int(row["document_id"]),
                    text=str(row["text"]),
                    score=score,
                    relevance=relevance_label(score),
                )
            )
        return results


def _law_hint(query: str) -> str | None:
    if "시행규칙" in query:
        return "시행규칙"
    if "시행령" in query:
        return "시행령"
    if "감정평가에 관한 규칙" in query:
        return "감정평가에 관한 규칙"
    if "법률" in query or "감정평가법" in query:
        return "감정평가 및 감정평가사에 관한 법률"
    return None
