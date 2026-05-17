# Epic 1 Test Design: Local RAG Development Workspace

_Last updated: 2026-05-17_

## Scope

Epic 1 establishes the local-first backend workspace for the RAG application: FastAPI skeleton, safe settings, PostgreSQL/pgvector local database, SQLAlchemy/Alembic foundation, source inventory/canonical schema documentation, and local smoke/logging commands.

## Test Strategy

- Prefer fast local checks that do not require LLM, embedding, LangSmith, or external API keys.
- Keep tests deterministic and runnable in CI or a developer machine.
- Use Docker-dependent database checks only where the story explicitly requires local PostgreSQL/pgvector.
- Verify secret safety through configuration examples and log assertions where practical.

## Story-Level Test Design

### Story 1.1 — 백엔드 프로젝트 기본 골격 만들기

Primary checks:
- `backend/pyproject.toml` exists and declares a documented Python version compatible with FastAPI, LangChain, and LangGraph.
- `backend/app/main.py` exposes a FastAPI app.
- A health endpoint returns success without database, LLM, embedding, or LangSmith credentials.
- Setup documentation explains environment creation, dependency installation, and local API startup.

Suggested automated tests:
- Import app test: `from app.main import app` succeeds.
- FastAPI test client health check returns 200 and expected payload.
- Static file existence check for approved backend folders.

### Story 1.2 — 환경변수와 secret 관리 만들기

Primary checks:
- Typed settings load from environment and optional `.env` values.
- Missing optional provider keys do not fail local startup.
- `.env.example` documents database URL, LLM, embedding, LangSmith, and safe defaults.
- Real secret-like values are not committed or logged.

Suggested automated tests:
- Settings instantiate with minimal environment.
- Environment override test for a non-secret setting.
- LangSmith disabled by default when related variables are absent.

### Story 1.3 — PostgreSQL + pgvector 로컬 DB 준비하기

Primary checks:
- Docker Compose starts PostgreSQL with pgvector support.
- `.env.example` database URL matches documented compose defaults.
- Backend connectivity check reports success when DB is available.
- Connectivity failure message is clear when DB is unavailable.
- Reset procedure is documented.

Suggested automated tests:
- Static compose validation.
- Optional integration test requiring Docker: connect to database and verify `vector` extension availability.

### Story 1.4 — SQLAlchemy와 Alembic migration 기반 만들기

Primary checks:
- `backend/alembic` exists with migration configuration.
- Alembic uses the same application database settings.
- Baseline migration succeeds against local DB.
- No future domain tables are prematurely created.

Suggested automated tests:
- Alembic config imports settings without secrets.
- Optional DB integration: run `alembic upgrade head` and verify version table exists.

### Story 1.5 — Source inventory와 canonical schema 문서 초안 만들기

Primary checks:
- `docs/source-inventory.md` exists and describes supported/unsupported/deferred/sample/official/user-provided states.
- `docs/canonical-document-schema.md` exists and describes canonical fields and data modes.
- Unsupported/deferred sources are explicitly represented and not silently treated as ingested.

Suggested automated tests:
- Documentation existence checks.
- Markdown content checks for required terms: `sample`, `official`, `user_provided`, `unknown`, `unsupported`, `deferred`.

### Story 1.6 — 로컬 로그와 개발자 smoke command 만들기

Primary checks:
- Smoke command confirms backend startup/health without LLM or embedding keys.
- Startup/configuration/logging shows optional tracing disabled when absent.
- Logs do not expose secret values.
- Smoke procedure is documented for future agents.

Suggested automated tests:
- Smoke command returns zero exit code in minimal local mode.
- Captured logs contain non-sensitive status messages.
- Captured logs do not contain configured secret sentinel values.

## Epic-Level Quality Gates

Before Epic 1 is considered complete:

1. `backend` can be installed in a clean local environment using documented commands.
2. Health/smoke command succeeds with no external AI provider credentials.
3. Database-dependent checks are clearly separated from no-DB checks.
4. `.env.example` exists and contains no real secrets.
5. Local logging is useful but redacts or avoids secret values.
6. Source inventory and canonical schema documents establish data mode and unsupported/deferred handling.
7. CI/local test command is documented and repeatable.

## Risks and Mitigations

| Risk | Mitigation |
|------|------------|
| First story overbuilds future domain models | Keep Story 1.1 to skeleton/health/docs only. |
| Local startup accidentally requires provider keys | Tests instantiate app/settings with no provider keys. |
| DB checks make every test slow/flaky | Separate Docker integration checks from fast unit/static checks. |
| Secrets leak through docs or logs | Use `.env.example` placeholders and log redaction/sentinel tests. |
| Later stories lack shared schema vocabulary | Story 1.5 must document canonical schema and data modes before ingestion stories. |
