# Story 1.6: 로컬 로그와 개발자 smoke command 만들기

Status: ready-for-dev

## Story

As a 개발자,
I want local logging과 최소 smoke command를 갖추고 싶다,
so that 웹 UI나 외부 AI provider credentials 없이도 workspace 상태를 검증할 수 있다.

## Acceptance Criteria

1. Given 백엔드 앱이 로컬에 설치되어 있다, When health check 또는 smoke command를 실행한다, Then backend가 시작되고 응답할 수 있음을 확인한다, And LLM 또는 embedding provider key가 필요하지 않다.
2. Given 앱이 시작되거나 실패한다, When local logs를 확인한다, Then startup, configuration, database connectivity, optional tracing disabled 상태를 확인할 수 있다, And 민감한 secret 값은 출력되지 않는다.
3. Given future dev agent가 workspace를 검증해야 한다, When 문서화된 smoke test 절차를 따른다, Then ingestion 구현 전에 Epic 1 readiness를 확인할 수 있다.

## Tasks / Subtasks

- [ ] Local logging module 추가 (AC: 2)
  - [ ] `backend/app/core/logging.py` 생성
  - [ ] settings 기반 log level 적용
  - [ ] secret redaction helper 제공
  - [ ] startup/config/tracing 상태를 raw secret 없이 기록 가능하게 함
- [ ] 최소 smoke command 추가 (AC: 1, 2, 3)
  - [ ] `backend/scripts/smoke.py` 생성
  - [ ] FastAPI app import/health path 확인
  - [ ] settings summary/logging/tracing disabled 상태 확인
  - [ ] DB connectivity는 선택적으로 확인하고 실패를 명확히 표시
  - [ ] LLM/embedding provider key 없이 성공 가능해야 함
- [ ] 문서 업데이트 (AC: 3)
  - [ ] backend README에 smoke command 절차 추가
  - [ ] DB optional 여부와 no-provider-key 보장 명시
- [ ] 테스트 추가/업데이트 (AC: 1, 2, 3)
  - [ ] smoke command exit code 0 테스트
  - [ ] smoke output/log가 non-sensitive 상태 정보를 포함하는지 테스트
  - [ ] secret sentinel 값이 출력되지 않는지 테스트

## Dev Notes

### Architecture Guardrails

- Local logs are baseline observability mechanism.
- LangSmith는 optional이며 설정이 없으면 local logs만으로 동작해야 한다.
- Secret/API key/DB URL raw value는 logs/output에 노출하지 않는다.
- DB connectivity는 Story 1.3의 `check_db.py`와 settings를 재사용하되, smoke 전체를 실패시키는 hard dependency가 되면 안 된다.

### Scope Boundaries

Do:
- logging utility, smoke command, docs/tests.

Do not:
- Implement ingestion/RAG/chat smoke yet.
- Require running DB, LLM, embedding, or LangSmith for smoke success.

## Dev Agent Record

### Agent Model Used

TBD by dev agent

### Debug Log References

### Completion Notes List

### File List
