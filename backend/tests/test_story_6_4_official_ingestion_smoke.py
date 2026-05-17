import subprocess
import sys
from pathlib import Path


BACKEND_ROOT = Path(__file__).resolve().parents[1]


def test_official_ingestion_smoke_persists_official_document_and_lineage(tmp_path):
    db_path = tmp_path / "official-smoke.db"

    result = subprocess.run(
        [sys.executable, str(BACKEND_ROOT / "scripts" / "official_ingestion_smoke.py"), "--database-url", f"sqlite+pysqlite:///{db_path}"],
        cwd=BACKEND_ROOT,
        text=True,
        capture_output=True,
        timeout=45,
        env={"LANGSMITH_TRACING": "false"},
    )

    assert result.returncode == 0, result.stderr
    assert "official_document=pass" in result.stdout
    assert "domain_metadata=pass" in result.stdout
    assert "official_data_mode=pass" in result.stdout
    assert "failed_source_not_ingested=pass" in result.stdout
    assert "sample_official_separation=pass" in result.stdout
    assert "source_lineage=pass" in result.stdout
    assert "live_api=not_required" in result.stdout


def test_official_ingestion_smoke_help_mentions_local_fixture():
    result = subprocess.run(
        [sys.executable, str(BACKEND_ROOT / "scripts" / "official_ingestion_smoke.py"), "--help"],
        cwd=BACKEND_ROOT,
        text=True,
        capture_output=True,
        timeout=15,
    )

    assert result.returncode == 0
    assert "local official xml fixture" in result.stdout.lower()
