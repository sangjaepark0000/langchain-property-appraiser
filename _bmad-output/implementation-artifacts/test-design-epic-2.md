# Epic 2 Test Design: Document Ingestion and Searchable Knowledge Base

## Scope

Epic 2 adds document/chunk persistence, markdown/txt loading, chunking, embedding abstraction/fallback, ingestion service/CLI smoke, source inventory state connection, and official/public source research records.

## Strategy

- Fast tests should not require external LLM/embedding keys.
- DB model/migration stories may use Docker-backed integration checks when local DB is available.
- Loader/chunker tests should use small deterministic fixtures under `sample_data/` or temporary files.
- Unsupported formats must be explicit errors/statuses, never silent skips.
- Metadata lineage and `data_mode` must survive document → chunk → persistence paths.

## Story-Level Checks

### Story 2.1 — Document와 Chunk 저장 모델 만들기

- SQLAlchemy models for `documents` and `chunks` exist.
- Alembic migration creates only the required document/chunk tables and relationships.
- Document fields include source path/name/type, data mode, ingestion status, timestamps.
- Chunk fields include text, index, lineage/metadata, and document FK.
- Migration upgrade succeeds against local DB.

### Story 2.2 — Markdown/TXT loader와 canonical document 변환 만들기

- Markdown/txt files convert to canonical document objects.
- Source path, file name, file type, and data mode are preserved.
- Unsupported file types return explicit unsupported errors.
- Loader structure supports future file type extension.

### Story 2.3 — Chunking과 metadata enrichment 만들기

- Documents split into configurable chunks.
- Chunk index, document reference, source path/type/data mode/lineage are preserved.
- Empty documents are explicit errors/skipped states.
- Short documents produce one valid chunk.

### Story 2.4 — Embedding provider abstraction과 fallback 만들기

- Embedding logic is behind a provider abstraction.
- Missing provider keys use deterministic fake/mock embeddings or explicit skip mode.
- Failures are logged/tracked without silent success.

### Story 2.5 — Ingestion service와 CLI smoke command 만들기

- Sample markdown/txt ingestion runs loader → chunker → metadata → embedding/fallback → DB save.
- CLI output includes processed documents/chunks and failure/unsupported list.
- DB/debug command can verify saved metadata and lineage.

### Story 2.6 — Source inventory 상태와 ingestion 결과 연결하기

- Source statuses support supported, unsupported, deferred, ingested, failed.
- Unsupported sources are explicit, not ingested as success.
- Summary reports source-level document/chunk counts and failure reasons.

### Story 2.7 — 공식/공개 데이터 source 조사와 수집 방식 기록하기

- Candidate official/public sources record URL, access method, format, auth/API key needs, metadata availability.
- Unsupported/deferred formats are clearly marked.
- No actual official data is represented as ingested before implementation.

## Epic Quality Gates

1. Local DB migrations for document/chunk model pass.
2. Loader/chunker preserve `data_mode`, source metadata, and lineage.
3. Ingestion smoke works without external embedding key.
4. Unsupported input is visible in output/status.
5. Official/user/sample data are not conflated.
