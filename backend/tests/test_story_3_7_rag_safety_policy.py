def make_sample_evidence():
    return [
        {
            "chunk_id": 1,
            "document_id": 10,
            "chunk_index": 0,
            "text": "Fictional Parcel Alpha has a blue roof.",
            "score": 0.91,
            "relevance": "high",
            "source_path": "sample_data/sample-property-alpha.md",
            "source_name": "sample-property-alpha.md",
            "source_url": "unknown",
            "data_mode": "sample",
            "is_official": False,
            "citation": {
                "source_path": "sample_data/sample-property-alpha.md",
                "source_name": "sample-property-alpha.md",
                "source_url": "unknown",
                "data_mode": "sample",
                "chunk_index": 0,
                "document_id": 10,
                "chunk_id": 1,
            },
        }
    ]


def test_official_law_question_discloses_no_official_data_without_fabrication():
    from app.rag.answer import compose_answer

    result = compose_answer("What official regulation article applies?", make_sample_evidence())

    assert "official data is not available" in result.answer.lower()
    assert "article 1" not in result.answer.lower()
    assert "effective date" not in result.answer.lower()
    assert "law.go.kr" not in result.answer.lower()


def test_legal_or_appraisal_determination_is_not_stated_as_conclusive():
    from app.rag.answer import compose_answer

    result = compose_answer("Is this appraisal legally valid and appropriate?", make_sample_evidence())

    assert "limited evidence-based assistance" in result.answer.lower()
    assert "not a legal conclusion" in result.answer.lower()
    assert "is legally valid" not in result.answer.lower()


def test_citations_only_use_retrieved_metadata_and_do_not_fabricate_url():
    from app.rag.answer import compose_answer

    result = compose_answer("What is known?", make_sample_evidence())

    assert result.citations == [make_sample_evidence()[0]["citation"]]
    assert result.citations[0]["source_url"] == "unknown"
    assert "molit.go.kr" not in str(result.citations)


def test_insufficient_evidence_official_question_mentions_no_official_data():
    from app.rag.answer import compose_answer

    result = compose_answer("국토교통부고시 기준상 적법한가?", [])

    assert result.status == "insufficient_evidence"
    assert "official data is not available" in result.answer.lower()
    assert result.citations == []
