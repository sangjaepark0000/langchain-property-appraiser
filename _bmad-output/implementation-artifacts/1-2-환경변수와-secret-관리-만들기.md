# Story 1.2: 환경변수와 secret 관리 만들기

Status: ready-for-dev

## Story

As a 개발자,
I want 애플리케이션 설정을 환경변수와 `.env` 파일에서 로드하고 싶다,
so that secret과 provider 설정을 코드에 하드코딩하지 않고 관리할 수 있다.

## Acceptance Criteria

1. Given 백엔드 애플리케이션이 시작된다, When 설정이 로드된다, Then `pydantic-settings` 또는 동등한 typed settings module을 통해 설정을 읽는다, And optional provider key가 없어도 local startup이 실패하지 않는다.
2. Given 저장소에 설정 예시가 있다, When `.env.example`을 확인한다, Then database URL, LLM provider 설정, embedding provider 설정, LangSmith 설정, safe default가 문서화되어 있다, And 실제 secret 값은 커밋되어 있지 않다.
3. Given LangSmith 설정이 없다, When 애플리케이션이 시작된다, Then tracing은 안전하게 비활성화된다, And local logging은 계속 사용할 수 있다.

## Tasks / Subtasks

- [ ] Typed settings module 추가 (AC: 1, 3)
  - [ ] `pydantic-settings` 의존성 추가
  - [ ] `backend/app/core/config.py` 생성
  - [ ] Settings class에서 env와 `.env` 로딩 지원
  - [ ] provider key와 LangSmith 설정은 optional로 선언
  - [ ] LangSmith/tracing enabled 값은 key가 없으면 false가 되도록 구현
- [ ] `.env.example` 추가 (AC: 2)
  - [ ] root `.env.example` 생성
  - [ ] database URL, LLM provider, embedding provider, LangSmith 설정 문서화
  - [ ] 실제 secret처럼 보이는 값 대신 placeholder/safe default만 사용
- [ ] FastAPI startup 안전성 유지 (AC: 1, 3)
  - [ ] `backend/app/main.py`가 settings를 import/load해도 missing optional secrets로 실패하지 않게 유지
  - [ ] health endpoint 또는 app state에 non-secret 설정 summary만 노출 가능
  - [ ] secret 값은 response/log에 노출하지 않음
- [ ] 문서 업데이트 (AC: 2, 3)
  - [ ] `backend/README.md`에 `.env.example` 복사/사용법 추가
  - [ ] LangSmith 미설정 시 tracing disabled와 local logging baseline 설명
- [ ] 테스트 추가/업데이트 (AC: 1, 2, 3)
  - [ ] minimal environment에서 settings instantiate 테스트
  - [ ] env override 테스트
  - [ ] LangSmith key 없음 → tracing disabled 테스트
  - [ ] `.env.example` 필수 키와 placeholder 안전성 테스트
  - [ ] 기존 health/import 테스트 유지

## Dev Notes

### Previous Story Intelligence

Story 1.1에서 FastAPI backend skeleton, `backend/app/core/`, `backend/app/main.py`, `backend/pyproject.toml`, `backend/README.md`, `backend/tests/`가 생성되었다. 기존 health endpoint와 no-credential startup 보장을 깨면 안 된다. [Source: `_bmad-output/implementation-artifacts/1-1-백엔드-프로젝트-기본-골격-만들기.md#Dev Agent Record`]

### Architecture Guardrails

- API key, DB URL, LangSmith key는 코드에 하드코딩하지 않는다. `.env`와 environment variables로 설정한다. 설정 관리는 `pydantic-settings`를 사용한다. [Source: `_bmad-output/planning-artifacts/architecture.md#Authentication & Security`]
- LangSmith는 optional이며, 설정이 없으면 local logs만으로 동작해야 한다. 기본적으로 민감 원문이 trace에 남지 않도록 한다. [Source: `_bmad-output/planning-artifacts/architecture.md#Authentication & Security`]
- Root `.env.example` documents required environment variables. `backend/app/core/config.py` loads settings through `pydantic-settings`. [Source: `_bmad-output/planning-artifacts/architecture.md#File Organization Patterns`]
- V1은 인증/사용자 계정/authorization을 포함하지 않는다. 이 story에서 auth 설정을 만들지 말 것. [Source: `_bmad-output/planning-artifacts/architecture.md#Authentication & Security`]

### Required Setting Concepts

Implement minimal typed settings for current and near-future stories without overbuilding:

- `app_name` / `environment` safe defaults
- `database_url` optional or safe local default documented for Story 1.3
- `llm_provider` and optional LLM API keys
- `embedding_provider` and optional embedding API keys
- `langsmith_tracing` / `langsmith_api_key` / optional project name
- local log level

Secret values must not be logged or returned by API. If a diagnostic summary is needed, expose booleans such as `has_llm_api_key`, not raw key values.

### Scope Boundaries

Do:
- Add typed config module, `.env.example`, docs, and tests.
- Keep app startup and health endpoint working without optional provider keys.
- Add `pydantic-settings` dependency only as needed for settings.

Do not:
- Add Docker Compose or require a real DB connection; Story 1.3 owns that.
- Add SQLAlchemy/Alembic; Story 1.4 owns that.
- Implement LangSmith tracing integration beyond safe config flags; later graph/logging stories can wire tracing behavior.
- Add real API keys, tokens, or user document retention policies.

### Testing Requirements

Epic 1 test design requires:
- Settings instantiate with minimal environment.
- Environment override test for a non-secret setting.
- LangSmith disabled by default when related variables are absent.
- `.env.example` documents required values with placeholders only.
[Source: `_bmad-output/implementation-artifacts/test-design-epic-1.md#Story 1.2 — 환경변수와 secret 관리 만들기`]

### References

- `_bmad-output/planning-artifacts/epics.md#Story 1.2: 환경변수와 secret 관리 만들기`
- `_bmad-output/planning-artifacts/architecture.md#Authentication & Security`
- `_bmad-output/planning-artifacts/architecture.md#File Organization Patterns`
- `_bmad-output/implementation-artifacts/test-design-epic-1.md#Story 1.2 — 환경변수와 secret 관리 만들기`

## Dev Agent Record

### Agent Model Used

TBD by dev agent

### Debug Log References

### Completion Notes List

### File List
