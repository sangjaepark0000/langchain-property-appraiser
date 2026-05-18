from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.db.base import Base
from app.db.session import get_db_session
from app.main import app
from app.models.chunk import Chunk
from app.models.conversation import Conversation  # noqa: F401
from app.models.document import Document
from app.models.message import Message
from app.models.retrieval_trace import RetrievalTrace


def build_client(seed: bool = True):
    engine = create_engine("sqlite+pysqlite:///:memory:", connect_args={"check_same_thread": False}, poolclass=StaticPool)
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    if seed:
        session = Session()
        doc = Document(
            source_id="alpha",
            source_path="sample_data/alpha.md",
            source_name="alpha.md",
            source_type="markdown",
            data_mode="sample",
            ingestion_status="ingested",
            metadata_={},
        )
        session.add(doc)
        session.flush()
        session.add(
            Chunk(
                document_id=doc.id,
                chunk_index=0,
                text="Fictional Parcel Alpha has a blue roof.",
                metadata_={"embedding": [1.0, 0.0], "data_mode": "sample"},
                source_lineage={"chunk_index": 0},
                embedding=[1.0, 0.0],
            )
        )
        session.commit()
        session.close()

    def override_db():
        db = Session()
        try:
            yield db
        finally:
            db.close()

    app.dependency_overrides[get_db_session] = override_db
    return TestClient(app), Session


def test_chat_api_skips_retrieval_for_greeting_smalltalk():
    client, Session = build_client()

    response = client.post("/chat", json={"question": "hi"})

    assert response.status_code == 200
    body = response.json()
    assert body["insufficient_evidence"] is False
    assert body["citations"] == []
    assert body["data_mode"] == "none"
    assert body["retrieval_trace"]["relevance_result"] == "not_applicable"
    assert "검토하고 싶은 서류" in body["answer"]
    session = Session()
    assert session.query(RetrievalTrace).count() == 1
    session.close()
    app.dependency_overrides.clear()


def test_chat_api_creates_conversation_and_returns_contract_shape():
    client, Session = build_client()

    response = client.post("/chat", json={"question": "Fictional Parcel Alpha", "query_vector": [1.0, 0.0]})

    assert response.status_code == 200
    body = response.json()
    assert body["conversation_id"]
    assert body["message_id"]
    assert body["answer"]
    assert body["citations"]
    assert body["data_mode"] == "sample"
    assert body["insufficient_evidence"] is False
    assert body["retrieval_trace"]["relevance_result"] == "sufficient"
    session = Session()
    assert session.query(Message).filter(Message.conversation_id == body["conversation_id"]).count() == 2
    session.close()
    app.dependency_overrides.clear()


def test_chat_api_appends_followup_to_existing_conversation():
    client, Session = build_client()
    first = client.post("/chat", json={"question": "Fictional Parcel Alpha", "query_vector": [1.0, 0.0]}).json()

    second_response = client.post(
        "/chat",
        json={"question": "What was my previous question?", "conversation_id": first["conversation_id"], "query_vector": [1.0, 0.0]},
    )

    assert second_response.status_code == 200
    second = second_response.json()
    assert second["conversation_id"] == first["conversation_id"]
    session = Session()
    assert session.query(Message).filter(Message.conversation_id == first["conversation_id"]).count() == 4
    session.close()
    app.dependency_overrides.clear()


def test_chat_api_returns_trace_summary_for_insufficient_evidence():
    client, Session = build_client()

    response = client.post("/chat", json={"question": "official law article?", "query_vector": [0.0, 1.0]})

    assert response.status_code == 200
    body = response.json()
    assert body["insufficient_evidence"] is True
    assert body["retrieval_trace"]["insufficient_evidence_reason"]
    assert body["retrieval_trace"]["rewrite_status"] in {"skipped", "rewritten", "not_needed"}
    session = Session()
    assert session.query(RetrievalTrace).count() == 1
    session.close()
    app.dependency_overrides.clear()
