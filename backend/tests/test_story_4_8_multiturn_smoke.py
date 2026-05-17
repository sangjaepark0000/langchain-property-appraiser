import subprocess
import sys
from pathlib import Path


BACKEND_ROOT = Path(__file__).resolve().parents[1]


def test_multiturn_crag_smoke_script_runs_without_external_tracing(tmp_path):
    db_path = tmp_path / "multiturn.db"

    result = subprocess.run(
        [sys.executable, str(BACKEND_ROOT / "scripts" / "multiturn_smoke.py"), "--database-url", f"sqlite+pysqlite:///{db_path}"],
        cwd=BACKEND_ROOT,
        text=True,
        capture_output=True,
        timeout=40,
        env={"LANGSMITH_TRACING": "false"},
    )

    assert result.returncode == 0, result.stderr
    assert "sample_ingestion=pass" in result.stdout
    assert "turn_1=pass" in result.stdout
    assert "turn_2=pass" in result.stdout
    assert "turn_3=pass" in result.stdout
    assert "messages=6" in result.stdout
    assert "traces=3" in result.stdout
    assert "insufficient_or_rewrite_path=pass" in result.stdout
    assert "official_hallucination=pass" in result.stdout
    assert "langsmith=not_required" in result.stdout


def test_multiturn_smoke_help_mentions_local_traces():
    result = subprocess.run(
        [sys.executable, str(BACKEND_ROOT / "scripts" / "multiturn_smoke.py"), "--help"],
        cwd=BACKEND_ROOT,
        text=True,
        capture_output=True,
        timeout=15,
    )

    assert result.returncode == 0
    assert "local logs" in result.stdout.lower()
    assert "retrieval trace" in result.stdout.lower()
