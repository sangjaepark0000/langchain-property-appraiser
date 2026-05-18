import subprocess
import sys
from pathlib import Path

from app.ingestion.chunker import chunk_document
from app.ingestion.official_sources import load_normalized_official_source, parse_source_notes


ROOT = Path(__file__).resolve().parents[2]
BACKEND_ROOT = ROOT / "backend"
NORMALIZED = ROOT / "official_sources" / "normalized"


def test_parse_source_notes_classifies_framework_and_standards_separately():
    rule_notes = parse_source_notes(NORMALIZED / "appraisal_act_enforcement_rule" / "source-notes.md")
    standards_notes = parse_source_notes(NORMALIZED / "appraisal_standards_rule" / "source-notes.md")

    assert rule_notes["corpus_group"] == "appraisal_act_framework"
    assert rule_notes["law_level"] == "enforcement_rule"
    assert rule_notes["effective_date"] == "2026-03-12"
    assert standards_notes["corpus_group"] == "appraisal_standards"
    assert standards_notes["document_kind"] == "appraisal_method_rule"


def test_downloaded_enforcement_rule_chunks_by_article_and_detects_deleted_article():
    document = load_normalized_official_source(NORMALIZED / "appraisal_act_enforcement_rule")
    chunks = chunk_document(document)

    assert document.data_mode == "official"
    assert document.metadata["domain_metadata"]["source_authority"] == "국가법령정보센터"
    assert len(chunks) > 20
    deleted = [chunk for chunk in chunks if chunk.metadata.get("article_number") == "제27조"]
    assert deleted
    assert deleted[0].metadata["change_type"] == "deleted"
    assert deleted[0].metadata["domain_metadata"]["revision_date"] == "2026-03-12"
    assert "제27조 삭제" in deleted[0].text


def test_downloaded_official_chunks_are_small_enough_for_openai_embedding_context():
    for source_dir in NORMALIZED.iterdir():
        if not source_dir.is_dir() or not (source_dir / "extracted.txt").exists():
            continue
        chunks = chunk_document(load_normalized_official_source(source_dir))
        assert chunks
        assert max(len(chunk.text) for chunk in chunks) <= 6250


def test_ingest_official_sources_script_loads_four_official_documents_without_live_api(tmp_path):
    db_path = tmp_path / "official-downloaded.db"
    result = subprocess.run(
        [
            sys.executable,
            str(BACKEND_ROOT / "scripts" / "ingest_official_sources.py"),
            "--source-root",
            str(NORMALIZED),
        ],
        cwd=BACKEND_ROOT,
        text=True,
        capture_output=True,
        timeout=60,
        env={"DATABASE_URL": f"sqlite+pysqlite:///{db_path}", "LANGSMITH_TRACING": "false"},
    )

    assert result.returncode == 0, result.stderr
    assert "status=success" in result.stdout
    assert "documents_processed=4" in result.stdout
    assert "data_mode=official" in result.stdout
    assert "source=appraisal_act_enforcement_rule status=ingested" in result.stdout
    assert "source=appraisal_standards_rule status=ingested" in result.stdout
