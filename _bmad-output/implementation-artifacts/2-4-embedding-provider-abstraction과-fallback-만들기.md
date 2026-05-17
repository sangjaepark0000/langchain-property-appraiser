# Story 2.4: Embedding provider abstraction과 fallback 만들기

Status: review

## Story

As a 개발자,
I want embedding 생성 로직을 provider abstraction 뒤에 두고 key가 없을 때 fallback을 제공하고 싶다,
so that local smoke test가 외부 provider credentials 때문에 막히지 않는다.

## Acceptance Criteria

1. 설정된 provider를 통해 chunk embedding을 생성할 수 있고 provider-specific 코드는 ingestion service에 직접 섞이지 않는다.
2. provider key가 없으면 local smoke mode에서 deterministic fake/mock embedding 또는 명확한 skip mode를 사용할 수 있고 상태가 명확히 표시된다.
3. embedding 생성 실패 원인이 기록되고 partial success/failure 상태가 추적 가능하다.

## Tasks / Subtasks

- [x] Embedding provider protocol/result 추가
- [x] deterministic fake embedding provider 추가
- [x] provider factory 추가
- [x] failure/skip 상태 표현
- [x] 테스트 추가

## Dev Notes

- 실제 외부 provider 연동은 최소화/후속 확장 가능 구조로 둔다.
- 기본 local mode는 외부 key 없이 deterministic fake embedding을 사용한다.

## Dev Agent Record

### Agent Model Used

TBD

### Debug Log References

- `cd backend && .venv/bin/pytest` → 43 passed

### Completion Notes List

- Added embedding provider protocol and result object.
- Added deterministic fake embedding fallback.
- Added provider factory and partial failure tracking helper.

### File List

- `backend/app/rag/embeddings.py`
- `backend/tests/test_story_2_4_embeddings.py`
