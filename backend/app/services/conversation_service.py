from __future__ import annotations

from dataclasses import dataclass

from sqlalchemy.orm import Session

from app.models.conversation import Conversation
from app.models.message import Message


@dataclass(frozen=True)
class AppendMessageResult:
    conversation_id: int
    message: Message
    created_conversation: bool


def append_message(
    session: Session,
    *,
    conversation_id: int | None,
    role: str,
    content: str,
    metadata: dict | None = None,
) -> AppendMessageResult:
    created = False
    if conversation_id is None:
        conversation = Conversation(metadata_={})
        session.add(conversation)
        session.flush()
        conversation_id = conversation.id
        created = True
    else:
        conversation = session.get(Conversation, conversation_id)
        if conversation is None:
            raise ValueError(f"Conversation {conversation_id} does not exist")

    message = Message(
        conversation_id=conversation_id,
        role=role,
        content=content,
        metadata_=metadata or {},
    )
    session.add(message)
    session.commit()
    session.refresh(message)
    return AppendMessageResult(conversation_id=conversation_id, message=message, created_conversation=created)


def get_message_history(session: Session, conversation_id: int) -> list[Message]:
    return (
        session.query(Message)
        .filter(Message.conversation_id == conversation_id)
        .order_by(Message.created_at, Message.id)
        .all()
    )
