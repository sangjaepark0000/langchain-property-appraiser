# Story 2.1: Document와 Chunk 저장 모델 만들기

Status: review

## Story

As a 개발자,
I want 문서와 chunk를 저장할 최소 DB 모델을 만들고 싶다,
so that ingestion 결과를 source metadata와 함께 추적 가능한 형태로 저장할 수 있다.

## Acceptance Criteria

1. Given SQLAlchemy/Alembic 기반이 준비되어 있다, When document와 chunk 모델을 추가한다, Then `documents`와 `chunks` table이 migration으로 생성된다, And 각 chunk는 원본 document와 연결된다.
2. Given 문서 metadata가 필요하다, When document record를 저장한다, Then source path/name, source type, data mode, ingestion status, created timestamp를 저장할 수 있다, And data mode는 `sample`, `official`, `user_provided`, `unknown` 중 하나로 표현된다.
3. Given chunk metadata가 필요하다, When chunk record를 저장한다, Then chunk text, chunk index, source lineage, token/character range 또는 이에 준하는 위치 정보를 저장할 수 있다, And 원본 문서와의 추적 관계가 유지된다.

## Tasks / Subtasks

- [x] SQLAlchemy models 추가 (AC: 1, 2, 3)
  - [x] `backend/app/models/document.py`
  - [x] `backend/app/models/chunk.py`
  - [x] Document ↔ Chunk relationship
  - [x] data_mode와 ingestion_status enum/check 제약
- [x] Alembic migration 추가 (AC: 1)
  - [x] documents table 생성
  - [x] chunks table 생성
  - [x] FK/index 최소 구성
- [x] 테스트 추가 (AC: 1, 2, 3)
  - [x] model metadata/table/column 정적 검증
  - [x] migration이 documents/chunks를 생성하는지 검증
  - [x] local DB 가능 시 upgrade head 검증

## Dev Notes

- 기존 Alembic baseline과 DB settings를 재사용한다.
- Canonical schema 문서의 document/chunk/data_mode/lineage 필드를 반영한다.
- 아직 ingestion service는 구현하지 않는다.

## Dev Agent Record

### Agent Model Used

TBD by dev agent

### Debug Log References

- `cd backend && .venv/bin/pytest` → 31 passed
- `docker compose up -d db && cd backend && python -m alembic -c alembic.ini upgrade head` → documents/chunks created, version `20260517_0002`

### Completion Notes List

- Added Document and Chunk SQLAlchemy models with metadata, data mode, ingestion status, lineage, and relationship.
- Added Alembic migration creating `documents` and `chunks` tables.
- Updated Alembic env to import models for metadata registration.
- Adjusted baseline migration test to validate only the baseline revision now that later migrations exist.

### File List

- `backend/app/models/document.py`
- `backend/app/models/chunk.py`
- `backend/alembic/env.py`
- `backend/alembic/versions/20260517_0002_documents_chunks.py`
- `backend/tests/test_story_1_4_alembic_foundation.py`
- `backend/tests/test_story_2_1_document_chunk_models.py`
