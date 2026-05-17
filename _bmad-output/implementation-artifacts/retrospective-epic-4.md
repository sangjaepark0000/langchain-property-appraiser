# Retrospective: Epic 4 Conversation Runtime + CRAG

## Completed

- Conversation/message persistence.
- Retrieval trace persistence with privacy-preserving query preview/hash.
- LangGraph conversation flow.
- Retrieval grading, deterministic query rewrite/re-retrieval, and insufficient evidence response path.
- Multi-turn `/chat` API contract and 3-turn local CRAG smoke test.

## Validation

- Final Epic 4 validation: `cd backend && .venv/bin/pytest` → 120 passed on Story 4.8 branch before merge.

## Lessons

- LangGraph state keys must be explicitly declared; unknown keys can be dropped silently.
- Local SQLite smoke paths need `Base.metadata.create_all()` and explicit model imports because Alembic targets PostgreSQL.
- Trace summaries should expose debugging signals while avoiding excessive raw query storage.

## Follow-ups

- Frontend should consume `/chat` rather than `/query` for multi-turn UX.
- Later official-data stories should add real source ingestion before relaxing insufficient-evidence behavior for legal/government questions.
