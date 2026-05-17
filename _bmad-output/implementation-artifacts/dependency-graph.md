# Story Dependency Graph
_Last updated: 2026-05-17T01:04:53.426999+00:00_

## Stories

| Story | Epic | Title | Sprint Status | Issue | PR | PR Status | Dependencies | Ready to Work |
|-------|------|-------|--------------|-------|----|-----------|--------------|---------------|
| 1.1 | 1 | 백엔드 프로젝트 기본 골격 만들기 | backlog | #1 | — | — | none | ✅ Yes |
| 1.2 | 1 | 환경변수와 secret 관리 만들기 | backlog | #2 | — | — | 1.1 | ❌ No (1.1 not merged) |
| 1.3 | 1 | PostgreSQL + pgvector 로컬 DB 준비하기 | backlog | #3 | — | — | 1.2 | ❌ No (1.2 not merged) |
| 1.4 | 1 | SQLAlchemy와 Alembic migration 기반 만들기 | backlog | #4 | — | — | 1.3 | ❌ No (1.3 not merged) |
| 1.5 | 1 | Source inventory와 canonical schema 문서 초안 만들기 | backlog | #5 | — | — | 1.4 | ❌ No (1.4 not merged) |
| 1.6 | 1 | 로컬 로그와 개발자 smoke command 만들기 | backlog | #6 | — | — | 1.5 | ❌ No (1.5 not merged) |
| 2.1 | 2 | Document와 Chunk 저장 모델 만들기 | backlog | #7 | — | — | none | ❌ No (epic 1 not complete) |
| 2.2 | 2 | Markdown/TXT loader와 canonical document 변환 만들기 | backlog | #8 | — | — | 2.1 | ❌ No (epic 1 not complete) |
| 2.3 | 2 | Chunking과 metadata enrichment 만들기 | backlog | #9 | — | — | 2.2 | ❌ No (epic 1 not complete) |
| 2.4 | 2 | Embedding provider abstraction과 fallback 만들기 | backlog | #10 | — | — | 2.3 | ❌ No (epic 1 not complete) |
| 2.5 | 2 | Ingestion service와 CLI smoke command 만들기 | backlog | #11 | — | — | 2.4 | ❌ No (epic 1 not complete) |
| 2.6 | 2 | Source inventory 상태와 ingestion 결과 연결하기 | backlog | #12 | — | — | 2.5 | ❌ No (epic 1 not complete) |
| 2.7 | 2 | 공식/공개 데이터 source 조사와 수집 방식 기록하기 | backlog | #13 | — | — | 2.6 | ❌ No (epic 1 not complete) |
| 3.1 | 3 | RAG smoke test용 sample knowledge fixture 만들기 | backlog | #14 | — | — | none | ❌ No (epic 1 not complete) |
| 3.2 | 3 | Vector retrieval 기본 검색 만들기 | backlog | #15 | — | — | 3.1 | ❌ No (epic 1 not complete) |
| 3.3 | 3 | Citation과 source metadata 포함 검색 결과 만들기 | backlog | #16 | — | — | 3.2 | ❌ No (epic 1 not complete) |
| 3.4 | 3 | 근거 기반 answer composer 만들기 | backlog | #17 | — | — | 3.3 | ❌ No (epic 1 not complete) |
| 3.5 | 3 | 단일 질문 RAG CLI smoke command 만들기 | backlog | #18 | — | — | 3.4 | ❌ No (epic 1 not complete) |
| 3.6 | 3 | `POST /chat` 또는 `/query` 기본 RAG API 만들기 | backlog | #19 | — | — | 3.5 | ❌ No (epic 1 not complete) |
| 3.7 | 3 | RAG response safety policy 적용하기 | backlog | #20 | — | — | 3.6 | ❌ No (epic 1 not complete) |
| 3.8 | 3 | RAG API/CLI smoke test 자동화하기 | backlog | #21 | — | — | 3.7 | ❌ No (epic 1 not complete) |
| 4.1 | 4 | Conversation과 Message 저장 모델 만들기 | backlog | #22 | — | — | none | ❌ No (epic 1 not complete) |
| 4.2 | 4 | Retrieval trace 저장 모델 만들기 | backlog | #23 | — | — | 4.1 | ❌ No (epic 1 not complete) |
| 4.3 | 4 | LangGraph conversation state 기본 흐름 만들기 | backlog | #24 | — | — | 4.2 | ❌ No (epic 1 not complete) |
| 4.4 | 4 | Retrieval grading 만들기 | backlog | #25 | — | — | 4.3 | ❌ No (epic 1 not complete) |
| 4.5 | 4 | Query rewrite와 re-retrieval 만들기 | backlog | #26 | — | — | 4.4 | ❌ No (epic 1 not complete) |
| 4.6 | 4 | Insufficient evidence 응답 경로 만들기 | backlog | #27 | — | — | 4.5 | ❌ No (epic 1 not complete) |
| 4.7 | 4 | Multi-turn chat API contract 확장하기 | backlog | #28 | — | — | 4.6 | ❌ No (epic 1 not complete) |
| 4.8 | 4 | 3턴 대화 smoke test 만들기 | backlog | #29 | — | — | 4.7 | ❌ No (epic 1 not complete) |
| 5.1 | 5 | SvelteKit frontend 초기화와 기본 레이아웃 만들기 | backlog | #30 | — | — | none | ❌ No (epic 1 not complete) |
| 5.2 | 5 | Chat input과 message list 만들기 | backlog | #31 | — | — | 5.1 | ❌ No (epic 1 not complete) |
| 5.3 | 5 | Backend chat API 연결하기 | backlog | #32 | — | — | 5.2 | ❌ No (epic 1 not complete) |
| 5.4 | 5 | Citation과 source panel 표시하기 | backlog | #33 | — | — | 5.3 | ❌ No (epic 1 not complete) |
| 5.5 | 5 | Data mode와 safety 상태 표시하기 | backlog | #34 | — | — | 5.4 | ❌ No (epic 1 not complete) |
| 5.6 | 5 | Loading, error, insufficient evidence 상태 표시하기 | backlog | #35 | — | — | 5.5 | ❌ No (epic 1 not complete) |
| 5.7 | 5 | 3턴 웹 채팅 smoke test 만들기 | backlog | #36 | — | — | 5.6 | ❌ No (epic 1 not complete) |
| 6.1 | 6 | 법령·고시 domain metadata schema 확장 설계하기 | backlog | #37 | — | — | none | ❌ No (epic 1 not complete) |
| 6.2 | 6 | 공식 source 후보 우선순위와 지원 상태 확정하기 | backlog | #38 | — | — | 6.1 | ❌ No (epic 1 not complete) |
| 6.3 | 6 | 첫 official source loader/parser 구현하기 | backlog | #39 | — | — | 6.2 | ❌ No (epic 1 not complete) |
| 6.4 | 6 | Official data ingestion smoke test 만들기 | backlog | #40 | — | — | 6.3 | ❌ No (epic 1 not complete) |
| 6.5 | 6 | 최근 X기간 필터 설계와 검색 조건 연결하기 | backlog | #41 | — | — | 6.4 | ❌ No (epic 1 not complete) |
| 6.6 | 6 | 알림 레벨을 작업 우선순위로 정의하기 | backlog | #42 | — | — | 6.5 | ❌ No (epic 1 not complete) |
| 6.7 | 6 | Domain safety policy와 response copy 정리하기 | backlog | #43 | — | — | 6.6 | ❌ No (epic 1 not complete) |

## Dependency Chains

- **1.2** depends on: 1.1
- **1.3** depends on: 1.2
- **1.4** depends on: 1.3
- **1.5** depends on: 1.4
- **1.6** depends on: 1.5
- **2.2** depends on: 2.1
- **2.3** depends on: 2.2
- **2.4** depends on: 2.3
- **2.5** depends on: 2.4
- **2.6** depends on: 2.5
- **2.7** depends on: 2.6
- **3.2** depends on: 3.1
- **3.3** depends on: 3.2
- **3.4** depends on: 3.3
- **3.5** depends on: 3.4
- **3.6** depends on: 3.5
- **3.7** depends on: 3.6
- **3.8** depends on: 3.7
- **4.2** depends on: 4.1
- **4.3** depends on: 4.2
- **4.4** depends on: 4.3
- **4.5** depends on: 4.4
- **4.6** depends on: 4.5
- **4.7** depends on: 4.6
- **4.8** depends on: 4.7
- **5.2** depends on: 5.1
- **5.3** depends on: 5.2
- **5.4** depends on: 5.3
- **5.5** depends on: 5.4
- **5.6** depends on: 5.5
- **5.7** depends on: 5.6
- **6.2** depends on: 6.1
- **6.3** depends on: 6.2
- **6.4** depends on: 6.3
- **6.5** depends on: 6.4
- **6.6** depends on: 6.5
- **6.7** depends on: 6.6

## Notes

- Initial BAD graph generated in Pi sequential fallback mode.
- Conservative dependency mapping is sequential within each epic; epic ordering blocks later epics until earlier epics are complete and merged.
- GitHub issues were created/linked for all stories using the `bad` label.
