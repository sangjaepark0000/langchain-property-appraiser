import logging

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.db.base import Base
from app.models.chunk import Chunk
from app.models.document import Document
from app.models.message import Message


def make_session():
    engine = create_engine("sqlite+pysqlite:///:memory:")
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    return Session()


def seed_chunk(session):
    doc = Document(
        source_id="alpha",
        source_path="sample_data/sample-property-alpha.md",
        source_name="sample-property-alpha.md",
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


def test_conversation_graph_creates_conversation_records_user_and_assistant_messages():
    from app.graph.conversation import run_conversation_graph

    session = make_session()
    seed_chunk(session)

    result = run_conversation_graph(session, question="Fictional Parcel Alpha", query_vector=[1.0, 0.0])

    assert result.conversation_id is not None
    messages = session.query(Message).filter(Message.conversation_id == result.conversation_id).order_by(Message.id).all()
    assert [message.role for message in messages] == ["user", "assistant"]
    assert "blue roof" in messages[1].content
    assert result.answer.status == "answered"
    session.close()


def test_conversation_graph_loads_history_for_follow_up_question():
    from app.graph.conversation import run_conversation_graph

    session = make_session()
    seed_chunk(session)
    first = run_conversation_graph(session, question="Fictional Parcel Alpha", query_vector=[1.0, 0.0])
    second = run_conversation_graph(
        session,
        question="What was my previous question?",
        conversation_id=first.conversation_id,
        query_vector=[1.0, 0.0],
    )

    assert second.conversation_id == first.conversation_id
    assert len(second.history) >= 2
    assert second.history[0].content == "Fictional Parcel Alpha"
    assert session.query(Message).filter(Message.conversation_id == first.conversation_id).count() == 4
    session.close()


def test_conversation_graph_logs_node_transitions(caplog):
    from app.graph.conversation import run_conversation_graph

    session = make_session()
    seed_chunk(session)

    with caplog.at_level(logging.INFO, logger="app.graph.conversation"):
        run_conversation_graph(session, question="Fictional Parcel Alpha", query_vector=[1.0, 0.0])

    logged = "\n".join(record.getMessage() for record in caplog.records)
    assert "node=start" in logged
    assert "node=load_history" in logged
    assert "node=rag_answer" in logged
    assert "node=persist_assistant" in logged
    assert "conversation_id=" in logged
    session.close()
