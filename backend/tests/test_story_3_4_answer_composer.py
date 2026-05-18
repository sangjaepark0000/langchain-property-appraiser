def make_result(text: str, *, data_mode: str = "sample") -> dict:
    return {
        "chunk_id": 1,
        "document_id": 10,
        "chunk_index": 0,
        "text": text,
        "score": 0.91,
        "relevance": "high",
        "source_path": "sample_data/sample-property-alpha.md",
        "source_name": "sample-property-alpha.md",
        "source_url": "unknown",
        "data_mode": data_mode,
        "is_official": data_mode == "official",
        "citation": {
            "source_path": "sample_data/sample-property-alpha.md",
            "source_name": "sample-property-alpha.md",
            "data_mode": data_mode,
            "chunk_index": 0,
            "document_id": 10,
            "chunk_id": 1,
        },
    }


def test_answer_composer_extracts_answer_with_citations_and_data_mode():
    from app.rag.answer import compose_answer

    result = compose_answer("What roof color?", [make_result("Fictional Parcel Alpha has a blue roof.")])

    assert "blue roof" in result.answer
    assert result.data_mode == "sample"
    assert result.citations[0]["source_path"] == "sample_data/sample-property-alpha.md"
    assert result.fallback is True
    assert result.provider == "extractive-fallback"


def test_answer_composer_returns_insufficient_evidence_without_context():
    from app.rag.answer import compose_answer

    result = compose_answer("What official rule applies?", [])

    assert result.status == "insufficient_evidence"
    assert "근거가 부족" in result.answer
    assert result.citations == []


def test_sample_answer_is_marked_as_local_sample_not_official():
    from app.rag.answer import compose_answer

    result = compose_answer("What roof color?", [make_result("Fictional Parcel Alpha has a blue roof.")])

    assert "샘플/로컬 데이터" in result.answer
    assert "official legal conclusion" not in result.answer.lower()
    assert result.is_official is False


def test_configured_provider_is_used_through_abstraction():
    from app.rag.answer import AnswerProvider, AnswerProviderResult, compose_answer

    class StaticProvider(AnswerProvider):
        name = "static-provider"

        def generate(self, question: str, evidence: list[dict]) -> AnswerProviderResult:
            return AnswerProviderResult(answer="provider answer", provider=self.name, fallback=False)

    result = compose_answer("question", [make_result("evidence text")], provider=StaticProvider())

    assert "provider answer" in result.answer
    assert "샘플/로컬 데이터" in result.answer
    assert result.provider == "static-provider"
    assert result.fallback is False
    assert result.citations


def test_openai_answer_provider_builds_grounded_prompt_without_live_api():
    from app.rag.answer import OpenAIAnswerProvider

    class FakeResponse:
        content = "감정평가법 시행규칙 제27조는 삭제되었습니다. 법률 자문이 아닌 참고용 답변입니다."

    class FakeClient:
        def __init__(self) -> None:
            self.messages = None

        def invoke(self, messages, config=None):
            self.messages = messages
            self.config = config
            return FakeResponse()

    client = FakeClient()
    evidence = [
        {
            **make_result("제27조 삭제 <2026. 3. 12.>", data_mode="official"),
            "citation": {
                "law_name": "감정평가 및 감정평가사에 관한 법률 시행규칙",
                "article_number": "제27조",
                "effective_date": "2026-03-12",
                "revision_date": "2026-03-12",
                "source_authority": "국가법령정보센터",
                "document_kind": "current_consolidated_rule",
            },
        }
    ]

    result = OpenAIAnswerProvider(api_key="test-key", model="gpt-test", client=client).generate("제27조는?", evidence)

    assert result.provider == "langchain-openai:gpt-test"
    assert result.fallback is False
    assert client.config == {"run_name": "appraisal_law_answer"}
    assert client.messages[0][0] == "system"
    assert client.messages[1][0] == "user"
    assert "말이 되는 검토 의견" in client.messages[1][1]
    assert "확인 포인트" in client.messages[1][1]
    assert "제공된 근거만" in client.messages[1][1]
    assert "감정평가 및 감정평가사에 관한 법률 시행규칙" in client.messages[1][1]
    assert "제27조 삭제" in client.messages[1][1]


def test_get_answer_provider_uses_openai_when_configured():
    from app.core.config import Settings
    from app.rag.answer import ExtractiveFallbackAnswerProvider, OpenAIAnswerProvider, get_answer_provider

    fallback = get_answer_provider(Settings(LLM_PROVIDER="openai", LLM_API_KEY=""))
    assert isinstance(fallback, ExtractiveFallbackAnswerProvider)

    provider = get_answer_provider(Settings(LLM_PROVIDER="openai", LLM_API_KEY="test-key", LLM_MODEL="gpt-test"))
    assert isinstance(provider, OpenAIAnswerProvider)
    assert provider.model == "gpt-test"
