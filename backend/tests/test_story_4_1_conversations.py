from pathlib import Path

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.db.base import Base
from app.models.conversation import Conversation
from app.models.message import Message


ROOT = Path(__file__).resolve().parents[2]
MIGRATION = ROOT / "backend" / "alembic" / "versions" / "20260517_0004_conversations_messages.py"


def make_session():
    engine = create_engine("sqlite+pysqlite:///:memory:")
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    return Session()


def test_conversation_and_message_models_are_related():
    session = make_session()
    conversation = Conversation(title="Sample chat", metadata_={"data_mode": "sample"})
    session.add(conversation)
    session.flush()
    message = Message(
        conversation_id=conversation.id,
        role="user",
        content="What is Alpha?",
        metadata_={"source": "test"},
    )
    session.add(message)
    session.commit()

    loaded = session.query(Conversation).one()
    assert loaded.id == conversation.id
    assert loaded.messages[0].content == "What is Alpha?"
    assert loaded.messages[0].conversation_id == conversation.id
    session.close()


def test_conversation_service_creates_new_conversation_when_id_missing():
    from app.services.conversation_service import append_message

    session = make_session()

    result = append_message(session, conversation_id=None, role="user", content="first question")

    assert result.conversation_id is not None
    assert result.created_conversation is True
    assert result.message.role == "user"
    assert session.query(Conversation).count() == 1
    assert session.query(Message).count() == 1
    session.close()


def test_conversation_service_appends_to_existing_conversation_and_reads_history():
    from app.services.conversation_service import append_message, get_message_history

    session = make_session()
    first = append_message(session, conversation_id=None, role="user", content="first")
    second = append_message(session, conversation_id=first.conversation_id, role="assistant", content="answer")

    history = get_message_history(session, first.conversation_id)

    assert second.created_conversation is False
    assert [message.content for message in history] == ["first", "answer"]
    assert all(message.conversation_id == first.conversation_id for message in history)
    session.close()


def test_conversation_migration_creates_tables_and_foreign_key():
    text = MIGRATION.read_text(encoding="utf-8")

    assert "create_table(\n        \"conversations\"" in text
    assert "create_table(\n        \"messages\"" in text
    assert "ForeignKeyConstraint([\"conversation_id\"], [\"conversations.id\"], ondelete=\"CASCADE\")" in text
    assert "ix_messages_conversation_id_created_at" in text
