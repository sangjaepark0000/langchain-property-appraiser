import subprocess
import sys
from pathlib import Path


BACKEND_ROOT = Path(__file__).resolve().parents[1]


def test_automated_rag_smoke_script_validates_cli_api_and_no_evidence(tmp_path):
    db_path = tmp_path / "rag-smoke.db"

    result = subprocess.run(
        [sys.executable, str(BACKEND_ROOT / "scripts" / "rag_smoke.py"), "--database-url", f"sqlite+pysqlite:///{db_path}"],
        cwd=BACKEND_ROOT,
        text=True,
        capture_output=True,
        timeout=30,
    )

    assert result.returncode == 0, result.stderr
    assert "sample_ingestion=pass" in result.stdout
    assert "cli_query=pass" in result.stdout
    assert "api_contract=pass" in result.stdout
    assert "no_evidence=pass" in result.stdout
    assert "official_hallucination=pass" in result.stdout
    assert "BRAVE" not in result.stdout
    assert "API_KEY" not in result.stdout


def test_rag_smoke_script_help_documents_local_fallback():
    result = subprocess.run(
        [sys.executable, str(BACKEND_ROOT / "scripts" / "rag_smoke.py"), "--help"],
        cwd=BACKEND_ROOT,
        text=True,
        capture_output=True,
        timeout=15,
    )

    assert result.returncode == 0
    assert "external keys" in result.stdout.lower()
