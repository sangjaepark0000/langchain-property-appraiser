from pathlib import Path

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.db.base import Base
from app.models.conversation import Conversation
from app.models.message import Message
from app.models.retrieval_trace import RetrievalTrace


ROOT = Path(__file__).resolve().parents[2]
MIGRATION = ROOT / "backend" / "alembic" / "versions" / "20260517_0006_retrieval_traces.py"


def make_session():
    engine = create_engine("sqlite+pysqlite:///:memory:")
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    return Session()


def test_retrieval_trace_model_links_to_conversation_and_message():
    session = make_session()
    conversation = Conversation(metadata_={})
    session.add(conversation)
    session.flush()
    message = Message(conversation_id=conversation.id, role="user", content="hello", metadata_={})
    session.add(message)
    session.flush()
    trace = RetrievalTrace(
        conversation_id=conversation.id,
        message_id=message.id,
        query_preview="hello",
        query_hash="abc",
        retrieved_chunk_ids=[1, 2],
        relevance_result="sufficient",
        insufficient_evidence_reason=None,
        summary={"retrieved_count": 2},
    )
    session.add(trace)
    session.commit()

    loaded = session.query(RetrievalTrace).one()
    assert loaded.conversation.id == conversation.id
    assert loaded.message.id == message.id
    assert loaded.retrieved_chunk_ids == [1, 2]
    session.close()


def test_trace_service_redacts_query_and_records_summary():
    from app.services.retrieval_trace_service import create_retrieval_trace

    session = make_session()
    long_query = "secret-address 12345 " + "x" * 200

    trace = create_retrieval_trace(
        session,
        original_query=long_query,
        retrieved_chunk_ids=[7],
        relevance_result="insufficient",
        insufficient_evidence_reason="low relevance",
    )

    assert trace.query_preview.endswith("…")
    assert len(trace.query_preview) <= 83
    assert trace.query_hash
    assert "secret-address" in trace.query_preview
    assert trace.summary["retrieved_count"] == 1
    assert trace.summary["has_rewrite"] is False
    session.close()


def test_trace_service_records_query_rewrite_and_reretrieval_results():
    from app.services.retrieval_trace_service import create_retrieval_trace

    session = make_session()

    trace = create_retrieval_trace(
        session,
        original_query="first query",
        rewritten_query="rewritten query",
        retrieved_chunk_ids=[1],
        rewritten_retrieved_chunk_ids=[2, 3],
        relevance_result="rewritten_sufficient",
    )

    assert trace.rewritten_query_preview == "rewritten query"
    assert trace.rewritten_query_hash != trace.query_hash
    assert trace.rewritten_retrieved_chunk_ids == [2, 3]
    assert trace.summary["has_rewrite"] is True
    session.close()


def test_retrieval_trace_migration_creates_table_and_links():
    text = MIGRATION.read_text(encoding="utf-8")

    assert "create_table(\n        \"retrieval_traces\"" in text
    assert "conversation_id" in text
    assert "message_id" in text
    assert "retrieved_chunk_ids" in text
    assert "rewritten_retrieved_chunk_ids" in text
    assert "ix_retrieval_traces_conversation_id_created_at" in text
