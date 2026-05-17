---
stepsCompleted: ["step-01-init", "step-02-discovery", "step-02b-vision", "step-02c-executive-summary", "step-03-success", "step-04-journeys", "step-05-domain", "step-06-innovation", "step-07-project-type", "step-08-scoping", "step-09-functional", "step-10-nonfunctional", "step-11-polish"]
inputDocuments:
  - "_bmad-output/brainstorming/brainstorming-session-2026-05-15-151738.md"
documentCounts:
  productBriefs: 0
  research: 0
  brainstorming: 1
  projectDocs: 0
classification:
  projectType: web_app
  domain: legaltech / regtech 성격의 감정평가 업무 보조
  complexity: high
  projectContext: greenfield
  productFraming: RAG 챗봇 중심의 법령 변경 검토 보조 웹 MVP
workflowType: 'prd'
releaseMode: phased
---

# Product Requirements Document - langchain-property-appraiser

**Author:** PSJ  
**Date:** 2026-05-15

## Executive Summary

본 제품은 LangChain/LangGraph 기반 멀티턴 RAG 챗봇을 완성하며 배우고, 향후 상품화 가능한 구조로 확장하기 위한 웹 애플리케이션이다. 장기 도메인 예시는 감정평가 업무의 법령·고시 변경 검토 보조다. 사용자는 자연어로 지식베이스를 질의하고, 답변의 근거 문서 조각, 출처, 메타데이터, 데이터 모드를 확인할 수 있다.

제품의 1차 목표는 감정평가 도메인 완성보다 RAG Core, CRAG, 멀티턴 상태 관리, source inventory, loader/parser 확장성, 웹 채팅 연결을 검증하는 것이다. 개발 순서는 Discovery & Skeleton → RAG Core → LangGraph CRAG API → Svelte Web Chat → Domain Data Integration → Productization이다.

도메인 확장 시 제품은 법률 위반 여부나 감정평가 적정성을 단정하지 않는다. 최근 X기간 이내 개정·시행된 법령/고시, 시행일·평가기준일 차이, 구 조항 표현, 출처 불명확성, 근거 부족 상태를 자연어 대화로 짚어주는 검토 보조 도구로 작동한다. 알림 레벨은 위법/적법 판단이 아니라 작업 우선순위다.

공식 법령/고시 데이터, 출처 URL, 개정일, 시행일, 실제 업무 문서는 임의 생성하지 않는다. 공개/공식 지식베이스 자료는 source inventory를 통해 조사·수집·색인하고, 사용자 업무 문서는 사용자가 명시적으로 입력하거나 업로드한 경우에만 처리한다. 테스트/샘플 데이터 기반 응답은 공식 법령 검토 결과처럼 표시하지 않는다.

### What Makes This Special

이 제품의 가치는 AI가 전문 판단을 대신하는 데 있지 않다. RAG 시스템을 만들고 고치며 배울 수 있는 구조를 제공하고, 도메인 확장 시 사용자가 익숙한 업무에서 놓칠 수 있는 변경사항·날짜 조건·근거 부족 지점을 대화 중에 드러내는 데 있다.

챗봇은 버튼 중심 워크플로우가 아니라 자연어 멀티턴 대화를 주 인터페이스로 사용한다. 사용자는 후속 질문, 필터 조정, 검토 이력 기록, 참고용 초안 요청을 자연어로 수행할 수 있다. CRAG 흐름은 검색 결과가 부족하거나 부정확할 때 질의를 보정하고, 충분한 근거가 없으면 단정하지 않는다.

### Project Classification

- **Project Type:** Web application
- **Domain:** Legaltech / Regtech 성격의 감정평가 업무 보조
- **Complexity:** High
- **Project Context:** Greenfield
- **Primary Interface:** 자연어 멀티턴 RAG 챗봇; 알림 카드와 출처 패널은 보조 표시 요소
- **Core Technical Direction:** FastAPI, Svelte, LangChain, LangGraph, 선택적 LangSmith, DB/vector store 기반 RAG
- **RAG Pattern Goals:** 멀티턴 RAG, Corrective RAG(CRAG), 출처 기반 답변, 검색 품질 보정, 대화 상태 관리
- **Learning / Commercialization Goal:** 향후 다른 도메인에도 적용 가능한 RAG 챗봇 구조 연습·검증

## Success Criteria

### User Success

초기 사용자는 웹 UI 이전에도 CLI 또는 백엔드 API로 문서를 로딩하고 자연어 질문에 대한 근거 기반 답변을 받을 수 있다. 이후 동일한 RAG/CRAG 흐름을 Svelte 웹 채팅 UI에서 멀티턴 대화로 사용할 수 있다.

사용자는 답변이 어떤 문서 조각을 근거로 삼았는지 확인할 수 있다. 근거가 부족한 경우 시스템은 단정하지 않고 “근거 부족” 또는 추가 정보 필요 상태로 응답한다.

감정평가 도메인 기능은 공식 데이터 또는 사용자가 제공한 업무 자료가 확보된 뒤 확장한다. 도메인 데이터가 없는 상태에서는 시스템이 감정평가 법령 검토 결과처럼 가장하지 않는다.

### Business Success

1차 성공은 감정평가 도메인 검증보다 LangChain, LangGraph, CRAG, 멀티턴 RAG, 문서 로딩·청킹·임베딩·검색 파이프라인을 구현하고, 웹 상품화 가능한 RAG 챗봇 구조를 확보하는 것이다.

감정평가 도메인은 장기 적용 예시로 유지한다. 초기 구현은 도메인 무관 문서에서도 동작하는 범용 RAG 챗봇 기반을 우선하며, 이후 법령/고시/규정 변경 검토, 사내 문서 Q&A, 전문직 문서 검토로 확장 가능해야 한다.

### Technical Success

- 도메인 무관 markdown/txt 문서를 로딩하고 청킹·메타데이터 부여·임베딩·벡터 저장소 적재를 수행한다.
- 목표 데이터 소스의 실제 제공 형식을 조사하고 source inventory를 작성한다.
- 지식베이스 자료와 사용자 업무 문서를 데이터 모델, 메타데이터, 보관 정책에서 분리한다.
- LangGraph 기반 챗봇은 멀티턴 대화 상태, 검색 결과 관련성 평가, 질의 재작성, 재검색, 출처 기반 답변, 근거 부족 응답을 지원한다.
- RAG Core는 웹 UI보다 먼저 CLI 또는 백엔드 API 수준에서 검증된다.
- 테스트/샘플 데이터 모드에서는 공식 데이터가 아님을 답변 또는 UI에 명확히 표시하고 silent fallback을 허용하지 않는다.

### Measurable Outcomes

- markdown/txt 문서 2개 이상을 로딩·청킹·임베딩·벡터 저장소 적재할 수 있다.
- CLI 또는 백엔드 API에서 자연어 질문을 입력하면 근거 문서 조각과 함께 답변을 반환한다.
- 검색 결과가 질문과 관련 없거나 부족한 경우 CRAG 흐름이 질의 재작성 또는 재검색을 1회 이상 수행한다.
- 재검색 후에도 근거가 부족하면 단정 답변 대신 “근거 부족” 상태로 응답한다.
- 최소 3턴 이상의 후속 대화에서 이전 질문, 현재 주제, 참조 문서 맥락을 유지한다.
- 데이터 소스 후보별 제공 형식과 필수 메타데이터를 정리한 source inventory를 작성한다.
- 지원하지 않는 지식베이스 소스 형식은 source inventory에 unsupported/deferred 상태로 기록한다.
- 웹 UI는 RAG Core 검증 이후 동일한 질의/응답 흐름을 자연어 채팅으로 제공한다.

## Product Scope

### MVP - Minimum Viable Product

MVP는 감정평가 도메인 데모보다 RAG Core 구현을 우선한다. 첫 단계는 문서 로딩·청킹·임베딩·검색, 멀티턴 대화 상태 관리, CRAG 기반 검색 품질 보정, 출처 포함 답변, 근거 부족 응답을 CLI 또는 백엔드 API 수준에서 구현하는 것이다.

두 번째 단계는 검증된 RAG Core를 Svelte 웹 채팅 UI에 연결하는 것이다. 웹 UI는 자연어 멀티턴 대화를 중심으로 하며, 출처/근거와 데이터 모드 표시를 보조적으로 제공한다.

감정평가/법령 도메인 기능은 세 번째 단계로 둔다. 공개/공식 법령·고시 자료는 source inventory를 통해 조사·수집·색인하고, 공식 법령/고시 데이터, API 접근 권한, 실제 또는 비식별 사용자 업무 문서가 확보된 뒤 최근 X기간 필터, 알림 레벨, 확인/메모 이력, 법령 변경 검토 보조 흐름을 확장한다.

### Growth Features (Post-MVP)

- 공식 법령/고시 데이터 수집 파이프라인
- 국가법령정보센터 API 또는 다운로드 파일 연동
- 국토교통부 고시/훈령/예규 데이터 확장
- XML/HTML/JSON 등 구조화 데이터 loader/parser 확장
- 최근 X기간 필터와 알림 레벨 분류
- 자연어 확인/무시/메모 이력 저장
- 프론트엔드 PDF/DOCX 텍스트 추출
- 세션별 리포트 다운로드
- 사용자별 사건 관리

### Vision (Future)

장기적으로는 감정평가뿐 아니라 법령·규정·기준 변경을 주기적으로 확인해야 하는 전문직 업무 전반에 적용 가능한 RAG 챗봇 플랫폼으로 확장한다. 사용자는 자연어 대화를 통해 익숙한 반복 업무에서 놓칠 수 있는 변경사항과 날짜 조건을 확인하고, 검토 근거와 이력을 남길 수 있다.

## User Journeys

### Journey 1: 개발자/빌더가 RAG Core를 완성하며 구조를 학습한다

PSJ는 LangChain과 LangGraph로 실제 동작하는 RAG 챗봇을 만들고 싶다. 단순 튜토리얼이 아니라, 나중에 상품화 가능한 구조를 직접 완성하면서 배우는 것이 목표다. 처음에는 감정평가 도메인 데이터가 없어도 괜찮다. 중요한 것은 문서 로딩, 청킹, 임베딩, 검색, CRAG, 멀티턴 상태 관리가 서로 어떻게 연결되는지 체감하는 것이다.

PSJ는 markdown/txt 문서를 ingestion pipeline에 넣는다. 시스템은 문서를 canonical document schema로 변환하고, chunk metadata를 붙이고, vector store에 저장한다. 이후 CLI 또는 API에서 자연어 질문을 던지면 시스템은 관련 chunk를 검색하고 출처와 함께 답변한다.

검색 결과가 부정확하거나 근거가 부족할 수 있다. PSJ는 LangGraph 흐름에서 retrieval grading, query rewrite, re-retrieval, insufficient evidence response가 어떻게 동작하는지 확인한다. 성공 순간은 챗봇이 단순히 답하는 것이 아니라 검색 실패와 근거 부족 상태까지 설명 가능한 흐름으로 처리되는 것을 확인하는 때다.

### Journey 2: 개발자/빌더가 RAG 시스템을 수정·확장한다

첫 번째 동작 버전이 완성된 뒤, PSJ는 markdown/txt 이후 HTML, JSON, XML 문서를 처리하거나 source inventory에 조사된 법령/고시 자료를 추가하려 한다.

PSJ는 기존 코드를 크게 뜯어고치지 않고 새로운 loader/parser를 추가한다. 모든 loader는 공통 document schema를 반환하므로 chunker, embedder, retriever, LangGraph 챗봇 흐름은 그대로 재사용된다. 지원하지 않는 형식은 silent failure하지 않고 source inventory에 unsupported/deferred로 기록된다.

성공 순간은 새로운 문서 형식을 추가해도 전체 RAG 흐름이 깨지지 않고, 데이터 소스·형식·메타데이터·검색 결과를 명확히 추적할 수 있는 때다.

### Journey 3: 개발자/빌더가 API와 DB 스키마를 설계하고 검증한다

PSJ는 RAG 챗봇을 웹 서비스로 확장 가능한 애플리케이션으로 만들고 싶다. 이 과정에서 documents, chunks, conversations, messages, retrieval traces, source inventory, user notes 같은 데이터를 어떻게 DB에 모델링할지 확인한다.

V1은 Python/FastAPI 기반 단일 스택을 기본 후보로 둔다. SQLAlchemy/SQLModel과 migration 도구를 사용해 RAG 시스템의 핵심 데이터를 저장하는 스키마를 설계한다. 지식베이스 자료와 사용자 업무 문서를 분리하고, 멀티턴 대화, 검색 결과, CRAG 평가 결과, 근거 chunk, 사용자 메모가 추적 가능하도록 저장 구조를 검증한다.

Ruby on Rails와 관련 gem은 대안으로 검토할 수 있지만, V1에서는 LangChain/LangGraph 학습 목표와 구현 단순성을 우선한다.

### Journey 4: 미래 전문직 사용자가 자연어로 문서 검토 보조를 받는다

미래의 감정평가사 또는 전문직 사용자는 익숙한 반복 업무 중 놓칠 수 있는 변경사항이 걱정된다. 사용자는 복잡한 버튼 플로우 대신 “최근 1년 안에 이 문서와 관련해서 바뀐 게 있어?”라고 자연어로 묻는다.

시스템은 사용자가 제공한 문서 또는 사건 정보와 RAG 지식베이스를 바탕으로 관련 가능성이 있는 변경사항을 찾아준다. 답변은 단정적 판단이 아니라 변경된 조항, 날짜, 출처, 근거 부족 여부, 작업 우선순위 레벨을 함께 제공한다.

사용자는 “왜 우선 확인이야?”, “그 조항 쉽게 설명해줘”, “이건 확인했다고 메모해줘”처럼 후속 대화를 이어간다. 성공 순간은 사용자가 “평소처럼 지나칠 수 있던 지점을 챗봇이 짚어줬고, 확인했다는 기록도 남겼다”고 느끼는 때다.

### Journey 5: 운영자가 지식베이스 소스를 조사하고 관리한다

시스템 운영자 또는 개발자는 RAG 지식베이스에 넣을 공개/공식 자료를 조사한다. 국가법령정보센터, 법제처, 국토교통부 고시/훈령/예규, 기타 공식 자료의 접근 방식, 제공 형식, 메타데이터 제공 여부를 확인한다.

운영자는 `docs/source-inventory.md`에 각 소스의 URL, 접근 방식, 파일 형식, 필수 메타데이터, 우선순위, loader 지원 상태, 보류 사유를 기록한다. 지원 가능한 소스는 ingestion pipeline에 연결하고, 지원하기 어려운 소스는 deferred/unsupported 상태로 남긴다.

성공 순간은 RAG 지식베이스의 범위와 한계가 투명하게 관리되고, “무엇이 들어갔고 무엇이 아직 안 들어갔는지”를 설명할 수 있는 때다.

### Journey Requirements Summary

- 문서 로딩, 청킹, 메타데이터 부여, 임베딩, 벡터 저장소 적재
- canonical document schema
- loader/parser 확장 구조
- source inventory 관리
- API 기반 RAG Core 실행 경로
- DB schema 설계와 migration 기반 변경 관리
- documents, chunks, conversations, messages, retrieval traces 저장
- 지식베이스 자료와 사용자 업무 문서의 데이터 모델 분리
- LangGraph 기반 멀티턴 상태 관리
- CRAG 기반 검색 결과 평가, 질의 재작성, 재검색, 근거 부족 응답
- 출처/근거 포함 답변
- 샘플/테스트 데이터와 공식 데이터 구분
- 자연어 중심 웹 채팅 UI
- 도메인 레이어를 후순위로 붙일 수 있는 구조

## Domain-Specific Requirements

### Compliance & Regulatory

- 시스템은 법률 위반 여부, 감정평가 적정성, 법적 책임 가능성을 단정하지 않는다.
- 모든 법령/고시 관련 답변은 최근 변경사항 기반의 검토 보조 정보이며, 최종 법률·전문적 판단은 사용자 또는 관련 전문가 책임임을 명시한다.
- 법률 문구나 보완 의견을 생성하는 경우에도 참고용 초안으로 표시하며, 시스템이 최종 제출 문안의 적법성이나 적정성을 보증하지 않는다.
- 공식 법령/고시 데이터, 출처 URL, 개정일, 시행일은 임의 생성하지 않는다. 실제 데이터가 없으면 테스트/샘플 데이터 모드로 표시한다.

### Technical Constraints

- 법령/고시 답변에는 가능한 경우 원문 출처, 법령명/자료명, 조항, 개정일, 시행일, 수집일을 분리하여 표시한다.
- 평가기준일, 작성일, 제출일, 개정일, 시행일을 혼동하지 않도록 데이터 모델과 답변 문구에서 명확히 구분한다.
- 지식베이스 자료와 사용자 업무 문서는 데이터 모델, 메타데이터, 보관 정책에서 분리한다.
- 사용자 업무 문서는 사용자가 명시적으로 입력하거나 업로드한 경우에만 처리한다.
- 사용자 업무 문서 처리 시 원본 저장 여부, 삭제 가능 여부, 외부 LLM provider 전송 여부를 명확히 해야 한다.
- V1은 민감정보 리스크를 줄이기 위해 테스트 문서 또는 사용자가 확인한 텍스트 입력을 우선 지원한다.

### Integration Requirements

- RAG 지식베이스 자료는 공개/공식 자료를 우선 대상으로 하며, source inventory를 통해 접근 방식, 제공 형식, 필수 메타데이터, loader/parser 지원 상태를 관리한다.
- 국가법령정보센터 API, 법제처/국토교통부 자료, 고시/훈령/예규 등은 후속 도메인 확장 시 source inventory에 등록하고 처리 가능성을 평가한다.
- 구조화된 XML/HTML/JSON 소스는 우선 지원 후보로 고려하고, PDF/DOCX/HWP/OCR 기반 자료는 필요성과 구현 난이도에 따라 후순위로 둔다.

### Risk Mitigations

- 검색 결과가 부족하거나 출처가 불명확하면 시스템은 단정 답변 대신 “근거 부족”, “출처 확인 필요”, “추가 자료 필요” 상태로 응답한다.
- 지원하지 않는 파일 형식이나 데이터 소스는 조용히 누락하지 않고 source inventory에 unsupported/deferred 상태로 기록한다.
- 샘플/테스트 데이터 기반 응답은 공식 법령 검토 결과처럼 표시하지 않는다.
- 알림 레벨은 위법/적법 판단이 아니라 작업 우선순위로 정의한다.
- 챗봇은 자연어 대화를 허용하되, 법률 판단을 보증하는 표현과 출처 없는 단정적 설명을 피한다.

## Web App Specific Requirements

### Project-Type Overview

본 제품은 자연어 멀티턴 RAG 챗봇을 제공하는 웹 애플리케이션이다. V1은 감정평가 도메인 완성보다 RAG Core 검증과 웹 연결을 우선하며, FastAPI 기반 API 서버와 Svelte 기반 웹 채팅 UI를 중심으로 구현한다.

### Technical Architecture Considerations

- 백엔드는 Python/FastAPI 기반으로 구현한다.
- 프론트엔드는 Svelte 또는 SvelteKit 기반의 얇은 웹 채팅 클라이언트로 구현한다.
- LangChain은 문서 로딩, 청킹, 임베딩, 검색/RAG 구성에 사용한다.
- LangGraph는 멀턴 대화 상태, CRAG 흐름, 검색 결과 평가, 질의 재작성, 근거 부족 응답을 오케스트레이션한다.
- DB는 documents, chunks, conversations, messages, retrieval traces, source inventory 상태를 저장할 수 있어야 한다.
- Vector store는 RAG Core 검증에 적합한 로컬 또는 PostgreSQL/pgvector 계열을 우선 검토한다.
- 웹 UI는 자연어 채팅을 주 인터페이스로 하며, 출처/근거/데이터 모드는 보조적으로 표시한다.
- LangSmith는 개발/디버깅용 선택적 observability 도구로 사용한다.

### Browser Matrix

- V1은 최신 Chrome/Edge 데스크톱 브라우저를 우선 지원한다.
- 모바일 브라우저 및 구형 브라우저 최적화는 후순위로 둔다.

### Responsive Design

- V1은 데스크톱 중심 레이아웃으로 시작한다.
- 채팅 영역, 답변 영역, 출처/근거 표시 영역이 작은 화면에서 깨지지 않는 수준의 기본 반응형만 요구한다.

### Performance Targets

- 소규모 문서 기준 ingestion은 개발자가 CLI/API로 실행 가능한 수준이면 충분하다.
- 채팅 응답은 스트리밍이 없어도 동작해야 하며, 장시간 작업은 상태 메시지를 제공해야 한다.
- 검색/답변 과정에서 retrieval trace를 남겨 디버깅 가능해야 한다.

### SEO Strategy

- SEO는 V1 요구사항이 아니다.
- 제품은 공개 콘텐츠 사이트가 아니라 내부/학습용 RAG 챗봇에 가깝다.

### Accessibility Level

- 기본 키보드 입력, 명확한 오류 메시지, 읽기 쉬운 답변 구조, 데이터 모드 표시를 지원한다.
- 고급 접근성 인증 수준은 V1 범위가 아니다.

### Frontend Requirements

- Svelte 프론트는 채팅 입력, 메시지 목록, 답변 출력, 출처/근거 표시, 데이터 모드 표시, 근거 부족/오류 상태 표시, 로딩 상태, 세션 ID 유지를 포함한다.
- 버튼 중심 워크플로우가 아니라 자연어 대화를 주 인터페이스로 한다.
- 알림 카드나 출처 패널은 대화 이해를 돕는 보조 표시 요소로만 사용한다.
- 로그인, 복잡한 대시보드, 알림 카드 UI, 고급 문서 업로드, 관리자 화면, 모바일 최적화는 후속 범위로 둔다.

### Observability Requirements

- LangSmith 설정이 제공되면 LangGraph node transition, retrieval, CRAG grading/rewrite, answer generation을 trace할 수 있어야 한다.
- LangSmith 설정이 없거나 비활성화된 경우에도 시스템은 로컬 로그만으로 정상 동작해야 한다.
- 민감한 사용자 업무 문서 원문은 기본적으로 trace에 남기지 않는다.
- 개발 모드에서만 retrieval count, rewritten query, trace id 같은 디버그 정보를 선택적으로 확인할 수 있다.

### Implementation Considerations

- RAG Core는 웹 UI보다 먼저 CLI 또는 API 레벨에서 검증한다.
- Svelte 프론트는 검증된 FastAPI chat/query API를 호출하는 얇은 클라이언트로 시작한다.
- API 응답에는 답변 텍스트뿐 아니라 참조 chunk, 출처, 데이터 모드, 근거 부족 여부, retrieval trace 요약을 포함할 수 있어야 한다.
- 실시간 스트리밍은 후순위이며, 필요 시 SSE를 우선 검토한다.
- Ruby on Rails와 관련 gem은 대안으로 검토할 수 있으나 V1 기본 스택에서는 제외한다.

## Project Scoping & Phased Development

### MVP Strategy & Philosophy

**MVP Approach:** 학습 중심의 RAG Core vertical slice를 먼저 완성하고, 이후 API, 웹 채팅 UI, 도메인 데이터 레이어를 단계적으로 확장한다.

**Resource Requirements:** 1인 개발 기준으로 진행 가능해야 하며, 핵심 역량은 Python/FastAPI, LangChain, LangGraph, Svelte, DB/Vector Store, 기본 문서 처리와 RAG 디버깅이다.

Phase 0은 장기 리서치가 아니라 개발이 헛돌지 않게 하는 짧은 정찰/골격 단계다. 공식 API 키나 모든 데이터 소스 확보가 없어도 Phase 1로 진행할 수 있어야 한다.

### MVP Feature Set (Phase 0-3)

#### Phase 0: Discovery & Skeleton

**Scope:**
- source inventory 초안 작성
- 데이터 소스 형식 조사
- canonical document schema 초안 작성
- DB/vector store 후보 결정 또는 임시 선택
- FastAPI/Svelte 프로젝트 골격 생성
- LangSmith optional 설정 계획
- `.env.example` 작성
- `README.md` 초기 실행법 작성

**Exit Criteria:**
- `docs/source-inventory.md` 초안이 존재한다.
- `docs/canonical-document-schema.md` 초안이 존재한다.
- FastAPI/Svelte 프로젝트 skeleton이 생성된다.
- `.env.example`과 초기 실행 README가 존재한다.
- 공식 API 키나 모든 데이터 소스가 없어도 다음 단계로 진행 가능하다.

#### Phase 1: RAG Core Vertical Slice

**Scope:**
- markdown/txt ingestion
- 청킹, 메타데이터 부여, 임베딩
- vector store 저장
- retriever 구현
- source 포함 답변 생성
- CLI 또는 API smoke test

**Exit Criteria:**
- markdown/txt 문서 2개 이상을 ingestion할 수 있다.
- 자연어 질문을 입력하면 source 포함 답변을 받을 수 있다.
- 검색된 chunk와 답변 근거를 개발자가 확인할 수 있다.

#### Phase 2: LangGraph CRAG API

**Scope:**
- 멀티턴 대화 state
- retrieval grading
- query rewrite
- re-retrieval
- insufficient evidence response
- FastAPI chat/query endpoint
- LangSmith optional tracing

**Exit Criteria:**
- 최소 3턴 이상의 대화에서 이전 문맥을 유지한다.
- 근거 부족 케이스에서 query rewrite 또는 insufficient evidence 응답을 확인할 수 있다.
- LangSmith가 설정된 경우 주요 LangGraph node transition과 retrieval/rewrite/answer 흐름을 trace할 수 있다.
- LangSmith가 없어도 로컬 로그 기반으로 정상 동작한다.

#### Phase 3: Svelte Chat UI

**Scope:**
- 채팅 입력/메시지 목록
- 출처/근거 표시
- 데이터 모드 표시
- 로딩/오류/근거 부족 상태 표시
- 세션 ID 유지
- FastAPI chat/query API 연결

**Exit Criteria:**
- 브라우저에서 자연어 질문을 입력하고 답변을 받을 수 있다.
- 최소 3턴 이상의 대화를 웹 UI에서 이어갈 수 있다.
- 답변에 출처/근거와 데이터 모드가 표시된다.
- 근거 부족/오류 상태가 사용자에게 명확히 표시된다.

### Post-MVP Features

#### Phase 4: Domain Data Integration

**Scope:**
- source inventory 기반 처리 가능 법령/고시 소스 ingestion
- 최근 X기간 필터
- 알림 레벨 초안
- 지식베이스 자료와 사용자 업무 문서 분리
- 도메인별 답변 정책 적용

**Exit Criteria:**
- 법령/고시 source 하나 이상이 ingestion되거나 unsupported/deferred로 명확히 기록된다.
- 최근 X기간 필터가 검색 또는 후처리에 반영된다.
- 알림 레벨이 위법 판단이 아니라 작업 우선순위로 표시된다.

#### Phase 5: Productization

**Scope:**
- 공식 API/다운로드 자동화
- XML/HTML/JSON/PDF/DOCX/HWP 등 고급 loader/parser 확장
- 사용자별 사건 관리
- 확인/메모/리포트 이력 관리
- 배포/운영 흐름 정리

**Exit Criteria:**
- 공식 데이터 수집 또는 다운로드 흐름이 자동화된다.
- 사용자별 세션/사건/이력 관리가 가능하다.
- 배포와 운영에 필요한 설정, 로그, 데이터 관리 절차가 정리된다.

### Risk Mitigation Strategy

**Technical Risks:** RAG, CRAG, LangGraph, DB/vector store, 웹 UI를 한 번에 구현하면 범위가 커진다. 이를 줄이기 위해 Phase 0-3을 작게 나누고, RAG Core가 CLI/API에서 검증된 뒤 웹 UI를 붙인다.

**Market Risks:** 감정평가 도메인 데이터와 실제 사용자 자료가 없으면 도메인 효용 검증이 어렵다. 초기에는 도메인 검증보다 RAG 챗봇 상품화 패턴 학습을 성공 기준으로 두고, 도메인 레이어는 source inventory와 공식 자료 확보 이후 확장한다.

**Resource Risks:** 1인 개발자가 모든 기능을 동시에 구현하기 어렵다. 각 phase는 독립적인 exit criteria를 가지며, 공식 API 연동, 고급 문서 형식, 사용자 관리, 리포트 기능은 후순위로 둔다.

## Functional Requirements

### Knowledge Source Management

- FR1: 개발자/운영자는 RAG 지식베이스 후보 소스의 출처, 접근 방식, 제공 형식, 필수 메타데이터, 우선순위, 처리 상태를 관리할 수 있다.
- FR2: 시스템은 지식베이스 자료, 사용자 업무 문서, 테스트/샘플 자료를 구분하고 현재 데이터 모드를 표시할 수 있다.
- FR3: 시스템은 지원 가능한 소스와 미지원/보류 소스를 구분하며, 미지원 소스를 조용히 누락하지 않고 상태로 기록할 수 있다.

### Ingestion & Retrieval

- FR4: 개발자는 지원 문서 형식을 로딩하고 공통 document schema로 변환할 수 있다.
- FR5: 시스템은 문서를 검색 가능한 단위로 분할하고 메타데이터와 원본 source lineage를 유지한 채 지식베이스에 적재할 수 있다.
- FR6: 사용자는 자연어 질문으로 지식베이스를 검색하고 근거 기반 답변을 받을 수 있다.
- FR7: 시스템은 답변에 참조 문서 조각, 출처, 메타데이터, 데이터 모드 정보를 포함할 수 있다.

### Multi-Turn CRAG Conversation

- FR8: 사용자는 멀티턴 대화를 통해 후속 질문, 문맥 기반 요청, 필터 조정, 검토 이력 기록, 참고용 초안 요청을 자연어로 수행할 수 있다.
- FR9: 시스템은 CRAG 흐름을 통해 검색 결과의 충분성을 평가하고, 필요한 경우 질의 보정·재검색·근거 부족 응답을 수행할 수 있다.
- FR10: 시스템은 대화 메시지, 참조 문서 조각, 질의 보정 이력, 근거 부족 원인을 추적할 수 있다.

### Web Chat Experience

- FR11: 사용자는 웹 화면에서 버튼 중심 워크플로우가 아닌 자연어 멀티턴 RAG 챗봇을 사용할 수 있다.
- FR12: 시스템은 웹 화면에서 메시지, 출처/근거, 데이터 모드, 로딩, 오류, 근거 부족 상태를 표시할 수 있다.

### Safety & Domain Extension

- FR13: 시스템은 법률 위반 여부, 감정평가 적정성, 법적 책임 가능성을 단정하지 않고 참고용 검토 보조로 응답할 수 있다.
- FR14: 시스템은 제공되지 않은 실제 업무 문서나 공식 법령 데이터를 임의 생성해 실제 자료처럼 가장하지 않는다.
- FR15: 시스템은 법령/고시 도메인 확장을 위해 법령명, 조항, 개정일, 시행일, 수집일, 출처 URL, 최근 X기간 필터, 알림 레벨을 지원할 수 있다.

### Developer Workflow & Observability

- FR16: 개발자는 웹 UI 없이 RAG Core smoke test를 실행할 수 있다.
- FR17: 개발자는 RAG/CRAG/LangGraph 실행 흐름과 주요 중간 결과를 로컬 로그 또는 선택적 tracing 도구로 확인할 수 있다.

## Non-Functional Requirements

### Performance

- NFR1: 소규모 문서 세트 기준 ingestion과 RAG 질의는 개발 중 반복 실행 가능한 수준으로 완료되어야 한다.
- NFR2: 장시간 실행되는 ingestion, retrieval, answer generation 작업은 사용자 또는 개발자가 멈춤과 진행 중을 구분할 수 있는 상태를 제공해야 한다.

### Security & Privacy

- NFR3: API key, LangSmith key, LLM provider key 등 비밀값은 코드나 문서 본문에 하드코딩하지 않아야 한다.
- NFR4: 민감한 사용자 업무 문서 원문은 기본적으로 외부 tracing 로그에 남기지 않아야 한다.
- NFR5: 사용자 업무 문서 원문을 외부 LLM 또는 tracing 도구에 전송하는 경우, 전송 여부와 범위가 설정으로 통제 가능해야 한다.

### Reliability & Failure Handling

- NFR6: 지원하지 않는 문서 형식이나 데이터 소스는 조용히 누락하지 않고 unsupported/deferred 또는 명확한 오류 상태로 기록되어야 한다.
- NFR7: 검색 근거가 부족한 경우 시스템은 단정 답변 대신 근거 부족 상태로 응답해야 한다.
- NFR8: 공식 데이터가 없는 경우 시스템은 공식 법령 검토 결과처럼 응답하지 않아야 한다.
- NFR9: LangSmith 또는 외부 tracing 설정이 없어도 RAG Core와 웹 챗봇은 정상 동작해야 한다.

### Observability & Debuggability

- NFR10: 개발자는 ingestion, retrieval, grading, rewrite, answer generation의 주요 실행 단계와 실패 원인을 확인할 수 있어야 한다.
- NFR11: LangSmith가 설정된 경우 LangGraph node transition과 RAG/CRAG 중간 결과를 추적할 수 있어야 하며, 비활성화된 경우에도 로컬 로그로 주요 실행 상태를 확인할 수 있어야 한다.

### Maintainability & Extensibility

- NFR12: loader/parser는 새로운 문서 형식을 추가해도 기존 RAG 흐름을 크게 변경하지 않도록 공통 schema 기반으로 확장 가능해야 한다.
- NFR13: 지식베이스 자료와 사용자 업무 문서는 데이터 모델과 보관 정책에서 분리되어야 한다.
- NFR14: RAG Core, Web Chat, Domain Layer는 단계적으로 교체 또는 확장 가능하도록 결합도를 낮게 유지해야 한다.

### Accessibility & Usability

- NFR15: 웹 채팅 UI는 키보드 입력, 읽기 쉬운 메시지 구조, 명확한 로딩/오류/근거 부족 상태 표시를 제공해야 한다.
