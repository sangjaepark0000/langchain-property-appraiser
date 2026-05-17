# Epic 2 Retrospective: Ingestion Foundation and Source Inventory

Date: 2026-05-17
Status: complete

## Completed Scope

Epic 2 delivered the ingestion foundation needed before RAG answering:

- Document and Chunk persistence models with Alembic migration.
- Markdown/TXT canonical document loaders.
- Configurable character chunking with metadata, lineage, and citation fields.
- Embedding provider abstraction with deterministic local fake fallback.
- Ingestion service and CLI smoke/debug commands.
- Source-level ingestion status summaries.
- Official/public source inventory research with official data kept deferred/not ingested.

## Validation Summary

Final local validation after Story 2.7:

- `cd backend && .venv/bin/pytest` → 55 passed
- Story 2.5 DB-backed ingestion smoke verified persistence/listing of one document and one chunk.

## What Went Well

- Incremental story sequence worked cleanly: model → loader → chunker → embedding → service → inventory.
- Local fake embedding fallback removed external credential dependency from smoke flows.
- Source status summaries prevent unsupported/deferred files from being silently treated as successful ingestion.
- Official source research remained documentation-only, avoiding premature mixing of sample and official data.

## Risks / Follow-ups

- Current chunking is character-based; token-aware chunking may be needed before production quality retrieval.
- Embeddings are deterministic fake values until a real provider is wired.
- Official source ingestion requires XML/API loader, HTML notice parser, and API key handling.
- PDF/DOCX/HWP/OCR support remains out of MVP ingestion scope.
- Vector persistence/search is not yet implemented and belongs to Epic 3.

## Recommended Next Steps

1. Start Epic 3 with sample RAG knowledge fixtures.
2. Keep `data_mode=sample` explicit until official ingestion stories are implemented.
3. Add vector storage/retrieval only after fixture docs and answer smoke tests are in place.
