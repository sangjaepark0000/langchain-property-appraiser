from __future__ import annotations

import argparse
import os
import subprocess
import sys
from pathlib import Path

BACKEND_ROOT = Path(__file__).resolve().parents[1]
PROJECT_ROOT = BACKEND_ROOT.parent


def run(command: list[str], env: dict[str, str]) -> subprocess.CompletedProcess[str]:
    return subprocess.run(command, cwd=BACKEND_ROOT, env=env, text=True, capture_output=True, timeout=40)


def assert_pass(condition: bool, name: str, detail: str = "") -> None:
    if not condition:
        raise AssertionError(f"{name} failed: {detail}")
    print(f"{name}=pass")


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Run a 3-turn local CRAG smoke test using local logs and retrieval trace only; LangSmith is not required."
    )
    parser.add_argument("--database-url", default="sqlite+pysqlite:///./multiturn-smoke.db")
    args = parser.parse_args()

    env = {**os.environ, "DATABASE_URL": args.database_url, "LANGSMITH_TRACING": "false"}
    sample_alpha = PROJECT_ROOT / "sample_data" / "sample-property-alpha.md"

    ingest = run([sys.executable, "scripts/ingest_file.py", str(sample_alpha)], env)
    assert_pass(ingest.returncode == 0 and "documents_processed=1" in ingest.stdout, "sample_ingestion", ingest.stderr)

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
assert turn1['conversation_id']
assert turn1['answer']
print('turn_1=pass')
turn2 = client.post('/chat', json={'question':'What was my previous question?', 'conversation_id':turn1['conversation_id'], 'query_vector':[1.0, 0.0]}).json()
assert turn2['conversation_id'] == turn1['conversation_id']
print('turn_2=pass')
turn3 = client.post('/chat', json={'question':'What official law article applies?', 'conversation_id':turn1['conversation_id'], 'query_vector':[0.0, 1.0], 'rewrite_query_vector':[0.0, 1.0]}).json()
assert turn3['conversation_id'] == turn1['conversation_id']
assert turn3['insufficient_evidence'] is True
assert 'official data is not available' in turn3['answer'].lower()
assert 'law.go.kr' not in turn3['answer'].lower()
assert 'article 1' not in turn3['answer'].lower()
print('turn_3=pass')
with SessionLocal() as session:
    messages = session.query(Message).filter(Message.conversation_id == turn1['conversation_id']).count()
    traces = session.query(RetrievalTrace).filter(RetrievalTrace.conversation_id == turn1['conversation_id']).count()
    last_trace = session.query(RetrievalTrace).order_by(RetrievalTrace.id.desc()).first()
    assert messages == 6, messages
    assert traces == 3, traces
    assert last_trace.summary.get('rewrite_status') in {'skipped', 'rewritten', 'not_needed'}
    print(f'messages={messages}')
    print(f'traces={traces}')
print('insufficient_or_rewrite_path=pass')
print('official_hallucination=pass')
print('langsmith=not_required')
'''
    chat = run([sys.executable, "-c", chat_code], env)
    if chat.returncode != 0:
        raise AssertionError(f"chat flow failed: {chat.stderr}")
    print(chat.stdout, end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
