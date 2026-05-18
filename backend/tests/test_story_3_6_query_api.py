from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.db.base import Base
from app.db.session import get_db_session
from app.main import app
from app.models.chunk import Chunk
from app.models.document import Document


def build_client_with_db(seed: bool = False) -> TestClient:
    engine = create_engine(
        "sqlite+pysqlite:///:memory:", connect_args={"check_same_thread": False}, poolclass=StaticPool
    )
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    if seed:
        session = Session()
        doc = Document(
            source_id="alpha",
            source_path="sample_data/sample-property-alpha.md",
            source_name="sample-property-alpha.md",
            source_type="markdown",
            data_mode="sample",
            ingestion_status="loaded",
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
            )
        )
        session.commit()
        session.close()

    def override_db():
        session = Session()
        try:
            yield session
        finally:
            session.close()

    app.dependency_overrides[get_db_session] = override_db
    return TestClient(app)


def test_query_api_returns_answer_citations_and_data_mode():
    client = build_client_with_db(seed=True)

    response = client.post("/query", json={"question": "Fictional Parcel Alpha", "query_vector": [1.0, 0.0]})

    assert response.status_code == 200
    body = response.json()
    assert body["answer"]
    assert body["citations"]
    assert body["data_mode"] == "sample"
    assert body["insufficient_evidence"] is False
    assert body["retrieved_count"] == 1
    app.dependency_overrides.clear()


def test_query_api_returns_consistent_error_shape_for_bad_payload():
    client = build_client_with_db()

    response = client.post("/query", json={"question": ""})

    assert response.status_code == 422
    body = response.json()
    assert body["error"]["code"] == "validation_error"
    assert body["error"]["message"]
    assert "details" in body["error"]
    app.dependency_overrides.clear()


def test_query_api_returns_insufficient_evidence_without_server_error():
    client = build_client_with_db(seed=False)

    response = client.post("/query", json={"question": "unknown"})

    assert response.status_code == 200
    body = response.json()
    assert body["insufficient_evidence"] is True
    assert "근거가 부족" in body["answer"]
    assert body["citations"] == []
    app.dependency_overrides.clear()
