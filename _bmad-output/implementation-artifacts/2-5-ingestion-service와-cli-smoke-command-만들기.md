# Story 2.5: Ingestion service와 CLI smoke command 만들기

Status: review

## Story

As a 개발자,
I want sample markdown/txt 파일을 ingestion하는 service와 CLI command를 갖추고 싶다,
so that 웹 UI 없이 문서를 지식베이스에 적재하는 흐름을 검증할 수 있다.

## Acceptance Criteria

1. sample markdown/txt ingestion CLI는 loader → chunker → metadata enrichment → embedding/fallback → DB 저장 흐름을 실행하고 처리된 document/chunk 수를 출력한다.
2. 일부 파일 실패/unsupported는 성공으로 숨기지 않고 성공/실패/unsupported 목록을 명확히 표시한다.
3. DB/debug command로 저장된 document, chunk, data mode, source lineage를 확인할 수 있다.

## Tasks / Subtasks

- [x] ingestion service 추가
- [x] DB 저장 구현
- [x] CLI smoke command 추가
- [x] debug/list command 추가
- [x] sample data 추가
- [x] 테스트 추가

## Dev Notes

- 기존 loader/chunker/embedding/model/migration 기반을 재사용한다.
- 외부 embedding key 없이 fake fallback으로 동작해야 한다.

## Dev Agent Record

### Agent Model Used

TBD

### Debug Log References

- `cd backend && .venv/bin/pytest` → 47 passed
- DB-backed ingestion smoke → 1 document, 1 chunk persisted and listed

### Completion Notes List

- Added ingestion service orchestrating loader, chunker, embedding fallback, and optional DB persistence.
- Added CLI commands for ingestion and DB inspection.
- Added sample data and README instructions.

### File List

- `backend/app/services/ingest_service.py`
- `backend/scripts/ingest_file.py`
- `backend/scripts/list_ingested.py`
- `backend/README.md`
- `sample_data/README.md`
- `sample_data/sample-property-notes.md`
- `backend/tests/test_story_2_5_ingestion_service.py`
