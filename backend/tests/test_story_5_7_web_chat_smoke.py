import subprocess
import sys
from pathlib import Path


BACKEND_ROOT = Path(__file__).resolve().parents[1]


def test_web_chat_smoke_script_verifies_frontend_contract_and_backend_3_turn_flow(tmp_path):
    db_path = tmp_path / "web-chat-smoke.db"

    result = subprocess.run(
        [sys.executable, str(BACKEND_ROOT / "scripts" / "web_chat_smoke.py"), "--database-url", f"sqlite+pysqlite:///{db_path}"],
        cwd=BACKEND_ROOT,
        text=True,
        capture_output=True,
        timeout=45,
        env={"LANGSMITH_TRACING": "false"},
    )

    assert result.returncode == 0, result.stderr
    assert "backend_3_turn_conversation=pass" in result.stdout
    assert "same_conversation_id=pass" in result.stdout
    assert "frontend_message_contract=pass" in result.stdout
    assert "frontend_citation_contract=pass" in result.stdout
    assert "frontend_data_mode_contract=pass" in result.stdout
    assert "frontend_insufficient_evidence_contract=pass" in result.stdout
    assert "official_hallucination=pass" in result.stdout


def test_web_chat_smoke_help_mentions_no_browser_dependency():
    result = subprocess.run(
        [sys.executable, str(BACKEND_ROOT / "scripts" / "web_chat_smoke.py"), "--help"],
        cwd=BACKEND_ROOT,
        text=True,
        capture_output=True,
        timeout=15,
    )

    assert result.returncode == 0
    assert "without browser automation" in result.stdout.lower()
