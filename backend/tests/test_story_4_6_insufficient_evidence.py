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
from app.models.message import Message  # noqa: F401
from app.models.retrieval_trace import RetrievalTrace


def make_session():
    engine = create_engine("sqlite+pysqlite:///:memory:", connect_args={"check_same_thread": False}, poolclass=StaticPool)
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    return Session(), Session


def seed_chunk(session, *, embedding=None):
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
            metadata_={"embedding": embedding or [1.0, 0.0], "data_mode": "sample"},
            source_lineage={"chunk_index": 0},
            embedding=embedding or [1.0, 0.0],
        )
    )
    session.commit()


def test_graph_returns_normal_insufficient_evidence_after_failed_reretrieval():
    from app.graph.conversation import run_conversation_graph

    session, _ = make_session()
    seed_chunk(session, embedding=[1.0, 0.0])

    result = run_conversation_graph(
        session,
        question="official law article?",
        query_vector=[0.0, 1.0],
        rewrite_query_vector=[0.0, 1.0],
        max_rewrite_attempts=1,
    )

    assert result.answer.status == "insufficient_evidence"
    assert result.insufficient_evidence is True
    assert "official data is not available" in result.answer.answer.lower()
    assert result.insufficient_evidence_reason
    trace = session.query(RetrievalTrace).one()
    assert trace.summary["insufficient_evidence"] is True
    assert trace.summary["insufficient_evidence_reason"] == result.insufficient_evidence_reason
    session.close()


def test_insufficient_evidence_does_not_fabricate_official_sources_or_articles():
    from app.rag.query import answer_question

    session, _ = make_session()
    seed_chunk(session, embedding=[1.0, 0.0])

    result = answer_question(session, "국토교통부고시 몇 조에 따라 적법한가?", query_vector=[0.0, 1.0])

    answer = result.answer.answer.lower()
    assert result.insufficient_evidence is True
    assert "official data is not available" in answer
    assert "law.go.kr" not in answer
    assert "article 1" not in answer
    assert "2024-" not in answer
    session.close()


def test_determination_question_includes_limited_assistance_reason_in_trace():
    from app.rag.query import answer_question

    session, _ = make_session()
    seed_chunk(session, embedding=[1.0, 0.0])

    result = answer_question(session, "Is this appraisal legally valid and appropriate?", query_vector=[0.0, 1.0])

    assert result.insufficient_evidence is True
    assert "not a legal conclusion" in result.answer.answer.lower()
    trace = session.query(RetrievalTrace).one()
    assert "limited evidence" in trace.summary["insufficient_evidence_reason"].lower()
    session.close()


def test_query_api_returns_200_for_insufficient_evidence_with_reason():
    session, Session = make_session()
    seed_chunk(session, embedding=[1.0, 0.0])
    session.close()

    def override_db():
        db = Session()
        try:
            yield db
        finally:
            db.close()

    app.dependency_overrides[get_db_session] = override_db
    client = TestClient(app)
    response = client.post("/query", json={"question": "official law article?", "query_vector": [0.0, 1.0]})

    assert response.status_code == 200
    body = response.json()
    assert body["insufficient_evidence"] is True
    assert body["insufficient_evidence_reason"]
    assert body["citations"] == []
    app.dependency_overrides.clear()
