from __future__ import annotations

from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Literal

from sqlalchemy.orm import Session

from app.ingestion.chunker import CanonicalChunk, chunk_document
from app.ingestion.loaders import UnsupportedFileTypeError, load_document
from app.models.chunk import Chunk
from app.models.document import Document
from app.rag.embeddings import EmbeddingResult, embed_texts
from app.schemas.document import CanonicalDocument

SourceStatus = Literal["supported", "unsupported", "deferred", "ingested", "failed"]


@dataclass
class SourceInventoryEntry:
    source_path: str
    status: SourceStatus
    document_count: int = 0
    chunk_count: int = 0
    failure_reason: str | None = None

    def to_dict(self) -> dict:
        return asdict(self)


@dataclass
class IngestedItem:
    document: CanonicalDocument
    chunks: list[CanonicalChunk]
    embeddings: list[EmbeddingResult]
    persisted_document_id: int | None = None


@dataclass
class IngestionResult:
    items: list[IngestedItem] = field(default_factory=list)
    unsupported_files: list[str] = field(default_factory=list)
    failed_files: list[str] = field(default_factory=list)
    source_summaries: dict[str, SourceInventoryEntry] = field(default_factory=dict)

    @property
    def documents_processed(self) -> int:
        return len(self.items)

    @property
    def chunks_processed(self) -> int:
        return sum(len(item.chunks) for item in self.items)

    @property
    def embeddings_generated(self) -> int:
        return sum(1 for item in self.items for embedding in item.embeddings if embedding.status == "success")

    @property
    def status(self) -> str:
        if self.failed_files or self.unsupported_files:
            return "partial_success" if self.items else "failed"
        return "success"

    def to_summary_dict(self) -> dict:
        return {
            "status": self.status,
            "documents_processed": self.documents_processed,
            "chunks_processed": self.chunks_processed,
            "embeddings_generated": self.embeddings_generated,
            "sources": {source: summary.to_dict() for source, summary in self.source_summaries.items()},
        }


def persist_ingested_item(item: IngestedItem, session: Session) -> int:
    doc = item.document
    document_model = Document(
        source_id=doc.source_id,
        source_path=doc.source_path,
        source_url=doc.source_url,
        source_name=doc.source_name,
        source_type=doc.source_type,
        data_mode=doc.data_mode,
        ingestion_status="ingested",
        metadata_=doc.metadata,
    )
    session.add(document_model)
    session.flush()
    for chunk, embedding in zip(item.chunks, item.embeddings, strict=True):
        metadata = dict(chunk.metadata)
        vector = None
        if embedding.status == "success" and embedding.vector:
            vector = embedding.vector
            metadata["embedding"] = embedding.vector
            metadata["embedding_provider"] = embedding.provider
            metadata["embedding_fallback"] = embedding.fallback
        session.add(
            Chunk(
                document_id=document_model.id,
                chunk_index=chunk.chunk_index,
                text=chunk.text,
                metadata_=metadata,
                source_lineage=chunk.lineage,
                embedding=vector,
                char_start=chunk.char_start,
                char_end=chunk.char_end,
            )
        )
    item.persisted_document_id = document_model.id
    return document_model.id


def ingest_paths(
    paths: list[str | Path],
    *,
    data_mode: str = "sample",
    persist: bool = True,
    session: Session | None = None,
) -> IngestionResult:
    result = IngestionResult()
    for path in paths:
        source = Path(path)
        source_key = str(source)
        try:
            document = load_document(source, data_mode=data_mode)
            chunks = chunk_document(document)
            embeddings = embed_texts([chunk.text for chunk in chunks])
            item = IngestedItem(document=document, chunks=chunks, embeddings=embeddings)
            if persist:
                if session is None:
                    raise RuntimeError("session is required when persist=True")
                persist_ingested_item(item, session)
            result.items.append(item)
            result.source_summaries[source_key] = SourceInventoryEntry(
                source_path=source_key,
                status="ingested",
                document_count=1,
                chunk_count=len(chunks),
            )
        except UnsupportedFileTypeError as exc:
            result.unsupported_files.append(source_key)
            result.source_summaries[source_key] = SourceInventoryEntry(
                source_path=source_key,
                status="unsupported",
                failure_reason=str(exc),
            )
        except Exception as exc:
            failure = f"{source}: {exc}"
            result.failed_files.append(failure)
            result.source_summaries[source_key] = SourceInventoryEntry(
                source_path=source_key,
                status="failed",
                failure_reason=str(exc),
            )
    if persist and session is not None:
        session.commit()
    return result
