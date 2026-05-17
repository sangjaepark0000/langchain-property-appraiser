from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.db.base import Base
from app.models.chunk import Chunk
from app.models.conversation import Conversation  # noqa: F401
from app.models.document import Document
from app.models.message import Message  # noqa: F401
from app.models.retrieval_trace import RetrievalTrace


def make_session():
    engine = create_engine("sqlite+pysqlite:///:memory:")
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    return Session()


def seed_chunk(session, *, text="Fictional Parcel Alpha has a blue roof.", embedding=None):
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
    chunk = Chunk(
        document_id=doc.id,
        chunk_index=0,
        text=text,
        metadata_={"embedding": embedding or [1.0, 0.0], "data_mode": "sample"},
        source_lineage={"chunk_index": 0},
        embedding=embedding or [1.0, 0.0],
    )
    session.add(chunk)
    session.commit()
    return chunk


def test_deterministic_rewrite_fallback_preserves_original_question():
    from app.rag.rewrite import rewrite_query

    result = rewrite_query("What about it?", history=["Fictional Parcel Alpha"])

    assert result.original_query == "What about it?"
    assert "Fictional Parcel Alpha" in result.rewritten_query
    assert result.fallback is True
    assert result.status == "rewritten"


def test_answer_question_reretrieves_after_weak_initial_grade_and_records_trace():
    from app.rag.query import answer_question

    session = make_session()
    chunk = seed_chunk(session, embedding=[1.0, 0.0])

    result = answer_question(
        session,
        "What about it?",
        query_vector=[0.45, 0.89],
        rewrite_query_vector=[1.0, 0.0],
        history_texts=["Fictional Parcel Alpha"],
        max_rewrite_attempts=1,
    )

    trace = session.query(RetrievalTrace).one()
    assert result.rewrite.status == "rewritten"
    assert result.rewrite.fallback is True
    assert result.grading.status == "sufficient"
    assert trace.relevance_result == "sufficient"
    assert trace.retrieved_chunk_ids == [chunk.id]
    assert trace.rewritten_retrieved_chunk_ids == [chunk.id]
    assert trace.rewritten_query_preview is not None
    assert trace.summary["rewrite_attempts"] == 1
    session.close()


def test_answer_question_does_not_exceed_rewrite_attempt_limit():
    from app.rag.query import answer_question

    session = make_session()
    seed_chunk(session, embedding=[1.0, 0.0])

    result = answer_question(
        session,
        "unrelated",
        query_vector=[0.0, 1.0],
        rewrite_query_vector=[0.0, 1.0],
        history_texts=["Fictional Parcel Alpha"],
        max_rewrite_attempts=1,
    )

    trace = session.query(RetrievalTrace).one()
    assert result.rewrite.attempts == 1
    assert trace.summary["rewrite_attempts"] == 1
    assert result.answer.status == "insufficient_evidence"
    session.close()


def test_graph_exposes_rewrite_status_in_result_and_assistant_metadata():
    from app.graph.conversation import run_conversation_graph
    from app.models.message import Message

    session = make_session()
    seed_chunk(session, embedding=[1.0, 0.0])

    result = run_conversation_graph(
        session,
        question="What about it?",
        query_vector=[0.45, 0.89],
        rewrite_query_vector=[1.0, 0.0],
        max_rewrite_attempts=1,
    )

    assistant = session.query(Message).filter(Message.role == "assistant").one()
    assert result.rewrite.status == "rewritten"
    assert assistant.metadata_["rewrite_status"] == "rewritten"
    assert assistant.metadata_["rewrite_fallback"] is True
    session.close()
