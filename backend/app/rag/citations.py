from __future__ import annotations

from typing import Any

from sqlalchemy.orm import Session

from app.models.chunk import Chunk
from app.rag.retriever import RetrievalResult

UNKNOWN = "unknown"


def _fallback(*values: Any) -> Any:
    for value in values:
        if value is None:
            continue
        if isinstance(value, str) and not value.strip():
            continue
        return value
    return UNKNOWN


def hydrate_retrieval_results(session: Session, results: list[RetrievalResult]) -> list[dict[str, Any]]:
    hydrated: list[dict[str, Any]] = []
    for result in results:
        chunk = session.get(Chunk, result.chunk_id)
        if chunk is None or chunk.document is None:
            continue
        document = chunk.document
        chunk_metadata = chunk.metadata_ or {}
        document_metadata = document.metadata_ or {}
        chunk_domain_metadata = chunk_metadata.get("domain_metadata") or {}
        document_domain_metadata = document_metadata.get("domain_metadata") or {}
        lineage = chunk.source_lineage or {}

        source_path = _fallback(chunk_metadata.get("source_path"), document.source_path, document_metadata.get("source_path"))
        source_name = _fallback(chunk_metadata.get("source_name"), document.source_name, document_metadata.get("source_name"))
        source_url = _fallback(chunk_metadata.get("source_url"), document.source_url, document_metadata.get("source_url"))
        data_mode = _fallback(chunk_metadata.get("data_mode"), document.data_mode, document_metadata.get("data_mode"))
        chunk_index = _fallback(chunk_metadata.get("chunk_index"), lineage.get("chunk_index"), chunk.chunk_index)
        law_name = _fallback(
            chunk_domain_metadata.get("law_name"),
            chunk_metadata.get("law_name"),
            document_domain_metadata.get("law_name"),
            document_metadata.get("law_name"),
            source_name,
        )
        article_number = _fallback(
            chunk_metadata.get("article_number"), chunk_domain_metadata.get("article_number"), lineage.get("article_number")
        )
        article_title = _fallback(chunk_metadata.get("article_title"), chunk_domain_metadata.get("article_title"))
        effective_date = _fallback(
            chunk_domain_metadata.get("effective_date"), chunk_metadata.get("effective_date"), document_domain_metadata.get("effective_date")
        )
        revision_date = _fallback(
            chunk_domain_metadata.get("revision_date"), chunk_metadata.get("revision_date"), document_domain_metadata.get("revision_date")
        )
        source_authority = _fallback(
            chunk_domain_metadata.get("source_authority"),
            chunk_metadata.get("source_authority"),
            document_domain_metadata.get("source_authority"),
            document_metadata.get("source_authority"),
        )

        citation = {
            "source_path": source_path,
            "source_name": source_name,
            "source_url": source_url,
            "data_mode": data_mode,
            "chunk_index": chunk_index,
            "document_id": document.id,
            "chunk_id": chunk.id,
            "law_name": law_name,
            "article_number": article_number,
            "article_title": article_title,
            "effective_date": effective_date,
            "revision_date": revision_date,
            "source_authority": source_authority,
            "corpus_group": _fallback(chunk_metadata.get("corpus_group"), document_metadata.get("corpus_group")),
            "law_level": _fallback(chunk_metadata.get("law_level"), document_metadata.get("law_level")),
            "document_kind": _fallback(chunk_metadata.get("document_kind"), document_metadata.get("document_kind")),
            "chunk_type": _fallback(chunk_metadata.get("chunk_type"), lineage.get("chunk_type")),
            "change_type": _fallback(chunk_metadata.get("change_type")),
            "revision_marker": _fallback(chunk_metadata.get("revision_marker")),
        }
        hydrated.append(
            {
                "chunk_id": chunk.id,
                "document_id": document.id,
                "chunk_index": chunk_index,
                "text": result.text,
                "score": result.score,
                "relevance": result.relevance,
                "source_path": source_path,
                "source_name": source_name,
                "source_url": source_url,
                "data_mode": data_mode,
                "is_official": data_mode == "official",
                "citation": citation,
                "metadata": chunk_metadata,
                "source_lineage": lineage,
            }
        )
    return hydrated
