from __future__ import annotations

import re

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
    if document.data_mode == "official" and document.metadata.get("loader") == "normalized_official_source":
        official_chunks = _chunk_official_law_text(document)
        if official_chunks:
            return official_chunks
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


_BOUNDARY_RE = re.compile(r"(?m)^(제\d+조(?:의\d+)?(?:\([^\n)]*\)|\s+삭제)|부칙\s*<[^\n]+>)")
_ARTICLE_RE = re.compile(r"^(제\d+조(?:의\d+)?)(?:\(([^\n)]*)\))?")
_DELETED_RE = re.compile(r"^(제\d+조(?:의\d+)?)\s+삭제\s*<([^>]+)>")
_REVISION_RE = re.compile(r"<개정\s*([^>]+)>")
_OFFICIAL_MAX_CHARS = 6000
_OFFICIAL_OVERLAP_CHARS = 250


def _chunk_official_law_text(document: CanonicalDocument) -> list[CanonicalChunk]:
    text = document.text
    matches = list(_BOUNDARY_RE.finditer(text))
    if not matches:
        return []

    chunks: list[CanonicalChunk] = []
    for index, match in enumerate(matches):
        start = match.start()
        end = matches[index + 1].start() if index + 1 < len(matches) else len(text)
        chunk_text = text[start:end].strip()
        if not chunk_text:
            continue
        segments = _split_long_official_chunk(chunk_text, max_chars=_OFFICIAL_MAX_CHARS, overlap_chars=_OFFICIAL_OVERLAP_CHARS)
        for part_index, segment in enumerate(segments):
            segment_offset = chunk_text.find(segment[: min(len(segment), 80)])
            segment_start = start + max(segment_offset, 0)
            segment_end = segment_start + len(segment)
            chunk_index = len(chunks)
            chunk_metadata = _official_chunk_metadata(document, segment, chunk_index, segment_start, segment_end)
            if len(segments) > 1:
                chunk_metadata["chunk_part_index"] = part_index
                chunk_metadata["chunk_part_count"] = len(segments)
            lineage = {
                "source_id": document.source_id,
                "source_path": document.source_path,
                "document_source_id": document.source_id,
                "chunk_index": chunk_index,
                "char_start": segment_start,
                "char_end": segment_end,
                "article_number": chunk_metadata.get("article_number"),
                "chunk_type": chunk_metadata.get("chunk_type"),
                "chunk_part_index": chunk_metadata.get("chunk_part_index"),
                "chunk_part_count": chunk_metadata.get("chunk_part_count"),
            }
            citation = {
                "source_name": document.source_name,
                "source_path": document.source_path,
                "source_url": document.source_url,
                "data_mode": document.data_mode,
                "chunk_index": chunk_index,
                "article_number": chunk_metadata.get("article_number"),
                "article_title": chunk_metadata.get("article_title"),
            }
            chunks.append(
                CanonicalChunk(
                    document_source_id=document.source_id,
                    chunk_index=chunk_index,
                    text=segment,
                    metadata=chunk_metadata,
                    lineage=lineage,
                    citation=citation,
                    char_start=segment_start,
                    char_end=segment_end,
                )
            )
    return chunks


def _split_long_official_chunk(chunk_text: str, *, max_chars: int, overlap_chars: int) -> list[str]:
    if len(chunk_text) <= max_chars:
        return [chunk_text]
    first_line, _, body = chunk_text.partition("\n")
    prefix = first_line.strip()
    source = body.strip() if body.strip() else chunk_text
    segments: list[str] = []
    start = 0
    step = max_chars - overlap_chars
    while start < len(source):
        end = min(start + max_chars, len(source))
        if end < len(source):
            boundary = max(source.rfind("\n", start, end), source.rfind(". ", start, end), source.rfind("다.", start, end))
            if boundary > start + max_chars // 2:
                end = boundary + 1
        piece = source[start:end].strip()
        if piece:
            if prefix and not piece.startswith(prefix):
                piece = f"{prefix}\n{piece}"
            segments.append(piece)
        if end >= len(source):
            break
        start = max(end - overlap_chars, start + 1)
    return segments


def _official_chunk_metadata(
    document: CanonicalDocument, chunk_text: str, chunk_index: int, char_start: int, char_end: int
) -> dict:
    metadata = {
        **document.metadata,
        "source_path": document.source_path,
        "source_url": document.source_url,
        "source_name": document.source_name,
        "source_type": document.source_type,
        "data_mode": document.data_mode,
        "chunk_index": chunk_index,
        "char_start": char_start,
        "char_end": char_end,
    }
    domain_metadata = dict(document.metadata.get("domain_metadata") or {})
    first_line = chunk_text.splitlines()[0].strip()
    if first_line.startswith("부칙"):
        metadata["chunk_type"] = "supplementary_provision"
    else:
        metadata["chunk_type"] = "article"
        article_match = _ARTICLE_RE.match(first_line)
        if article_match:
            domain_metadata["article_number"] = article_match.group(1)
            domain_metadata["article_title"] = article_match.group(2)
            metadata["article_number"] = article_match.group(1)
            metadata["article_title"] = article_match.group(2)
        deleted_match = _DELETED_RE.match(first_line)
        if deleted_match:
            metadata["change_type"] = "deleted"
            metadata["revision_marker"] = deleted_match.group(2)
            domain_metadata["article_number"] = deleted_match.group(1)
            domain_metadata["article_title"] = None
    revision_markers = _REVISION_RE.findall(chunk_text)
    if revision_markers:
        metadata["revision_markers"] = revision_markers
    metadata["domain_metadata"] = domain_metadata
    return metadata
