from __future__ import annotations

import argparse
import os
import subprocess
import sys
from pathlib import Path

BACKEND_ROOT = Path(__file__).resolve().parents[1]
PROJECT_ROOT = BACKEND_ROOT.parent
FRONTEND_ROOT = PROJECT_ROOT / "frontend"


def run(command: list[str], env: dict[str, str]) -> subprocess.CompletedProcess[str]:
    return subprocess.run(command, cwd=BACKEND_ROOT, env=env, text=True, capture_output=True, timeout=45)


def require(condition: bool, name: str, detail: str = "") -> None:
    if not condition:
        raise AssertionError(f"{name} failed: {detail}")
    print(f"{name}=pass")


def verify_frontend_contract() -> None:
    page = (FRONTEND_ROOT / "src" / "routes" / "+page.svelte").read_text()
    message_list = (FRONTEND_ROOT / "src" / "lib" / "components" / "MessageList.svelte").read_text()
    citation_panel = (FRONTEND_ROOT / "src" / "lib" / "components" / "CitationPanel.svelte").read_text()
    data_mode = (FRONTEND_ROOT / "src" / "lib" / "components" / "DataModeNotice.svelte").read_text()
    status = (FRONTEND_ROOT / "src" / "lib" / "components" / "StatusPanel.svelte").read_text()

    require("messages = [...messages, { role: 'user'" in page and "role: 'assistant'" in page, "frontend_message_contract")
    require("CitationPanel" in message_list and "source_name" in citation_panel and "chunk_index" in citation_panel, "frontend_citation_contract")
    require("dataMode" in data_mode and "공식 판단이 아닙니다" in data_mode, "frontend_data_mode_contract")
    require("insufficient_evidence" in status and "근거가 충분하지 않습니다" in status, "frontend_insufficient_evidence_contract")


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Run backend 3-turn chat plus frontend contract smoke without browser automation.",
        formatter_class=argparse.RawTextHelpFormatter,
    )
    parser.add_argument("--database-url", default="sqlite+pysqlite:///./web-chat-smoke.db")
    args = parser.parse_args()

    env = {**os.environ, "DATABASE_URL": args.database_url, "LANGSMITH_TRACING": "false"}
    sample_alpha = PROJECT_ROOT / "sample_data" / "sample-property-alpha.md"
    ingest = run([sys.executable, "scripts/ingest_file.py", str(sample_alpha)], env)
    require(ingest.returncode == 0 and "documents_processed=1" in ingest.stdout, "sample_ingestion", ingest.stderr)

    chat_code = r'''
from fastapi.testclient import TestClient
from app.main import app
from app.db.base import Base
from app.db.session import SessionLocal, engine
from app.models.chunk import Chunk  # noqa: F401
from app.models.conversation import Conversation  # noqa: F401
from app.models.document import Document  # noqa: F401
from app.models.message import Message
from app.models.retrieval_trace import RetrievalTrace

Base.metadata.create_all(bind=engine)
client = TestClient(app)
turn1 = client.post('/chat', json={'question':'Fictional Parcel Alpha', 'query_vector':[1.0, 0.0]}).json()
turn2 = client.post('/chat', json={'question':'What was my previous question?', 'conversation_id':turn1['conversation_id'], 'query_vector':[1.0, 0.0]}).json()
turn3 = client.post('/chat', json={'question':'What official law article applies?', 'conversation_id':turn1['conversation_id'], 'query_vector':[0.0, 1.0], 'rewrite_query_vector':[0.0, 1.0]}).json()
assert turn1['conversation_id'] == turn2['conversation_id'] == turn3['conversation_id']
assert turn3['insufficient_evidence'] is True
assert 'official data is not available' in turn3['answer'].lower()
assert 'law.go.kr' not in turn3['answer'].lower()
assert 'article 1' not in turn3['answer'].lower()
with SessionLocal() as session:
    assert session.query(Message).filter(Message.conversation_id == turn1['conversation_id']).count() == 6
    assert session.query(RetrievalTrace).filter(RetrievalTrace.conversation_id == turn1['conversation_id']).count() == 3
print('backend_3_turn_conversation=pass')
print('same_conversation_id=pass')
print('official_hallucination=pass')
'''
    chat = run([sys.executable, "-c", chat_code], env)
    if chat.returncode != 0:
        raise AssertionError(f"backend chat smoke failed: {chat.stderr}")
    print(chat.stdout, end="")
    verify_frontend_contract()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
