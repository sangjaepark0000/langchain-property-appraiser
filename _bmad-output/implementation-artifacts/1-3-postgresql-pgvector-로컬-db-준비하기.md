# Story 1.3: PostgreSQL + pgvector 로컬 DB 준비하기

Status: ready-for-dev

## Story

As a 개발자,
I want Docker Compose로 PostgreSQL과 pgvector 로컬 데이터베이스를 실행하고 싶다,
so that RAG metadata와 vector-ready storage를 일관된 local 환경에서 개발할 수 있다.

## Acceptance Criteria

1. Given 로컬에 Docker가 사용 가능하다, When 문서화된 compose 명령을 실행한다, Then PostgreSQL이 pgvector 지원과 함께 시작된다, And 연결 정보는 `.env.example`에 문서화된 값과 일치한다.
2. Given database container가 실행 중이다, When backend가 database connectivity를 확인한다, Then 설정된 database URL로 연결할 수 있다, And 연결 실패 시 명확한 local error message를 제공한다.
3. Given 개발자가 local state를 reset해야 한다, When 문서화된 절차를 따른다, Then local database를 중지, 제거, 재생성하는 방법을 명확히 알 수 있다.

## Tasks / Subtasks

- [ ] Docker Compose 기반 local DB 추가 (AC: 1)
  - [ ] root `docker-compose.yml` 생성
  - [ ] PostgreSQL + pgvector 지원 image 사용
  - [ ] persistent volume과 local port 정의
  - [ ] pgvector extension 초기화 SQL 추가
- [ ] `.env.example` 연결 정보 정합성 보장 (AC: 1)
  - [ ] compose database/user/password/db name과 `DATABASE_URL` 일치
  - [ ] 민감 real secret 없이 local-only safe defaults 사용
- [ ] DB connectivity check 추가 (AC: 2)
  - [ ] backend script 또는 command로 settings의 `DATABASE_URL` 사용
  - [ ] 연결 성공 시 pgvector extension 사용 가능 여부 확인
  - [ ] 연결 실패 시 host/port/db 설정 확인을 유도하는 명확한 error message 제공
- [ ] reset/run 문서 추가 (AC: 1, 3)
  - [ ] DB 시작/중지/로그/상태 확인 명령 문서화
  - [ ] volume 포함 reset 절차 문서화
- [ ] 테스트 추가/업데이트 (AC: 1, 2, 3)
  - [ ] compose 파일이 pgvector image/volume/port/init SQL을 포함하는지 정적 검증
  - [ ] `.env.example` DATABASE_URL과 compose 값이 일치하는지 검증
  - [ ] connectivity script가 missing/invalid DB에서 명확한 에러 메시지를 반환하는지 검증

## Dev Notes

### Previous Story Intelligence

Story 1.2에서 `backend/app/core/config.py`의 typed settings와 root `.env.example`이 추가되었다. DB connectivity는 이 settings의 `database_url`을 사용해야 하며, secret 값을 로그/응답에 노출하지 않아야 한다.

### Architecture Guardrails

- V1은 PostgreSQL을 기본 relational database로 사용하고 vector storage는 PostgreSQL 확장인 pgvector를 사용한다.
- PostgreSQL + pgvector는 local development DB로 Docker Compose를 통해 실행한다.
- `docker-compose.yml`은 root에 둔다.
- Root `.env.example`이 required environment variables를 문서화한다.
- SQLAlchemy/Alembic은 Story 1.4 범위이므로 이 story에서는 raw connectivity/smoke 수준만 구현한다.

### Scope Boundaries

Do:
- Docker Compose, pgvector init SQL, DB connectivity script, docs, static tests.

Do not:
- Add SQLAlchemy models, sessions, Alembic, migrations, document/chunk tables.
- Require DB for normal FastAPI startup/health endpoint.
- Add production Dockerization or cloud deployment.

### Testing Requirements

- Fast tests should not require Docker.
- Docker/DB integration checks may be documented/manual or skipped unless DB is available.
- Failure path must be tested without requiring a running DB.

## Dev Agent Record

### Agent Model Used

TBD by dev agent

### Debug Log References

### Completion Notes List

### File List
