---
stepsCompleted: [1, 2]
inputDocuments: []
session_topic: '최근 개정 법규 중심의 감정평가 서류 위반 가능성 점검 AI 웹 서비스'
session_goals: 'LangChain/LangGraph 학습용 MVP 아이디어 구체화, 채팅 가능한 웹 서비스 설계, 법률 리스크를 낮춘 검토 보조 범위 정의, 최근 변경 법규 우선 점검 흐름 탐색'
selected_approach: 'progressive-flow'
techniques_used: ['Question Storming', 'Mind Mapping', 'SCAMPER Method', 'Solution Matrix']
ideas_generated: []
context_file: ''
---

# Brainstorming Session Results

**Facilitator:** PSJ
**Date:** 2026-05-15

## Session Overview

**Topic:** 최근 개정 법규 중심의 감정평가 서류 위반 가능성 점검 AI 웹 서비스

**Goals:** LangChain/LangGraph를 실제로 사용해보며 감을 잡기 위한 학습용 MVP를 구체화한다. 수익화 목적은 아니며, 감정평가사가 작성한 서류를 업로드하고 채팅으로 질의응답할 수 있는 웹 서비스를 만든다. 특히 기존 법규 전반을 완벽히 판단하기보다 최근 개정된 법규를 우선 점검하여 변경사항 미반영, 누락, 위반 가능성, 검토 필요 지점을 찾아주는 방향을 탐색한다.

### Context Guidance

별도 컨텍스트 파일은 제공되지 않았다.

### Session Setup

사용자는 토지감정평가사가 작성한 서류가 최근 변경된 법규 또는 현행 법규에 위반될 가능성이 있는지 확인해주는 서비스를 아이디어로 제시했다. 법률적 책임 및 고소 위험을 고려하여 서비스는 확정적 법률 판단이 아니라 검토 보조, 위험 신호 탐지, 관련 조항과 개정사항 근거 제시, 전문가 최종 확인을 돕는 형태가 적합하다.

핵심 초점은 전체 법규를 완벽히 판정하는 것보다, 비교적 오류 가능성이 낮은 기존 법규 검토는 보조로 두고, 최근 바뀐 법규와 문서 내용 간의 불일치 가능성을 우선 탐지하는 것이다.

## Technique Selection

**Approach:** Progressive Technique Flow
**Journey Design:** 전문가 지식이 없어도 답할 수 있도록, 정답 도출이 아니라 질문·가설·리서치 항목·MVP 선택지로 전환한다.

**Progressive Techniques:**

- **Phase 1 - Exploration:** Question Storming으로 사용자가 답을 몰라도 되는 질문과 가설을 넓게 도출
- **Phase 2 - Pattern Recognition:** Mind Mapping으로 기능군, 리스크, 데이터 소스, 구현 흐름을 묶기
- **Phase 3 - Development:** SCAMPER Method로 최근 개정 법규 우선 점검 MVP를 구체화
- **Phase 4 - Action Planning:** Solution Matrix로 구현 선택지를 비교하고 LangGraph 구조로 정리

**Journey Rationale:** 사용자는 법규 전문가가 아니므로, 브레인스토밍은 전문 답변을 요구하지 않고 제품/구현 관점의 선택지를 만드는 방식으로 진행한다. 모르는 항목은 리서치 필요로 분리하고, 첫 MVP는 사용자가 감정평가 서류와 최근 개정 법규 자료를 함께 업로드해 비교 검토하는 구조를 우선 고려한다.

## Technique Execution Notes

### Direction Change: RAG 기반 개정 법규 수집/처리 포함

사용자는 개정 법규를 사용자가 매번 업로드하는 방식보다는, 시스템이 관련 개정 법규를 크롤링/API 수집하여 RAG 지식베이스로 보유해야 한다고 명확히 했다. 따라서 MVP는 단순 문서 비교형에서 **데이터 수집 파이프라인 + RAG 기반 감정평가 서류 점검 챗봇**으로 확장된다.

**Captured Ideas:**

**[Data #1]: Official Law Source Registry**
_Concept_: 국가법령정보센터, 법제처, 국토교통부 고시/행정규칙, 관보 등 공식 출처 후보를 소스 레지스트리로 관리한다.
_Novelty_: 법률 검토 AI의 신뢰성을 LLM 답변이 아니라 출처 메타데이터와 공식 원문 링크로 확보한다.

**[Data #2]: Amendment-First RAG Pipeline**
_Concept_: 전체 법령보다 최근 개정/시행/공포된 자료를 우선 수집하고, 개정일·시행일·조항·출처 URL 메타데이터를 붙여 임베딩한다.
_Novelty_: 일반 법률 RAG가 아니라 “최근 변경사항 감지”에 최적화된 RAG로 범위를 좁힌다.

**[Data #3]: Crawl-to-RAG Processing Graph**
_Concept_: crawler → parser → amendment extractor → chunker → metadata enricher → embedding → vector DB ingestion 과정을 별도 LangGraph/배치 파이프라인으로 만든다.
_Novelty_: 사용자 채팅 그래프와 데이터 갱신 그래프를 분리하여 학습용으로도 구조가 명확하다.
