# Story 2.3: Chunking과 metadata enrichment 만들기

Status: review

## Story

As a 개발자,
I want canonical document를 검색 가능한 chunk로 나누고 metadata를 보강하고 싶다,
so that retrieval 결과가 원본 문서와 위치 정보를 추적할 수 있다.

## Acceptance Criteria

1. Canonical document를 설정 가능한 크기의 chunk 목록으로 분할하고 각 chunk에는 chunk index와 document reference가 포함된다.
2. 각 chunk metadata에는 source path, file type, data mode, source lineage, citation 정보가 보존된다.
3. 빈 문서는 명확한 오류 또는 skipped 상태로 처리되고, 짧은 문서는 하나의 유효 chunk가 된다.

## Tasks / Subtasks

- [x] CanonicalChunk schema 추가
- [x] character 기반 configurable chunker 구현
- [x] metadata enrichment/lineage 보존
- [x] empty/short document 처리
- [x] 테스트 추가

## Dev Notes

- 기본값은 보수적으로 character chunk size 1000, overlap 100 사용.
- token chunking은 후속 최적화로 둔다.
- DB 저장은 후속 ingestion service 범위다.

## Dev Agent Record

### Agent Model Used

TBD

### Debug Log References

- `cd backend && .venv/bin/pytest` → 39 passed

### Completion Notes List

- Added CanonicalChunk schema.
- Added configurable character chunker with overlap.
- Preserved metadata, lineage, citation fields and explicit empty document error.

### File List

- `backend/app/schemas/chunk.py`
- `backend/app/ingestion/chunker.py`
- `backend/tests/test_story_2_3_chunking.py`
