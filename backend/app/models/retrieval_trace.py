from __future__ import annotations

from datetime import datetime
from sqlalchemy import JSON, DateTime, ForeignKey, Index, String, Text, func
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base
from app.models.conversation import Conversation
from app.models.message import Message


class RetrievalTrace(Base):
    __tablename__ = "retrieval_traces"
    __table_args__ = (
        Index("ix_retrieval_traces_conversation_id_created_at", "conversation_id", "created_at"),
        Index("ix_retrieval_traces_message_id", "message_id"),
    )

    id: Mapped[int] = mapped_column(primary_key=True)
    conversation_id: Mapped[int | None] = mapped_column(ForeignKey("conversations.id", ondelete="SET NULL"), nullable=True)
    message_id: Mapped[int | None] = mapped_column(ForeignKey("messages.id", ondelete="SET NULL"), nullable=True)
    query_preview: Mapped[str] = mapped_column(Text, nullable=False)
    query_hash: Mapped[str] = mapped_column(String(64), nullable=False)
    rewritten_query_preview: Mapped[str | None] = mapped_column(Text, nullable=True)
    rewritten_query_hash: Mapped[str | None] = mapped_column(String(64), nullable=True)
    retrieved_chunk_ids: Mapped[list[int]] = mapped_column(JSON().with_variant(JSONB, "postgresql"), nullable=False, default=list)
    rewritten_retrieved_chunk_ids: Mapped[list[int] | None] = mapped_column(JSON().with_variant(JSONB, "postgresql"), nullable=True)
    relevance_result: Mapped[str] = mapped_column(String(100), nullable=False)
    insufficient_evidence_reason: Mapped[str | None] = mapped_column(Text, nullable=True)
    summary: Mapped[dict] = mapped_column(JSON().with_variant(JSONB, "postgresql"), nullable=False, default=dict)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)

    conversation: Mapped[Conversation | None] = relationship()
    message: Mapped[Message | None] = relationship()
