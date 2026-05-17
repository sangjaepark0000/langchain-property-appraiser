# Story 2.6: Source inventory 상태와 ingestion 결과 연결하기

Status: review

## Story

As a 개발자/운영자,
I want source inventory의 지원 상태와 ingestion 결과를 연결하고 싶다,
so that 어떤 source가 지원, 미지원, 보류, 적재 완료 상태인지 추적할 수 있다.

## Acceptance Criteria

1. source inventory 항목이 ingestion 대상 source 처리 결과에 따라 supported, unsupported, deferred, ingested, failed 중 적절한 상태로 기록된다.
2. unsupported source는 unsupported로 명확히 표시되고 성공 적재로 처리되지 않는다.
3. ingestion summary에서 source별 처리 상태, document 수, chunk 수, 실패 사유를 확인할 수 있다.

## Tasks / Subtasks

- [x] SourceInventoryEntry/SourceStatus 모델 추가
- [x] ingestion 결과와 source status 연결
- [x] source별 summary 출력
- [x] unsupported/failed 상태 테스트

## Dev Notes

- DB source inventory 테이블은 후속 확장으로 두고, 현재는 ingestion summary와 JSON export 가능한 dataclass 중심으로 구현한다.

## Dev Agent Record

### Agent Model Used

TBD

### Debug Log References

- `cd backend && .venv/bin/pytest` → 51 passed

### Completion Notes List

- Added source inventory status dataclass and source-level summaries.
- Ingestion now marks ingested, unsupported, and failed sources explicitly.
- CLI prints per-source status, document count, chunk count, and failure reason.

### File List

- `backend/app/services/ingest_service.py`
- `backend/scripts/ingest_file.py`
- `backend/README.md`
- `backend/tests/test_story_2_6_source_inventory.py`
