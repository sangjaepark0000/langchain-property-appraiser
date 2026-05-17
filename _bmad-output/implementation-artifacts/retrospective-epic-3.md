# Epic 3 Retrospective: Evidence-Based RAG Answering and Smoke Tests

Date: 2026-05-17
Status: complete

## Completed Scope

Epic 3 delivered a local-first RAG core from sample fixtures through retrieval, answer composition, API, CLI, and smoke automation:

- RAG smoke sample knowledge fixtures and expected questions.
- Basic vector retrieval over stored chunk metadata embeddings.
- Citation/source metadata hydration for retrieval results.
- Evidence-based answer composer with deterministic extractive fallback.
- Single-question RAG CLI smoke command.
- `POST /query` RAG API response contract.
- Deterministic response safety policy.
- Automated API/CLI RAG smoke test script.
- pgvector-backed `chunks.embedding vector(16)` storage with metadata fallback retained.

## Validation Summary

Final local validation after Story 3.8:

- `cd backend && .venv/bin/pytest` → 84 passed
- `scripts/rag_smoke.py` is covered by automated tests and validates sample ingestion, CLI query, API contract, no evidence, and official hallucination checks.

## What Went Well

- RAG core now runs without external LLM or embedding credentials.
- Data mode and citation metadata are explicit throughout retrieval, answer, CLI, and API paths.
- Safety policy prevents sample/local data from being presented as official legal or appraisal conclusions.
- Automated smoke testing gives a stable regression base before CRAG/multi-turn work.

## Risks / Follow-ups

- Retrieval now has a PostgreSQL/pgvector storage/search path, while sqlite/local smoke still uses Python cosine fallback.
- Answer composer is extractive fallback, not a full LLM provider integration.
- API currently exposes basic `/query`; multi-turn conversation context is not implemented yet.
- Embedding dimension is currently `16` for local fake embeddings; real provider integration may require a dimension migration or provider-specific vector columns.
- Official source ingestion remains deferred, so official/legal answers must remain guarded.

## Recommended Next Steps

1. Start Epic 4 by adding Conversation and Message persistence models.
2. Add migration and tests carefully because this changes DB schema.
3. Keep RAG response contract stable while layering conversation runtime on top.
