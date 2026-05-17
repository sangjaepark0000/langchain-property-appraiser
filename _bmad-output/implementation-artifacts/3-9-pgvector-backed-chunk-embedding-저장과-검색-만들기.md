# Story 3.9: pgvector-backed chunk embedding 저장과 검색 만들기

Status: ready-for-dev

## Story

As a 개발자,
I want chunk embedding을 pgvector column에 저장하고 PostgreSQL/pgvector 검색 경로를 사용할 수 있게 하고 싶다,
so that RAG retrieval이 smoke용 JSON metadata fallback에서 production-oriented vector storage로 발전할 수 있다.

## Acceptance Criteria

1. `chunks` 테이블에 pgvector embedding column이 추가되고 Alembic migration으로 관리된다.
2. ingestion persistence는 embedding을 기존 metadata fallback과 pgvector column 양쪽에 저장한다.
3. retriever는 PostgreSQL/pgvector dialect에서는 vector column 검색 경로를 우선 사용하고, sqlite/local smoke에서는 기존 metadata cosine fallback을 유지한다.
4. embedding dimension은 설정으로 노출되며 기본 local fake embedding dimension과 일치한다.
5. 테스트와 문서는 pgvector path와 fallback path를 모두 명확히 검증/설명한다.

## Tasks / Subtasks

- [ ] pgvector dependency와 설정 추가
- [ ] portable SQLAlchemy vector type 추가
- [ ] chunks.embedding model/migration 추가
- [ ] ingestion persistence vector column 저장
- [ ] PostgreSQL pgvector search path + metadata fallback 구현
- [ ] tests/docs 업데이트

## Dev Notes

- 기본 dimension은 fake embedding 기본값인 16으로 둔다.
- SQLite tests는 JSON-backed fallback type으로 유지한다.
- HNSW index는 migration에 포함하되 PostgreSQL/pgvector 전용으로 둔다.

## Dev Agent Record

### Agent Model Used

TBD

### Debug Log References

### Completion Notes List

### File List
