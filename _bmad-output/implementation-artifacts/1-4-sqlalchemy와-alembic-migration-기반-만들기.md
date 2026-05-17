# Story 1.4: SQLAlchemy와 Alembic migration 기반 만들기

Status: review

## Story

As a 개발자,
I want SQLAlchemy와 Alembic을 local database에 맞게 설정하고 싶다,
so that future RAG entities를 controlled migration으로 추가할 수 있다.

## Acceptance Criteria

1. Given 백엔드 database configuration이 있다, When Alembic을 초기화한다, Then migration configuration이 `backend/alembic` 아래에 존재한다, And migration은 애플리케이션과 동일한 database settings를 사용한다.
2. Given local database가 실행 중이다, When initial migration command를 실행한다, Then migration이 성공적으로 완료된다, And database에 현재 migration version이 기록된다.
3. Given 아직 domain table이 필요하지 않다, When baseline migration을 만든다, Then 불필요한 future table을 미리 만들지 않는다, And 이후 story에서 필요한 entity를 추가할 준비만 갖춘다.

## Tasks / Subtasks

- [x] SQLAlchemy/Alembic 의존성 추가 (AC: 1)
  - [x] SQLAlchemy 2.x 추가
  - [x] Alembic 추가
- [x] DB foundation module 생성 (AC: 1)
  - [x] `backend/app/db/base.py` 생성
  - [x] `backend/app/db/session.py` 생성
  - [x] settings의 `DATABASE_URL` 사용
  - [x] SQLAlchemy models와 Pydantic schemas 분리 원칙 유지
- [x] Alembic 설정 추가 (AC: 1, 2)
  - [x] `backend/alembic.ini` 또는 backend-local alembic config 추가
  - [x] `backend/alembic/env.py`에서 app settings와 metadata 사용
  - [x] `backend/alembic/versions/` 생성
- [x] baseline migration 추가 (AC: 2, 3)
  - [x] baseline revision 생성
  - [x] domain/future table을 만들지 않음
  - [x] `alembic upgrade head` 시 version table만 기록되게 유지
- [x] 문서 업데이트 (AC: 2)
  - [x] local DB 실행 후 migration 실행 명령 문서화
  - [x] reset 후 migration 재실행 절차 문서화
- [x] 테스트 추가/업데이트 (AC: 1, 2, 3)
  - [x] Alembic config/env가 settings와 metadata를 import하는지 정적 검증
  - [x] baseline migration이 domain table을 생성하지 않는지 검증
  - [x] 선택적 DB integration: local DB 사용 가능 시 `alembic upgrade head` 검증

## Dev Notes

### Previous Story Intelligence

Story 1.3에서 root `docker-compose.yml`, pgvector init SQL, `backend/scripts/check_db.py`, settings 기본 `DATABASE_URL`이 추가되었다. 이 story는 해당 local DB 설정을 재사용해 migration foundation만 만든다.

### Architecture Guardrails

- SQLAlchemy + Alembic은 schema modeling/migrations의 표준이다.
- `app/db/`는 database engine/session/base setup을 담당한다.
- SQLAlchemy models는 `app/models/`, Pydantic schemas는 `app/schemas/`에 분리한다.
- Alembic migrations는 `backend/alembic/` 아래에 둔다.
- 아직 상세 domain schema는 확정되지 않았으므로 baseline migration에서 future tables를 미리 만들지 않는다.

### Scope Boundaries

Do:
- SQLAlchemy/Alembic foundation, metadata/base/session, baseline empty migration, docs/tests.

Do not:
- Create documents/chunks/conversations/messages/retrieval_traces/source_inventory tables yet.
- Add ingestion/retrieval logic.
- Replace `check_db.py` with ORM-only behavior.

### Testing Requirements

- Fast tests should validate config and migration files without requiring Docker.
- Optional integration can run Alembic against local compose DB when available.

## Dev Agent Record

### Agent Model Used

TBD by dev agent

### Debug Log References

- `cd backend && .venv/bin/pytest` → 19 passed
- `docker compose up -d db && cd backend && python -m alembic -c alembic.ini upgrade head` → baseline version recorded (`20260517_0001`)

### Completion Notes List

- Added SQLAlchemy/Alembic dependencies and DB base/session foundation.
- Added Alembic environment using application settings and `Base.metadata`.
- Added empty baseline migration that creates no domain tables.
- Removed fixed Docker `container_name` to avoid conflicts across worktrees/projects.

### File List

- `docker-compose.yml`
- `backend/README.md`
- `backend/pyproject.toml`
- `backend/app/db/base.py`
- `backend/app/db/session.py`
- `backend/alembic.ini`
- `backend/alembic/env.py`
- `backend/alembic/versions/20260517_0001_baseline.py`
- `backend/tests/test_story_1_4_alembic_foundation.py`
