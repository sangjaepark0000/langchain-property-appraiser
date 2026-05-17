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
    assert "insufficient" in result.answer.lower()
    assert result.citations == []


def test_sample_answer_is_marked_as_local_sample_not_official():
    from app.rag.answer import compose_answer

    result = compose_answer("What roof color?", [make_result("Fictional Parcel Alpha has a blue roof.")])

    assert "sample/local data" in result.answer
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
    assert "sample/local data" in result.answer
    assert result.provider == "static-provider"
    assert result.fallback is False
    assert result.citations
