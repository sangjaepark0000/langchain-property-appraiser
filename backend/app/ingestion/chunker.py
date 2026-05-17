from __future__ import annotations

from app.schemas.chunk import CanonicalChunk
from app.schemas.document import CanonicalDocument


class EmptyDocumentError(ValueError):
    pass


def chunk_document(
    document: CanonicalDocument,
    *,
    chunk_size: int = 1000,
    chunk_overlap: int = 100,
) -> list[CanonicalChunk]:
    if chunk_size <= 0:
        raise ValueError("chunk_size must be positive")
    if chunk_overlap < 0:
        raise ValueError("chunk_overlap must be non-negative")
    if chunk_overlap >= chunk_size:
        raise ValueError("chunk_overlap must be smaller than chunk_size")

    text = document.text
    if not text.strip():
        raise EmptyDocumentError("Cannot chunk an empty document")

    chunks: list[CanonicalChunk] = []
    step = chunk_size - chunk_overlap
    start = 0
    while start < len(text):
        end = min(start + chunk_size, len(text))
        chunk_text = text[start:end]
        chunk_index = len(chunks)
        metadata = {
            **document.metadata,
            "source_path": document.source_path,
            "source_url": document.source_url,
            "source_name": document.source_name,
            "source_type": document.source_type,
            "data_mode": document.data_mode,
            "chunk_index": chunk_index,
            "char_start": start,
            "char_end": end,
        }
        lineage = {
            "source_id": document.source_id,
            "source_path": document.source_path,
            "document_source_id": document.source_id,
            "chunk_index": chunk_index,
            "char_start": start,
            "char_end": end,
        }
        citation = {
            "source_name": document.source_name,
            "source_path": document.source_path,
            "source_url": document.source_url,
            "data_mode": document.data_mode,
            "chunk_index": chunk_index,
        }
        chunks.append(
            CanonicalChunk(
                document_source_id=document.source_id,
                chunk_index=chunk_index,
                text=chunk_text,
                metadata=metadata,
                lineage=lineage,
                citation=citation,
                char_start=start,
                char_end=end,
            )
        )
        if end == len(text):
            break
        start += step
    return chunks
