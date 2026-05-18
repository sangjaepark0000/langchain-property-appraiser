from pathlib import Path
import subprocess
import sys


ROOT = Path(__file__).resolve().parents[2]
BACKEND_ROOT = ROOT / "backend"


def test_export_rag_graph_script_writes_mermaid_flow(tmp_path):
    output = tmp_path / "rag-flow.md"

    result = subprocess.run(
        [sys.executable, str(BACKEND_ROOT / "scripts" / "export_rag_graph.py"), "--output", str(output)],
        cwd=BACKEND_ROOT,
        text=True,
        capture_output=True,
        timeout=30,
    )

    assert result.returncode == 0, result.stderr
    text = output.read_text(encoding="utf-8")
    assert "```mermaid" in text
    assert "start" in text
    assert "load_history" in text
    assert "rag_answer" in text
    assert "persist_assistant" in text
    assert "인사/잡담" in text
