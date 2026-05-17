import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
SAMPLE_DIR = ROOT / "sample_data"
QUESTIONS = SAMPLE_DIR / "rag-smoke-questions.json"


def test_sample_data_has_at_least_two_rag_knowledge_files():
    files = [p for p in SAMPLE_DIR.iterdir() if p.suffix in {".md", ".txt"} and p.name != "README.md"]

    assert len(files) >= 2
    for path in files:
        text = path.read_text(encoding="utf-8")
        assert "SAMPLE DATA ONLY" in text
        assert "not official" in text.lower()


def test_sample_documents_contain_explicit_retrieval_facts():
    combined = "\n".join(path.read_text(encoding="utf-8") for path in SAMPLE_DIR.glob("sample-*.md"))

    assert "Fictional Parcel Alpha" in combined
    assert "blue roof" in combined
    assert "Fictional Parcel Beta" in combined
    assert "north access road" in combined


def test_expected_smoke_questions_include_citations_and_no_evidence_case():
    questions = json.loads(QUESTIONS.read_text(encoding="utf-8"))

    assert any(q["expected_source_path"].endswith("sample-property-alpha.md") for q in questions)
    assert any(q["expected_source_path"].endswith("sample-property-beta.md") for q in questions)
    no_evidence = [q for q in questions if q["expected_outcome"] == "insufficient_evidence"]
    assert no_evidence
    assert no_evidence[0]["expected_source_path"] is None


def test_sample_fixture_does_not_claim_official_ingestion():
    combined = "\n".join(path.read_text(encoding="utf-8") for path in SAMPLE_DIR.iterdir() if path.is_file())

    forbidden = ["official knowledge base", "실제 감정평가", "법적 효력", "국토교통부고시"]
    for phrase in forbidden:
        assert phrase not in combined
