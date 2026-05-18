from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
SCRIPT = ROOT / "backend" / "scripts" / "ask_with_context.py"


def test_prompt_context_script_exists_and_does_not_require_db_ingestion():
    text = SCRIPT.read_text(encoding="utf-8")

    assert "prompt context" in text
    assert "compose_answer" in text
    assert "persist_ingested_item" not in text
    assert "ingest_paths" not in text
    assert "SessionLocal" not in text
    assert '"document_kind": "prompt_inserted_context"' in text


def test_sample_appraisal_report_readme_says_prompt_context_not_default_rag_ingestion():
    readme = (ROOT / "sample_data" / "README.md").read_text(encoding="utf-8")

    assert "prompt-inserted context tests" in readme
    assert "should not be ingested into the RAG database by default" in readme
