from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import JSON, CheckConstraint, DateTime, String, Text, func
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base

if TYPE_CHECKING:
    from app.models.chunk import Chunk


DATA_MODE_VALUES = ("sample", "official", "user_provided", "unknown")
INGESTION_STATUS_VALUES = ("loaded", "ingested", "skipped", "unsupported", "failed")


class Document(Base):
    __tablename__ = "documents"
    __table_args__ = (
        CheckConstraint(
            "data_mode IN ('sample', 'official', 'user_provided', 'unknown')",
            name="ck_documents_data_mode",
        ),
        CheckConstraint(
            "ingestion_status IN ('loaded', 'ingested', 'skipped', 'unsupported', 'failed')",
            name="ck_documents_ingestion_status",
        ),
    )

    id: Mapped[int] = mapped_column(primary_key=True)
    source_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    source_path: Mapped[str | None] = mapped_column(Text, nullable=True)
    source_url: Mapped[str | None] = mapped_column(Text, nullable=True)
    source_name: Mapped[str] = mapped_column(String(512), nullable=False)
    source_type: Mapped[str] = mapped_column(String(100), nullable=False)
    data_mode: Mapped[str] = mapped_column(String(50), nullable=False, default="unknown", index=True)
    ingestion_status: Mapped[str] = mapped_column(String(50), nullable=False, default="loaded", index=True)
    metadata_: Mapped[dict] = mapped_column("metadata", JSON().with_variant(JSONB, "postgresql"), nullable=False, default=dict)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)

    chunks: Mapped[list[Chunk]] = relationship(back_populates="document", cascade="all, delete-orphan")
