# Story 6.4: Official data ingestion smoke test 만들기

Status: review

## Story

As a 개발자,
I want 첫 official source ingestion smoke test를 만들고 싶다,
so that 공식/공개 데이터가 sample data와 구분되어 저장되는지 확인할 수 있다.

## Acceptance Criteria

1. official ingestion smoke test는 최소 하나의 official document를 canonical schema와 domain metadata 포함해 저장하고 `data_mode=official`로 표시한다.
2. official source ingestion 실패 시 실패 사유를 명확히 기록하고 실패 데이터를 official knowledge base에 포함된 것처럼 표시하지 않는다.
3. official data와 sample data가 함께 있을 때 data mode/source metadata로 구분 가능하고 RAG source lineage가 유지된다.
4. smoke는 live API credential 없이 local fixture로 실행 가능하며, live source 사용은 사전 작업으로 남긴다.

## Tasks / Subtasks

- [x] official ingestion smoke script 추가
- [x] successful official fixture ingestion 검증
- [x] invalid official fixture failure 검증
- [x] sample/official mixed data_mode 구분 검증
- [x] tests 추가

## Dev Notes

- Use local official XML fixture, not live API.

## Dev Agent Record

### Agent Model Used

TBD

### Debug Log References

- `cd backend && .venv/bin/pytest` → 155 passed

### Completion Notes List

- Added local official ingestion smoke script using recorded XML fixture.
- Smoke verifies persisted official document/chunk data_mode, domain_metadata, and source_lineage.
- Smoke verifies invalid official XML fails and is not persisted as official knowledge base.
- Smoke verifies sample and official documents can coexist and remain distinguishable.

### File List

- `backend/scripts/official_ingestion_smoke.py`
- `backend/tests/test_story_6_4_official_ingestion_smoke.py`
